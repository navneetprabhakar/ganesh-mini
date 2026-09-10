import math

import numpy as np
import pytest

from scripts.train.gradient_conflict import (
    conflict_decision,
    deterministic_pcgrad,
    evenly_spaced_group_indices,
    gradient_dot,
    gradient_norm,
    pairwise_cosines,
    rotated_lane_order,
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
