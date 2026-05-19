---
icon: file-import
---

# Loader

## What is Loader?

**Loader** is designed for **extracting information from the provided source**.

To give you an idea what a Loader does, this is a snippet of a sample JSON output:

```json
{
    "text": "[Header] This is the Header of the Document",
    "structure": "uncategorized",
    "metadata": {
        "source": "pdf-example.pdf",
        "source_type": "pdf",
        "loaded_datetime": "2024-10-17 17:10:30",
        "font_size": 12,
        "font_family": "TimesNewRomanPSMT",
        "font_color": "#000000",
        "coordinates": [
            72,
            292,
            49,
            36
        ],
        "links": [],
        "layout_width": 612,
        "layout_height": 792,
        "page_number": 1,
        "sorted_element_format": [
            [
                12,
                "TimesNewRomanPSMT",
                "#000000"
            ]
        ]
    }
}
```

<details>

<summary>This is the complete JSON Schema for the output</summary>

```json
{
 "$schema": "https://json-schema.org/draft/2020-12/schema",
 "type": "array",
 "items": {
   "type": "object",
   "properties": {
     "text": {
       "type": "string",
       "description": "Text content of the document"
     },
     "structure": {
       "type": "string",
       "description": "Structure of the document",
       "enum": [
         "uncategorized",
         "header",
         "title",
         "heading",
         "heading 1",
         "heading 2",
         "heading 3",
         "heading 4",
         "heading 5",
         "heading 6",
         "paragraph",
         "table",
         "audio",
         "image",
         "video",
         "footer",
         "footnote"
       ]
     },
     "metadata": {
       "type": "object",
       "properties": {
         "source": {
           "type": "string",
           "description": "Source of the document"
         },
         "source_type": {
           "type": "string",
           "description": "Type of source either pdf, website, or other",
           "enum": [
             "pdf",
             "docx",
             "xlsx",
             "pptx",
             "csv",
             "txt",
             "website",
             "audio",
             "image",
             "video"
           ]
         },
         "loaded_datetime": {
           "type": "string",
           "description": "Date and time when the data was loaded"
         }
       },
       "required": [
         "source",
         "source_type",
         "loaded_datetime"
       ],
       "description": "Metadata of the document"
     }
   },
   "required": [
     "text",
     "structure",
     "metadata"
   ]
 }
}

```

</details>

Our Loader has the following sub components to handle various types of documents:

1. Audio
2. CSV
3. DOCX
4. HTML
5. Image
6. JSON
7. PDF
8. PPTX
9. TXT
10. XLSX

## API Reference

For more information about Loader, please take a look at our [API Reference page](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_docproc/api/loader.html).
