"""Optional English-first starter; develop one ticket application across three days."""

from collections import deque

from consoles_style import color_text
from ticket_data import SUPPORTED_CATEGORIES, TICKETS
from ticket_display import display_state, display_tickets


def build_registry(records):
    """Build an ID-keyed registry of independent ticket copies."""
    registry = {}
    for record in records:
        ticket_id = record["id"]
        if ticket_id in registry:
            raise ValueError(f"Duplicate ticket ID: {ticket_id}")
        registry[ticket_id] = record.copy()
    return registry


def scan_lookup(records, ticket_id):
    """Return the first matching record from a list, or None."""
    for record in records:
        if record["id"] == ticket_id:
            return record
    return None


def indexed_lookup(registry, ticket_id):
    """Return a live registry record by ID, or None."""
    return registry.get(ticket_id)


def update_priority(registry, ticket_id, priority):
    """Update an existing ticket's priority and report whether it existed."""
    ticket = registry.get(ticket_id)
    if ticket is None:
        return False
    ticket["priority"] = priority
    return True


def filter_by_category(registry, category):
    """Return independent copies of registry records in the requested category."""
    return [
        ticket.copy()
        for ticket in registry.values()
        if ticket["category"] == category
    ]


def enqueue_ticket(state, ticket_id):
    """Append a known, open ticket to pending unless it is already queued."""
    ticket = state["registry"].get(ticket_id)
    if (
        ticket is None
        or ticket["status"] != "open"
        or ticket_id in state["pending"]
    ):
        return False
    state["pending"].append(ticket_id)
    return True


def process_next(state):
    """Complete the oldest pending ticket and save its prior status for undo."""
    if not state["pending"]:
        return None
    ticket_id = state["pending"].popleft()
    ticket = state["registry"][ticket_id]
    state["undo"].append(
        {"ticket_id": ticket_id, "previous_status": ticket["status"]}
    )
    ticket["status"] = "completed"
    return ticket_id


def undo_process(state):
    """Restore the latest processed ticket and return it to the queue front."""
    if not state["undo"]:
        return None
    action = state["undo"].pop()
    ticket_id = action["ticket_id"]
    state["registry"][ticket_id]["status"] = action["previous_status"]
    state["pending"].appendleft(ticket_id)
    return ticket_id


def repair_queue(registry, pending):
    """Return a new queue without missing IDs and list the removed IDs."""
    repaired_queue = deque()
    removed_ids = []
    for ticket_id in pending:
        if ticket_id in registry:
            repaired_queue.append(ticket_id)
        else:
            removed_ids.append(ticket_id)
    return repaired_queue, removed_ids


def cancel_ticket(state, ticket_id):
    """Remove an open ticket and its pending references, if it exists."""
    ticket = state["registry"].get(ticket_id)
    if ticket is None or ticket["status"] != "open":
        return False

    del state["registry"][ticket_id]
    state["pending"] = deque(
        pending_id
        for pending_id in state["pending"]
        if pending_id != ticket_id
    )
    return True


def main():
    """Demonstrate the assignment stages with the supplied ticket modules."""
    print("Starting tickets:")
    display_tickets("All supplied tickets", TICKETS)

    registry = build_registry(TICKETS)
    try:
        build_registry(
            [
                {"id": "T999", "title": "First", "category": "account",
                "priority": "low", "status": "open"},
                {"id": "T999", "title": "Second", "category": "account",
                "priority": "high", "status": "open"},
            ]
        )
    except ValueError as error:
        print(f"Duplicate ID check: {error}")
    else:
        raise RuntimeError("The duplicate-ID example was not rejected.")

    print("\nList scan and registry lookup:")
    found_by_scan = scan_lookup(TICKETS, "T301")
    found_by_index = indexed_lookup(registry, "T301")
    t301 = color_text("T301", "ticket")
    t999 = color_text("T999", "ticket")
    if found_by_scan is not None:
        display_tickets(f"List scan: {t301}", [found_by_scan])
    else:
        print(f"List scan: {t301} was not found.")
    if found_by_index is not None:
        display_tickets(f"Registry lookup: {t301}", [found_by_index])
    else:
        print(f"Registry lookup: {t301} was not found.")
    if indexed_lookup(registry, "T999") is None:
        print(f"{t999} was not found.")

    supplied_t301 = scan_lookup(TICKETS, "T301")
    if update_priority(registry, "T301", "high"):
        display_tickets(f"Updated live {t301}", [registry["T301"]])
    if supplied_t301 is not None and supplied_t301["priority"] == "normal":
        print(f"The supplied {t301} record remains unchanged.")
    if not update_priority(registry, "T999", "high"):
        print("A missing ticket was not added to the registry.")

    selected_category = "account"
    if selected_category in SUPPORTED_CATEGORIES:
        saved_account_selection = filter_by_category(
            registry, selected_category
        )
        display_tickets("Account requests", saved_account_selection)
    else:
        saved_account_selection = []
        print(f"Unsupported category: {selected_category}")
    if "classroom" in SUPPORTED_CATEGORIES:
        display_tickets("Classroom requests", filter_by_category(
            registry, "classroom"
        ))
    if "parking" not in SUPPORTED_CATEGORIES:
        print("Parking is not a supported category.")

    state = {
        "registry": build_registry(TICKETS),
        "pending": deque(),
        "undo": [],
    }
    for ticket_id in ("T301", "T302", "T301", "T999", "T306"):
        colored_id = color_text(ticket_id, "ticket")
        print(f"Enqueue {colored_id}: {enqueue_ticket(state, ticket_id)}")
    display_state("Tuesday: waiting work", state)
    processed = process_next(state)
    print(f"Process next: {color_text(processed, 'ticket') if processed else processed}")
    processed = process_next(state)
    print(f"Process next: {color_text(processed, 'ticket') if processed else processed}")
    update_priority(state["registry"], "T302", "low")
    undone = undo_process(state)
    print(
        f"Undo latest processing: "
        f"{color_text(undone, 'ticket') if undone else undone}"
    )
    display_state("Tuesday: waiting work after undo", state)

    repair_registry = build_registry(TICKETS)
    original_pending = deque(("T301", "T999", "T302", "T998"))
    repaired, removed = repair_queue(repair_registry, original_pending)
    repair_state = {
        "registry": repair_registry,
        "pending": repaired,
        "undo": [],
    }
    colored_removed = ", ".join(
        color_text(ticket_id, "ticket") for ticket_id in removed
    )
    print(f"Stale IDs removed: [{colored_removed}]")
    display_state("Thursday: repaired waiting work", repair_state)
    processed = process_next(repair_state)
    print(
        f"Process from repaired queue: "
        f"{color_text(processed, 'ticket') if processed else processed}"
    )
    display_state("Thursday: after repaired-queue processing", repair_state)

    cancellation_state = {
        "registry": build_registry(TICKETS),
        "pending": deque(("T301", "T302")),
        "undo": [],
    }
    print(
        f"Cancel pending {color_text('T301', 'ticket')}: "
        f"{cancel_ticket(cancellation_state, 'T301')}"
    )
    print(
        f"Cancel open {color_text('T304', 'ticket')}: "
        f"{cancel_ticket(cancellation_state, 'T304')}"
    )
    print(
        f"Cancel missing {color_text('T999', 'ticket')}: "
        f"{cancel_ticket(cancellation_state, 'T999')}"
    )
    print(
        f"Cancel completed {color_text('T306', 'ticket')}: "
        f"{cancel_ticket(cancellation_state, 'T306')}"
    )
    display_state("Thursday: after cancellation", cancellation_state)

    snapshot_registry = build_registry(TICKETS)
    saved_account_selection = filter_by_category(snapshot_registry, "account")
    update_priority(snapshot_registry, "T301", "high")
    cancel_ticket(
        {
            "registry": snapshot_registry,
            "pending": deque(),
            "undo": [],
        },
        "T304",
    )
    display_tickets("Saved account snapshot", saved_account_selection)
    display_tickets("Live account records", filter_by_category(
        snapshot_registry, "account"
    ))


if __name__ == "__main__":
    main()
