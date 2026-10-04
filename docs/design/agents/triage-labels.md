# Triage Labels

The skills speak in terms of five canonical triage roles. This file maps those
roles to the label strings created in the BB Tasks project `BB`. The label
names are identical to the role names, so no mapping is needed.

| Label in mattpocock/skills | Label in our tracker | Meaning                                  |
| -------------------------- | -------------------- | ---------------------------------------- |
| `needs-triage`             | `needs-triage`       | Maintainer needs to evaluate this issue  |
| `needs-info`               | `needs-info`         | Waiting on reporter for more information |
| `ready-for-agent`          | `ready-for-agent`    | Fully specified, ready for an AFK agent  |
| `ready-for-human`          | `ready-for-human`    | Requires human implementation            |
| `wontfix`                  | `wontfix`            | Will not be actioned                     |

All five exist as labels on the `BB` tracker project. A label that doesn't
exist yet is created once with `bb tasks label create --project BB --name
<label>`; skills then only ever apply existing labels.

When a skill mentions a role (e.g. "apply the AFK-ready triage label"), use
the corresponding label string from this table.
