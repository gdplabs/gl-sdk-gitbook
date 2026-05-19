# 📈 Experiment Tracker

## Why Track Experiments?

Evaluation results produced by `evaluate()` or an individual evaluator are ephemeral — they exist only in memory unless persisted. Running the same evaluation multiple times across configuration changes (model swaps, prompt iterations, dataset updates) produces no historical baseline for comparison. Without tracking, there is no way to determine whether a given change improved or regressed performance relative to prior runs.

An experiment tracker records every run — dataset identity, evaluator configuration, per-metric scores, and timestamp — so that runs become **comparable over time**:

* **Leaderboard** — rank runs by `aggregate_success` or `aggregate_score` to identify the best-performing configuration
* **Regression detection** — a drop in pass rate is visible when compared against historical runs, not buried in a single invocation
* **Audit trail** — every run is traceable by dataset, evaluator parameters, and timestamp

`BaseExperimentTracker` is the abstract base class. Pass any tracker instance to the `evaluate()` function and results are logged automatically.

## Available Experiment Trackers

1. [CSVExperimentTracker](experiment-tracker.md#csvexperimenttracker)
2. [LangfuseExperimentTracker](experiment-tracker.md#langfuseexperimenttracker)
   1. [Refresh Langfuse Experiment Tracker](experiment-tracker.md#refresh-langfuse-experiment-tracker)
   2. [Export Langfuse Experiment Results to CSV](experiment-tracker.md#export-langfuse-experiment-results-to-csv)

***

### 🪶 CSVExperimentTracker

**Use when:** You want a lightweight, local tracker that will log the results in CSV. It is great for quick tests, prototyping, or when you do not need a full UI.

Example usage:

```python
from gllm_evals.experiment_tracker.csv_experiment_tracker import CSVExperimentTracker

tracker = CSVExperimentTracker(
    project_name="my_project",
    output_dir="./gllm_evals/experiments"
)
tracker.log(...)
```

#### Parameters

* **project\_name** (`str`): Name of the project. Used to namespace experiment runs.
* **output\_dir** (`str`, optional): Directory to store the output CSV files. Defaults to `./gllm_evals/experiments`.
* **score\_key** (`str | list[str]`, optional): Key to extract scores from evaluation results. Supports dot notation (e.g. `"metrics.accuracy"`) or a nested key path as a list (e.g. `["generation", "score"]`). Defaults to `"score"`.
* **extra\_score\_keys** (`list[str] | None`, optional): Additional score keys to extract as extra CSV columns (not used for leaderboard selection). Defaults to `["aggregate_score", "aggregate_success"]`.
* **leaderboard\_score\_key** (`str`, optional): Score key used for leaderboard primary ranking. Set to `"aggregate_success"` to rank by binary pass rate (default), or `"score"` for backward compatibility. Defaults to `"aggregate_success"`.
* **summary\_evaluators** (`list | None`, optional): Custom summary evaluator callables that compute batch-level statistics. Each callable receives `(evaluation_results, data)` and returns a dict. Defaults to `None`.

***

### 🌐 LangfuseExperimentTracker

**Use when:** You want a production-grade tracker integrated with Langfuse. It is great for detailed traces & spans, dataset & run management, and session & dataset level scoring.

Example usage:

```python
from langfuse import get_client

from gllm_evals.experiment_tracker.langfuse_experiment_tracker import LangfuseExperimentTracker

tracker = LangfuseExperimentTracker(
    project_name="my_project",
    langfuse_client=get_client(),
)
tracker.log(...)
```

#### New User Configuration

If you are new to Langfuse, you can follow these steps to use Langfuse Experiment Tracker:

1. **Create an Organization**\
   Click the `New Organization` and enter the organization name on the `Organizations` page. This gives you a top-level space to manage projects and members. The organization can be filled with your company/team/client name. Use a human-readable name (e.g. `client-XZY`).
2. **Manage members**
   1. Invite teammates to the org/project with the roles you need (viewer/editor/admin).
   2. **Important:** Set yourself (or one trusted person) as the **admin** so they can invite and manage other project members in the organization.
3. **Create a Project**\
   Experiments, datasets, traces, and API keys are project-scoped. Enter your project name to create the project. The project can be filled with your project/application name (e.g. `project-abc`).
4. **Create API credentials**\
   You can create API key now or later in your **Project → Settings → API Keys**, then generate keys and copy:
   1. **Public key**
   2. **Secret key**
   3. **Langfuse host**
5.  **Configure your environment**\
    Most Langfuse clients (and our `evaluate()` integration) read these env vars:

    ```bash
    export LANGFUSE_HOST="https://langfuse.obrol.id"
    export LANGFUSE_PUBLIC_KEY="pk-xxxxxxxx"
    export LANGFUSE_SECRET_KEY="sk-xxxxxxxx"
    ```
6. **Run an evaluation with Langfuse tracking enabled**\
   With this credentials, you can now use the Langfuse Experiment Tracker.

***

#### What happens automatically

* **Auto-dataset creation (when needed).**\
  If you pass a dataset that does **not** already exist in Langfuse, we automatically create it with either the column `expected_response` will automatically be the ground truth response OR based on the given mapping dictionary. To see the mapping example, you can visit [this subsection](evaluate-helper-function.md#using-langfuse-experiment-tracker-with-custom-mapping). You’ll find it under **Project → Datasets** in the left sidebar after a round of evaluation.
* **Experiment run logging.**\
  Your evaluation will be logged including runs, metrics/scores, and the underlying traces.

***

#### Where to see results (in Langfuse)

* **Datasets:** the dataset created/linked by `evaluate()`.\
  Pat&#x68;_:_ Project → **Datasets**
* **Dataset runs:** executions over a dataset with per-item outputs and evaluator scores.\
  Pat&#x68;_:_ Project → **Datasets** → select a dataset → **Runs**
* **Traces / Observations:** drill into individual calls/spans, inputs/outputs, timings.\
  Pat&#x68;_:_ Project → **Traces** (and Observations)
* **Sessions:** grouped traces per experiment; you can review, share, and even score sessions.\
  Pat&#x68;_:_ Project → **Sessions**.

***

#### :repeat: Refresh Langfuse Experiment Tracker

To refresh the scores in Langfuse after updating them, you can run using the following function:

```python
import asyncio
from langfuse import get_client

from gllm_evals.experiment_tracker.langfuse_experiment_tracker import LangfuseExperimentTracker
from glchat_sdk.evals.constant import GLChatDefaults

async def main():
    """The main function to run refresh langfuse session-level score"""

    run_id = "" # Fill this with the session id you want to refresh
    exp_tracker = LangfuseExperimentTracker(langfuse_client=get_client(), project_name=GLChatDefaults.PROJECT_NAME)
    exp_tracker.refresh_score(run_id=run_id)

if __name__ == "__main__":
    asyncio.run(main())
```

***

#### :file\_folder: Export Langfuse Experiment Results to CSV

You can export the Langfuse experiment results with all the updated scores to CSV using the following function:

```python
import asyncio
from langfuse import get_client

from gllm_evals.experiment_tracker.langfuse_experiment_tracker import LangfuseExperimentTracker
from glchat_sdk.evals.constant import GLChatDefaults

async def main():
    """The main function to export langfuse experiment results to CSV."""

    run_id = "" # Fill this with the session id you want to export
    exp_tracker = LangfuseExperimentTracker(langfuse_client=get_client(), project_name=GLChatDefaults.PROJECT_NAME)
    exp_tracker.export_experiment_results(run_id=run_id, export_type="csv")

if __name__ == "__main__":
    asyncio.run(main())
```
