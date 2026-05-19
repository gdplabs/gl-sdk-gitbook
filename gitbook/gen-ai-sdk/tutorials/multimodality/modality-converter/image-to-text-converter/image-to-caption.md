# Image to Caption

## Introduction

The Image to Caption component converts images to natural language captions for multimodal AI workflows. It generates multiple captions using multimodal LLMs (e.g., Gemini) and incorporates context such as image metadata, domain knowledge, and reference attachments to generate contextual captions.

## Installation

{% tabs %}
{% tab title="Linux, macOS, or Windows WSL" %}
```
# you can use a Conda environment
pip install --extra-index-url https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/ "gllm-multimodal"
```
{% endtab %}

{% tab title="Windows Powershell" %}
```powershell
# you can use a Conda environment
$token = (gcloud auth print-access-token)
pip install --extra-index-url "https://oauth2accesstoken:$token@glsdk.gdplabs.id/gen-ai-internal/simple/" "gllm-multimodal"
```
{% endtab %}

{% tab title="Windows Command Prompt" %}
```
# you can use a Conda environment
FOR /F "tokens=*" %T IN ('gcloud auth print-access-token') DO pip install --extra-index-url "gllm-multimodal"
```
{% endtab %}
{% endtabs %}

## Quickstart

The simplest way to initialize Image to Caption component is to use the built-in preset.

{% file src="../../../../../.gitbook/assets/obat.webp" %}

```python
import asyncio

from gllm_inference.schema import Attachment
from gllm_multimodal.modality_converter.image_to_text.image_to_caption import LMBasedImageToCaption

image = Attachment.from_path("./obat.webp")
converter = LMBasedImageToCaption.from_preset("default")
captions = asyncio.run(converter.convert(image.data))
print(f"Captions: {captions.result}")
```

**Output:**

```
Captions:
Kumpulan kapsul berwarna oranye, masing-masing bertuliskan angka "82" dan simbol unik.
Detail tumpukan kapsul farmasi yang siap untuk didistribusikan.
Setiap kapsul oranye ini memiliki kode identifikasi "82" tercetak di permukaannya.
Kapsul-kapsul ini menunjukkan pola dan nomor yang seragam, khas produk farmasi.
Gambar close-up yang memperlihatkan banyak kapsul oranye dengan penandaan yang jelas.
```

## Contextual Image Captioning <a href="#contextual-image-captioning" id="contextual-image-captioning"></a>

Sometimes giving only the image doesn't tell the whole story. Image to Caption supports passing **additional context** for more contextual image captioning.

### Image One Liner <a href="#contextual-image-captioning" id="contextual-image-captioning"></a>

`image_one_liner` is a brief, one-line summary or title of the image.

```python
image = Attachment.from_path("./obat.webp")
converter = LMBasedImageToCaption.from_preset("default")
captions = asyncio.run(converter.convert(
    image.data,
    number_of_captions=5,
    image_one_liner="Pil antivirus eksperimental",
))
print(f"Captions: {captions.result}")
```

**Output:**

```
Captions:
Pil antivirus eksperimental yang terlihat dalam gambar ini sedang menjalani tahap uji coba.
Kapsul berwarna oranye dengan kode '82' dan simbol unik ini adalah bagian dari pengembangan pil antivirus eksperimental.
Harapan baru di dunia medis, pil-pil antivirus eksperimental ini berpotensi besar dalam melawan infeksi virus.
Setumpuk pil antivirus eksperimental, masing-masing mewakili upaya penelitian untuk menemukan pengobatan yang efektif.
Pil antivirus eksperimental ini menunjukkan kemajuan signifikan dalam ilmu farmasi untuk menanggulangi berbagai penyakit virus.
```

### Image Description <a href="#contextual-image-captioning" id="contextual-image-captioning"></a>

`image_description` adds detailed description of the image's content from relevant sources (e.g. article, pdf page).

```python
image = Attachment.from_path("./obat.webp")
converter = LMBasedImageToCaption.from_preset("default")
captions = asyncio.run(converter.convert(
    image.data,
    number_of_captions=5,
    image_description="Sebuah obat eksperimental yang dikonsumsi pasien pengidap Covid-19 dapat mengurangi risiko rawat inap atau kematian sekitar setengahnya, berdasarkan hasil uji klinis sementara. Obat antivirus bernama molnupiravir itu diberikan dalam bentuk tablet dua kali sehari kepada pasien yang baru saja didiagnosis dengan Covid-19. Produsen obat AS Merck mengatakan hasilnya sangat positif sehingga pengawas eksternal meminta agar uji coba dihentikan lebih awal. Perusahaan itu mengatakan mereka akan mengajukan permohonan izin penggunaan darurat (Emergency Use Authorisation, EUA) untuk obat itu di AS dalam dua minggu ke depan. Dr Anthony Fauci, kepala penasihat medis untuk Presiden AS Joe Biden, menyebut hasil ini 'berita yang sangat baik', namun meminta kehati-hatian sampai lembaga pengawas obat dan makanan AS, FDA, meninjau data dari uji klinis."
))
print(f"Captions: {captions.result}")
```

```
Captions:
Pil antivirus eksperimental molnupiravir, yang dikembangkan oleh Merck, menunjukkan potensi besar dalam mengurangi risiko rawat inap atau kematian akibat Covid-19.
Uji klinis sementara menunjukkan pil molnupiravir ini mampu mengurangi risiko rawat inap atau kematian pasien Covid-19 hingga separuhnya.
Merck berencana mengajukan permohonan Emergency Use Authorisation (EUA) untuk pil molnupiravir ini di AS, setelah hasil uji coba yang sangat positif.
Dikonsumsi dua kali sehari, pil molnupiravir menawarkan pendekatan baru dalam pengobatan pasien yang baru didiagnosis Covid-19.
Pil antivirus molnupiravir yang digambarkan Dr Anthony Fauci sebagai 'berita yang sangat baik' ini diharapkan bisa menjadi senjata baru melawan pandemi Covid-19.
```

### Domain Knowledge <a href="#contextual-image-captioning" id="contextual-image-captioning"></a>

`domain_knowledge` provides relevant, keyword-based domain-specific information that are not present in `image_description.`

```python
image = Attachment.from_path("./obat.webp")
converter = LMBasedImageToCaption.from_preset("default")
captions = asyncio.run(converter.convert(
    image.data,
    number_of_captions=5,
    domain_knowledge="Efek samping tidak diketahui, Covid-19, Merck, Obat eksperimental, Antivirus"
))
print(f"Captions: {captions.result}")
```

```
Captions:
Kapsul-kapsul ini adalah obat eksperimental antivirus dari Merck yang dikembangkan untuk melawan Covid-19.
Menampilkan obat eksperimental Covid-19 dari Merck, yang efek sampingnya masih belum diketahui secara penuh.
Salah satu harapan baru: obat eksperimental antivirus yang dikembangkan Merck untuk penanganan Covid-19.
Sebagai bagian dari upaya global, pil antivirus eksperimental dari Merck ini ditujukan untuk pasien Covid-19.
Obat eksperimental Merck ini mewakili langkah maju dalam penelitian antivirus untuk pengobatan Covid-19.
```

### Attachment Context

Beyond textual input, the use of supporting images is highly beneficial. This method's primary strength is its capacity to deliver spatial or structural metadata about the primary image (including positional data), which substantially enhances the Large Language Model's (LLM's) overall contextual comprehension.

```python
image = Attachment.from_path("./obat.webp")
supporting_images = [Attachment.from_path("./berita.png")]
converter = LMBasedImageToCaption.from_preset("default")
captions = asyncio.run(converter.convert(
    image.data,
    number_of_captions=5,
    attachment_contexts=supporting_images
))
print(f"Captions: {captions.result}")
```

```
Captions:
Tumpukan pil Molnupiravir, antivirus oral eksperimental pertama yang menjanjikan untuk pasien COVID-19.
Kapsul Molnupiravir ini terbukti mengurangi risiko kematian dan perawatan di rumah sakit bagi penderita COVID-19.
Obat antivirus oral Molnupiravir diberikan dua kali sehari kepada pasien COVID-19 yang baru didiagnosis.
Molnupiravir, pil eksperimental yang dikembangkan oleh Merck, menunjukkan hasil uji coba yang sangat positif melawan COVID-19.
Dengan hasil uji coba yang positif, pil Molnupiravir menjadi harapan baru dalam penanganan pandemi COVID-19.
```

### Combined <a href="#contextual-image-captioning" id="contextual-image-captioning"></a>

You can also combine `image_one_liner`, `image_description`, and `domain_knowledge` together for fully contextual captioning.

```python
image = Attachment.from_path("./obat.webp")
converter = LMBasedImageToCaption.from_preset("default")
captions = asyncio.run(converter.convert(
    image.data,
    image_one_liner="Pil antivirus eksperimental",
    image_description="Sebuah obat eksperimental yang dikonsumsi pasien pengidap Covid-19 dapat mengurangi risiko rawat inap atau kematian sekitar setengahnya, berdasarkan hasil uji klinis sementara. Obat antivirus bernama molnupiravir itu diberikan dalam bentuk tablet dua kali sehari kepada pasien yang baru saja didiagnosis dengan Covid-19. Produsen obat AS Merck mengatakan hasilnya sangat positif sehingga pengawas eksternal meminta agar uji coba dihentikan lebih awal. Perusahaan itu mengatakan mereka akan mengajukan permohonan izin penggunaan darurat (Emergency Use Authorisation, EUA) untuk obat itu di AS dalam dua minggu ke depan. Dr Anthony Fauci, kepala penasihat medis untuk Presiden AS Joe Biden, menyebut hasil ini 'berita yang sangat baik', namun meminta kehati-hatian sampai lembaga pengawas obat dan makanan AS, FDA, meninjau data dari uji klinis.",
    domain_knowledge="Efek samping tidak diketahui, Covid-19, Merck, Obat eksperimental, Antivirus"
))
print(f"Captions: {captions.result}")
```

```
Captions:
Pil molnupiravir, obat antivirus eksperimental dari Merck untuk pasien Covid-19.
Obat eksperimental molnupiravir terbukti dapat mengurangi risiko rawat inap atau kematian akibat Covid-19.
Merck akan mengajukan permohonan Emergency Use Authorisation (EUA) untuk molnupiravir, pil antivirus ini, di AS.
Harapan baru dalam penanganan Covid-19: molnupiravir, obat antivirus yang menunjukkan hasil positif dalam uji klinis.
Molnupiravir, obat dalam bentuk tablet yang dikonsumsi dua kali sehari oleh pasien Covid-19 yang baru didiagnosis.
```

## Customize Model

When using preset, the captioning model can be changed via the `DEFAULT_IMAGE_CAPTIONING_MODEL_ID` environment variable

```dotenv
DEFAULT_IMAGE_CAPTIONING_MODEL_ID="openai/gpt-5"
```

## Customize Model and Prompt

Using a custom LM Request Processor allows you to customize model and/or prompt.

```python
import asyncio

from gllm_inference.schema import Attachment
from gllm_multimodal.modality_converter.image_to_text.image_to_caption import LMBasedImageToCaption

lmrp = build_lm_request_processor(
    model_id="google/gemini-2.5-flash",
    credentials="<your-api-key>", # or use the environment variable GOOGLE_API_KEY
    system_template="Create {number_of_captions} captions based on the provided images. Your output should be a valid JSON",
    user_template="<INPUT_STRUCTURE>Title: {image_one_liner} Content: {image_description} Main Image Filename: {filename} Metadata: {image_metadata} Injected Domain Knowledge: {domain_knowledge} </INPUT_STRUCTURE>",
    output_parser_type="json"
)
image = Attachment.from_path("./school_backpack.jpg")
converter = LMBasedImageToCaption(lm_request_processor=lmrp)
captions = asyncio.run(converter.convert(image.data))
print(f"Captions: \n{captions.result}")
```
