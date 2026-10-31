# AL03: Ticket Registry, Queue, and Undo

Name: Elijah  
Partners: Mark  
Shared repository: https://github.com/ElijahFer7120/ALGO_AL03_PROJECT_MARK_ELI_SARAH.git  

## My contribution

On this assignment I helped build and test the live ticket application in `main.py` and `test_assignment.py`. In our shared sessions I drove and co-wrote the Monday registry work (`build_registry`, `scan_lookup`, `indexed_lookup`, `update_priority`, `filter_by_category` and their demos), the Tuesday waiting-work flow (`enqueue_ticket`, `process_next`, `undo_process` and the process/undo demonstration), and the Thursday repair and cancel stage (`repair_queue`, `cancel_ticket`, repair/cancel/snapshot demos). I also worked on the matching checks in `test_assignment.py` so rejected actions, empty queue/history, FIFO processing, LIFO undo, queue repair, cancellation, and snapshot independence were covered. Mark copied in the supplied modules and added the extra console colors for ticket numbers and priorities; I focused on the assessed functions, demos, and tests.

I was the only one of our group in class on Thursday. Because our group was unable to work together on Thursday, Sarah decided to turn her assignment alone. Tonight Mark and I worked through the assignment together on Discord—Monday, Tuesday, and Thursday stages in `main.py` and `test_assignment.py`—switching the keyboard about every 20–30 minutes until we had a full runnable project and passing checks.

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
- [Add any extra notes from tonight]

## Assistance

[Tools / help I used tonight — fill in]. Supplied modules came from the instructor starter; Mark copied them into the project.

## Instructor Comments
