# Run and Wait

Run a runnable and wait for completion. Your runnable entrypoint can use
Prefect `@task` for internal steps; `@flow` is not required because the server
manages the flow wrapper.

Note: GL Runner marks the run as `success` or `failed` based on whether the
entrypoint raises an exception. Prefect task state in the runnable is not
propagated to the GL Runner run status, so custom Prefect states are visible in
Prefect UI but do not change the GL Runner terminal status.

```python
result = runnable.run(payload={"question": "status"}, timeout=120, poll_interval=2)
print(result)
```

Use `trigger()` when you need a run record without waiting:

```python
run = runnable.trigger(payload={"question": "status"})
print(run.id, run.status)
```

`run()` triggers the execution, polls `GET /v1/runs/{run_id}`, and stops when
the status is `success`, `failed`, or `cancelled`.

CLI (key-first — IDs resolved automatically):

```bash
python ./scripts/run.py --runnable-key hello-world --payload '{"question":"status"}' --wait
```

Advanced / direct ID lookup:

```bash
python ./scripts/run.py --runnable-id <id> --payload '{"question":"status"}' --wait
```

Tip:

- Use a longer `timeout` if your runnable does heavier work.
