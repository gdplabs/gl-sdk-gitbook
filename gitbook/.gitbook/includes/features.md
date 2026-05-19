---
title: Features
---

<details>

<summary>Prerequisites</summary>

Before installing, make sure you have:

1. [Python 3.11+](https://glair.gitbook.io/hello-world/prerequisites#python-v3.11-or-v3.12)
2. [Pip](https://pip.pypa.io/en/stable/installation/) or&#x20;
3. [gcloud CLI](https://cloud.google.com/sdk/docs/install) - required because `gllm-training` is a private library hosted in a private Google Cloud repository

After installing, please run

```bash
gcloud auth login
```

to authorize gcloud to access the Cloud Platform with Google user credentials.

{% hint style="info" %}
Our internal `gllm-training` package is hosted in a secure Google Cloud Artifact Registry.\
You need to authenticate via `gcloud CLI` to access and download the package during installation.
{% endhint %}

4. The minimum requirements:
   1. CUDA-compatible GPU
   2. Recommendation GPU:&#x20;
      1. RTX A5000&#x20;
      2. RTX 40/50 series.&#x20;
   3. Windows/Linux, currently not support for macOS

</details>
