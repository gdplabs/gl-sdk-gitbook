`aip config ...` is deprecated and gated. Use `aip accounts ...` and
`aip accounts add`/`aip accounts use` for credentials whenever possible.

{% hint style="warning" %}
Legacy config commands are disabled by default. Set
`AIP_ENABLE_LEGACY_CONFIG=1` to run old scripts while you migrate.
{% endhint %}

## When to use legacy config

- Global settings stored in `~/.aip/config.yaml` (for example `timeout` or
  `history_default_limit`).
- Short-term compatibility for existing automation.

## Recommended replacements

- `aip config list` → `aip accounts list`
- `aip config configure` → `aip accounts add <name>`
- `aip config set api_url/api_key` → `aip accounts edit <name> --url ... --key ...`
- `aip config get` → `aip accounts show <name>` (or read `~/.aip/config.yaml`)
- `aip config reset` → `aip accounts remove <name>` for each profile

## Legacy commands (gated)

```bash
AIP_ENABLE_LEGACY_CONFIG=1 aip config list
AIP_ENABLE_LEGACY_CONFIG=1 aip config get api_url
AIP_ENABLE_LEGACY_CONFIG=1 aip config set api_url "https://your-aip-instance.com"
AIP_ENABLE_LEGACY_CONFIG=1 aip config set api_key "$AIP_API_KEY"
AIP_ENABLE_LEGACY_CONFIG=1 aip config set history_default_limit 25
AIP_ENABLE_LEGACY_CONFIG=1 aip config unset api_url
AIP_ENABLE_LEGACY_CONFIG=1 aip config reset --force
```

## Audit helper

Use the built-in audit tool to find deprecated config usage in scripts and CI:

```bash
AIP_ENABLE_LEGACY_CONFIG=1 aip config audit --path "**/*.sh" --path "**/*.yml"
```
