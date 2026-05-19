# Parser Router

**ParserRouter** is designed to identify the appropriate [`ParserType`](https://github.com/GDP-ADMIN/gl-sdk/blob/main/libs/gllm-docproc/gllm_docproc/model/parser_type.py) for loaded elements, accepting either a JSON file path or an in-memory list of element dictionaries.

\
It identifies the parser type by inspecting the `source_type` field in the `metadata` of the first element, and returns the result as a dictionary keyed by `ParserType.KEY`, or marks it as `uncategorized` if no match is found.

<details>

<summary>Prerequisites</summary>

If you want to try the snippet code in this page:

* Completion of all setup steps listed on the [Prerequisites](/broken/pages/qFjvrdtREuJTNsHqV6HE) page.

</details>

## **Installation**

{% tabs %}
{% tab title="Linux, macOS, or Windows WSL" %}
```bash
# you can use a Conda environment
pip install --extra-index-url https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/ "gllm-docproc"
```
{% endtab %}

{% tab title="Windows Powershell" %}
```powershell
# you can use a Conda environment
$token = (gcloud auth print-access-token)
pip install --extra-index-url "https://oauth2accesstoken:$token@glsdk.gdplabs.id/gen-ai-internal/simple/" "gllm-docproc"
```
{% endtab %}

{% tab title="Windows Command Prompt" %}
```bash
# you can use a Conda environment
FOR /F "tokens=*" %T IN ('gcloud auth print-access-token') DO SET TOKEN=%T
pip install --extra-index-url "https://oauth2accesstoken:%TOKEN%@glsdk.gdplabs.id/gen-ai-interna
```
{% endtab %}
{% endtabs %}

You can use the following as a sample file: [pymupdfloader-output.json](https://assets.analytics.glair.ai/generative/pdf/pymupdfloader-output.json)

## Running the Router

{% stepper %}
{% step %}
Create a script called `main.py`:

{% tabs %}
{% tab title="Using a path to a JSON file" %}
{% code lineNumbers="true" %}
```python
from gllm_docproc.dpo_router.parser_router import ParserRouter
from gllm_docproc.model.parser_type import ParserType

# Example source: path to loaded elements JSON file
source = "./loaded_elements.json"

# Initialize ParserRouter
router = ParserRouter()

# Route the file to get the parser type
result = router.route(source)

# Access the detected parser type
print(f"Detected parser type: {result[ParserType.KEY]}")
```
{% endcode %}
{% endtab %}

{% tab title=" Using list of element dictionaries" %}
{% code lineNumbers="true" %}
```python
import json
from gllm_docproc.dpo_router.parser_router import ParserRouter
from gllm_docproc.model.parser_type import ParserType

# Load elements from JSON file into memory
with open("./loaded_elements.json", "r", encoding="utf-8") as f:
    elements = json.load(f)

# Initialize ParserRouter
router = ParserRouter()

# Route the in-memory elements to get the parser type
result = router.route(elements)

# Access the detected parser type
print(f"Detected parser type: {result[ParserType.KEY]}")
```
{% endcode %}
{% endtab %}
{% endtabs %}
{% endstep %}

{% step %}
Run the script:

```bash
python main.py
```
{% endstep %}

{% step %}
Example output:

```json
Detected parser type: pdf_parser
```
{% endstep %}
{% endstepper %}

{% hint style="info" %}
The returned dictionary has:

* **Key:** `ParserType.KEY` (`"parser_type"`)
* **Value:** one of the values defined in [ParserType](https://app.gitbook.com/s/tTgcodhP2cUh2QvSVXyn/getting-started/introduction), such as `"pdf_parser"`, `"docx_parser"`, `"audio_parser"`, etc.
{% endhint %}
