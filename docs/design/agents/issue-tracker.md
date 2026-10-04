# Issue tracker: BB Tasks

Issues, specs, and tickets for this repo live in **BB Tasks**, the builtin
tracker plugin, under the tracker project `BB` (prefix `BB-…`). The tracker
project is linked to the bb project `proj_2pvwdfhujq`, so `bb tasks` works
here without `--project`.

Use the `bb tasks` CLI for all operations. The `tasks` skill documents the
full surface; this file records the conventions the engineering skills follow.

## Conventions

- **Create a task**: `bb tasks create --title "..." --description "..."`. Use
  `--description-file <path>` for long bodies rather than shell-quoting them.
- **Read a task**: `bb tasks show <KEY>`, or `bb tasks show <KEY> --json` when
  the output drives commands or code.
- **List tasks**: `bb tasks list [--status <s>] [--label <name>]`, capped at
  100 rows; raise with `--limit 1-500` and page with `--cursor` in JSON mode.
  A mutation makes an old cursor stale, so restart paging after a write.
- **Comment**: `bb tasks comment <KEY> --body "..."`. One substantive comment
  per meaningful milestone, not a progress ping per step.
- **Labels**: `bb tasks update <KEY> --add-label <name>` /
  `--remove-label <name>`. Labels must already exist (`bb tasks label create`).
- **Status**: `bb tasks update <KEY> --status <backlog|todo|in_progress|in_review|done|canceled>`.
  Use `in_review` when implementation is done but review remains; `done` only
  when the completion criteria are met.
- **Move between states**: the same `update --status` call. There is no
  separate close.

## Hierarchy: subtasks, not dependencies

`--parent <KEY>` nests a task one level under another; `--no-parent` promotes
it back to the top level. A spec → tickets breakdown is a parent task with
child tasks.

**There is no many-to-many *blocked by* edge in this tracker.** Blocking edges
must be written as prose in the description ("Blocked by: BB-3, BB-7") and are
maintained by hand. `/to-tickets` and `/wayfinder` still declare their edges
explicitly, but "work the frontier, blockers first" is a human judgement call
here, not something the tracker can answer.

## Dispatch: ticket → thread

- **Dispatch**: `bb tasks dispatch <KEY> --preset <name>` spawns a new agent
  thread on the ticket, with the preset's provider, model, permissions, and
  environment. Add `--instructions` for dispatch-specific context.
- **Attach / detach**: `bb tasks attach <KEY>` / `bb tasks detach <KEY>
  [--thread <id>]` keep a thread's association accurate across handoffs.
- **List workers**: `bb tasks threads <KEY>`.
- **Artifacts**: `bb tasks attachment add <KEY> --file <path>`; read back with
  `bb tasks attachment get <id> --out <path>`.

## Reporting back to a thread

`bb tasks comment <KEY> --body "..." --notify` delivers the comment to the
thread that authored the ticket's most recent agent reply, resuming it if idle.
Without a prior agent reply the comment is recorded without being delivered.

## When a skill says "publish to the issue tracker"

Create a task with `bb tasks create`, applying the `ready-for-agent` label.
Emit `::task{key="BB-12"}` on its own line in the thread response so the reader
gets a live card.

## When a skill says "fetch the relevant ticket"

Run `bb tasks show <KEY>`, plus `bb tasks threads <KEY>` when the task's
attached workers matter.

## When a skill says "close" or "resolve"

`bb tasks update <KEY> --status done`, with a comment saying what was verified.
Never mark a blocked task done.

## Dispatching agents

**This is the mechanism for spawning agents on this repo. Do not use Hermes
`delegate_task`** — it runs agents outside BB, so they never appear on the board
and cannot be audited or resumed. Dispatch instead:

```sh
bb tasks dispatch <KEY> --preset default
```

The `default` preset is the only dispatch preset here. It spawns a real bb thread
(`acp-hermes-agent`, project-default environment) and attaches it to the ticket
automatically.

**The ticket body is the agent's entire brief.** A dispatched thread has no
memory of the chat that spawned it. Acceptance criteria, evidence standards, and
out-of-scope notes go in the body *before* dispatching, not in a follow-up
comment.

**Concurrency cap: 3 dispatched agents at once.** The host permits 8; 3 is this
project's deliberate limit. Check before dispatching:

```sh
bb tasks list --project BB --status in_progress
```

Wait for a slot rather than exceeding the cap. Do not raise a bb concurrency
limit to enforce this — that is a server-side runaway guard, not scheduling.

## Wayfinding: label vocabulary

Beyond the five triage labels, the `/wayfinder` flow uses these on the `BB`
project:

| Label | Meaning |
|---|---|
| `wayfinder:map` | The map issue: destination, notes, decisions-so-far, fog |
| `wayfinder:research` | AFK — read sources, write a cited report |
| `wayfinder:prototype` | HITL — raise fidelity on a design question |
| `wayfinder:grilling` | HITL — a decision that needs the user |
| `wayfinder:task` | Work that must happen before a decision can be made |

## Deleting tasks

There is **no `bb tasks delete` command**, and `bb plugin rpc list tasks` /
`bb plugin rpc inspect` return **nothing** — the tasks plugin's methods are not
in the discoverable set. The methods still work when called directly, and the
server validates input against the plugin's zod schema (a bad id fails loudly
with `HTTP 400: rpc input validation failed` rather than doing something
destructive):

```sh
echo '{"taskId":"<ulid>"}' > /tmp/in.json
bb plugin rpc call tasks deleteTask --input-file /tmp/in.json --json
echo '{"projectId":"<ulid>","force":false}' > /tmp/in.json
bb plugin rpc call tasks deleteProject --input-file /tmp/in.json --json
```

Note that `null` input is rejected — write `{}` for no-argument methods such as
`listProjects`.

Because the shape is not discoverable, **read the expected input from the
plugin's own bundle** before calling: the contract lives in
`bb-app/server/dist/builtin-plugins/tasks/dist/server.js` (grep
`deleteTask:{input:`). Deletion is irreversible: confirm with the user, and
verify what would be lost (descriptions, comments, attachments, attached
threads) before acting. Prefer deleting individual tasks over `deleteProject`;
pass `force: false` so a non-empty project refuses rather than cascading.
