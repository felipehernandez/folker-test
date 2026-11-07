# General Strategy

## ADRs (`.aidocs/adrs/`)

- **In plan mode**: you **must** read all ADRs once per session before designing any approach, to understand past decisions and their rationale. Do not re-read them within the same session.
- **In plan mode**: after designing an approach, check whether any of the following apply. If **any** apply, you **must** propose an ADR to the user and include its creation as a step in the plan:
  - Changing data storage strategy (new database, schema redesign, single-table vs multi-table, new ORM/library)
  - Adding, replacing, or removing a core dependency (frameworks, ORMs, SDKs that touch >1 package)
  - Changing communication patterns between services (sync vs async, new queues/topics, API contract changes)
  - Altering authentication, authorization, or security boundaries
  - Modifying deployment topology (new Lambdas, merging/splitting services, new infrastructure components)
  - Any change that would be hard to reverse once data is written or external contracts are established
- When in doubt about whether something merits an ADR, **ask the user if they want to document it**.

## Lessons Learned (`.aidocs/lessons/`)

- **In any mode**: you **must** read all lessons learned at the start of a task to avoid repeating past mistakes.
- **In any mode**: after completing any task of non-trivial size, check whether **any** of the following apply. If **any** apply, you **must** propose documenting a lesson and create the corresponding file:
  - An approach was proposed, implemented, or partially implemented — and then discarded or replaced because it turned out to be wrong, fragile, or a worse design
  - A library, framework, or tool behaved in a non-obvious or surprising way (undocumented edge case, misleading API, unexpected default)
  - A pattern, convention, or constraint was learned from an external codebase or reference that should be applied consistently in this project
  - A user correction revealed a gap in understanding of the project's architecture, conventions, or quality bar
  - A fix or workaround was non-trivial to arrive at and would not be obvious to reproduce from the code alone
- When in doubt about whether something merits a lesson, **ask the user if they want to document it**.