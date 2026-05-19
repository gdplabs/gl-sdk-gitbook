# Installation

Install the SDK from the monorepo in editable mode during development.

```bash
pip install -e python/gl-runner-sdk
```

## Environment variables

| Variable | Default | Description |
|----------|---------|-------------|
| `GL_RUNNER_API_KEY` | required | API key for authentication |
| `GL_RUNNER_BASE_URL` | `http://localhost:4200` | Base URL |

Copy `.env.example` to `.env` for local SDK usage. For integration tests, copy
`.env.test.example` to `.env.test` and fill in a live API key.

## Tests

```bash
python -m pytest
```

Integration tests auto-skip unless they can reach `GL_RUNNER_BASE_URL` and
`GL_RUNNER_API_KEY` is configured.
