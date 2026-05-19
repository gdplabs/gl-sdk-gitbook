---
icon: wrench
---

# Creating a Skill

A beginner-friendly, step-by-step guide to building a custom Agent Skill from scratch — no scripts, no dependencies, just a single file.

***

## What You Need (The Bare Minimum)

A skill requires exactly **two things**:

1. **A folder** — with a name using only lowercase letters, numbers, and hyphens
2. **A `SKILL.md` file inside that folder** — containing YAML frontmatter and markdown instructions

That's it. No scripts, no config files, no dependencies.

```
my-skill-name/
└── SKILL.md
```

***

## The SKILL.md File Structure

Every `SKILL.md` has two parts:

#### 1. YAML Frontmatter (Required)

This is metadata at the very top of the file, wrapped in `---` fences:

```yaml
---
name: my-skill-name
description: A clear description of what this skill does and when to use it.
---
```

| Field         | Required? | Rules                                                                                                                                                     |
| ------------- | --------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`        | ✅ Yes     | Max 64 characters. Lowercase letters, numbers, hyphens only. No starting/ending hyphens.                                                                  |
| `description` | ✅ Yes     | Max 1024 characters. Describes what the skill does **and when to use it**. This is how the agent decides whether to activate your skill — so be specific! |

{% hint style="info" %}
**Tip:** The `description` is the most important part. A vague description like "helps with formatting" means the agent won't know when to trigger your skill. Be explicit: "When the user asks to format meeting notes, apply this specific template..."
{% endhint %}

#### 2. Markdown Body (Your Instructions)

Everything below the frontmatter is the instructions the agent will follow. There are no format restrictions — write whatever helps the agent do the job. Common sections include:

* **Instructions** — step-by-step guidance
* **Examples** — sample inputs and expected outputs
* **Rules / Guidelines** — constraints and edge cases

{% hint style="warning" %}
**Keep it under \~5,000 tokens** (roughly 500 lines). If your skill needs more detail, you can add a `references/` folder with additional files the agent can read on demand.
{% endhint %}

***

## Example Skill

Let's build a real skill that demonstrates the difference between what an LLM does _without_ a skill vs. _with_ one. The complete Skill Directory can be downloaded here:

{% embed url="https://drive.google.com/drive/u/4/folders/10LjAGcIkfGGd15mXCKpoV0te5Ip_5u9W" %}

### The Idea

We'll create a skill that formats daily standup updates into a very specific, unconventional format that no LLM would produce on its own:

* A **haiku summary** at the top (5-7-5 syllable poem)
* A **custom priority code** using nature emoji (🔥 P1-FIRE, 🌊 P2-WAVE, 🍃 P3-LEAF, ☁️ P4-CLOUD)
* A **"vibe check"** energy rating from 1–5 using moon phases (🌑🌒🌓🌔🌕)
* A strict, opinionated section order that differs from typical standup formats

***

### Step-by-Step: Build It

#### Step 1: Create the Folder

Create a folder called `haiku-standup`:

```
haiku-standup/
```

#### Step 2: Create SKILL.md

Inside that folder, create a file called `SKILL.md` with this content:

````markdown
---
name: haiku-standup
description: >
  Format daily standup updates into the team's custom standup template.
  Use when the user mentions "standup", "daily update", "what I did yesterday",
  or asks to format their work status. Applies haiku summaries, nature-emoji
  priority codes, and moon-phase energy ratings.
---

# Haiku Standup Formatter

Format every standup update using the exact structure below. Never skip sections.
Never reorder them. Always generate the haiku — do not ask the user to write one.

## Output Template

```
📋 STANDUP — [TODAY'S DATE in YYYY-MM-DD]

🎋 [A haiku summarizing the update — must be valid 5-7-5 syllable structure]

🔥 BLOCKER [PRIORITY-CODE]
[Blocker description — what it is and what it's blocking]
(If no blockers, write: "☁️ ALL CLEAR — No blockers today")

✅ DONE
- [Completed item 1]
- [Completed item 2]

🎯 TODAY
- [Planned item 1]
- [Planned item 2]

Vibe Check: [MOON-RATING] ([N]/5)
```

## Priority Codes

Assign a priority code to every blocker using this scale:

| Code       | Emoji | Meaning                               |
|------------|-------|---------------------------------------|
| P1-FIRE    | 🔥    | Blocked NOW — cannot make progress    |
| P2-WAVE    | 🌊    | Slowed down — workaround exists       |
| P3-LEAF    | 🍃    | Minor friction — can work around it   |
| P4-CLOUD   | ☁️    | Informational — not actually blocking |

If the user doesn't specify severity, infer it from context. When in doubt, default
to P2-WAVE.

## Vibe Check (Energy Rating)

Ask the user for their energy level OR infer it from their tone:

| Rating | Display              | Meaning         |
|--------|----------------------|-----------------|
| 1/5    | 🌑🌑🌑🌑🌑           | Rough day       |
| 2/5    | 🌒🌑🌑🌑🌑           | Low energy      |
| 3/5    | 🌒🌒🌓🌑🌑           | Steady          |
| 4/5    | 🌒🌒🌒🌔🌑           | Good flow       |
| 5/5    | 🌕🌕🌕🌕🌕           | On fire         |

If the user doesn't mention energy, default to 3/5 (Steady) unless their tone
clearly suggests otherwise (e.g., frustrated = 2/5, excited = 4/5).

## Rules

1. The haiku MUST be a valid 5-7-5 syllable haiku about the actual work described.
2. Always use today's real date, not a placeholder.
3. If the user provides unstructured text, extract and categorize items yourself.
4. "DONE" items go in past tense. "TODAY" items go in present/future tense.
5. Never add items the user didn't mention.
6. If something could be either DONE or TODAY, ask for clarification.
````

#### Step 3: Package It

Depending on your platform (you can use it on _any_ client that can use Skills!):

{% tabs %}
{% tab title="Claude Code" %}
Place the folder in either of these locations:

* Project-level: `.claude/skills/haiku-standup/`
* Personal: `~/.claude/skills/haiku-standup/`

Claude Code discovers skills automatically. Note that Claude Code **does not retroactively** detect skills; you will have to restart Claude Code if you've installed the skill after booting up Claude Code.
{% endtab %}

{% tab title="Claude.ai" %}
1. Zip the `haiku-standup` folder (the zip should contain the folder, not just the file)
2. Go to **Settings → Capabilities**
3. Scroll to **Skills** and click **Upload skill**
4. Upload the zip file
5. Toggle the skill **ON**
{% endtab %}

{% tab title="VSCode" %}
Place the folder at:

* `.github/skills/haiku-standup/`
{% endtab %}
{% endtabs %}

#### Step 4: Test It

Start a new chat and send the following prompt (no need for fancy system prompts or any special instructions):

> Standup: Yesterday I migrated the user table to the new schema and pair-programmed with Alex on the search feature. Today I'm writing tests for the migration. I'm stuck waiting on QA to finish their test plan.

The agent should produce output matching the exact template from the skill — haiku, priority codes, moon-phase rating and all. Following the [implementing-with-agent.md](../quickstart/implementing-with-agent.md "mention") Tutorial, the sample output can be something like this (your mileage will vary):

{% columns %}
{% column %}
<details>

<summary> With Skill</summary>

📋 STANDUP — 2026-02-11

🎋 Users moved to new Paired on search, tests in progress Waiting on QA

🔥 BLOCKER P1-FIRE Waiting on QA to finish their test plan — blocking writing and running the migration tests.

✅ DONE

* Migrated the user table to the new schema
* Pair-programmed with Alex on the search feature

🎯 TODAY

* Write tests for the migration

Vibe Check: 🌒🌒🌓🌑🌑 (3/5)

</details>
{% endcolumn %}

{% column %}
<details>

<summary>Without Skill</summary>

Nice — that’s a good standup. I polished it and added a few things you can do while you wait on QA, plus a short message you can send to QA to unblock things.

Polished standup (short)

* Yesterday: Migrated the user table to the new schema; pair-programmed with Alex on the search feature.
* Today: Writing unit + integration tests for the migration and preparing rollback tests for staging.
* Blockers: Waiting on QA to finish their test plan for acceptance criteria / QA sign-off.

Polished standup (one-line for Slack) "Yesterday: migrated user table to new schema and pair-programmed with Alex on search. Today: writing migration unit/integration/rollback tests. Blocked: waiting on QA’s test plan — pinged them for ETA."

Suggested message to QA (copy/paste) Hi @QA-team — quick status check on the test plan for the user-table migration. We need acceptance criteria and any test cases that cover data integrity, constraint/index validation, rollback behavior, and performance for the upcoming deploy. ETA? I can draft test cases or pair with you to speed this up. Thanks!

What you can do while waiting (practical, unblockable work)

* Write unit tests that validate transformation/mapping logic (these don't require QA).
* Add integration tests that run the migration against a snapshot dataset and verify row counts, key constraints, nullability, and sample rows.
* Create automated rollback/rollback-simulation tests.
* Add a staging smoke-test job (CI) to apply the migration and run basic checks.
* Draft the QA test cases/acceptance criteria to save QA time (they can review & approve).
* Prepare monitoring/alerts and runbook for post-deploy issues.
* Validate performance: run simple timing checks on critical queries using the new schema.

Migration test checklist (use this to draft tests or QA plan)

* Schema: expected columns, types, nullability, default values.
* Data mapping: sample rows transformed correctly, no data loss for critical columns.
* Row counts: total rows before vs after (or per-batch if you chunked migration).
* Foreign keys & indexes: constraints enforced, indexes present and used.
* Uniqueness: unique constraints still hold (or conflicts handled).
* Nullability and defaults: fields set as expected.
* Rollback: reverse migration restores previous schema/data (or documented rollback steps).
* Backups: verify backup exists and restore has been tested.
* Performance: critical queries run within SLA on new schema; migration window/time acceptable.
* Edge cases: very large rows, duplicate keys, malformed data.
* Concurrency: app behavior while migration runs (writes/reads during migration).
* Monitoring: alerts for migration failures, long-running steps, or replication lag.
* Acceptance criteria: explicit pass/fail conditions and sample test cases.

Example quick test snippets (pseudo)

* SQL check for new column and non-null counts: SELECT COUNT(_) FROM information\_schema.columns WHERE table\_name='users' AND column\_name='new\_col'; SELECT COUNT(_) FROM users WHERE new\_col IS NULL; -- should be 0 (if non-null)
* Row-count/integrity test: -- before snapshot: store count -- after migration: assert new\_count = old\_count OR explain expected delta
* Python/pytest pseudo: def test\_user\_mapping(): result = transform\_user(raw\_row) assert result\['email'] == raw\_row\['email'] assert result\['created\_at'] is not None

Want me to:

* Draft the QA test plan (full list of test cases and acceptance criteria)?
* Draft the actual unit/integration test code (tell me language/framework)?
* Send the QA message for you (I can adapt tone/recipients)?

Which of those would be most helpful right now?

</details>
{% endcolumn %}
{% endcolumns %}

The one with the skill keeps it short, concise, and well-formatted. There's no additional system prompt, no need for additional context — it just works.

***

### Common Mistakes to Avoid

| Mistake                                                     | Fix                                                                         |
| ----------------------------------------------------------- | --------------------------------------------------------------------------- |
| Vague `description` ("helps with formatting")               | Be specific about triggers: "When the user asks to format standup notes..." |
| Name uses uppercase or spaces                               | Use only `lowercase-with-hyphens`                                           |
| Zip file contains just the SKILL.md without a parent folder | Always zip the **folder** containing the file                               |
| Instructions are ambiguous                                  | Include concrete examples of expected output                                |
| Trying to do too much in one skill                          | Keep skills focused — one skill, one task                                   |

***

## Quick Reference: Minimum Viable Skill

```
my-skill/
└── SKILL.md
```

```markdown
---
name: my-skill
description: When the user asks to [DO THING], apply [SPECIFIC APPROACH].
---

# My Skill

[Your instructions here — what to do, how to format it, what rules to follow]

## Example

Input: [example input]
Output: [example output]
```

That's all you need to get started. Write the skill, test it, fix what doesn't work, and iterate. The first version is never perfect — and that's fine.

***

## Further Reading

* [Agent Skills Specification](https://agentskills.io/specification) — the full format spec
* [Example Skills Repository](https://github.com/anthropics/skills) — real-world examples from Anthropic
* [Creating Custom Skills (Claude Help Center)](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills) — official guide
* [Agent Skills Standard on GitHub](https://github.com/agentskills/agentskills) — the open standard repo
