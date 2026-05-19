# Table Chunker

**Table Chunker** is designed to handle the chunking of table element effectively. Recognizing that tables require specialized treatment to **maintain their integrity and usability when segmented into chunks**. Table Chunker ensuring that related data remains connected and contextually meaningful.

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
pip install --extra-index-url "https://oauth2accesstoken:%TOKEN%@glsdk.gdplabs.id/gen-ai-internal/simple/" "gllm-docproc"
```
{% endtab %}
{% endtabs %}

You can use the following as a sample file: [input](https://assets.analytics.glair.ai/generative/docx/docxparser-output.json).

{% stepper %}
{% step %}
Create a script called `main.py`:

{% code lineNumbers="true" %}
```python
import json
from gllm_docproc.chunker.table import MARKDOWN, TableChunker

# table element you want to chunk
with open('./data/source/table_element.json', 'r') as file:
    table_element = json.load(file)

# initialize Table Chunker
chunker = TableChunker(
    chunk_size=4000,
    chunk_overlap=0,
    table_format=MARKDOWN
)

# chunk table element
chunked_elements = chunker.chunk([table_element], is_table_need_index=True)
print(chunked_elements)
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
The loader will generate the following: [output JSON](https://assets.analytics.glair.ai/generative/docx/structuredelementchunker-output.json).
{% endstep %}
{% endstepper %}
