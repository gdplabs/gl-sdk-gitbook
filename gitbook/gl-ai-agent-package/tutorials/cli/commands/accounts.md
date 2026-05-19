---
icon: square-user
---

Accounts are named credential profiles in `~/.aip/config.yaml`.

*Use when:* You switch between environments (dev, staging, prod) during agent development.

## Placeholders

- `<ACCOUNT_NAME>`: profile name, for example `prod`.

## Common Commands

```bash
aip accounts add <ACCOUNT_NAME>
aip accounts list
aip accounts use <ACCOUNT_NAME>
aip accounts show <ACCOUNT_NAME>
```

## Rotate Credentials

```bash
aip accounts edit <ACCOUNT_NAME>
```

Non-interactive update:

```bash
aip accounts edit <ACCOUNT_NAME> --url "https://your-aip-instance.com" --key "${AIP_API_KEY}"
```

## Rename and Remove

```bash
aip accounts rename <ACCOUNT_NAME> <NEW_ACCOUNT_NAME>
aip accounts remove <NEW_ACCOUNT_NAME>
```

## Expected Result

- `aip accounts use <ACCOUNT_NAME>` succeeds and `aip status` shows valid connectivity.
