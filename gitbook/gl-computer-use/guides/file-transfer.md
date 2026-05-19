---
icon: file-arrow-up
---

# File Transfer

GL Computer Use can upload files to the sandbox before a task starts and download files from the sandbox after it completes.

## Upload Files Before the Task

Pass a list of `File` objects to the `files` parameter. Each `File` specifies a destination path inside the sandbox and the file content as bytes.

```python
import asyncio
from gl_computer_use import GLComputerUseClient, File


async def main() -> None:
    client = GLComputerUseClient()

    # Prepare input files
    csv_file = File(
        path="/home/user/data.csv",
        data=b"name,age\nAlice,30\nBob,25\n",
    )
    script_file = File(
        path="/home/user/analyze.py",
        data=b"import csv\nwith open('data.csv') as f:\n    print(list(csv.reader(f)))\n",
    )

    result = await client.run_once(
        "Run the analyze.py script and tell me the output",
        files=[csv_file, script_file],
    )
    print(result.output)


asyncio.run(main())
```

## Download Files After the Task

Pass sandbox paths to `retrieve_files`. After the task completes, `result.file_urls` maps each path to a download URL (presigned when using MinIO, or a local path when using local artifact storage).

```python
import asyncio
from gl_computer_use import GLComputerUseClient


async def main() -> None:
    client = GLComputerUseClient()

    result = await client.run_once(
        "Open a terminal. Generate a summary report and save it to /home/user/report.txt",
        retrieve_files=["/home/user/report.txt"],
    )

    for path, url in result.file_urls.items():
        if url:
            print(f"Download {path} at: {url}")
        else:
            print(f"File {path} was not retrieved")


asyncio.run(main())
```

## Upload and Retrieve in One Task

```python
import asyncio
from gl_computer_use import GLComputerUseClient, File


async def main() -> None:
    client = GLComputerUseClient()

    input_file = File(
        path="/home/user/input.txt",
        data=b"Count the words in this file.\n" * 10,
    )

    result = await client.run_once(
        "Read /home/user/input.txt, count the total words, "
        "and save the result to /home/user/output.txt",
        files=[input_file],
        retrieve_files=["/home/user/output.txt"],
    )

    print("Task output:", result.output)
    for path, url in result.file_urls.items():
        print(f"Retrieved {path}: {url or '(failed)'}")


asyncio.run(main())
```

{% hint style="info" %}
With local artifact storage (the default), `result.file_urls` values are local file paths, not URLs. Switch to MinIO artifact storage to get presigned HTTPS URLs — see [Artifact Storage](artifact-storage.md).
{% endhint %}

## File Object Fields

| Field | Type | Description |
|---|---|---|
| `path` | `str` | Absolute destination path inside the sandbox |
| `data` | `bytes` | File content |
