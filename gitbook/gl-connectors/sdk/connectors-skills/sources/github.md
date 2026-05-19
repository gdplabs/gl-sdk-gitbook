---
icon: square-github
---

# Github

Install skills directly from GitHub repositories—both public and private.

### Source Formats

The `source` parameter accepts three formats:

| Format    | Example                                                                 |
| --------- | ----------------------------------------------------------------------- |
| HTTPS URL | `https://github.com/anthropics/skills/tree/main/skills/algorithmic-art` |
| SSH       | `git@github.com:anthropics/skills.git`                                  |
| Shorthand | `anthropics/skills`                                                     |

When using SSH or shorthand formats, use the `directory` and `rev` parameters to specify the exact location.

{% hint style="warning" %}
**Note:** When using the SSH format, the `token` parameter is **required**.
{% endhint %}

#### Equivalent Examples

A full HTTPS URL:

{% code lineNumbers="true" %}
```python
await SkillFactory.from_github(
    source="https://github.com/anthropics/skills/tree/main/skills/algorithmic-art",
    destination=[".agents/skills"],
)
```
{% endcode %}

Is equivalent to shorthand with parameters:

{% code lineNumbers="true" %}
```python
await SkillFactory.from_github(
    source="anthropics/skills",
    destination=[".agents/skills"],
    directory="skills/algorithmic-art",
    rev="main",
)
```
{% endcode %}

### Parameters

| Parameter     | Required | Description                                                   |
| ------------- | -------- | ------------------------------------------------------------- |
| `source`      | Yes      | GitHub repository in any supported format                     |
| `destination` | Yes      | Local path(s) for skill installation                          |
| `directory`   | No       | Subdirectory within the repository containing the skill       |
| `rev`         | No       | Revision to checkout—commit hash, branch name, or tag/release |
| `token`       | No       | GitHub personal access token                                  |

### Authentication

The `token` parameter serves two purposes:

* **Private repositories** — Required for accessing non-public repositories
* **Rate limits** — Authenticated requests have significantly higher GitHub API rate limits

{% code lineNumbers="true" %}
```python
await SkillFactory.from_github(
    source="your-org/private-skills",
    destination=[".agents/skills"],
    directory="skills/internal-tool",
    token="ghp_xxxx",
)
```
{% endcode %}
