Review the uncommitted changes in this repository against the plan in $ARGUMENTS.

1. Collect context: git status, git diff, git diff --cached, and the plan.
2. Check: does the change do what the plan says, and nothing else? Are all planned tests present
   and meaningful? Look for security problems, missing edge cases, error handling, performance,
   and inconsistency with the surrounding code.
3. Run the test suite.

Do not change any code. Write the report to plans/<plan name>-review.md (for
plans/search.md: plans/search-review.md) - the only file you may create - and show it.
A fresh session can then fix the items from the file.

Report:
Summary: one or two sentences.
Action items, most important first, each with a file:line reference, marked
  MUST-FIX (bug, security issue, plan violation), RECOMMENDED, or CONSIDER.
