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

    if response.status_code == 200:  # noqa: PLR2004
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
