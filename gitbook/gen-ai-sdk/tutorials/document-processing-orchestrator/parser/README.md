---
icon: heading
---

# Parser

## What is Parser?

**Parser** is responsible for defining element structures based on output from **Loader**.

To give you an idea what a Parser does, this is a snippet of a sample JSON output:

```json
{
    "text": "[Header] This is the Header of the Document",
    "structure": "header", // 👈 parser defines this as "header" (previous value from Loader is "uncategorized")
    "metadata": {
        "source": "pdf-example.pdf",
        "source_type": "pdf",
        ...
    }
}
```

You can compare with the output from Loader [here](../loader/).

Possible `structure` values:

1. `PAGE`
2. `HEADER`
3. `TITLE`
4. `HEADING` (`HEADING 1` through `HEADING 6` )
5. `PARAGRAPH`
6. `FOOTER`
7. `FOOTNOTE`
8. `TABLE`
9. `IMAGE`
10. `AUDIO`
11. `VIDEO`
12. `UNCATEGORIZED`

Our Parser has the following sub components:

1. Document
   1. [DOCX Parser](docx.md)
   2. [PDF Parser](pdf.md)
   3. [PPTX Parser](pptx.md)
   4. [TXT Parser](txt.md)
   5. [XLSX Parser](xlsx.md)
2. HTML parser
   1. [HTML Flat Parser](html.md)
3. Image parser
   1. Image MIME Normalizer Parser
   2. Image Plain Small Filter Parser
4. Table Parser
   1. Table Caption Parser

## API Reference

For more information about Parser, please take a look at our [API Reference page](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_docproc/api/parser.html).
