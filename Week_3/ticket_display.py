"""Presentation helpers only; ticket operations live in main.py."""

from console_style import color_priority, color_text, print_color


def display_tickets(title, records):
    """Show a readable ticket report without changing its records."""
    print()
    print_color(title, "heading")
    if not records:
        print("No tickets to display.")
        return
    for record in records:
        ticket_id = color_text(record["id"], "ticket")
        priority = color_priority(record["priority"])
        print(f"{ticket_id} - {record['title']}")
        print(
            f"  Category: {record['category']} | "
            f"Priority: {priority} | Status: {record['status']}"
        )


def display_state(title, state):
    """Show live tickets, pending order, and the next reversible action."""
    records = []
    for ticket_id in state["registry"]:
        records.append(state["registry"][ticket_id])
    display_tickets(title, records)

    print_color("Waiting work (next first)", "heading")
    if not state["pending"]:
        print("No tickets waiting.")
    else:
        for position, ticket_id in enumerate(state["pending"], start=1):
            colored_id = color_text(ticket_id, "ticket")
            if ticket_id in state["registry"]:
                ticket = state["registry"][ticket_id]
                print(f"  {position}. {colored_id} - {ticket['title']}")
            else:
                print(f"  {position}. {colored_id} - ticket no longer available")

    if state["undo"]:
        last_action = state["undo"][-1]
        colored_id = color_text(last_action["ticket_id"], "ticket")
        print(f"Undo available: return {colored_id} to waiting work.")
    else:
        print("No processing action to undo.")