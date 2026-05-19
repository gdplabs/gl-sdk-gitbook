---
icon: person-chalkboard
---

# Direct Preference Optimization (DPO)

## What is Direct Preference Optimization (DPO)?

Direct Preference Optimization (DPO) is a preference-based fine-tuning technique that aligns a model using paired comparisons between responses, rather than relying on reinforcement learning or reward models. For each input prompt, DPO uses a `chosen response` (preferred) and a `rejected response` (less preferred) to directly increase the likelihood of generating the chosen output while decreasing the likelihood of the rejected one. This is achieved through a closed-form optimization objective that simplifies training while still capturing preference signals effectively. DPO is particularly useful when you have datasets that express relative human preferences, and it typically produces stable, efficient, and preference-aligned model behaviors.

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

Let's move on to a basic example fine-tuned using `DPOTrainer`. To run DPO fine-tuning, you need to specify a `model name`, `dpo_column_mapping` and `dataset path`. Make sure your data sets contained of `prompt`, `chosen` as a correct response and `rejected` as a rejected response.

```python
# Main Code
from gllm_training import DPOTrainer

dpo_trainer = DPOTrainer(
    model_name="Qwen/Qwen3-0.6b",
    datasets_path="examples/dpo_csv"
)
dpo_trainer.train()

```

## Fine tuning model using YAML file.

We can run experiments in a more structured way by using a YAML file. The current DPO fine-tuning SDK supports both online data from Google Spreadsheets and local data in CSV format.

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
**`Experiment configuration (dpo_experiment_config.yml)`**

You can use a YAML file to plan your fine tuning experiments. To fine tuning with YAML, you need to define the required variables in the file.

```yaml
fine_tune_hyperparam_1: &fine_tune_hyperparam_1_conf
  hyperparameters_id: "1"
  max_seq_length: 16000
  load_in_16bit: true
  trust_remote_code: true
  enable_thinking: false
  thinking_mode: "off"
  add_generation_prompt: false
  gpu_memory_utilization: 0.9

  # LoraConfig
  r: 16
  lora_alpha: 16
  lora_dropout: 0 # Currently only supports dropout = 0
  bias: "none" # Currently only supports bias = "none"
  target_modules:
    - "q_proj"
    - "k_proj"
    - "v_proj"
    - "o_proj"
    - "gate_proj"
    - "up_proj"
    - "down_proj"
  use_gradient_checkpointing: "unsloth"
  random_state: 3407

  # DPO Config
  num_train_epochs: 1
  learning_rate: 5.0e-6
  weight_decay: 0.0
  warmup_ratio: 0.1
  lr_scheduler_type: "linear"
  optim: "adamw_8bit"
  logging_steps: 2
  per_device_train_batch_size: 2
  gradient_accumulation_steps: 4
  save_steps: 50

  # Output directory
  model_output_dir: "data/dpo/model"

  # Resume training
  resume_from_checkpoint: false
  model_cache_dir: ".hf_cache"

experiment_1:
  experiment_id: "1"
  hyperparameters: *fine_tune_hyperparam_1_conf
  storage_config: *s3_storage_config
  topic: "DPO Fine Tuned"
  model_name: "Qwen/Qwen3-0.6b"
  framework: "unsloth"
  multimodal: false
  spreadsheet_id: "1pibHZZCmyc4NHaXGkMxYhBcHwaOLJeC-3hUa9gIcN9g"
  train_sheet: "training_data"
  prompt_sheet: "prompt"
  prompt_name: "prompt_default"
  dpo_column_mapping_config:
    input_columns:
      prompt: "prompt"
    chosen: "chosen"
    rejected: "rejected"
  save_processed_dataset: true
  output_processed_dir: "data/dpo/dataset"
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

* **placeholder\_in\_user\_prompt**: The placeholder name inside the `user` prompt template (e.g., `query`)
* **column\_name\_in\_your\_data**: The actual column name from your Google Sheet or CSV file (e.g., `user_query`)

```yaml
input_columns:
    query: user_query
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
**Fine tuning**

To run your fine-tuning, you need to load the YAML data using the `YamlConfigLoader` function, and select the experiment ID when executing the load function.

```python
from gllm_training import DPOTrainer, YamlConfigLoader
from dotenv import load_dotenv

load_dotenv(override=True)

config_loader = YamlConfigLoader(base_dir="./")
config = config_loader.load("dpo_experiment_config.yaml", "experiment_1")
dpo_trainer = DPOTrainer(
    **config
)
dpo_trainer.train()
```
{% endstep %}
{% endstepper %}

### Example 2: Fine tuning using local data.

The remaining hyperparameter configurations for fine-tuning are the same as when using online data. Below is an example YAML configuration for using local data for training and validation.

```yaml
experiment_2:
  experiment_id: "2"
  hyperparameters: *fine_tune_hyperparam_1_conf
  storage_config: *s3_storage_config
  topic: "DPO Fine Tuned"
  model_name: "Qwen/Qwen3-0.6b"
  framework: "unsloth"
  multimodal: false
  datasets_path: "examples/dpo_csv"
  train_filename: "training_data.csv"
  prompt_filename: "prompt_data.csv"
  prompt_name: "prompt_default"
  dpo_column_mapping_config:
    input_columns:
      prompt: "prompt"
    chosen: "chosen"
    rejected: "rejected"
  save_processed_dataset: true
  output_processed_dir: "data/dpo/dataset"
```

## Datasets Format

### Data training and validation

The column names should correspond to what you define in the `column_mapping_config`.

**Minimum Required Columns:**

| Column Name | Description                                                                |
| ----------- | -------------------------------------------------------------------------- |
| `prompt`    | The input query or instruction provided to the model.                      |
| `chosen`    | The preferred or "good" response that the model should learn to favor.     |
| `rejected`  | The less preferred or "bad" response that the model should learn to avoid. |

### Prompts

The prompt data should contained columns:

| Column Name | Description                                                                                                                         |
| ----------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| `name`      | A unique identifier for the prompt template                                                                                         |
| `system`    | The system prompt, which sets the model's role and context. It does not contain placeholders                                        |
| `user`      | The user prompt template. It **must** contain placeholders (e.g., `{prompt}`) that will be replaced by data from your input columns |

## Logging Monitoring

During the DPO fine-tuning process, the SDK automatically generates comprehensive logs to help you monitor training progress and debug issues. These logs are stored in two formats:

### JSONL Logs (Structured Training Metrics)

The SDK generates structured JSONL logs that capture detailed training metrics at each step. These logs are stored in:

```
data/dpo/model/exp_{experiment_id}/{model_name}/logs/dpo_train_steps.jsonl
```

**Example path**: `data/dpo/model/exp_1/Qwen3-0.6b/logs/dpo_train_steps.jsonl`

Each line in the JSONL file contains a JSON object with training metrics such as:

* `step`: Training step number
* `loss`: DPO training loss at that step
* `learning_rate`: Current learning rate
* `epoch`: Current epoch number
* `rewards/chosen`: Implicit rewards for chosen (preferred) responses
* `rewards/rejected`: Implicit rewards for rejected (less preferred) responses
* `rewards/margins`: Margin between chosen and rejected rewards
* `logps/chosen`: Log probabilities of chosen responses
* `logps/rejected`: Log probabilities of rejected responses
* And other relevant metrics

You can parse these logs programmatically or use tools like `jq` to analyze the training progression:

```bash
# View the last 10 training steps
tail -n 10 data/dpo/model/exp_1/Qwen3-0.6b/logs/dpo_train_steps.jsonl | jq .

# Extract training metrics with reward margins
cat data/dpo/model/exp_1/Qwen3-0.6b/logs/dpo_train_steps.jsonl | jq -r 'select(.loss != null) | "Step \(.step): loss=\(.loss) margin=\(.["rewards/margins"]) accuracy=\(.["rewards/accuracies"])"'

# Get the final training summary (last line)
tail -n 1 data/dpo/model/exp_1/Qwen3-0.6b/logs/dpo_train_steps.jsonl | jq .
```

**Note**: The JSONL file contains training metrics including preference margins between chosen and rejected responses. Use `select()` to filter for the specific type of data you need. The `rewards/accuracies` metric shows how often the model correctly predicts which response is preferred.

### TensorBoard Logs (Visual Monitoring)

For visual monitoring and analysis, the SDK also generates TensorBoard-compatible logs stored in:

```
data/dpo/model/exp_{experiment_id}/{model_name}/logs_tensorboard
```

**Example path**: `data/dpo/model/exp_999/Qwen3-0.6b/logs_tensorboard`

To visualize your training progress:

1. **Launch TensorBoard**:

```bash
tensorboard --logdir data/dpo/model/exp_999/Qwen3-0.6b/logs_tensorboard
```

2. **Open your browser** and navigate to `http://localhost:6006`
3. **Monitor key metrics**:
   * Training loss curves
   * Reward margins (chosen vs rejected)
   * Implicit reward trends
   * Learning rate scheduling
   * Log probability distributions
   * Step-by-step progress
   * Epoch progression

### Log Configuration

You can customize logging behavior through the hyperparameters configuration:

```yaml
fine_tune_hyperparam_1: &fine_tune_hyperparam_1_conf
  hyperparameters_id: "1"
  # ... other hyperparameters ...
  report_to: "tensorboard"  # Enable TensorBoard logging
  logging_steps: 2  # Log every N steps
  save_steps: 50  # Save checkpoint every N steps
  eval_strategy: "no"  # Evaluation strategy (set to "steps" to enable eval logging)
```

### Best Practices

1. **Monitor reward margins**: Check that the margin between chosen and rejected rewards increases over time - if margins stay flat or decrease, the model isn't learning to distinguish between preferred and non-preferred responses
2. **Track loss patterns**: Use TensorBoard to see DPO loss trends - the loss should decrease steadily; sudden spikes may indicate learning rate issues or data quality problems with chosen/rejected pairs
3. **Debug preference learning**: JSONL logs show reward statistics for each step - look for positive margins (chosen rewards higher than rejected), check if margins are too small (weak preferences), or if they fluctuate wildly (inconsistent data)
4. **Monitor implicit rewards**: Both chosen and rejected rewards should be reasonable - if rejected rewards are too high or chosen rewards are too low, your preference data may have labeling issues
5. **Compare experiments**: Save logs from each experiment to compare which hyperparameters and preference datasets produce the best alignment - use Tensorboard to view multiple experiments side-by-side

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
from gllm_training import DPOTrainer
from gllm_training.schema import StorageConfig

finetuner = DPOTrainer(
    model_name="Qwen/Qwen3-0.6b",
    storage_config=StorageConfig(
        provider="s3",
        upload_to_cloud=True,
        object_prefix="fine-tuned-models",
        bucket_name="glair-gen-ai-llm-model",
    ),
)
finetuner.save_existing_model(
    model_path="data/fine_tuned/exp_1/Qwen3-1.7b/exp_id_1:dpo_fine_tune_hyperparam_1:prompt_1:Qwen3-0.6b:adapter"
)
```
{% endstep %}
{% endstepper %}
