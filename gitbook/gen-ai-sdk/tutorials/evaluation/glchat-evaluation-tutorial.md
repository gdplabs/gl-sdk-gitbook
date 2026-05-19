---
hidden: true
---

# 📚 GLChat Evaluation Tutorial

In this guide, we will learn how to **generate GLChat message response** and **evaluate its performance** using **gllm-evals** for QA dataset evaluation.

The evaluation focuses on question-answering capabilities with support for web search capability and PII handling. The dataset and experiment results then can be accessed in **Langfuse** for monitoring. To view more details on each component, you can click them in the sidebar inside the **Evaluation** page.

## Prerequisites

Before you can start evaluating GLChat QA dataset, you need to prepare the following:

### Required Parameters for GLChat

**1. User ID (`user_id`)**

The `user_id` is a unique identifier for the user who will be interacting with the specified GLChat application. This information is needed to create a conversation or message.

**Where to get it:**

* **From your existing user in GLChat**: If you already have an existing user in your GLChat application, you can use it as the `user_id`.

<figure><img src="../../../.gitbook/assets/Screenshot 2025-10-03 at 11.23.47.png" alt=""><figcaption></figcaption></figure>

* You can also provide any user that has access to the application you want to test.

**2. Chatbot ID (`chatbot_id`)**

The `chatbot_id` identifies which chatbot or application configuration to use for the conversation. This information is needed to create a conversation or message.

**3. \[Optional] Model Name (`model_name`)**

The `model_name` specifies which language model to use for generating GLChat response. Model name can be filled with the model display name in an application / chatbot. If not specified, the response will be generated using the default model there.

<figure><img src="../../../.gitbook/assets/Screenshot 2025-10-03 at 13.53.41.png" alt=""><figcaption></figcaption></figure>

### Required Keys

#### For Langfuse

We will need Langfuse credentials to trace, debug, and view the evaluation results for our GLChat QA system. If you do not have any Langfuse credentials yet, you can follow the [New User Configuration](https://gdplabs.gitbook.io/sdk/tutorials/evaluation/experiment-tracker#new-user-configuration) to get them. The required keys are: `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY`, and `LANGFUSE_HOST`.

#### For GLChat

We will also need access to the GLChat credentials to generate the response. Please contact GLChat team if you do not have them yet. The required keys are: `GLCHAT_BASE_URL` and `GLCHAT_API_KEY`.

## Step 0: Install the Required Libraries

We need to install the required libraries for GLChat evaluation, including GLChat SDK, gllm-evals, and Langfuse.

```bash
pip install glchat-sdk langfuse
```

* To install `gllm-evals`, you can follow [this](getting-started.md#installation) section.
* For more details about GLChat SDK, you can also visit the [GLChat Gitbook](https://gdplabs.gitbook.io/glchat/sdk/quick-start).

## Step 1: Setup Environment and Configuration

Prepare the environment variables for the evaluation script:

{% code title=".env" %}
```
# Langfuse
LANGFUSE_PUBLIC_KEY=
LANGFUSE_SECRET_KEY=
LANGFUSE_HOST=

# GLChat
GLCHAT_BASE_URL=
GLCHAT_API_KEY=
```
{% endcode %}

With the environment variables set, we can now initialize the Langfuse and GLChat clients.

```python
from langfuse import get_client
from glchat_sdk import GLChat

# Initialize Langfuse client
langfuse = get_client()

# Verify Langfuse connection
if langfuse.auth_check():
    print("Langfuse client is authenticated and ready!")
else:
    print("Authentication failed. Please check your credentials and host.")

# Initialize GLChat client
glchat_client = GLChat(
    base_url=os.getenv("GLCHAT_BASE_URL"),
    api_key=os.getenv("GLCHAT_API_KEY")
)
print("GLChat client initialized successfully!")
```

## Step 2: Prepare Your Dataset

Before we can evaluate our GLChat QA system, we need to prepare a dataset with all the information needed for evaluation.

For example purpose, you can download the following CSV file:

{% file src="../../../.gitbook/assets/glchat_qa_sample_dataset.csv" %}

In this example dataset, we have the following key fields:

**Input Fields:**

* `question_id`: Unique identifier for each query.
* `query`: The question to ask.
* `enable_search?`: Whether to enable web search functionality.
* `enable_pii?`: Whether to enable PII processing.

**Expected Output Fields:**

* `expected_response`: The expected answer.

**Metadata Fields:**

* `category`: The question category. This field categorizes each question based on its topic.

We then can create a mapping that tells Langfuse **which of your dataset's fields** should be logged into **Langfuse’s canonical fields**.

Langfuse's fields consist of:

* `input`: the input fields that are useful for the model (e.g., query, retrieved context).
* `expected_output`: the **target** you want to compare against (e.g., reference answer/label/ground truth).
* `metadata`: any extra attributes or information for each data row (e.g., category, topic, type, additional notes).

Your `mapping` simply points each Langfuse field to **the column name in your dataset**.

Below is the mapping example based on the dataset above:

```python
langfuse_mapping = {
    "input": {
        "question_id": "question_id",
        "query": "query",
        "enable_search?": "enable_search",
        "enable_pii?": "enable_pii"
    },
    "expected_output": {
        "expected_response": "expected_response"
    },
    "metadata": {
        "category": "category"
    }
}
```

## Step 3: Instrument your GLChat Functions

Before we can evaluate our GLChat system, we need to create the functions needed to produce a GLChat response, such as conversation creation and message sending operations. Optionally, we can wrap them with Langfuse's `@observe` decorator to track and monitor the processes.

We'll start by creating basic instrumentation setup for GLChat:

```python
import asyncio
import contextvars
from typing import Any
from langfuse import observe
from glchat_sdk import GLChat

@observe(name="create_glchat_conversation", as_type="generation")
def create_glchat_conversation(
    glchat_client: GLChat,
    *,
    username: str,
    chatbot_id: str,
    model_name: str,
) -> dict[str, Any]:
    """Create a new conversation in GLChat with instrumentation.

    Args:
        glchat_client: The GLChat client
        username: The username for the conversation
        chatbot_id: The ID of the chatbot to use
        model_name: The name of the model to use

    Returns:
        dict: The response from the API containing conversation details
    """
    return glchat_client.conversation.create(
        user_id=username,
        chatbot_id=chatbot_id,
        model_name=model_name
    )

@observe(name="create_glchat_message", as_type="generation")
def create_glchat_message(
    glchat_client: GLChat,
    *,
    chatbot_id: str,
    message: str,
    files: list[str],
    user_id: str,
    conversation_id: str,
    chat_history: str | None,
    model_name: str,
    anonymize_lm: bool,
    search_type: str,
) -> Any:
    """Send a message to GLChat conversation with instrumentation.

    Args:
        glchat_client: The GLChat client
        chatbot_id: The ID of the chatbot
        message: The message to send
        files: List of file paths to attach
        user_id: The user ID
        conversation_id: The conversation ID
        chat_history: Previous chat history
        model_name: The model to use
        anonymize_lm: Whether to anonymize the language model
        search_type: Type of search to perform

    Returns:
        The response stream from the API
    """
    custom_headers = {
        "tag": "evaluation",
    }

    return glchat_client.message.create(
        chatbot_id=chatbot_id,
        message=message,
        files=files or None,
        user_id=user_id,
        conversation_id=conversation_id,
        chat_history=chat_history,
        model_name=model_name,
        anonymize_lm=anonymize_lm,
        search_type=search_type,
        headers=custom_headers
    )
```

Besides them, you may also need to create other supporting functions such as parsing GLChat response:

```python
import json
from typing import Iterator


def parse_response(responses: Iterator[bytes], is_anonymize_lm: bool = False) -> str:
    """Parse Server-Sent Events (SSE) response from the chatbot.

    Args:
        responses (Iterator[bytes]): An iterator of bytes containing SSE data chunks
        is_anonymize_lm (bool): Whether to look for deanonymized content

    Returns:
        str: The final response extracted from the SSE data
    """
    final_response = ""
    for chunk in responses:
        chunk_str = chunk.decode("utf-8")

        # Parse the SSE data
        if chunk_str.startswith("data:"):
            try:
                # Extract JSON data after "data:"
                json_str = chunk_str[5:]
                data = json.loads(json_str)

                if is_anonymize_lm:
                    # Look for deanonymized_data type
                    if data.get("status") == "data":
                        message_data = data.get("message", "")
                        if isinstance(message_data, str):
                            try:
                                message_json = json.loads(message_data)
                                if message_json.get("data_type") == "deanonymized_data":
                                    deanonymized_data = message_json.get("data_value", {})
                                    ai_message = deanonymized_data.get("ai_message", {})
                                    final_response = ai_message.get("deanonymized_content, "")
                            except json.JSONDecodeError:
                                pass
                else:
                    if data.get("status") == "response":
                        final_response = data.get("message", "")
            except json.JSONDecodeError:
                continue

    return final_response
```

You can view more details on the provided GLChat gitbook above.

## Step 4: Generate Model Outputs

Before calling `evaluate()`, generate your model outputs first and save them into each row (for example in `actual_output`). The example below uses a helper function called `generate_response` that handles conversation creation, message sending, and response parsing.

```python
from glchat_sdk import GLChat


@observe(name="generate_response", as_type="generation")
async def generate_response(glchat_client: GLChat, row: dict[str, str]) -> str:
    """Generate a response from a chatbot for one dataset row."""

    question_id = row["question_id"]
    query = row["query"]
    search_type = "web" if row["enable_search"] == "TRUE" else "normal"
    anonymize_lm = True if row["enable_pii"] == "TRUE" else False

    try:
        # Create GLChat conversation
        conversation_response = await asyncio.to_thread(
            create_glchat_conversation,
            glchat_client,
            username="test_user_1",
            chatbot_id="general-purpose",
            model_name="GPT 4.1"
        )

        conversation_id = conversation_response.get("id")
        if not conversation_id:
            raise ValueError("Failed to create conversation")

        logger.info(f"Created conversation {conversation_id} for question {question_id}")

        # Send message and get response
        message_response = await asyncio.to_thread(
            create_glchat_message,
            glchat_client,
            chatbot_id="general-purpose",
            message=query,
            user_id="test_user_1",
            conversation_id=conversation_id,
            model_name="GPT 4.1",
            anonymize_lm=anonymize_lm,
            search_type=search_type,
        )

        # Parse message response
        final_response = parse_response(message_response, anonymize_lm)
        logger.info(f"Generated response for question {question_id}")
        return final_response

    except Exception as e:
        logger.error(f"Error in generate_response for question {row['query']}: {e}")
        return f"Error: {str(e)}"

```

## Step 5: Perform end-to-end Evaluation

To run the end-to-end evaluation, we can use a convenience function in `gllm-evals` called `evaluate`. This function provides a streamlined way to run AI evaluations with minimal setup. It orchestrates the entire evaluation process, from data loading to result tracking, in a single function call.

In this example, we first call `generate_response` for each row and store the result into `actual_output`. Then we pass the enriched dataset to `evaluate()`. We will use [GEvalGenerationEvaluator](evaluator/#gevalgenerationevaluator) for QA evaluation and [LangfuseExperimentTracker](experiment-tracker.md#langfuseexperimenttracker) for tracking.

```python
import asyncio
import os

from glchat_sdk import GLChat
from langfuse import get_client

from gllm_evals.evaluator.geval_generation_evaluator import GEvalGenerationEvaluator
from gllm_evals.evaluate import evaluate
from gllm_evals.experiment_tracker.langfuse_experiment_tracker import LangfuseExperimentTracker
from gllm_evals.dataset.spreadsheet_dataset import SpreadsheetDataset


async def main():
    """Main function example."""

    # create a glchat client
    glchat_client = GLChat(base_url=os.getenv("GLCHAT_BASE_URL"), api_key=os.getenv("GLCHAT_API_KEY"))

    dataset = (await SpreadsheetDataset.from_gsheets(
        sheet_id="1CVWqNzX_tdnvkV0fQ3NPDuEE9HtTXk8k2XtgIg6Ml6M",
        worksheet_name="test",
        client_email=os.getenv("GOOGLE_SHEETS_CLIENT_EMAIL"),
        private_key=os.getenv("GOOGLE_SHEETS_PRIVATE_KEY"),
    )).to_standard_format()

    for row in dataset:
        row["actual_output"] = await generate_response(glchat_client, row)

    results = await evaluate(
        data=dataset,
        evaluators=[GEvalGenerationEvaluator(model_credentials=os.getenv("OPENAI_API_KEY"))],
        experiment_tracker=LangfuseExperimentTracker(
            langfuse_client=get_client(),
            mapping=langfuse_mapping,
        ),
    )
    print(results)


if __name__ == "__main__":
    asyncio.run(main())
```

To learn more about `evaluate()` function, you can visit the following [section](evaluate-helper-function.md#function-signature).

## Step 6: View Evaluation Results in Langfuse <a href="#step-6-view-evaluation-results-in-langfuse" id="step-6-view-evaluation-results-in-langfuse"></a>

After running the evaluation, all the dataset and experiment you've provided will automatically be logged to Langfuse. This step shows you how to navigate the Langfuse UI and interpret your evaluation results.

### Accessing Your Langfuse Dashboard <a href="#accessing-your-langfuse-dashboard" id="accessing-your-langfuse-dashboard"></a>

1. **Navigate to your Langfuse project**: Go to [https://langfuse.obrol.id/](https://langfuse.obrol.id/).
2. **Select your organization and project**: Choose your dedicated organization and project (or that you've just created).
3. **Access the dashboard**: You'll see various sections for analyzing your data.

#### **View Dataset**

To view the dataset you've just created, you can go to: Project → **Datasets** → select a dataset → **Items**. In this page, we can see all the data rows you have just evaluated based on the provided Langfuse mapping. This dataset can also be reused for future evaluation.

<figure><img src="../../../.gitbook/assets/Screenshot 2025-10-02 at 15.50.03.png" alt=""><figcaption></figcaption></figure>

To see more detail for each row, you can click one of the data item above.

<figure><img src="../../../.gitbook/assets/Screenshot 2025-10-02 at 15.50.55.png" alt=""><figcaption></figcaption></figure>

#### View Dataset Runs

Dataset runs are the executions over a dataset with per-item output. A dataset run represents an experiment. To view the dataset runs, you can go to: Project → **Datasets** → select a dataset → **Runs**. In here, you can view all the scores for each experiment, **including LLM-as-a-judge score columns**—both as **aggregations** and **per-row** values.

<figure><img src="../../../.gitbook/assets/Screenshot 2025-10-02 at 16.17.31.png" alt=""><figcaption></figcaption></figure>

You can also click a specific dataset run to view all the data rows result for each experiment:

<figure><img src="../../../.gitbook/assets/Screenshot 2025-10-02 at 16.20.48.png" alt=""><figcaption></figcaption></figure>

#### **View Traces / Observations**

Trace / observation let you drill into individual spans, view the inputs, outputs (our evaluation results), and metadata. You can go to: Project → **Traces**.

Below is the trace example:

<figure><img src="../../../.gitbook/assets/Screenshot 2025-10-02 at 16.26.12.png" alt=""><figcaption></figcaption></figure>

#### **View Sessions**

Sessions contain grouped traces per experiment; you can review and annotate each data trace in sessions. You can access the sessions in Project → **Sessions**.

Below is the session screenshot example:

<figure><img src="../../../.gitbook/assets/Screenshot 2025-10-02 at 16.44.25.png" alt=""><figcaption></figcaption></figure>

{% hint style="success" %}
Congratulation! You have just created your first GLChat QA Evaluation!
{% endhint %}

## Conclusion

This cookbook provides a simple guide to evaluating GLChat QA systems using Langfuse. By following these steps, you can:

* Monitor your QA system's performance
* Evaluate different models and configurations systematically
* Track quality metrics and identify improvement opportunities
* Ensure reliable and high-quality QA responses in production

***

**Note**: This is a simple guide to get you started with GLChat QA evaluation using Langfuse. For more comprehensive evaluation information and advanced techniques, please refer to the [evaluation gitbook](./). For detailed information about generating GLChat responses and using the GLChat SDK, please consult the [GLChat GitBook](https://gdplabs.gitbook.io/glchat).
