---
icon: screen-users
---

# Group Relative Policy Optimization (GRPO)

## What is Group Relative Policy Optimization (GRPO)?

Group Relative Policy Optimization (GRPO) is a reinforcement learning-based fine-tuning approach that optimizes a model using relative feedback across groups of candidate responses, rather than requiring absolute scores for individual outputs. For each input, the model generates multiple candidate responses that are evaluated by a reward function. GRPO then updates the policy by increasing the likelihood of higher-scoring responses and decreasing the likelihood of lower-scoring ones within the same group. This approach is particularly effective when you have preference data or quality comparisons between responses, and it typically produces more robust and preference-aligned model behaviors.

{% include "../../../.gitbook/includes/features.md" %}

## Installation

{% tabs %}
{% tab title="Linux or Windows WSL" %}
```bash
pip install --extra-index-url "https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/" "gllm-training"
```
{% endtab %}

{% tab title="Windows Powershell" %}
```bash
pip install --extra-index-url "https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/" "gllm-training"
```
{% endtab %}

{% tab title="Windows Command Prompt" %}
```bash
FOR /F "tokens=*" %T IN ('gcloud auth print-access-token') DO pip install --extra-index-url "https://oauth2accesstoken:%T@glsdk.gdplabs.id/gen-ai-internal/simple/"  "gllm-training"
```
{% endtab %}
{% endtabs %}

## Quickstart

Let's move on to a basic example fine-tuned using `GRPOTrainer`. To run GRPO fine-tuning, you need to specify a `reward function`, `model name`, `column_mapping` and `dataset path`.

```python
# Main Code
from gllm_training import GRPOTrainer
from examples.reward_function.llm_as_judge_reward_function import output_format_reward

grpo_trainer = GRPOTrainer(
    model_name="Qwen/Qwen3-0.6b",
    datasets_path="examples/grpo_csv",
    reward_functions=[output_format_reward]
)
grpo_trainer.train()

```

## Fine tuning model using YAML file.

We can run experiments in a more structured way by using a YAML file. The current GRPO fine-tuning SDK supports both online data from Google Spreadsheets and local data in CSV format.

### Example 1: Fine tuning using online data.

We can prepared our experiment using YAML file with the data trained and validation from google spreadsheet.

{% stepper %}
{% step %}
**Configure environment variables (.env)**

Fill in the `GOOGLE_SHEETS_CLIENT_EMAIL` and `GOOGLE_SHEETS_PRIVATE_KEY` fields. If you don’t have these keys, please contact the infrastructure team.

```bash
GOOGLE_SHEETS_CLIENT_EMAIL="your-service-account@project.iam.gserviceaccount.com"
GOOGLE_SHEETS_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nYOUR_PRIVATE_KEY\n-----END PRIVATE KEY-----\n"
```
{% endstep %}

{% step %}
**Share the spreadsheet**

Share your Google Spreadsheet containing the training and validation data with the `GOOGLE_SHEETS_CLIENT_EMAIL`.

```
Share -> add your google sheet client email -> set as editor
```
{% endstep %}

{% step %}
**`Experiment configuration (grpo_experiment_config.yml)`**

You can use a YAML file to plan your fine tuning experiments. To fine tuning with YAML, you need to define the required variables in the file.

```yaml
fine_tune_hyperparam_1: &fine_tune_hyperparam_1_conf
  hyperparameters_id: "1"
  max_seq_length: 16000
  load_in_16bit: true
  full_finetuning: false
  enable_thinking: true
  thinking_mode: "off"
  add_generation_prompt: false
  fast_inference: true

  # LoraConfig
  r: 16
  lora_alpha: 32
  lora_dropout: 0.1
  bias: "none"
  target_modules:
    - "q_proj"
    - "k_proj"
    - "v_proj"
    - "o_proj"
  use_rslora: false
  logging_steps: 2
  per_device_train_batch_size: 2
  gradient_accumulation_steps: 4
  num_generations: 4
  num_train_epochs: 1
  save_steps: 50
  model_output_dir: "data/grpo/model"
  resume_from_checkpoint: false
  model_cache_dir: ".hf_cache"

vllm_sampling_params: &vllm_sampling_params_conf
  min_p: 0.1
  top_p: 1.0
  top_k: -1
  seed: 42
  max_tokens: 16000
  include_stop_str_in_output: true
  temperature: 0.6

experiment_1:
  experiment_id: "1"
  hyperparameters: *fine_tune_hyperparam_1_conf
  vllm_sampling_params: *vllm_sampling_params_conf
  storage_config: *s3_storage_config
  topic: "LLM AS A JUDGE GRPO"
  grpo_ability: "LLM AS A JUDGE"
  model_name: "Qwen/Qwen3-0.6b"
  framework: "unsloth"
  multimodal: false
  spreadsheet_id: "1YbnRUq9ef_ZeYJ78ae8uY9rCaqY3hMz00HwgxZKvCKU"
  train_sheet: "botanica_completeness_train"
  validation_sheet: "botanica_completeness_train"
  prompt_sheet: "prompt_single"
  prompt_name: "completeness_prompt_single_8_2_no_think"
  column_mapping_config:
    input_columns:
      query: "question"
      generated_response: "generated_response"
      expected_response: "expected_response"
    label_columns:
      score: "completeness_score"
      reason: "completeness_explanation"
  save_processed_dataset: true
  output_processed_dir: "data/grpo/dataset"
```
{% endstep %}

{% step %}
**(Notes) column\_mapping\_config**

The configuration is split into two main parts: `input_columns` and `label_columns`.

```yaml
column_mapping_config:
  input_columns:
    <placeholder_in_user_prompt>: <column_name_in_your_data>
  label_columns:
  # Option 1: dictionary format (assistant outputs JSON)
    <key_in_assistant_output>: <column_name_in_your_data>
  # Option 2: string format (assistant outputs plain text)
  # label_columns: <column_name_in_your_data>
```

**Input columns**

The `input_columns` section maps placeholders in your `user` prompt template to the actual column names in your dataset.

* **placeholder\_in\_user\_prompt**: The placeholder name inside the `user` prompt template (e.g., `query` for `{query}`)
* **column\_name\_in\_your\_data**: The actual column name from your Google Sheet or CSV file (e.g., `user_query`)

```yaml
input_columns:
    query: "question"
```

**Output columns**

Output columns supports dictionary or string formats for fine-tuned models.

1.  Output dictionary

    YAML format

    ```yaml
    label_columns:
        label: "target"
    ```

    Expected output

    ```json
    {
        "label": "Pentingnya Risiko Kepatuhan Terintegrasi di perbankan"
    }
    ```
2.  Output string

    YAML format

    ```yaml
    label_columns: "target"
    ```

    Expected output

    ```
    "Pentingnya Risiko Kepatuhan Terintegrasi di perbankan"
    ```
{% endstep %}

{% step %}
**Reward function**

Reward functions evaluate model outputs and convert them into numerical feedback that GRPO uses to update the policy. In practice, a reward function:

* Takes a batch of **completions** (model-generated outputs)
* Computes a **float reward** for each completion.
* Returns a **list of floats** where each element corresponds to exactly one completion.

```python
import re

def output_format_reward(completions: list[any], **kwargs: any) -> list[float]:  # noqa PLR0912
    rewards = []
    for completion in completions:
        # Extract content from nested structure
        if isinstance(completion, list) and len(completion) > 0:
            if isinstance(completion[0], list) and len(completion[0]) > 0:
                text = completion[0][0].get("content", "")
            elif isinstance(completion[0], dict):
                text = completion[0].get("content", "")
            else:
                text = str(completion)
        else:
            text = str(completion)

        reward = 0.0
        text_cleaned = text.strip()
        if re.search(r'"score"[\s]*:', text_cleaned, re.IGNORECASE):
            reward += 1.0
        else:
            reward -= 1.0
        if re.search(r'"reason"[\s]*:', text_cleaned, re.IGNORECASE):
            reward += 1.0
        else:
            reward -= 1.0
        think_match = re.search(r"<think>(.*?)</think>", text_cleaned, re.DOTALL)
        if think_match:
            think_content = think_match.group(1).strip()
            if not think_content:  # Empty or whitespace only
                reward += 1.0
            else:
                reward -= 1.0
        else:
            reward += 1.0

        rewards.append(reward)
    return rewards
```
{% endstep %}

{% step %}
**Fine tuning**

To run your fine-tuning, you need to load the YAML data using the `YamlConfigLoader` function, and select the experiment ID when executing the load function.

```python
from gllm_training import GRPOTrainer, YamlConfigLoader
from examples.reward_function.llm_as_judge_reward_function import output_format_reward
from dotenv import load_dotenv

load_dotenv(override=True)

config_loader = YamlConfigLoader(base_dir="./")
config = config_loader.load("grpo_experiment_config.yaml", "experiment_1")
grpo_trainer = GRPOTrainer(
    **config,
    reward_functions=[output_format_reward]
)
grpo_trainer.train()
```
{% endstep %}
{% endstepper %}

### Example 2: Fine tuning using local data.

The remaining hyperparameter configurations for fine-tuning are the same as when using online data. Below is an example YAML configuration for using local data for training and validation.

```yaml
experiment_2:
  experiment_id: "2"
  hyperparameters: *fine_tune_hyperparam_1_conf
  vllm_sampling_params: *vllm_sampling_params_conf
  storage_config: *s3_storage_config
  topic: "LLM AS A JUDGE GRPO"
  grpo_ability: "LLM AS A JUDGE"
  model_name: "Qwen/Qwen3-0.6b"
  framework: "unsloth"
  multimodal: false
  datasets_path: "examples/grpo_csv"
  train_filename: "training_data.csv"
  validation_filename: "validation_data.csv"
  prompt_filename: "prompt_data.csv"
  prompt_name: "prompt_default"
  column_mapping_config:
    input_columns:
      query: "question"
      generated_response: "generated_response"
      expected_response: "expected_response"
    label_columns:
      score: "completeness_score"
      reason: "completeness_explanation"
  save_processed_dataset: true
  output_processed_dir: "data/grpo/dataset"
```

## Datasets Format

### Data training and validation

The column names should correspond to what you define in the `column_mapping_config`.

**Minimum Required Columns:**

| Column Name          | Description                                                            |
| -------------------- | ---------------------------------------------------------------------- |
| `query`              | The primary input or query provided to the model.                      |
| `generated_response` | The output or response that is being evaluated for rewards.            |
| `expected_response`  | The reference data or ground truth used to calculate the reward score. |

### Prompts

The prompt data should contained columns:

| Column Name | Description                                                                                                                                                                       |
| ----------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`      | A unique identifier for the prompt template                                                                                                                                       |
| `system`    | The system prompt, which sets the model's role and context. It does not contain placeholders                                                                                      |
| `user`      | The user prompt template. It **must** contain placeholders (e.g., `{query}`, `{generated_response}`, `{expected_response}`) that will be replaced by data from your input columns |

## Logging Monitoring

During the GRPO fine-tuning process, the SDK automatically generates comprehensive logs to help you monitor training progress and debug issues. These logs are stored in two formats:

### JSONL Logs (Structured Training Metrics)

The SDK generates structured JSONL logs that capture detailed training metrics at each step. These logs are stored in:

```
data/grpo/model/exp_{experiment_id}/{model_name}/logs/grpo_train_steps.jsonl
```

**Example path**: `data/grpo/model/exp_999/Qwen3-0.6b/logs/grpo_train_steps.jsonl`

Each line in the JSONL file contains a JSON object with training metrics such as:

* `step`: Training step number
* `loss`: Training loss at that step
* `learning_rate`: Current learning rate
* `epoch`: Current epoch number
* `rewards/mean`: Average reward across generated responses
* `rewards/std`: Standard deviation of rewards
* `rewards/margin`: Difference between best and worst rewards in the group
* `policy_loss`: Policy optimization loss
* And other relevant metrics

You can parse these logs programmatically or use tools like `jq` to analyze the training progression:

```bash
# View the last 10 training steps
tail -n 10 data/grpo/model/exp_1/Qwen3-0.6b/logs/grpo_train_steps.jsonl | jq .

# Extract training metrics with reward information
cat data/grpo/model/exp_999/Qwen3-0.6b/logs/grpo_train_steps.jsonl | jq -r 'select(.loss != null) | "\(.step): loss=\(.loss) reward_mean=\(.["rewards/mean"])"'

# Get the final training summary (last line)
tail -n 1 data/grpo/model/exp_1/Qwen3-0.6b/logs/grpo_train_steps.jsonl | jq .
```

> **Note**: The JSONL file contains both training steps and reward metrics. Use `select()` to filter for the specific type of data you need.

### Tensorboard Logs (Visual Monitoring)

For visual monitoring and analysis, the SDK also generates TensorBoard-compatible logs stored in:

```
data/grpo/model/exp_{experiment_id}/{model_name}/logs_tensorboard
```

**Example path**: `data/`grpo`/model/exp_1/Qwen3-0.6b/logs_tensorboard`

To visualize your training progress:

1. **Launch TensorBoard**:

```bash
tensorboard --logdir data/grpo/model/exp_1/Qwen3-0.6b/logs_tensorboard
```

2. **Open your browser** and navigate to `http://localhost:6006`
3. **Monitor key metrics**:
   * Training/Validation loss curves
   * Learning rate scheduling
   * Step-by-step progress
   * Custom metrics (if configured)

#### Log Configuration

You can customize logging behavior through the hyperparameters configuration:

```yaml
fine_tune_hyperparam_1: &fine_tune_hyperparam_1_conf
  hyperparameters_id: "1"
  # ... other hyperparameters ...
  logging_steps: 10  # Log every N steps
  save_strategy: "steps"  # Save strategy affects log frequency
  eval_strategy: "steps"  # Evaluation strategy affects eval log frequency
```

### Best Practices

1. **Monitor reward signals**: Check that average rewards increase over time - if rewards stay flat or decrease, your reward function may not be aligned with your goals or the model isn't learning the desired behavior.
2. **Track policy stability**: Use Tensorboard to see policy loss trends - sudden spikes in policy loss or reward variance indicate training instability and may require reducing learning rate.
3. **Debug reward function**: JSONL logs show reward statistics for each step - look for reward mean trends, check if reward margin is too small (responses are too similar), or if standard deviation is too high (inconsistent quality).
4. **Monitor generation quality**: GRPO generates multiple responses per input, so watch that reward mean increases while maintaining reasonable diversity (reward std shouldn't be zero).
5. **Compare experiments**: Save logs from each experiment to compare which reward functions and hyperparameters produce the best policy improvements - use TensorBoard to view multiple experiments side-by-side

## Upload model to cloud storage

When running experiments, we don’t always save the model directly to the cloud. Instead, we may first evaluate its performance before uploading it to cloud storage. To support this workflow, we provide a `save_model` function that allows you to upload the model as a separate step after fine tuning.

{% stepper %}
{% step %}
**Configure environment variable (.env)**

Fill in the `AWS_ACCESS_KEY`, `AWS_SECRET_KEY` and `AWS_REGION` fields. If you don’t have these keys, please contact the infrastructure team.

```
AWS_ACCESS_KEY="<AWS_ACCESS_KEY>"
AWS_SECRET_KEY="<AWS_SECRET_KEY>"
AWS_REGION="<AWS_REGION>"
```
{% endstep %}

{% step %}
**Upload model**

To upload the model, you need to configure the storage configuration and specify the `model path` on `save_model` function. The model path should point to the directory of your best adapter model.

```python
from gllm_training import GRPOTrainer
from gllm_training.schema import StorageConfig

finetuner = GRPOTrainer(
    model_name="Qwen/Qwen3-0.6b",
    storage_config=StorageConfig(
        provider="s3",
        upload_to_cloud=True,
        object_prefix="fine-tuned-models",
        bucket_name="glair-gen-ai-llm-model",
    ),
)
finetuner.save_existing_model(
    model_path="data/fine_tuned/exp_1/Qwen3-1.7b/exp_id_1:grpo_fine_tune_hyperparam_1:prompt_1:Qwen3-1.7b:adapter"
)
```
{% endstep %}
{% endstepper %}
