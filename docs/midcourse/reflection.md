# Reflection

I used Codex as the main AI assistant and grounded its work in the Module 1-3
lecture notes, prompt libraries, the assignment brief, and the actual project
files. The most useful pattern was asking for one bounded behavior with explicit
constraints, then verifying it before continuing. This was especially helpful
for the due-date feature. The assistant connected the Pydantic date field, API
response, query filter, modal field, overdue pill, and tests without requiring a
new architecture. Seeing the live API return `is_overdue=true` made the result
more trustworthy than simply inspecting the code.

AI also slowed me down when plausible alternatives had to be reviewed. Tags
could have been stored as a comma-separated string, a list, or normalized
database records. A larger design would look more sophisticated but would not
fit the in-memory course project. I chose a validated string list and kept comma
parsing only in the frontend. I also corrected the assumption that every
past-due task should be overdue: completed tasks are excluded.

Testing changed how I evaluated the generated output. A green suite alone was
not enough. For the overdue Break Test, I reversed the date comparison and the
test correctly returned the future task instead of the late task. For tags, I
temporarily allowed blank entries and the validation test failed because the API
returned 201 instead of 422. Restoring each rule and rerunning all 32 tests
showed that the tests protected the intended behavior.

The main place human judgment was necessary was scope control. I rejected
notifications, background scheduling, tag database entities, authentication,
and deployment because they were not required. I also preserved exact API
status strings and transition rules during frontend work. The final code is not
just AI output that looks reasonable; it is a set of small decisions supported
by HTTP checks, focused tests, deliberate failures, and documented acceptance
or rejection of AI suggestions.
