# 📎 Attachments

Attachments are commonly used when the question or query given needs to access external files, such as: **images** for multi-modal request, **audio files**, **documents** for context-aware question, and **other** **reference files**.

## Available Attachments Type

1. [**S3AttachmentConfig**](attachments.md#s3attachmentconfig): For AWS cloud-based file storage.
2. [**GoogleDriveAttachmentConfig**](attachments.md#googledriveattachmentconfig): For Google Drive collaborative cloud storage.
3. [**LocalAttachmentConfig**](attachments.md#localattachmentconfig): For local directory storage.

***

### :cloud: S3AttachmentConfig

**Use when:** You store your files in Amazon S3 buckets. This is ideal for large-scale, production environment which allow you to put the files in the cloud.

Example usage:

```python
from gllm_evals.types import S3AttachmentConfig

attachments_config = S3AttachmentConfig(
    s3_bucket="your-s3-bucket",
    s3_prefix="your-s3-prefix", # directory where you store the files in the S3 bucket
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    aws_region=os.getenv("AWS_REGION"),
)

# you then can put the `attachments_config` as a parameter in a certain dataset
dataset = await SpreadsheetDataset.from_gsheets(
    sheet_id="your-sheet-id",
    worksheet_name="your-worksheet-name",
    client_email=os.getenv("GOOGLE_SHEETS_CLIENT_EMAIL"),
    private_key=os.getenv("GOOGLE_SHEETS_PRIVATE_KEY"),
    attachments_config=attachments_config,
),
```

***

### :card\_box: GoogleDriveAttachmentConfig

**Use when:** You store your files in google drive. This is ideal for collaborative environments and for team members already storing the files there without any plan to use S3.

Example usage:

```python
from gllm_evals.types import GoogleDriveAttachmentConfig

attachments_config = GoogleDriveAttachmentConfig(
    client_email=os.getenv("GOOGLE_CLIENT_EMAIL"),
    private_key=os.getenv("GOOGLE_PRIVATE_KEY"),
    folder_id="your-gdrive-folder-id",
)

# you then can put the `attachments_config` as a parameter in a certain dataset
dataset = await SpreadsheetDataset.from_gsheets(
    sheet_id="your-sheet-id",
    worksheet_name="your-worksheet-name",
    client_email=os.getenv("GOOGLE_SHEETS_CLIENT_EMAIL"),
    private_key=os.getenv("GOOGLE_SHEETS_PRIVATE_KEY"),
    attachments_config=attachments_config,
),
```

\*If you do not have any service account to fill the `client_email` and `private_key`, you can either create one OR store the files in [this directory](https://drive.google.com/drive/u/0/folders/1lqVxajjQ3bklY7ITS82fyDDAsuQN6trq). You can then contact evals team to provide you our credentials.

***

### :computer: LocalAttachmentConfig

**Use when:** You store the files directly from the local filesystem. This is best for development and testing, single-machine deployments, or on-premise projects.

Example usage:

```python
from gllm_evals.types import LocalAttachmentConfig

attachments_config = LocalAttachmentConfig(
    local_directory="path/to/your/directory"
)

# you then can put the `attachments_config` as a parameter in a certain dataset
dataset = await SpreadsheetDataset.from_gsheets(
    sheet_id="your-sheet-id",
    worksheet_name="your-worksheet-name",
    client_email=os.getenv("GOOGLE_SHEETS_CLIENT_EMAIL"),
    private_key=os.getenv("GOOGLE_SHEETS_PRIVATE_KEY"),
    attachments_config=attachments_config,
),
```

***

## Dataset Format

After storing the files in your preferable storage, you should include the `attachments` field in your dataset in a list format.

Usage example:

<table><thead><tr><th width="122.5999755859375">question_id</th><th>query</th><th>expected_response</th><th>attachments</th></tr></thead><tbody><tr><td>1</td><td>Who is this person?</td><td>This person is Kartini.</td><td>["kartini.png"]</td></tr><tr><td>2</td><td>The answer of 1+1?</td><td>The answer is 2.</td><td></td></tr><tr><td>3</td><td>Siapa nama penulis artikel ini?</td><td>Penulis artikel ini adalah xxx dan yyy.</td><td>["article_1.docx", "article2.docx"]</td></tr></tbody></table>

For row that does not need an attachment, you can leave it empty. When calling the a dataset class or alternative constructor, the attachments will be passed to your inference function with the `attachments` parameter.
