---
icon: server
---

# Run Pipeline on a Server

This guide will walk you through **deploying your RAG pipeline as a FastAPI web service** that can handle HTTP requests and stream real-time responses. You'll learn how to create a production-ready API server that exposes your pipeline functionality through REST endpoints.

**Running a pipeline on a server** allows you to **expose your AI pipeline as a web service**, enabling multiple clients to interact with your RAG system through HTTP requests. This approach provides scalability, accessibility, and the ability to integrate your pipeline into web applications, mobile apps, or other services.

For example, instead of running your pipeline locally each time, you can deploy it as an API where users can send queries via HTTP requests and receive streaming responses in real-time.

<details>

<summary>Prerequisites</summary>

This example specifically requires:

1. **Completion of the** [your-first-rag-pipeline.md](build-end-to-end-rag-pipeline/your-first-rag-pipeline.md "mention") **tutorial** - you need a working pipeline to deploy
2. Completion of all setup steps listed on the [prerequisites.md](../prerequisites.md "mention") page
3. A working pipeline implementation (e.g., from previous [your-first-rag-pipeline.md](build-end-to-end-rag-pipeline/your-first-rag-pipeline.md "mention"))

You should be familiar with these concepts and components:

1. [pipeline.md](../tutorials/orchestration/pipeline.md "mention") - Basic pipeline construction and execution
2. Basic understanding of APIs and HTTP requests

</details>

### Installation

{% tabs %}
{% tab title="Linux, macOS, or Windows WSL" %}
```bash
# you can use a Conda environment
pip install --extra-index-url "https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/" gllm-pipeline gllm-rag gllm-core gllm-generation gllm-inference gllm-retrieval gllm-misc gllm-datastore
```
{% endtab %}

{% tab title="Windows Powershell" %}
```powershell
# you can use a Conda environment
pip install --extra-index-url "https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/" gllm-pipeline gllm-rag gllm-core gllm-generation gllm-inference gllm-retrieval gllm-misc gllm-datastore
```
{% endtab %}

{% tab title="Windows Command Prompt" %}
```bash
# you can use a Conda environment
FOR /F "tokens=*" %T IN ('gcloud auth print-access-token') DO pip install --extra-index-url "https://oauth2accesstoken:%T@glsdk.gdplabs.id/gen-ai-internal/simple/"  gllm-pipeline gllm-rag gllm-core gllm-generation gllm-inference gllm-retrieval gllm-misc gllm-datastore
```
{% endtab %}
{% endtabs %}

***

## Project Setup

{% stepper %}
{% step %}
**Project Structure**

Ensure your project structure includes your working pipeline and server files:

```
<your-project>/
├── modules/
│   └── [your actual components]
├── pipeline.py                     # Your working RAG pipeline
├── main.py                         # 👈 FastAPI server (we'll create this)
├── run.py                          # 👈 Test client (we'll create this)
└── .env
```
{% endstep %}

{% step %}
**Environment Configuration**

Ensure you have all necessary environment variables configured in your `.env` file:

```env
CSV_DATA_PATH="data/imaginary_animals.csv"
ELASTICSEARCH_URL="http://localhost:9200/"
EMBEDDING_MODEL="text-embedding-3-small"
LANGUAGE_MODEL="gpt-4o-mini"
INDEX_NAME="first-quest"
OPENAI_API_KEY="<YOUR_OPENAI_API_KEY>"
```

{% hint style="info" %}
Make sure your pipeline works correctly in standalone mode before deploying it as a server.
{% endhint %}
{% endstep %}
{% endstepper %}

***

## Build Your FastAPI Server

### 1) Create the FastAPI Application

The **FastAPI application** serves as the web interface for your RAG pipeline, handling HTTP requests and managing streaming responses:

{% stepper %}
{% step %}
**Create the main server file**

Create `main.py` with the FastAPI server implementation:

{% code lineNumbers="true" %}
```python
"""Main entry point for the FastAPI application.

This module sets up a FastAPI server that exposes your RAG pipeline
through HTTP endpoints with streaming response capabilities.
"""

import asyncio
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from gllm_core.constants import EventLevel
from gllm_core.event import EventEmitter
from gllm_core.event.handler import ConsoleEventHandler, StreamEventHandler

from pipeline import e2e_pipeline

app = FastAPI()


async def run_pipeline(state: dict, config: dict):
    """Runs the end-to-end pipeline.

    Args:
        state (dict): The state dictionary containing input data and event emitters.
        config (dict): The configuration dictionary containing pipeline parameters.
    """
    event_emitter: EventEmitter = state.get("event_emitter")
    try:
        await event_emitter.emit("Starting pipeline")
        await e2e_pipeline.invoke(state, config)
    except Exception as error:
        await event_emitter.emit(str(error))
    finally:
        await event_emitter.emit("Finished pipeline")
        await event_emitter.close()


@app.post("/stream")
async def add_message(request: Request):
    """Endpoint to handle incoming requests and stream responses.

    Args:
        request (Request): The incoming request containing user query and parameters.

    Returns:
        StreamingResponse: A streaming response that emits events during pipeline execution.
    """
    body = await request.json()
    user_query = body.get("user_query")
    top_k = body.get("top_k")
    debug = body.get("debug", False)
    event_level = EventLevel.DEBUG if debug else EventLevel.INFO

    stream_handler = StreamEventHandler()
    console_handler = ConsoleEventHandler()
    event_emitter = EventEmitter([stream_handler, console_handler], event_level)
    state = {"user_query": user_query, "event_emitter": event_emitter}
    config = {"top_k": top_k}

    asyncio.create_task(run_pipeline(state, config))
    return StreamingResponse(stream_handler.stream())
```
{% endcode %}

**Key components:**

* **FastAPI app**: Web framework for creating REST API endpoints
* **Event system**: Handles real-time streaming of pipeline events
* **Pipeline runner**: Manages pipeline execution with proper error handling
* **Stream endpoint**: Provides HTTP interface for pipeline requests
{% endstep %}

{% step %}
**Understanding the server architecture**

The server uses several key patterns:

1. **Async execution**: Pipeline runs concurrently with response streaming
2. **Event streaming**: Real-time updates sent to clients during processing
3. **Error handling**: Proper exception management and cleanup
4. **Dual handlers**: Both console logging and stream responses

{% hint style="info" %}
The `StreamingResponse` allows clients to receive updates in real-time rather than waiting for the complete response.
{% endhint %}
{% endstep %}
{% endstepper %}

### 2) Start the Server

Deploy your FastAPI server and make it accessible for HTTP requests:

{% stepper %}
{% step %}
**Run the FastAPI server**

Start your server using Uvicorn (included with FastAPI):

```bash
uvicorn main:app --reload
```

You should see output similar to:

```
INFO:     Will watch for changes in these directories: ['/your/project/path']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using StatReload
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**Server options:**

* `--reload`: Automatically restart server when code changes
* `--host 0.0.0.0`: Make server accessible from other machines
* `--port 8001`: Use a different port if 8000 is occupied
{% endstep %}

{% step %}
**Verify server is running**

Check that your server is operational:

```bash
curl http://127.0.0.1:8000/docs
```

This should show the FastAPI interactive documentation interface, confirming your server is running correctly.

{% hint style="info" %}
FastAPI automatically generates interactive API documentation at `/docs` and `/redoc` endpoints.
{% endhint %}
{% endstep %}
{% endstepper %}

***

## Test Your Pipeline Server

### 1) Create a Test Client

Build a client application to test your deployed pipeline server:

{% stepper %}
{% step %}
**Create the test client**

Create `run.py` with a client that tests your server:

{% code lineNumbers="true" %}
```python
"""Script to run RAG pipeline and stream responses from the FastAPI server.

This client demonstrates how to interact with your deployed pipeline server,
sending requests and processing streaming responses.
"""

import json
import requests


def run() -> None:
    """Runs the RAG pipeline and streams responses from the FastAPI server."""
    render = True
    body = {
        "user_query": "Give me 3 aquatic animals!",
        "top_k": 5,
        "debug": True,
    }
    response = requests.post("http://127.0.0.1:8000/stream", json=body, stream=True)

    if response.status_code == 200:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                event = chunk.decode("utf-8", errors="ignore")
                event = json.loads(event)
                event_type = event["type"]
                if render:
                    if event_type == "status":
                        print(f"[{event['level']}][{event['timestamp']}] {event['value']}")
                    else:
                        print(event["value"], end="", flush=True)
                else:
                    print(event)
        print()
    else:
        print(f"Error status code: {response.status_code}")
        print(response.text)


if __name__ == "__main__":
    run()
```
{% endcode %}

**Client features:**

* **Streaming support**: Processes real-time responses from the server
* **Event filtering**: Separates status messages from content responses
* **Error handling**: Manages HTTP errors and connection issues
* **Formatted output**: Clean display of streaming pipeline results
{% endstep %}
{% endstepper %}

### 2) Test the Complete System

Run your test client to verify the server deployment works correctly:

{% stepper %}
{% step %}
**Execute the test client**

With your server running in one terminal, run the client in another:

```bash
python run.py
```
{% endstep %}

{% step %}
**Observe the streaming output**

You should see real-time pipeline execution logs and results:

```
[INFO][2025-01-19T10:15:30.123456] Starting pipeline
[INFO][2025-01-19T10:15:30.234567] [Start 'VectorRetriever'] Processing input
[INFO][2025-01-19T10:15:32.345678] [Finished 'VectorRetriever'] Successfully retrieved 5 chunks
[INFO][2025-01-19T10:15:32.456789] [Start 'Repacker'] Repacking 5 chunks
[INFO][2025-01-19T10:15:32.567890] [Finished 'Repacker'] Successfully repacked chunks
[INFO][2025-01-19T10:15:32.678901] [Start 'StuffResponseSynthesizer'] Processing query
Based on the available information, here are three aquatic animals:

1. **Crystal Jellyfish** - Found in the pristine waters of Aquamarine Bay
2. **Rainbow Trout** - Inhabits the flowing streams of Silverbrook River
3. **Azure Seahorse** - Lives among the coral reefs of Sapphire Lagoon

[INFO][2025-01-19T10:15:35.789012] [Finished 'StuffResponseSynthesizer'] Successfully synthesized response
[INFO][2025-01-19T10:15:35.890123] Finished pipeline
```

**What you'll see:**

* **Status events**: Pipeline step execution logs with timestamps
* **Streaming content**: Response text appearing in real-time
* **Debug information**: Detailed step-by-step pipeline execution (if `debug: true`)
{% endstep %}

{% step %}
**Verify successful deployment**

If everything works correctly, you should be able to see:

* Real-time pipeline execution logs
* Streaming response content as it's generated
* Proper error handling if issues occur
* Clean server shutdown when stopping

{% hint style="success" %}
Congratulations! Your RAG pipeline is now successfully deployed as a web service and ready for production use.
{% endhint %}
{% endstep %}
{% endstepper %}

***

## Troubleshooting

**Common Issues**

1. **Server fails to start**:
   * Check if port 8000 is already in use: `lsof -i :8000`
   * Verify all dependencies are installed correctly
   * Ensure your pipeline imports work: `python -c "from pipeline import e2e_pipeline"`
2. **No streaming responses received**:
   * Verify the `StreamEventHandler` is properly configured
   * Check that your pipeline uses the event emitter correctly
   * Test with `debug: true` to see detailed pipeline execution
3. **Client connection errors**:
   * Confirm server is running on the correct host and port
   * Check firewall settings if accessing from another machine
   * Verify the request JSON format matches the expected schema
4. **Pipeline execution errors**:
   * Review server console output for detailed error messages
   * Test your pipeline standalone before deploying as server
   * Check environment variables and API keys are properly configured

**Debug Tips**

1. **Enable detailed logging**: Set `debug: true` in client requests
2. **Test components separately**: Verify pipeline works before server deployment
3. **Monitor server logs**: Watch console output while testing client requests
4. **Use interactive docs**: Visit `http://127.0.0.1:8000/docs` to test endpoints manually
5. **Check network connectivity**: Ensure client can reach server host and port

***

Congratulations! You've successfully deployed your RAG pipeline as a FastAPI web service. Your pipeline is now accessible through HTTP endpoints, supporting real-time streaming responses and ready for integration into web applications, mobile apps, or other services. This server-based approach provides the foundation for building scalable AI-powered applications.
