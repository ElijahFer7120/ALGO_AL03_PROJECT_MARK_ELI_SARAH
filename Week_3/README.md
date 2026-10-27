# AL03: Ticket Registry, Queue, and Undo

Name: Mark  
Partners: [name(s)]  
Shared repository: [URL]  
My contribution: Implemented the ticket registry, lookup, priority update, category selection, queue processing, undo, queue repair, and cancellation functions. Wrote tests and a scripted demonstration.

## Run

Keep main.py, test_assignment.py, ticket_data.py, ticket_display.py,
console_style.py, and any other imported modules together.

```powershell
py -3.14 main.py
py -3.14 test_assignment.py
```

## Operation Comparison

| Operation | Representation fit / reason |
| --- | --- |
| Find one ticket by ID | A list scan checks records one by one (O(n)); a dictionary lookup uses the ID key (expected average O(1)). |
| Update one ticket's priority | A dictionary finds the live record directly by ID, so only that record needs to be changed. |
| Select tickets in a category | A list scan through dictionary values checks each ticket's category (O(n)); the result is copied so later changes do not alter the selection. |

## Work Notes and Reflections

- Processing and undo: Processing T301 and then T302 completed them in arrival order. One undo restored T302 to the front of the queue while T301 stayed completed.
- Contract or snapshot learning: The registry holds independent copies of the supplied records, and a saved category selection stays unchanged when the live registry is updated or a ticket is cancelled.

## Assistance

I used GitHub Copilot to help implement and test the required functions and demonstration. I reviewed the code against the assignment contracts and ran `python test_assignment.py` and `python main.py`. `ticket_data.py` and `ticket_display.py` were supplied assignment modules; `console_style.py` uses the supplied console-color helper.

## Instructor Comments
