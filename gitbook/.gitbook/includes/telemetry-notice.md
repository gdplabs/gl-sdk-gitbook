---
title: Telemetry notice
---

{% hint style="info" %}
When running the pipeline, you may encounter an error like this:

```
[2025-08-26T14:36:10+0700.550 chromadb.telemetry.product.posthog ERROR] Failed to send telemetry event CollectionQueryEvent: capture() takes 1 positional argument but 3 were given
```

Don't worry about this, since we do not use this Chroma feature. Your Pipeline should still work.
{% endhint %}
