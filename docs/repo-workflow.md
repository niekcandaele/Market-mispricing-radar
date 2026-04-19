# Repo Workflow

This repo is the visible control plane for the ZerveHack project.

Use it to make project state inspectable, not just to store files.

## What lives here

Keep in Git:
- product and technical docs
- issue and milestone tracking
- exported snippets or backups from Zerve
- demo notes, copy, and review artifacts

Keep primary execution in Zerve:
- data ingestion
- feature engineering
- scoring
- explanations
- Streamlit deployment

## Working loop

1. pick or create a Forgejo issue
2. create a branch tied to that issue
3. do the smallest useful chunk of work
4. push early when the branch tells a clear story
5. open a PR with status notes and linked issues
6. merge only when the repo state honestly matches reality

## Branch naming

Use short, readable branch names:
- `feat/<topic>`
- `docs/<topic>`
- `chore/<topic>`
- `bugfix/<topic>`

If useful, prefix with the issue number, for example:
- `docs/3-repo-workflow`
- `feat/6-schema-validation`

## Issue rules

Issues should describe one clear outcome.

Issue bodies should usually include:
- goal
- acceptance criteria
- blockers or dependencies
- short notes if scope changed

Use labels to show both type and status.

Preferred types:
- `type:feature`
- `type:bug`
- `type:chore`
- `type:docs`
- `type:research`

Preferred status labels:
- `status:in-progress`
- `status:blocked`
- `status:needs-review`
- `status:done`

## Milestones

Use milestones to show the current phase at a glance.

Current structure:
- `M1: setup` for repo and planning foundation
- `M2: core workflow` for source, schema, and scoring work
- later milestones for app polish and launch-quality work

Every substantial issue should belong to a milestone unless there is a good reason not to.

## Pull requests

PRs should be small enough to review quickly.

A good PR description says:
- what changed
- why it changed
- linked issues
- test or validation notes
- follow-up work if anything remains

Do not imply completion early. If a PR is partial, say so.

## Status honesty

When work starts:
- add or keep `status:in-progress`
- reference the branch or PR

When blocked:
- add `status:blocked`
- leave one short comment explaining the blocker

When ready for review:
- add `status:needs-review`
- remove stale `status:in-progress`

When finished:
- merge the PR
- close the linked issue
- remove stale status labels

## Collaboration expectation

Niek should be able to open Forgejo and immediately see:
- what the project is
- what is active now
- what is blocked
- what changed recently
- what comes next

That visibility matters more than fancy process.
