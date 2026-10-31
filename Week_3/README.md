# AL03: Ticket Registry, Queue, and Undo

Name: Mark  
Partners: Elijah  
Shared repository: https://github.com/ElijahFer7120/ALGO_AL03_PROJECT_MARK_ELI_SARAH.git  

## My contribution

I copied the supplied files we needed (`ticket_data.py`, `ticket_display.py`, `console_style.py`, and the starter templates for `main.py` / `test_assignment.py`). I added extra color so ticket numbers stand out in yellow and priority levels are easier to see (high red, normal magenta, low dark blue).

Tuesday’s lab was the three of us (Elijah, Sarah, and me). Sarah later finished and turned in her own work since she and I could not be in class on Thursday. Tonight Elijah and I worked through the assignment together on Discord—Monday, Tuesday, and Thursday stages in `main.py` and `test_assignment.py`—switching the keyboard about every 20–30 minutes until we had a full runnable project and passing checks.

## How we worked tonight

We paired on Discord and took turns driving. We covered registry/lookup/priority/category work, queue processing and undo, then Thursday repair/cancel/snapshot work and the matching tests. When the code was in place, we ran `main.py` and `test_assignment.py`, fixed issues, and talked through the results.

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

I used Cursor to help implement and test the required functions and demonstration in `main.py`. I reviewed the code against the assignment contracts and ran `python test_assignment.py` and `python main.py`. The ticket data and base display/style modules came from the instructor’s supplied files; I pasted `ticket_data.py` in unchanged.

## Instructor Comments
