---
icon: sourcetree
---

# Sources

Skills can be installed from various sources. Each source type may have its own specific parameters, but they all share a common interface.

## Core Parameters

All sources require these parameters:

| Parameter     | Description                                              |
| ------------- | -------------------------------------------------------- |
| `source`      | A valid Skill Directory (must contain a `SKILL.md` file) |
| `destination` | Local directory where the skill will be installed        |

Additional parameters (such as authentication) will vary depending on the source type.

## Currently Supported Sources

| Source  | Description                                                                      |
| ------- | -------------------------------------------------------------------------------- |
| Github  | We can obtain skills directly from Github repositories, be it public or private. |
| ClawHub | We can obtain skills directly from ClawHub-hosted services.                      |
