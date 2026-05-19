---
icon: books
---

# Supervised Fine Tuning (SFT)

## What is Supervised Fine Tuning?

Supervised Fine Tuning (SFT) is a training approach that uses labeled input-output pairs to teach the model specific behaviors and response patterns. The model learns by observing examples of correct inputs and their corresponding desired outputs, gradually adjusting its parameters to minimize the difference between its predictions and the target responses. This technique is particularly effective when you have clear examples of how the model should behave and provides predictable, measurable improvements in task-specific performance.

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

Let's jump into a basic example fine-tuned using `SFTTrainer`. SFT trainer cannot be empty, which means it must have at least the model name and csv datasets path.

```python
from gllm_training import SFTTrainer

finetuner = SFTTrainer(
    model_name="Qwen/Qwen3-1.7b",
    datasets_path="examples/sft_csv"
)
results = finetuner.train()
```

## Fine tuning model using YAML file.

We can run experiments in a more structured way by using a YAML file. The current fine-tuning SDK supports both online data from Google Spreadsheets and local data in CSV format.

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
**`Experiment configuration (sft_experiment_config.yml)`**

You can use a YAML file to plan your fine tuning experiments. To fine tuning with YAML, you need to define the required variables in the file.

```yaml
fine_tune_hyperparam_1: &fine_tune_hyperparam_1_conf
  hyperparameters_id: "1"
  max_seq_length: 2048
  load_in_8bit: true
  r: 16
  lora_alpha: 16
  target_modules: ["q_proj", "k_proj", "v_proj"]
  per_device_train_batch_size: 1
  learning_rate: 2.0e-4
  num_train_epochs: 1
  eval_strategy: "steps"
  save_strategy: "steps"
  load_best_model_at_end: true

storage_config: &storage_config
  provider: "s3"
  bucket_name: "your-s3-bucket"
  upload_to_cloud: false

experiment_1:
  experiment_id: "1"
  hyperparameters: *fine_tune_hyperparam_1_conf
  storage_config: *storage_config
  model_name: "Qwen/Qwen3-1.7b"
  framework: "unsloth"
  spreadsheet_id: "<your-google-sheets-id>"
  train_sheet: "<train_data_sheet_name>"
  validation_sheet: "<validation_data_sheet_name>"
  prompt_sheet: "<prompt_sheet>"
  prompt_name: "<your_prompt_name>"
  column_mapping_config:
    input_columns:
      query: "user_query"
    label_columns:
      label: "target"
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
from dotenv import load_dotenv
from gllm_training import YamlConfigLoader
from gllm_training import SFTTrainer
load_dotenv(override=True)

config_loader = YamlConfigLoader(base_dir="./")
config = config_loader.load("sft_experiment_config.yml", "experiment_1")
finetuner = SFTTrainer(**config)
finetuner.train()
```
{% endstep %}
{% endstepper %}

### Example 2: Fine tuning using local data.

The remaining hyperparameter configurations for fine-tuning are the same as when using online data. Below is an example YAML configuration for using local data for training and validation.

```yaml
experiment_1:
  experiment_id: "1"
  hyperparameters: *fine_tune_hyperparam_1_conf
  storage_config: *storage_config
  model_name: "Qwen/Qwen3-1.7b"
  framework: "unsloth"
  datasets_path: "examples/csv"
  train_filename: "training_data.csv"
  validation_filename: "validation_data.csv"
  prompt_filename: "prompt_data.csv"
  prompt_name: "prompt_default"
  column_mapping_config:
    input_columns:
      query: "query"    
    image_columns:
      image: "image_url"
    label_columns:
      label: "target"
```

## Datasets Format

### Data training and validation

The column names should correspond to what you define in the `column_mapping_config`.

**Minimum Required Columns:**

| Column Name | Description                                                                           |
| ----------- | ------------------------------------------------------------------------------------- |
| `query`     | The input query or prompt that will be used as input to the model                     |
| `target`    | The expected output or response that the model should learn to generate               |
| `image_url` | The url of image to be inserted in the user query, must be a public downloadable url  |

### Prompts

The prompt data should contained columns:

| Column Name | Description                                                                                                                        |
| ----------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| `name`      | A unique identifier for the prompt template                                                                                        |
| `system`    | The system prompt, which sets the model's role and context. It does not contain placeholders                                       |
| `user`      | The user prompt template. It **must** contain placeholders (e.g., `{query}`) that will be replaced by data from your input columns |

## Logging Monitoring

During the fine-tuning process, the SDK automatically generates comprehensive logs to help you monitor training progress and debug issues. These logs are stored in two formats:

### JSONL Logs (Structured Training Metrics)

The SDK generates structured JSONL logs that capture detailed training metrics at each step. These logs are stored in:

```
data/sft/model/exp_{experiment_id}/{model_name}/logs/sft_train_steps.jsonl
```

**Example path**: `data/sft/model/exp_1/Qwen3-1.7b/logs/sft_train_steps.jsonl`

Each line in the JSONL file contains a JSON object with training metrics such as:

* `step`: Training step number
* `loss`: Training loss at that step
* `learning_rate`: Current learning rate
* `epoch`: Current epoch number
* And other relevant metrics

You can parse these logs programmatically or use tools like `jq` to analyze the training progression:

```bash
# View the last 10 training steps
tail -n 10 data/sft/model/exp_1/Qwen3-0.6b/logs/sft_train_steps.jsonl | jq .

# Extract both training and evaluation losses with step information
cat data/sft/model/exp_1/Qwen3-0.6b/logs/sft_train_steps.jsonl | jq -r 'select(.loss != null) | "\(.step): \(.loss)"'

# Get the final training summary (last line)
tail -n 1 data/sft/model/exp_1/Qwen3-0.6b/logs/sft_train_steps.jsonl | jq .
```

> **Note**: The JSONL file contains both training steps (with `loss` field) and evaluation steps (with `eval_loss` field). Use `select()` to filter for the specific type of data you need.

### Tensorboard Logs (Visual Monitoring)

For visual monitoring and analysis, the SDK also generates TensorBoard-compatible logs stored in:

```
data/sft/model/exp_{experiment_id}/{model_name}/logs_tensorboard
```

**Example path**: `data/sft/model/exp_1/Qwen3-0.6b/logs_tensorboard`

To visualize your training progress:

1. **Launch TensorBoard**:

```bash
tensorboard --logdir data/sft/model/exp_1/Qwen3-0.6b/logs_tensorboard
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

1. **Monitor training stability**: Check that your loss decreases smoothly without sudden jumps - if you see spikes or irregular patterns, your learning rate might be too high or there could be data quality issues
2. **Track convergence**: Use TensorBoard to see when your model stops getting better - if training loss keeps going down but evaluation loss stops improving or starts going up, your model is overfitting
3. **Debug issues**: JSONL logs show detailed metrics for each training step - look for NaN values, wild loss swings (learning rate problem), or when training loss is much lower than evaluation loss (overfitting)
4. **Monitor evaluation metrics**: Good training means both training and evaluation losses go down together, with evaluation loss being slightly higher - if the gap between them gets too large, something is wrong

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
from gllm_training import SFTTrainer
from gllm_training.schema import StorageConfig

finetuner = SFTTrainer(
    model_name="Qwen/Qwen3-0.6b",
    storage_config=StorageConfig(
        provider="s3",
        upload_to_cloud=True,
        object_prefix="fine-tuned-models",
        bucket_name="glair-gen-ai-llm-model",
    ),
)
finetuner.save_existing_model(
    model_path="data/fine_tuned/exp_1/Qwen3-1.7b/exp_id_1:sft_fine_tuned_hyperparam_1:prompt_1:Qwen3-1.7b:adapter"
)
```
{% endstep %}
{% endstepper %}
