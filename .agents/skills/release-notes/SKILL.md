---
name: release-notes
description: Write release notes for CampusHub from git history. Use when asked for release notes, a changelog entry, "what changed since the last release" or a summary of recent work.
---
# Release notes from git history

Use the git command line; do not guess from memory.

1. Find the range. Run `git describe --tags --abbrev=0` to get the last tag. If there is
   no tag, use the last 20 commits (`git log --oneline -20`).
2. Collect changes: `git log <last-tag>..HEAD --pretty=format:"%h %s (%an)"`.
3. If the GitHub CLI is available (`gh --version` succeeds), also run
   `gh pr list --state merged --limit 30 --json number,title,labels` and use PR titles
   and numbers in the notes. If it is not available, skip this step without error.
4. Group the changes under these headings, leaving out empty ones:
   **New**, **Improved**, **Fixed**, **Security**, **For developers**.
5. Write one line per change for a student audience: what they will notice, not how the
   code changed. Mention PR numbers or commit hashes in brackets.
6. Show the notes to the user. Only write them to `CHANGELOG.md` if the user asks.
