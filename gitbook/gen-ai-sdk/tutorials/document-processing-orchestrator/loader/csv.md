# CSV

**CSV Loader** is a component designed for **extracting information from CSV documents** and **converting it into a standardized JSON format**.

<details>

<summary>Prerequisites</summary>

This example specifically requires completion of all setup steps listed on the [Prerequisites](../../../prerequisites.md) page.

</details>

## **Installation**

{% tabs %}
{% tab title="Linux, macOS, or Windows WSL" %}
```bash
# you can use a Conda environment
pip install --extra-index-url https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/ "gllm-docproc[csv]"
```
{% endtab %}

{% tab title="Windows Powershell" %}
```powershell
# you can use a Conda environment
$token = (gcloud auth print-access-token)
pip install --extra-index-url "https://oauth2accesstoken:$token@glsdk.gdplabs.id/gen-ai-internal/simple/" "gllm-docproc[csv]"
```
{% endtab %}

{% tab title="Windows Command Prompt" %}
```bash
# you can use a Conda environment
FOR /F "tokens=*" %T IN ('gcloud auth print-access-token') DO SET TOKEN=%T
pip install --extra-index-url "https://oauth2accesstoken:%TOKEN%@glsdk.gdplabs.id/gen-ai-internal/simple/" "gllm-docproc[csv]"
```
{% endtab %}
{% endtabs %}

You can use the following as a sample file: [customers-1000.csv](http://assets.analytics.glair.ai/generative/csv/customers-1000.csv).

## Pandas Loader

**PandasLoader** is responsible to extract **tabular data** from CSV and similar delimited text formats using the pandas library.

{% stepper %}
{% step %}
Create a script called `main.py`:

{% code lineNumbers="true" %}
```python
from gllm_docproc.loader.csv import PandasLoader

source = "./data/source/customers-1000.csv"

# initialize the PandasLoader
loader = PandasLoader()

# load the csv source
loaded_elements = loader.load(source)
```
{% endcode %}
{% endstep %}

{% step %}
Run the script:

```bash
python main.py
```
{% endstep %}

{% step %}
The loader will generate the following: [output JSON](https://assets.analytics.glair.ai/generative/csv/pandas_loader_output.json).
{% endstep %}
{% endstepper %}
