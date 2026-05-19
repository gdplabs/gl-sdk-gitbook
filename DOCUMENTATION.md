
# Updating GitBook

This section outlines the standard operating procedures for updating GitBook documentation with **slash commands** in AI IDE when code changes are made to the SDK libraries.

## How It Works

1. **Run the workflow** - Execute a slash command in Cursor/Windsurf with the appropriate update mode (see [Available Slash Commands](#available-slash-commands) below).
2. **Analyze changes** - The workflow analyzes SDK code changes and identifies affected documentation.
3. **Update documentation** - GitBook documentation in the `gitbook/**` folder is automatically updated to reflect code changes.
4. **Create pull request** - All documentation changes are packaged into a pull request to the `docs/gitbook-sync` branch.


## Prerequisites (Required Before Using Workflows)

Before running any documentation workflow, ensure you have:

### Required Access & Tools
1. **GitHub CLI** installed and authenticated (`gh auth status` must pass)
2. **Git** configured with your name and email
3. **Repository write access** to create branches and push changes
4. **`docs/gitbook-sync` branch exists** locally in origin and is fetchable (`git fetch origin docs/gitbook-sync` must succeed)

### Repository State
1. Working tree is clean (no uncommitted changes in `gitbook/`)
2. You are on a valid branch (not detached HEAD)

## When to Update Documentation

**Do update documentation when**:
1. New features or components are added to any library
2. Existing API signatures change (parameters, methods, classes)
3. Breaking changes are introduced
4. New providers or integrations are added
5. Configuration options are modified
6. Usage patterns or best practices change

**No need to update documentation when**:
1. Changes are only in test files or internal utilities
2. Changes are refactoring without API modifications
3. Changes are chore-related (e.g., formatting, comments, CI config)

## Available Slash Commands
Below is the list of available slash commands for updating GitBook documentation.

Use this section as the **single source of truth** for selecting a workflow mode.

| Situation                                                        | Use This Mode                         |
| ---------------------------------------------------------------- | ------------------------------------- |
| You want to check for documentation updates without making changes | [Check for Updates](#1-check-for-documentation-updates-read-only)  |
| You have an existing PR or feature branch with committed changes | [PR/Branch-Based Update](#prbranch-based-updates-default)              |
| You want to update docs for existing code (no recent PR)         | [File-Based Update](#file-based-updates)                   |
| Branch does not exist or is not accessible                       | [File-Based Update](#file-based-updates)                   |
| You want to audit documentation completeness                     | [File-Based Update](#file-based-updates)                   |
| You have uncommitted changes                                     | Commit first, then [PR/Branch Update](#prbranch-based-updates-default)

> If a valid PR or branch exists, **always prefer PR/Branch Mode**.
> File-Based Mode is for exceptional or retrospective cases.


### 1. Check for Documentation Updates (Read-Only)

**Command**: `/gitbook.check-for-update`

**Purpose**: Analyze documentation impact without making changes.

**Requirements**:

* PR or branch exists in the repository
* Changes are under `libs/`

**Example**:

```bash
/gitbook.check-for-update #2177
/gitbook.check-for-update feature/add-streaming
/gitbook.check-for-update
```

**Output**: Structured report with priority and suggested actions.

---

### 2. Update GitBook Documentation

**Command**: `/gitbook.update`

**Purpose**: Apply documentation updates based on SDK changes.

**Critical Constraints**:
* Only modifies `gitbook/**`
* Never modifies `libs/**`
* Always creates a PR targeting `docs/gitbook-sync`

**Branch Specification** (Optional):
By default, a new branch will be created following the naming convention.
You can optionally specify a target documentation branch to update.

---

### PR/Branch-Based Updates (Default)

Use this mode when a PR or feature branch with committed changes exists.

**Requirements**:

* PR or branch exists in the repository
* Commits include changes under `libs/`

**Example**:
Assume the code changes are committed in the `feature/add-streaming` branch and `#2177` PR.
```bash

# Create or update the `docs/add-streaming` branch
/gitbook.update
/gitbook.update feature/add-streaming
/gitbook.update #2177

# Update the existing `docs/lm-invoker-parameters` branch
/gitbook.update #2177 using branch docs/lm-invoker-parameters

```

**Behavior**:
Agent proceeds automatically in PR/Branch mode.

---

### File-Based Updates

Use this mode when no suitable PR or branch exists, or when auditing existing documentation.

**Requirements**:

* Files are under `libs/`
* Files exist and are readable
* User confirmation is mandatory before changes are applied

**Examples**:

```bash
# Create new branch (auto-generated name)
/gitbook.update please update docs based on libs/gllm-inference/gllm_inference/lm_invoker/openai_lm_invoker.py

# Update existing branch `docs/lm-invoker-parameters`
/gitbook.update please update docs based on libs/gllm-inference/gllm_inference/lm_invoker/openai_lm_invoker.py using branch docs/lm-invoker-parameters
```

**Behavior**:

1. Analyzes the specified file(s)
2. Identifies documentation gaps
3. Presents an update plan with target branch
4. **Waits for explicit user confirmation**
5. Applies approved changes only

**Confirmation Options**:

* `"yes"` → approve all
* `"yes"` + list → approve selected items
* `"no"` + explanation → reject and revise

**Notes**:
* If you wish to update an existing documentation PR, specify the target branch in your request
* Specifying an existing branch allows you to accumulate multiple documentation updates in a single PR
* If no branch is specified, a new branch will be created with a descriptive name based on the component being documented
* Use the same branch name for related documentation updates to keep them organized in one PR


## After Completion Checklist

* Only `gitbook/**` files changed
* Commit format is correct
* PR targets `docs/gitbook-sync`
* Source commits are referenced

