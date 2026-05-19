---
icon: lobster
---

# ClawHub

{% hint style="danger" %}
Major caveats when using ClawHub:

1. ClawHub skills **are not inherently compatible** with Agent Skills, despite being a subset of it. Many skills from the Clawhub registry is curated **for OpenClaw** (heartbeat, cron, etc. are **not** a part of the official Agent Skills specification as of the time of writing).
2. ClawHub skills are **user-generated**; while virus checks are provided, be careful when choosing a skill from ClawHub's ever-growing skill collection!
{% endhint %}

Install skills directly from ClawHub registries. By default, we source from the official ClawHub registry: [https://clawhub.ai/skills](https://clawhub.ai/skills)

However, self-hosted instances of ClawHub and own registries are supported.

### Source Formats

The `source` parameter accepts three formats:

| Format    | Example                                                                                            |
| --------- | -------------------------------------------------------------------------------------------------- |
| HTTPS URL | [https://clawhub.ai/pskoett/self-improving-agent](https://clawhub.ai/pskoett/self-improving-agent) |
| Shorthand | `pskoett/self-improving-agent`                                                                     |

#### Equivalent Examples

{% hint style="warning" %}
When using shorthand, we will always resort to fetching from the official ClawHub registry found at https://clawhub.ai. To use self-hosted instances, please use the full URL.
{% endhint %}

A full HTTPS URL:

{% code lineNumbers="true" %}
```python
await SkillFactory.from_clawhub(
    source="https://clawhub.ai/pskoett/self-improving-agent",
    destination=[".openclaw/skills"],
)
```
{% endcode %}

Is equivalent to shorthand with parameters:

{% code lineNumbers="true" %}
```python
await SkillFactory.from_clawhub(
    source="pskoett/self-improving-agent",
    destination=[".openclaw/skills"],
)
```
{% endcode %}

### Parameters

<table><thead><tr><th>Parameter</th><th width="249">Required</th><th>Default</th><th>Description</th></tr></thead><tbody><tr><td><code>source</code></td><td>Yes</td><td></td><td>GitHub repository in any supported format</td></tr><tr><td><code>destination</code></td><td>Yes</td><td></td><td>Local path(s) for skill installation</td></tr><tr><td><code>zipped</code></td><td>No</td><td>False</td><td>Whether the output should be in zip format</td></tr><tr><td><code>name</code></td><td>No</td><td>None</td><td>Custom installation folder name.</td></tr><tr><td><code>overwrite</code></td><td>No</td><td>False</td><td>Whether to overwrite pre-existing installation of said skill.</td></tr><tr><td><code>api_base</code></td><td>No</td><td><a href="https://wry-manatee-359.convex.site">https://wry-manatee-359.convex.site</a></td><td>ClawHub API base URL. Defaults to<br>public ClawHub. Override for self-hosted instances.</td></tr><tr><td><code>ignore_scan</code></td><td>No</td><td>False</td><td>If True, warn instead of raising<br>when security scan finds issues. Defaults to False.</td></tr></tbody></table>

