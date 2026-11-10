"""Reproduce the hypothetical migration-priority example with Python 3.11+."""

import csv
from dataclasses import dataclass
from graphlib import CycleError, TopologicalSorter
from heapq import heappop, heappush
from math import isfinite
from pathlib import Path
from platform import python_version


@dataclass(frozen=True)
class Task:
    identifier: str
    kind: str
    lifetime: float
    lead_time: float
    prerequisites: tuple[str, ...] = ()


def prioritise(tasks, horizon):
    """Return a dependency-safe priority order, own margins and inherited margins."""
    if not isfinite(horizon) or horizon < 0:
        raise ValueError("The planning horizon must be finite and nonnegative.")
    inventory = {task.identifier: task for task in tasks}
    if len(inventory) != len(tasks):
        raise ValueError("Each task requires a unique identifier.")

    successors = {identifier: [] for identifier in inventory}
    predecessors = {}
    own = {}
    for identifier, task in inventory.items():
        if task.kind not in ("confidentiality", "authentication", "renewal", "enabler"):
            raise ValueError(f"{identifier} requires a known security purpose.")
        if any(not isfinite(value) or value < 0 for value in (task.lifetime, task.lead_time)):
            raise ValueError(f"{identifier} requires finite, nonnegative time estimates.")
        if task.kind != "confidentiality" and task.lifetime != 0:
            raise ValueError(f"{identifier} has a lifetime outside the confidentiality model.")
        prerequisites = tuple(dict.fromkeys(task.prerequisites))
        for prerequisite in prerequisites:
            if prerequisite not in inventory:
                raise ValueError(f"{identifier} has an unresolved prerequisite: {prerequisite}")
            successors[prerequisite].append(identifier)
        predecessors[identifier] = prerequisites
        own[identifier] = None if task.kind == "enabler" else task.lifetime + task.lead_time - horizon

    try:
        topological = list(TopologicalSorter(predecessors).static_order())
    except CycleError as error:
        raise ValueError("Resolve the dependency cycle before prioritising.") from error

    priority = {identifier: margin if margin is not None else -float("inf")
                for identifier, margin in own.items()}
    for identifier in reversed(topological):
        for prerequisite in predecessors[identifier]:
            priority[prerequisite] = max(priority[prerequisite], priority[identifier])

    remaining = {identifier: len(deps) for identifier, deps in predecessors.items()}
    ready = []
    for identifier, count in remaining.items():
        if count == 0:
            heappush(ready, (-priority[identifier], identifier))
    order = []
    while ready:
        _, identifier = heappop(ready)
        order.append(identifier)
        for successor in successors[identifier]:
            remaining[successor] -= 1
            if remaining[successor] == 0:
                heappush(ready, (-priority[successor], successor))
    return order, own, priority


TASKS = (
    Task("evidence_archive", "renewal", 0.0, 3.5, ("pki_core",)),
    Task("gateway", "confidentiality", 1.5, 1.0),
    Task("patch_signing", "authentication", 0.0, 2.5, ("pki_core",)),
    Task("pki_core", "authentication", 0.0, 2.0, ("vendor_enablement",)),
    Task("records_vault", "confidentiality", 7.0, 3.0, ("pki_core",)),
    Task("vendor_enablement", "enabler", 0.0, 1.0),
)
EXPECTED_ORDER = [
    "vendor_enablement", "pki_core", "records_vault",
    "evidence_archive", "gateway", "patch_signing",
]


def assert_invalid(tasks, horizon, expected_message):
    try:
        prioritise(tasks, horizon)
    except ValueError as error:
        assert expected_message in str(error), str(error)
    else:
        raise AssertionError("Invalid input was accepted.")


def main():
    output = Path(__file__).resolve().parent
    rows = []
    for horizon in (4, 8):
        order, own, priority = prioritise(TASKS, horizon)
        positions = {identifier: index for index, identifier in enumerate(order, 1)}
        assert order == EXPECTED_ORDER
        assert prioritise(tuple(reversed(TASKS)), horizon)[0] == order
        assert own["records_vault"] == 10 - horizon
        assert priority["vendor_enablement"] == priority["pki_core"] == 10 - horizon
        for task in TASKS:
            assert all(positions[dep] < positions[task.identifier] for dep in task.prerequisites)
            rows.append((horizon, task.identifier, task.kind, task.lifetime, task.lead_time,
                         " ".join(task.prerequisites), own[task.identifier],
                         priority[task.identifier], positions[task.identifier]))

    flat = sorted((identifier for identifier, margin in own.items() if margin is not None),
                  key=lambda identifier: (-own[identifier], identifier))
    assert flat.index("records_vault") < flat.index("pki_core")
    assert_invalid((Task("a", "authentication", 0, 1, ("b",)),
                    Task("b", "authentication", 0, 1, ("a",))), 4, "cycle")
    assert_invalid((Task("a", "authentication", 0, 1, ("missing",)),), 4, "unresolved prerequisite")
    assert_invalid((TASKS[1], TASKS[1]), 4, "unique identifier")
    assert_invalid((Task("a", "confidentiality", -1, 1),), 4, "nonnegative")
    assert_invalid((Task("a", "authentication", 1, 1),), 4, "outside the confidentiality model")

    with (output / "migration_scenarios.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(("horizon_years", "task_id", "security_purpose", "confidentiality_years",
                         "end_to_end_lead_years", "prerequisites", "own_margin_years",
                         "propagated_margin_years", "execution_order"))
        writer.writerows(rows)
    findings = [
        f"Python {python_version()}, standard library only.",
        "Inputs are hypothetical. Both horizons are planning assumptions.",
        "Records vault own exposure margin: +6 years at z=4 and +2 years at z=8.",
        "Order under both scenarios: " + " -> ".join(EXPECTED_ORDER) + ".",
        "Flat sort violates the prerequisite from pki_core to records_vault.",
        "Checked precedence, priority inheritance, stable ties, invalid inputs and cycles.",
    ]
    (output / "validation.txt").write_text("\n".join(findings) + "\n", encoding="utf-8")
    print("\n".join(findings))


if __name__ == "__main__":
    main()
