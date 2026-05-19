---
icon: circle-info
---

Use `aip status` as the first health check before agent runs.

*Use when:* You need to confirm auth/network issues quickly.

## Command

```bash
aip status
```

## Expected Result

- API URL is reachable.
- Auth is valid.
- Basic resource checks complete.

## Common Failures and Fixes

- `401 Unauthorized`: rotate key with `aip accounts edit <ACCOUNT_NAME>`.
- `timeout` or `connection refused`: update URL and check network/VPN.
- TLS errors: use proper CA/proxy settings for your environment.

## Next Commands

```bash
aip agents list
aip tools list
aip mcps list
```
