"""Focused tests for AL03 ticket registry, queue, and undo behavior."""

from collections import deque
from copy import deepcopy

from main import (
    build_registry,
    cancel_ticket,
    enqueue_ticket,
    filter_by_category,
    indexed_lookup,
    process_next,
    repair_queue,
    scan_lookup,
    undo_process,
    update_priority,
)
from ticket_data import SUPPORTED_CATEGORIES, TICKETS


def make_records():
    """Return independent ticket fixtures with varied status and categories."""
    return [
        {
            "id": "T301",
            "title": "Account access",
            "category": "account",
            "priority": "normal",
            "status": "open",
        },
        {
            "id": "T302",
            "title": "Software issue",
            "category": "software",
            "priority": "high",
            "status": "open",
        },
        {
            "id": "T304",
            "title": "Account setup",
            "category": "account",
            "priority": "low",
            "status": "open",
        },
        {
            "id": "T306",
            "title": "Completed request",
            "category": "network",
            "priority": "normal",
            "status": "completed",
        },
    ]


def make_state(records=None):
    """Build an independent registry and empty Tuesday application state."""
    return {
        "registry": build_registry(make_records() if records is None else records),
        "pending": deque(),
        "undo": [],
    }


def check_registry_operations():
    """Check copying, lookup, priority updates, and category snapshots."""
    records = make_records()
    original_records = deepcopy(records)
    registry = build_registry(records)

    assert registry == {record["id"]: record for record in records}
    assert registry["T301"] is not records[0]
    assert scan_lookup(records, "T301") == records[0]
    assert scan_lookup(records, "T999") is None
    assert scan_lookup([], "T301") is None
    assert indexed_lookup(registry, "T301") == records[0]
    assert indexed_lookup(registry, "T999") is None
    assert indexed_lookup(build_registry([]), "T301") is None

    assert update_priority(registry, "T301", "high") is True
    assert registry["T301"]["priority"] == "high"
    assert records == original_records
    assert update_priority(registry, "T999", "high") is False
    assert "T999" not in registry

    saved_account_records = filter_by_category(registry, "account")
    assert [ticket["id"] for ticket in saved_account_records] == [
        "T301",
        "T304",
    ]
    assert filter_by_category(registry, "classroom") == []
    saved_account_records[0]["priority"] = "low"
    assert registry["T301"]["priority"] == "high"
    registry["T304"]["priority"] = "high"
    assert saved_account_records[1]["priority"] == "low"

    with_duplicate_id = [
        {"id": "T999", "title": "First"},
        {"id": "T999", "title": "Second"},
    ]
    try:
        build_registry(with_duplicate_id)
    except ValueError as error:
        assert "T999" in str(error)
    else:
        raise AssertionError("Duplicate ticket IDs must raise ValueError.")


def check_queue_processing_and_undo():
    """Check queue rejection, FIFO processing, and LIFO undo behavior."""
    state = make_state()
    assert undo_process(state) is None
    assert process_next(state) is None

    assert enqueue_ticket(state, "T301") is True
    assert enqueue_ticket(state, "T302") is True
    expected_state = deepcopy(state)
    assert enqueue_ticket(state, "T301") is False
    assert state == expected_state
    assert enqueue_ticket(state, "T999") is False
    assert state == expected_state
    assert enqueue_ticket(state, "T306") is False
    assert state == expected_state

    assert process_next(state) == "T301"
    assert process_next(state) == "T302"
    assert process_next(state) is None
    assert state["registry"]["T301"]["status"] == "completed"
    assert state["registry"]["T302"]["status"] == "completed"
    assert state["undo"] == [
        {"ticket_id": "T301", "previous_status": "open"},
        {"ticket_id": "T302", "previous_status": "open"},
    ]

    update_priority(state["registry"], "T302", "low")
    assert undo_process(state) == "T302"
    assert state["registry"]["T302"]["status"] == "open"
    assert state["registry"]["T302"]["priority"] == "low"
    assert list(state["pending"]) == ["T302"]
    assert state["registry"]["T301"]["status"] == "completed"
    assert state["undo"] == [
        {"ticket_id": "T301", "previous_status": "open"}
    ]
    assert undo_process(state) == "T301"
    assert state["registry"]["T301"]["status"] == "open"
    assert list(state["pending"]) == ["T301", "T302"]
    assert state["undo"] == []
    assert undo_process(state) is None

    assert len(state["pending"]) == len(set(state["pending"]))
    assert all(
        ticket_id in state["registry"]
        and state["registry"][ticket_id]["status"] == "open"
        for ticket_id in state["pending"]
    )


def check_queue_repair():
    """Check repair ordering, returned IDs, and input immutability."""
    registry = build_registry(make_records())
    original_queue = deque(("T301", "T999", "T302", "T998"))
    original_registry = deepcopy(registry)

    repaired, removed = repair_queue(registry, original_queue)
    assert isinstance(repaired, deque)
    assert list(repaired) == ["T301", "T302"]
    assert removed == ["T999", "T998"]
    assert list(original_queue) == ["T301", "T999", "T302", "T998"]
    assert registry == original_registry
    assert repaired is not original_queue

    all_valid, no_removed = repair_queue(
        registry, deque(("T302", "T301"))
    )
    assert list(all_valid) == ["T302", "T301"]
    assert no_removed == []
    all_missing, all_ids_removed = repair_queue(
        registry, deque(("T999", "T998"))
    )
    assert list(all_missing) == []
    assert all_ids_removed == ["T999", "T998"]
    empty, no_empty_removed = repair_queue(registry, deque())
    assert list(empty) == []
    assert no_empty_removed == []


def check_cancellation():
    """Check pending and non-pending cancellation and rejected-action safety."""
    state = make_state()
    state["pending"].extend(("T301", "T302", "T304"))
    state["undo"].append(
        {"ticket_id": "T306", "previous_status": "open"}
    )
    original_history = deepcopy(state["undo"])

    assert cancel_ticket(state, "T301") is True
    assert "T301" not in state["registry"]
    assert list(state["pending"]) == ["T302", "T304"]
    assert state["undo"] == original_history

    assert cancel_ticket(state, "T304") is True
    assert "T304" not in state["registry"]
    assert list(state["pending"]) == ["T302"]

    unchanged_state = deepcopy(state)
    assert cancel_ticket(state, "T999") is False
    assert state == unchanged_state
    assert cancel_ticket(state, "T306") is False
    assert state == unchanged_state


def check_snapshot_independence():
    """Check saved filtered records remain independent of live ticket changes."""
    records = make_records()
    registry = build_registry(records)
    saved_accounts = filter_by_category(registry, "account")
    original_snapshot = deepcopy(saved_accounts)

    assert update_priority(registry, "T301", "high") is True
    state = {"registry": registry, "pending": deque(), "undo": []}
    assert cancel_ticket(state, "T304") is True

    assert saved_accounts == original_snapshot
    assert saved_accounts[0]["priority"] == "normal"
    assert saved_accounts[1]["id"] == "T304"
    assert "T304" not in registry
    assert records == make_records()


def check_supplied_ticket_data():
    """Verify assignment examples against the supplied six-ticket dataset."""
    original_tickets = deepcopy(TICKETS)
    registry = build_registry(TICKETS)
    account_snapshot = filter_by_category(registry, "account")

    assert [ticket["id"] for ticket in account_snapshot] == ["T301", "T304"]
    assert "classroom" in SUPPORTED_CATEGORIES
    assert filter_by_category(registry, "classroom") == []
    assert "parking" not in SUPPORTED_CATEGORIES
    assert update_priority(registry, "T301", "high") is True
    assert registry["T301"]["priority"] == "high"
    assert TICKETS == original_tickets

    state = {"registry": registry, "pending": deque(), "undo": []}
    assert cancel_ticket(state, "T304") is True
    assert [ticket["id"] for ticket in account_snapshot] == ["T301", "T304"]
    assert account_snapshot[0]["priority"] == "normal"
    assert TICKETS == original_tickets


def assignment_checks():
    """Run all assignment behavior and edge-case checks."""
    check_registry_operations()
    check_queue_processing_and_undo()
    check_queue_repair()
    check_cancellation()
    check_snapshot_independence()
    check_supplied_ticket_data()


def main():
    """Run assertions without optimization and report success."""
    if not __debug__:
        raise RuntimeError("Run tests without Python optimization (-O).")
    assignment_checks()
    print("Assignment checks passed.")


if __name__ == "__main__":
    main()
