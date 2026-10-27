"""Optional English-first starter; develop one ticket application across three days."""

from collections import deque
import re  # Used beginning Tuesday.

from console_style import color_text
from ticket_data import TICKETS, SUPPORTED_CATEGORIES
from ticket_display import display_tickets, display_state


# ======================================================================
# MONDAY - Find, update, and select
# Begin after Monday's instruction. Work in this same file all week.
# ======================================================================



def build_registry(records):
    registry = {}
    for record in records:
        if record["id"] in registry:
            raise ValueError(f"Duplicate ID found: {record['id']}")
        registry[record["id"]] = record.copy()
    return registry
    """Return independent ticket records indexed by unique ID."""
    # Begin with an empty dictionary and visit each supplied record.
    # If its ID is already present, raise ValueError rather than overwrite it.
    # Otherwise, store a flat copy of the record under that ID.
    # Return the dictionary; leave the supplied records unchanged.
    raise NotImplementedError("Build the independent ticket registry.")


def scan_lookup(records, ticket_id):
    inspected = 0 
    for record in records:
        inspected += 1
        if record["id"] == ticket_id:
            return record.copy()
    return None
    """Return the first matching ticket, or None when absent."""
    # Visit the records in order, comparing each ID with the requested ID.
    # Return the first match; return None if no record matches.
    raise NotImplementedError("Find a ticket using a list scan.")


def indexed_lookup(registry, ticket_id):
    for key, record in registry.items():
        if key == ticket_id:
            return record
    return None
    """Return the matching live ticket, or None when absent."""
    # Check whether the requested ID is a key in the existing registry.
    # Return its record when present, or None when missing. Do not rebuild it.
    raise NotImplementedError("Find a ticket using its registry key.")


def update_priority(registry, ticket_id, priority):
    if ticket_id not in registry:
        return False
    registry[ticket_id]["priority"] = priority
    return True
    """Update one existing ticket's priority and report whether it was found."""
    # First check whether the ticket exists; if missing, return False unchanged.
    # Change only its priority field, then return True.
    raise NotImplementedError("Update the requested ticket's priority.")


def filter_by_category(registry, category):
    result = []
    for record in registry.values():
        if record["category"] == category:
            result.append(record.copy())
    return result
    """Return independent copies of tickets matching the selected category."""
    # Start an empty result list and visit the live records in registry order.
    # For each matching category, append a flat record copy, not the live record.
    # Return the list; no matches means an empty list.
    raise NotImplementedError("Select copied tickets by category.")


# ======================================================================
# TUESDAY - Process in order and undo one action
# Wait until Tuesday's instruction before beginning this stage.
# ======================================================================

def enqueue_ticket(state, ticket_id):
    ticket = state["registry"].get(ticket_id)
    if ticket is None or ticket["status"] != "open" or ticket_id in state["pending"]:
        return False
    state["pending"].append(ticket_id)
    return True
    # The following lines are unreachable and should be removed:
    # """Queue a known open ticket once, returning whether it was accepted."""
    # Check that the ID exists, its ticket is open, and it is not already waiting.
    # If any check fails, return False without changing any part of state.
    # Otherwise, add the ID at the back of pending and return True.


def process_next(state):
    if not state["pending"]:
        return None
    ticket_id = state["pending"].popleft()
    ticket = state["registry"].get(ticket_id)
    if ticket is None:
        return None
    state["undo"].append({"ticket_id": ticket_id, "previous_status": ticket["status"]})
    ticket["status"] = "completed"
    return ticket_id
    """Complete the oldest waiting ticket and remember its previous status."""
    # If pending is empty, return None without changing state.
    # Take the oldest ID from the front of pending and find its live ticket.
    # Append a history record with named ticket_id and previous_status fields.
    # Mark the ticket completed and return its ID.
    raise NotImplementedError("Process the oldest pending request.")


def undo_process(state):
    if not state["undo"]:
        return None
    last = state["undo"].pop()
    ticket_id = last["ticket_id"]
    ticket = state["registry"].get(ticket_id)
    if ticket is None:
        return None
    ticket["status"] = last["previous_status"]
    state["pending"].appendleft(ticket_id)
    return ticket_id
    """Restore the latest processed ticket and return it to the queue front."""
    # If history is empty, return None without changing state.
    # Remove the newest history record and use its named fields to find the ticket.
    # Restore only its prior status; keep unrelated priority changes.
    # Return the ID to the front of pending, then return that ID to the caller.
    raise NotImplementedError("Undo the latest successful processing action.")


# ======================================================================
# THURSDAY - Cancel consistently and preserve snapshots
# Wait until Thursday's instruction before beginning this stage.
# ======================================================================

def repair_queue(registry, pending):
    repaired_queue = deque()
    removed_ids = []
    for ticket_id in pending:
        if ticket_id in registry:
            repaired_queue.append(ticket_id)
        else:
            removed_ids.append(ticket_id)
    return repaired_queue, removed_ids
    """Return a new queue of known IDs and a list of removed missing IDs."""
    # Prepare a new empty deque and a list for removed IDs.
    # Visit pending in order: keep known IDs in the new queue, collect missing IDs.
    # Return both collections without changing registry or the original pending.
    # The owning application must install the returned queue into its state.
    raise NotImplementedError("Repair missing-ticket references without reordering.")


def cancel_ticket(state, ticket_id):
    ticket = state["registry"].get(ticket_id)
    if ticket is None or ticket["status"] != "open":
        return False
    if ticket_id in state["pending"]:
        state["pending"].remove(ticket_id)
    del state["registry"][ticket_id]
    return True
    """Remove an open ticket and any waiting request, leaving history unchanged."""
    # Check existence and open status before making any changes.
    # Return False unchanged for a missing or completed ticket.
    # Remove the eligible ticket from the registry and remove its pending reference.
    # You may reuse repair_queue, installing its returned queue into state.
    # Leave other requests in order and history unchanged; return True.
    raise NotImplementedError("Cancel an open ticket consistently.")


def main():
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
    """Show only the daily stages whose operations you have completed."""
    # MONDAY: build a fresh registry from TICKETS.
    # Compare scan/index answers before edits; display a found or missing result.
    # Update one priority. Check a category using SUPPORTED_CATEGORIES membership.
    # Select copied category records and show them using display_tickets.
    # Keep a selection to revisit later; do not call unfinished later-day functions.

    # TUESDAY: add a state dictionary with registry, pending deque, and undo list.
    # Queue two open IDs; process both in arrival order; undo the last processing.
    # Use display_state to make waiting work and restoration clear.
    # Reject unknown, completed, and duplicate pending requests without changes.

    # THURSDAY: use a separate stale-queue example and install its repaired queue.
    # Demonstrate open-ticket cancellation and unchanged state for rejected actions.
    # Compare an earlier saved selection with the registry after update/cancellation.
    # Run all tests, add brief personal README notes, and commit progress.
    # Each partner tests a full personal copy and submits their own repository URL.

    # Replace this message as your Monday baseline becomes ready.
    print("AL03 starter: begin with the Monday section.")


if __name__ == "__main__":
    main()