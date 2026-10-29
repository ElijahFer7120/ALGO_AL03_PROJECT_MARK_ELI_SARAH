# AL03: Ticket Registry, Queue, and Undo

Name: [John Elijah B. Ferrer]
Partners: [Mark Beckens, Sarah Imhoff]
Shared repository: [URL]
My contribution: [coding in stuff for monday]

## Run

Keep main.py, test_assignment.py, ticket_data.py, ticket_display.py,
console_style.py, and any other imported modules together.

```powershell
py -3.14 main.py
py -3.14 test_assignment.py
```

## Operation Comparison

One short reason per row is enough. Compare list and dictionary behavior;
do not implement every operation twice or maintain two live stores.

| Operation | Representation fit / reason |
| --- | --- |
| Find one ticket by ID | [a list uses an O(n) when scanning stuff, while a dictionary scans with O(1) to find the ID] |
| Update one ticket's priority | [ the list scans the first bit in O(n), while a dictionary, using O(1) locates the ticket and possibly updates it ]   |
| Select tickets in a category | [in a set, Ids are put into a list of category and showing which Ids are in a certain category, it makes things easier to look at what category each IDs are in rather going through the entire database and doesn't alter anything inside of it. ] |

## Work Notes and Reflections

Append brief observations, debugging challenges, changes, and learnings.

- Processing and undo: once it processes T301 and then T302 complete it in order of arrival, it goes into a waitng queue and the rest stays the same 
- Contract or snapshot learning: the program registry function holds a copy of the supplied records and it makes sure that every list or dictionary are updated for anything new added to it. 

These can be short bullets, not an essay or separate evidence document.

## Assistance

got help from github copilot with assisting me with coding and fixing certain issues and explain some concept i couldn't understand

## Instructor Comments

[Reserved for instructor feedback.]