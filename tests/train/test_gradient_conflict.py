import math

import numpy as np
import pytest

from scripts.train.gradient_conflict import (
    accumulate_gradients,
    assign_gradients,
    capture_gradients,
    conflict_decision,
    collect_lane_gradients,
    deterministic_pcgrad,
    evenly_spaced_group_indices,
    gradient_dot,
    gradient_norm,
    measure_gradient_conflicts,
    pairwise_cosines,
    rotated_lane_order,
    lane_backward_weights,
    split_optimizer_groups,
)


class Scalar:
    def __init__(self, value: float) -> None:
        self.value = value

    def cpu(self):
        return self

    def __float__(self) -> float:
        return self.value


class Tensor:
    def __init__(self, values) -> None:
        self.values = np.asarray(values, dtype=np.float32)

    @property
    def shape(self):
        return self.values.shape

    def detach(self):
        return self

    def float(self):
        return self

    def reshape(self, *shape):
        return Tensor(self.values.reshape(*shape))

    def clone(self):
        return Tensor(self.values.copy())

    def cpu(self):
        return self

    def __matmul__(self, other):
        return Scalar(float(self.values @ other.values))

    def __mul__(self, value):
        return Tensor(self.values * value)

    def add(self, other):
        self.values += other.values
        return self

    def sub_(self, other, *, alpha):
        self.values -= other.values * alpha
        return self


class Parameter:
    def __init__(self, grad=None) -> None:
        self.grad = grad


class Loss:
    def __init__(self, value, parameters, gradient_values, weight=1.0) -> None:
        self.value = value
        self.parameters = parameters
        self.gradient_values = gradient_values
        self.weight = weight

    def __mul__(self, weight):
        return Loss(self.value * weight, self.parameters, self.gradient_values, self.weight * weight)

    def backward(self):
        for parameter, values in zip(self.parameters, self.gradient_values):
            contribution = Tensor(np.asarray(values) * self.weight)
            parameter.grad = contribution if parameter.grad is None else parameter.grad.add(contribution)

    def detach(self):
        return self

    def cpu(self):
        return self

    def __float__(self):
        return float(self.value)


class Model:
    def __init__(self, parameters) -> None:
        self.parameters = parameters

    def zero_grad(self, *, set_to_none):
        assert set_to_none is True
        for parameter in self.parameters:
            parameter.grad = None

    def __call__(self, *, row, skip_logits):
        assert skip_logits is True
        result = type("Result", (), {})()
        result.logits = None
        result.loss = Loss(row["loss"], self.parameters, row["gradients"])
        return result


class Torch:
    @staticmethod
    def isfinite(loss):
        return math.isfinite(float(loss))


def test_pairwise_cosines_cover_each_pair_once() -> None:
    gradients = {
        "go": [Tensor([1.0, 0.0])],
        "java": [Tensor([0.0, 2.0])],
        "rust": [Tensor([-1.0, 0.0])],
    }
    rows = pairwise_cosines(gradients)
    assert [(row["left"], row["right"]) for row in rows] == [("go", "java"), ("go", "rust"), ("java", "rust")]
    assert [row["cosine"] for row in rows] == [0.0, -1.0, 0.0]


def test_pcgrad_removes_opposed_component_before_weighted_aggregation() -> None:
    gradients = {
        "go": [Tensor([1.0, 1.0])],
        "java": [Tensor([-1.0, 0.0])],
    }
    aggregate, telemetry = deterministic_pcgrad(gradients, {"go": 0.5, "java": 0.5}, ["go", "java"])
    assert telemetry["projection_count"] == 2
    assert np.allclose(aggregate[0].values, [-0.25, 0.75])
    assert telemetry["pairwise_cosines_before"][0]["cosine"] < 0
    assert telemetry["pairwise_cosines_after"][0]["cosine"] >= 0


def test_sparse_parameter_layout_is_supported() -> None:
    gradients = {
        "go": [Tensor([1.0]), None],
        "java": [Tensor([1.0]), Tensor([2.0])],
    }
    aggregate, telemetry = deterministic_pcgrad(gradients, {"go": 0.2, "java": 0.8}, ["java", "go"])
    assert np.allclose(aggregate[0].values, [1.0])
    assert np.allclose(aggregate[1].values, [1.6])
    assert math.isfinite(telemetry["aggregate_norm"])


def test_invalid_layout_weights_and_zero_norm_fail_closed() -> None:
    with pytest.raises(ValueError, match="layout"):
        gradient_dot([Tensor([1.0])], [])
    with pytest.raises(ValueError, match="sum to one"):
        deterministic_pcgrad(
            {"go": [Tensor([1.0])], "java": [Tensor([1.0])]},
            {"go": 0.4, "java": 0.4},
            ["go", "java"],
        )
    with pytest.raises(ValueError, match="positive norm"):
        pairwise_cosines({"go": [Tensor([0.0])], "java": [Tensor([1.0])]})
    assert gradient_norm([Tensor([3.0, 4.0])]) == 5.0


def test_group_selection_and_projection_order_are_deterministic() -> None:
    assert evenly_spaced_group_indices(64, 8) == [0, 9, 18, 27, 36, 45, 54, 63]
    assert rotated_lane_order(["go", "java", "javascript", "typescript", "python", "rust"], 3502, 0) == [
        "python", "rust", "go", "java", "javascript", "typescript"
    ]


def test_conflict_threshold_requires_both_global_and_javascript_family_evidence() -> None:
    js_conflict = [[{"left": "go", "right": "typescript", "cosine": -0.2}]] * 4
    other_conflict = [[{"left": "go", "right": "java", "cosine": -0.2}]] * 4
    clear = [[{"left": "go", "right": "typescript", "cosine": 0.2}]] * 4
    assert conflict_decision(js_conflict + clear)["stage_2_allowed"] is True
    assert conflict_decision(other_conflict + clear)["stage_2_allowed"] is False


def test_gradient_capture_accumulation_and_assignment_preserve_layout() -> None:
    parameters = [Parameter(Tensor([1.0])), Parameter(None)]
    captured = capture_gradients(parameters)
    parameters[0].grad.values[0] = 9.0
    assert np.allclose(captured[0].values, [1.0])
    accumulated = accumulate_gradients(captured, [Tensor([2.0]), Tensor([3.0])])
    assert np.allclose(accumulated[0].values, [3.0])
    assert np.allclose(accumulated[1].values, [3.0])
    assign_gradients(parameters, accumulated)
    assert np.allclose(parameters[0].grad.values, [3.0])
    assert np.allclose(parameters[1].grad.values, [3.0])


def test_group_contract_reconstructs_unweighted_lane_means() -> None:
    lane_weights = {"go": 0.6, "java": 0.4}
    rows = [
        {"optimizer_group": 0, "lane": "go", "objective_weight": 0.2},
        {"optimizer_group": 0, "lane": "java", "objective_weight": 0.4},
        {"optimizer_group": 0, "lane": "go", "objective_weight": 0.4},
        {"optimizer_group": 1, "lane": "go", "objective_weight": 0.3},
        {"optimizer_group": 1, "lane": "java", "objective_weight": 0.4},
        {"optimizer_group": 1, "lane": "go", "objective_weight": 0.3},
    ]
    groups = split_optimizer_groups(rows, 3, lane_weights)
    weighted = lane_backward_weights(groups[0], lane_weights)
    assert [weight for _, weight in weighted["go"]] == pytest.approx([1 / 3, 2 / 3])
    assert [weight for _, weight in weighted["java"]] == [1.0]


def test_group_contract_rejects_incomplete_or_misweighted_groups() -> None:
    weights = {"go": 0.6, "java": 0.4}
    with pytest.raises(ValueError, match="complete"):
        split_optimizer_groups([{"optimizer_group": 0}], 2, weights)
    bad = [
        {"optimizer_group": 0, "lane": "go", "objective_weight": 0.5},
        {"optimizer_group": 0, "lane": "java", "objective_weight": 0.5},
    ]
    with pytest.raises(ValueError, match="mass"):
        split_optimizer_groups(bad, 2, weights)


def test_collect_lane_gradients_builds_unweighted_lane_means_and_clears_model() -> None:
    parameters = [Parameter(), Parameter()]
    model = Model(parameters)
    rows = [
        {"lane": "go", "objective_weight": 0.2, "loss": 1.0, "gradients": [[1.0], [2.0]]},
        {"lane": "java", "objective_weight": 0.4, "loss": 4.0, "gradients": [[4.0], [1.0]]},
        {"lane": "go", "objective_weight": 0.4, "loss": 3.0, "gradients": [[4.0], [2.0]]},
    ]
    gradients, losses = collect_lane_gradients(
        model,
        rows,
        parameters,
        {"go": 0.6, "java": 0.4},
        lambda row, device: {"row": row},
        Torch,
    )
    assert np.allclose(gradients["go"][0].values, [3.0])
    assert np.allclose(gradients["go"][1].values, [2.0])
    assert np.allclose(gradients["java"][0].values, [4.0])
    assert losses["go"]["raw_loss_mean"] == 2.0
    assert all(parameter.grad is None for parameter in parameters)


def test_measure_gradient_conflicts_binds_group_identity_and_decision() -> None:
    parameters = [Parameter()]
    model = Model(parameters)
    groups = []
    for group_index in range(2):
        groups.append([
            {"lane": "javascript", "objective_weight": 0.5, "loss": 1.0, "gradients": [[1.0, 0.0]]},
            {"lane": "typescript", "objective_weight": 0.5, "loss": 1.0, "gradients": [[-1.0, 0.0]]},
        ])
    report = measure_gradient_conflicts(
        model,
        groups,
        [0, 1],
        parameters,
        {"javascript": 0.5, "typescript": 0.5},
        lambda row, device: {"row": row},
        Torch,
        negative_cosine_threshold=-0.05,
        minimum_negative_groups=2,
        minimum_javascript_typescript_groups=2,
    )
    assert [row["optimizer_group"] for row in report["groups"]] == [0, 1]
    assert report["decision"]["stage_2_allowed"] is True
