"""Deterministic LoRA-gradient measurement and PCGrad projection primitives."""

from __future__ import annotations

import itertools
import math
from typing import Any, Sequence


GradientList = Sequence[Any]


def split_optimizer_groups(
    rows: Sequence[dict[str, Any]],
    accumulation_steps: int,
    lane_weights: dict[str, float],
) -> list[list[dict[str, Any]]]:
    if not rows or accumulation_steps <= 0 or len(rows) % accumulation_steps:
        raise ValueError("rows must form complete optimizer groups")
    if not lane_weights or any(value <= 0 for value in lane_weights.values()):
        raise ValueError("lane weights must be positive")
    groups = []
    for start in range(0, len(rows), accumulation_steps):
        group = list(rows[start:start + accumulation_steps])
        declared = {row.get("optimizer_group") for row in group}
        if declared != {start // accumulation_steps} or set(row.get("lane") for row in group) != set(lane_weights):
            raise ValueError("optimizer group identity or lane coverage mismatch")
        realized = {
            lane: sum(float(row.get("objective_weight", 0.0)) for row in group if row.get("lane") == lane)
            for lane in lane_weights
        }
        if any(not math.isclose(realized[lane], lane_weights[lane], rel_tol=0.0, abs_tol=1e-12) for lane in lane_weights):
            raise ValueError("optimizer group objective mass mismatch")
        groups.append(group)
    return groups


def lane_backward_weights(
    group: Sequence[dict[str, Any]],
    lane_weights: dict[str, float],
) -> dict[str, list[tuple[dict[str, Any], float]]]:
    result = {lane: [] for lane in lane_weights}
    for row in group:
        lane = row.get("lane")
        if lane not in result:
            raise ValueError("row lane escaped the frozen lane weights")
        weight = float(row.get("objective_weight", 0.0)) / lane_weights[lane]
        if not math.isfinite(weight) or weight <= 0:
            raise ValueError("row objective weight is invalid")
        result[lane].append((row, weight))
    if any(not values for values in result.values()) or any(
        not math.isclose(sum(weight for _, weight in values), 1.0, rel_tol=0.0, abs_tol=1e-12)
        for values in result.values()
    ):
        raise ValueError("within-lane backward weights must sum to one")
    return result


def evenly_spaced_group_indices(total_groups: int, selected_groups: int) -> list[int]:
    if total_groups < 2 or selected_groups < 2 or selected_groups > total_groups:
        raise ValueError("group selection bounds are invalid")
    return [round(index * (total_groups - 1) / (selected_groups - 1)) for index in range(selected_groups)]


def rotated_lane_order(lanes: Sequence[str], seed: int, group_index: int) -> list[str]:
    if not lanes or len(set(lanes)) != len(lanes) or group_index < 0:
        raise ValueError("lane rotation inputs are invalid")
    offset = (seed + group_index) % len(lanes)
    return [*lanes[offset:], *lanes[:offset]]


def conflict_decision(
    group_cosines: Sequence[Sequence[dict[str, float | str]]],
    *,
    negative_cosine_threshold: float = -0.05,
    minimum_negative_groups: int = 4,
    minimum_javascript_typescript_groups: int = 4,
) -> dict[str, Any]:
    if not group_cosines or not -1.0 <= negative_cosine_threshold < 0:
        raise ValueError("conflict decision inputs are invalid")
    negative_groups = 0
    javascript_typescript_groups = 0
    for rows in group_cosines:
        negative = [row for row in rows if float(row["cosine"]) < negative_cosine_threshold]
        negative_groups += bool(negative)
        javascript_typescript_groups += any(
            lane in {"javascript", "typescript"}
            for row in negative
            for lane in (row["left"], row["right"])
        )
    passed = (
        negative_groups >= minimum_negative_groups
        and javascript_typescript_groups >= minimum_javascript_typescript_groups
    )
    return {
        "groups_measured": len(group_cosines),
        "negative_cosine_threshold": negative_cosine_threshold,
        "groups_with_negative_pair": negative_groups,
        "groups_with_javascript_or_typescript_negative_participation": javascript_typescript_groups,
        "minimum_groups_with_negative_pair": minimum_negative_groups,
        "minimum_javascript_or_typescript_groups": minimum_javascript_typescript_groups,
        "stage_2_allowed": passed,
    }


def capture_gradients(parameters: Sequence[Any]) -> list[Any | None]:
    if not parameters:
        raise ValueError("trainable parameter list cannot be empty")
    return [None if parameter.grad is None else parameter.grad.detach().clone() for parameter in parameters]


def accumulate_gradients(
    accumulated: Sequence[Any | None] | None,
    current: GradientList,
) -> list[Any | None]:
    if accumulated is None:
        return [None if tensor is None else tensor.detach().clone() for tensor in current]
    if len(accumulated) != len(current):
        raise ValueError("gradient layouts differ")
    result = [None if tensor is None else tensor.detach().clone() for tensor in accumulated]
    for index, tensor in enumerate(current):
        if tensor is None:
            continue
        if result[index] is None:
            result[index] = tensor.detach().clone()
        elif result[index].shape != tensor.shape:
            raise ValueError("gradient tensor shapes differ")
        else:
            result[index].add(tensor.detach())
    return result


def assign_gradients(parameters: Sequence[Any], gradients: GradientList) -> None:
    if len(parameters) != len(gradients) or not parameters:
        raise ValueError("gradient assignment layout differs")
    for parameter, gradient in zip(parameters, gradients):
        parameter.grad = None if gradient is None else gradient.detach().clone()


def collect_lane_gradients(
    model: Any,
    group: Sequence[dict[str, Any]],
    parameters: Sequence[Any],
    lane_weights: dict[str, float],
    collate_fn: Any,
    torch_module: Any,
    *,
    device: str = "cuda:0",
) -> tuple[dict[str, list[Any | None]], dict[str, Any]]:
    """Compute one response-token mean gradient per lane without an optimizer step."""
    if not parameters:
        raise ValueError("trainable parameter list cannot be empty")
    weighted_rows = lane_backward_weights(group, lane_weights)
    gradients = {}
    losses = {}
    for lane in lane_weights:
        model.zero_grad(set_to_none=True)
        lane_losses = []
        for row, within_lane_weight in weighted_rows[lane]:
            result = model(**collate_fn(row, device), skip_logits=True)
            if result.logits is not None:
                raise RuntimeError("gradient measurement materialized logits")
            weighted_loss = result.loss * within_lane_weight
            if not bool(torch_module.isfinite(weighted_loss)):
                raise RuntimeError("non-finite gradient measurement loss")
            weighted_loss.backward()
            lane_losses.append(float(result.loss.detach().cpu()))
        gradients[lane] = capture_gradients(parameters)
        if gradient_norm(gradients[lane]) <= 0:
            raise RuntimeError(f"zero trainable gradient for lane {lane}")
        losses[lane] = {
            "records": len(lane_losses),
            "raw_loss_min": min(lane_losses),
            "raw_loss_mean": sum(lane_losses) / len(lane_losses),
            "raw_loss_max": max(lane_losses),
        }
    model.zero_grad(set_to_none=True)
    return gradients, losses


def measure_gradient_conflicts(
    model: Any,
    groups: Sequence[Sequence[dict[str, Any]]],
    selected_group_indices: Sequence[int],
    parameters: Sequence[Any],
    lane_weights: dict[str, float],
    collate_fn: Any,
    torch_module: Any,
    *,
    negative_cosine_threshold: float,
    minimum_negative_groups: int,
    minimum_javascript_typescript_groups: int,
    device: str = "cuda:0",
) -> dict[str, Any]:
    if not selected_group_indices or len(set(selected_group_indices)) != len(selected_group_indices):
        raise ValueError("selected gradient-audit groups must be unique and non-empty")
    if min(selected_group_indices) < 0 or max(selected_group_indices) >= len(groups):
        raise ValueError("selected gradient-audit group is out of range")
    rows = []
    for group_index in selected_group_indices:
        gradients, losses = collect_lane_gradients(
            model,
            groups[group_index],
            parameters,
            lane_weights,
            collate_fn,
            torch_module,
            device=device,
        )
        rows.append({
            "optimizer_group": group_index,
            "lane_losses": losses,
            "lane_gradient_norms": {lane: gradient_norm(gradients[lane]) for lane in lane_weights},
            "pairwise_cosines": pairwise_cosines(gradients),
        })
    decision = conflict_decision(
        [row["pairwise_cosines"] for row in rows],
        negative_cosine_threshold=negative_cosine_threshold,
        minimum_negative_groups=minimum_negative_groups,
        minimum_javascript_typescript_groups=minimum_javascript_typescript_groups,
    )
    return {"groups": rows, "decision": decision}


def _validate(gradients: dict[str, GradientList]) -> tuple[list[str], int]:
    lanes = sorted(gradients)
    if len(lanes) < 2:
        raise ValueError("at least two lane gradients are required")
    widths = {len(gradients[lane]) for lane in lanes}
    if len(widths) != 1:
        raise ValueError("lane gradients must share one parameter layout")
    width = widths.pop()
    if width == 0:
        raise ValueError("lane gradients cannot be empty")
    return lanes, width


def gradient_dot(left: GradientList, right: GradientList) -> float:
    if len(left) != len(right):
        raise ValueError("gradient layouts differ")
    total = 0.0
    for lhs, rhs in zip(left, right):
        if lhs is None or rhs is None:
            continue
        if lhs.shape != rhs.shape:
            raise ValueError("gradient tensor shapes differ")
        total += float((lhs.detach().float().reshape(-1) @ rhs.detach().float().reshape(-1)).cpu())
    return total


def gradient_norm(gradient: GradientList) -> float:
    return math.sqrt(max(0.0, gradient_dot(gradient, gradient)))


def pairwise_cosines(gradients: dict[str, GradientList]) -> list[dict[str, float | str]]:
    lanes, _ = _validate(gradients)
    norms = {lane: gradient_norm(gradients[lane]) for lane in lanes}
    if any(not math.isfinite(value) or value <= 0 for value in norms.values()):
        raise ValueError("every lane gradient must have a finite positive norm")
    rows = []
    for left, right in itertools.combinations(lanes, 2):
        cosine = gradient_dot(gradients[left], gradients[right]) / (norms[left] * norms[right])
        rows.append({"left": left, "right": right, "cosine": max(-1.0, min(1.0, cosine))})
    return rows


def deterministic_pcgrad(
    gradients: dict[str, GradientList],
    lane_weights: dict[str, float],
    lane_order: Sequence[str],
) -> tuple[list[Any | None], dict[str, Any]]:
    """Project conflicting lane gradients, then aggregate with frozen lane weights."""
    lanes, width = _validate(gradients)
    if sorted(lane_order) != lanes or len(set(lane_order)) != len(lanes):
        raise ValueError("lane order must contain each lane exactly once")
    if set(lane_weights) != set(lanes) or any(not math.isfinite(value) or value <= 0 for value in lane_weights.values()):
        raise ValueError("lane weights must be finite and positive for every lane")
    if not math.isclose(sum(lane_weights.values()), 1.0, rel_tol=0.0, abs_tol=1e-12):
        raise ValueError("lane weights must sum to one")

    originals = {
        lane: [None if tensor is None else tensor.detach().clone() for tensor in gradients[lane]]
        for lane in lanes
    }
    projected = {
        lane: [None if tensor is None else tensor.detach().clone() for tensor in gradients[lane]]
        for lane in lanes
    }
    projection_rows = []
    ordered = list(lane_order)
    for index, lane in enumerate(ordered):
        for offset in range(1, len(ordered)):
            other = ordered[(index + offset) % len(ordered)]
            dot = gradient_dot(projected[lane], originals[other])
            denominator = gradient_dot(originals[other], originals[other])
            if not math.isfinite(dot) or not math.isfinite(denominator) or denominator <= 0:
                raise ValueError("gradient projection received a non-finite or zero-norm lane")
            applied = dot < 0
            if applied:
                scale = dot / denominator
                for parameter_index in range(width):
                    current = projected[lane][parameter_index]
                    reference = originals[other][parameter_index]
                    if current is not None and reference is not None:
                        current.sub_(reference, alpha=scale)
            projection_rows.append({"lane": lane, "against": other, "dot_before": dot, "applied": applied})

    aggregate: list[Any | None] = []
    for parameter_index in range(width):
        combined = None
        for lane in ordered:
            tensor = projected[lane][parameter_index]
            if tensor is None:
                continue
            contribution = tensor * lane_weights[lane]
            combined = contribution.clone() if combined is None else combined.add(contribution)
        aggregate.append(combined)
    if all(tensor is None for tensor in aggregate):
        raise ValueError("aggregate gradient is empty")

    telemetry = {
        "lane_order": ordered,
        "lane_weights": {lane: lane_weights[lane] for lane in ordered},
        "lane_norms_before": {lane: gradient_norm(originals[lane]) for lane in ordered},
        "pairwise_cosines_before": pairwise_cosines(originals),
        "pairwise_cosines_after": pairwise_cosines(projected),
        "projections": projection_rows,
        "projection_count": sum(row["applied"] for row in projection_rows),
        "aggregate_norm": gradient_norm(aggregate),
    }
    return aggregate, telemetry
