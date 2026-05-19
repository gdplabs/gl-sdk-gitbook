---
hidden: true
---

# 📑 Evaluate GLChat - Google Colab Guide

### What is This?

This guide helps you test how well **GLChat** answers questions. You'll provide test questions and see how accurately your selected application / chatbot responds. The evaluation process runs automatically in **Google Colab** and shows you detailed results about the chatbot's performance.

**What you'll accomplish:**

* Test the chatbot with your own questions and scenarios
* Get scores showing how well the chatbot performs
* View detailed analysis of each answer in a dashboard

**⚠️ Important First Step**: Before you begin, make sure to **copy** [**this Google Colab notebook**](https://colab.research.google.com/drive/17hXNvMM3SMifpKUQfRBATTM4QRF9AG88) **to your own Google Drive**. This ensures you have your own working copy and can save your progress.

### 1. Prerequisites

Before you begin, make sure you have:

* **Access to Google Account (@gdplabs.id)**: Required for authenticating with Google services (Google Drive, Google Sheets, and Google Cloud) during the evaluation process. The notebook needs to access your Google Drive to mount files and authenticate with gcloud to install the private SDK module.
* **Access to the** [**shared drive folder**](https://drive.google.com/drive/u/0/folders/1per1tZBH9DDQ_0jfsIwNgFbEL5fp-JAi): This folder contains a configuration file (`.env`) needed for the evaluation. The evaluation process requires the configuration file to connect to various services like Langfuse, Google Sheets service account credentials, and GLChat API settings.
* **Langfuse service is accessible**: Before running the evaluation, check that the Langfuse dashboard at https://langfuse.obrol.id/ can be opened (you should not see a "503 Service Temporarily Unavailable" error). See [Starting Langfuse Service](evaluate-glchat-google-colab-guide.md#starting-langfuse-service) if the service is not accessible.
* **Google API Key**: Each user or team must use their own Google API credentials for running the evaluation. You **must** set `GOOGLE_API_KEY` as a Colab Secret before running the evaluation.\
  Without this, you will get an error and the evaluation may fail. Follow the instruction on how to add a colab secret in [Using Colab Secrets](evaluate-glchat-google-colab-guide.md#using-colab-secrets) section below.
  * For the API key, **use the key assigned to your specific project**. If you don't have one, **ask the project's team lead** to provide it.
  * :warning: **Please keep the API key secure**. Do not share it publicly or paste it into documents, chats, screenshots, or code that others can see. If the key is leaked, someone else could use it, which may lead to unexpected costs or service issues for the project.

**📝 Note about this guide**: This guide is simplified and uses **Google Sheets as the default dataset source** and **Google Drive as the default storage for attachments**. If you need to use other dataset sources, see the available options [here](https://gdplabs.gitbook.io/sdk/tutorials/evaluation/dataset). If you need to use other attachment types, see the available options [here](https://gdplabs.gitbook.io/sdk/tutorials/evaluation/attachments).

#### Starting Langfuse Service

If the Langfuse URL shows "503 Service Temporarily Unavailable" or cannot be accessed, you need to turn on the Langfuse service. For GDP Labs' members, see [here](https://docs.google.com/document/d/1ujhUyEgyBM5FKSZ9Fnwc30IZ6nT-etYaADvZqAsewMs/edit?tab=t.0#heading=h.9zled7n1g5dn).

### 2. Important Notes Before You Start

#### Authentication During Execution

When you run the evaluation, you will encounter prompts for authentication:

**a. Google Drive Mount** (may be required)

* You may be prompted to mount your Google Drive
* This will ask you to authenticate with your Google account
* Click the URL that appears, sign in with your Google account (@gdplabs.id), and follow the authentication steps
* This allows the notebook to access files from your Google Drive

**b. Google Cloud Login (gcloud)** (may be required)

* You may see a URL asking you to authenticate with Google Cloud
* Click the URL to open it in a new tab
* Sign in with your Google account (@gdplabs.id)
* After authentication, copy from the provided URL
* Paste the URL back into the notebook cell where prompted
* Press Enter to continue
* This allows the notebook to install the private SDK module

#### Using Colab Secrets

If you don't provide your own credentials, the evaluation will use the default credentials from the encrypted file:

* **Langfuse**: Results will be logged to the `glchat_beta` project in Langfuse
* **Google Sheets**: Uses the evals team's Google Sheets service account credentials
* **GLChat**: Uses the GLChat beta base URL and API key

**How to Add Secrets**

1. In the Colab sidebar, look for the "Secrets" section (🔑 icon)
2. Click **Add new secret**.
3. Enter the secret name (e.g., `GOOGLE_API_KEY`).
4. Enter your value and save it.
5. Make sure to turn on the _Notebook Access_ toggle.

**Mandatory Secret**

You must define this before running the notebook:

* `GOOGLE_API_KEY` — Your Google API key credentials\
  (Required for Google API calls used in the evaluation.)

**Optional Secrets (Override Defaults)**

If you want to override values from the default credentials, you can add any of the following:

* `LANGFUSE_PUBLIC_KEY` - Your Langfuse public key
* `LANGFUSE_SECRET_KEY` - Your Langfuse secret key
* `LANGFUSE_HOST` - Your Langfuse host URL
* `GOOGLE_SHEETS_CLIENT_EMAIL` - Your Google Sheets service account email
* `GOOGLE_SHEETS_PRIVATE_KEY` - Your Google Sheets service account private key
* `GLCHAT_BASE_URL` - Your GLChat base URL
* `GLCHAT_API_KEY` - Your GLChat API key

Only add the secrets you want to customize.\
Any secret you define here will override the value from the encrypted config file.

### 3. Prepare Dataset

Before evaluation, you need to prepare a Google Sheets document with all the information needed for evaluation.

#### Storage Options for Your Dataset

You have two ways to store your Google Sheets:

**Option 1: Use Your Own Google Service Account**

* **What it is**: A Google service account is a special type of account that allows automated access to Google services. This requires technical setup.
* **What to do**: If you already have one or want to create it, you can store the Google Sheets yourself. You'll need to fill in secure credentials (called "Colab secrets") in the notebook. Look for the "Secrets" section in the Colab sidebar.

**Option 2: Use Our Shared Folder** (_\*recommended for non-engineers or engineers who do not have google service account credentials_)

* **What it is**: A simple folder where you can upload your Google Sheets directly.
* **What to do**: Put your Google Sheets in our [datasets folder](https://drive.google.com/drive/u/0/folders/1hmSVTstuqNzAdzeBNmoC3XQgpFmNXJt_) on Google Drive. This is simpler and doesn't require any technical setup.

**💡 Recommendation**: If you're not sure which option to choose, use **Option 2** (shared folder). It's easier and works for most use cases.

#### Dataset Requirements

Your dataset must use **standardized column names** so the system can automatically recognize and process your data correctly. The column names must match specific requirements.

**Before using the module**, please make sure your dataset columns match the required names. You can see the dataset example [here](https://docs.google.com/spreadsheets/d/1GwZ6ATEHGdAGMbK63iL-qMDLYOcX7JkG639_49rcsi8/edit?gid=0#gid=0) for the field requirements.

See the [Prepare Your Dataset](https://gdplabs.gitbook.io/sdk/tutorials/evaluation/evaluate-glchat-tutorial#step-2-prepare-your-dataset) section in our GitBook for the complete list of required column names and examples.

### 4. Prepare Attachments (Skip if You Don't Have Any)

If your evaluation includes file attachments (like images, PDFs, or documents), you'll need to upload them first.

#### Storage Options for Attachments

**Option 1: Use Your Own Google Service Account** (for technical users)

* If you already have a Google service account, you can upload attachments to any folder your service account can access.
* In the Colab notebook, fill in the `attachments_google_client_email` and `attachments_google_private_key` fields in the form in the `Dataset & Chatbot Configuration` cell.

**Option 2: Use Our Shared Folder** (recommended for most users)

* Create your own folder in [this Google Drive folder](https://drive.google.com/drive/u/0/folders/1lqVxajjQ3bklY7ITS82fyDDAsuQN6trq)
* Upload all your attachments there
* In the Colab notebook, put the folder ID in the `attachments_gdrive_folder_id` field in the form

**💡 Recommendation**: If you're not sure which option to choose, use **Option 2** (shared folder).

### 5. Fill the Configuration Form

In the Google Colab notebook, you'll find a form section. Fill in the following fields:

#### Required Fields

* **`google_sheets_id`**: The ID of your Google Sheets containing your dataset.
  * **How to find it**: Look at your Google Sheets URL. It looks like: `https://docs.google.com/spreadsheets/d/15oQq2HOM02qP3_ZLm4AStB7fqAhoGlshhkOsOFXCSK8/edit`
  * The ID is the long string between `/d/` and `/edit`
  * Example: `"15oQq2HOM02qP3_ZLm4AStB7fqAhoGlshhkOsOFXCSK8"`
* **`worksheet_name`**: The name of the worksheet tab in your Google Sheets containing your dataset
  * **How to find it**: Look at the bottom of your Google Sheets. You'll see tabs (like "Sheet1", "Sheet2", or a custom name). Use the exact name of the tab you want to evaluate.
  * Example: `"glchat_test_data"` or `"Sheet1"`
* **`user_id`**: Your user ID
  * Example: `"tester_eval1@glair.ai"`

#### Optional Fields

* **`chatbot_id`**: The chatbot ID you want to test. If you leave this empty, it will use `"general-purpose"` by default.
* **`model_name`**: The model name you want to test. If you leave this empty, it will use `"GPT 5 Mini"` by default. You can fill it with the model display name in the specified chatbot you want to test.
* **`attachments_gdrive_folder_id`**: The Google Drive folder ID where your attachments are stored (if you have attachments)
  * **Recommended**: Create your own folder inside the [attachments directory](https://drive.google.com/drive/u/0/folders/1lqVxajjQ3bklY7ITS82fyDDAsuQN6trq), upload your attachments there, and fill in the folder ID in this field.
  * **How to find the folder ID**: Look at your Google Drive folder URL. It looks like: `https://drive.google.com/drive/folders/1sY7a7yZiAfMlM0ozXlEnzb4EbN84sl2N`
  * The folder ID is the long string after `/folders/`
  * **If you leave this empty**: It will use `"1sY7a7yZiAfMlM0ozXlEnzb4EbN84sl2N"` by default, which is the [general folder](https://drive.google.com/drive/u/0/folders/1sY7a7yZiAfMlM0ozXlEnzb4EbN84sl2N). **However, this is not recommended** as it may cause conflicts with other users' attachments if the file name is identical.
* **`attachments_google_client_email`**: Your Google service account client email (only needed if using Option 1 for attachments)
  * Example: `"abc.iam.gserviceaccount.com"`
* **`attachments_google_private_key`**: Your Google service account private key (only needed if using Option 1 for attachments)
  * Example: `"abc123..."`

### 6. How to Run

The notebook is organized into different sections. **Do not use "Run all"** - instead, follow these steps in order:

#### Step 1: Run Setup Cells (Required First)

Before you can use any of the main features, you need to run the setup cells at the beginning of the notebook. These cells handle:

* Authenticating with Google services (Google Drive, Google Cloud)
* Installing the private SDK module
* Loading configuration files

**How to run:**

1. Scroll to the top of the notebook
2. You'll see cells for "Pre-configuration Cells" header.
3. Click on the first cell, then press **Shift + Enter** (or click the "Play" button ▶️ next to the cell)
4. Follow any authentication prompts that appear (see section 2 above for detailed instructions)
5. Continue running each cell one by one (Shift + Enter) until you've completed all the setup cells
6. Wait for each cell to finish before moving to the next one

**💡 Tip**: You'll know you've finished the setup when you see different section headers like "Run Evaluation".

#### Step 2: Choose What You Want to Do

After the setup is complete, you'll see different sections (headers) in the notebook. Each section does something different:

**1. Run Evaluation → Evaluate GLChat with your dataset**

* **What it does**: This runs the main evaluation process. It reads your dataset, sends questions to GLChat, and logs the results to Langfuse.
* **When to use**: Use this when you want to run a new evaluation or test your chatbot.
* **How to run**:
  * Find the "Run Evaluation" header in the notebook
  * Run the cell(s) under this section (click the cell and press Shift + Enter)
  * Wait for the evaluation to complete

**2. Refresh Scores → Update session-level scores in Langfuse**

* **What it does**: After you've manually annotated or updated scores in Langfuse, this section refreshes the session-level scores to reflect your changes.
* **When to use**: Use this after you've made changes to scores in the Langfuse dashboard and want to update the session-level metrics.
* **How to run**:
  * Find the "Refresh Langfuse Session-Level Score" header in the notebook
  * Fill the `run_id` variable there based on the langfuse session id you want to refresh
  * Run the cell(s) under this section

**3. Export Experiment Results → Download results as CSV for analysis**

* **What it does**: Exports your Langfuse experiment tracker data to a CSV file that you can download and analyze (for example, in Google Sheets).
* **When to use**: Use this when you want to do error analysis.
* **How to run**:
  * Find the "Export Langfuse Experiment Results to CSV" header in the notebook
  * Fill the `run_id` variable there based on the langfuse session id you want to export
  * Run the cell(s) under this section
  * The CSV file will be generated and you can download it

**Note:** During execution, you may encounter prompts for authentication (see section 2 above for detailed instructions).

### 7. View Your Results

After running the **"Run Evaluation"** section and the evaluation completes, you can view your results in Langfuse. The notebook will display the **run\_uri** and **leaderboard\_uri** in the output - use these links to access your results directly.

**What is Langfuse?** Langfuse is a web-based dashboard where you can view and analyze your evaluation results. It shows detailed information about how well the chatbot performed.

The evaluation results will show:

* Individual scores for each query
* Overall performance metrics
* Detailed evaluation breakdowns

You can filter and analyze the results using the Langfuse interface. For more information on how to use the dashboard, see the [View Evaluation Results in Langfuse](https://gdplabs.gitbook.io/sdk/tutorials/evaluation/evaluate-glchat-tutorial#step-6-view-evaluation-results-in-langfuse) section in our GitBook.

***

### Key Terms Explained

**Google Colab**: A free online tool that lets you run code in your web browser. You don't need to install anything on your computer.

**Service Account**: A special type of Google account that allows automated access to Google services. Usually only needed for advanced technical setups.

**Colab Secrets**: A secure way to store sensitive information (like passwords or keys) in Google Colab. You can find them in the Colab sidebar under the "Secrets" section.

**gcloud**: Google Cloud Platform's command-line tool. You may need to authenticate with it when running the evaluation.

**Environment Variables**: Configuration settings needed for the evaluation to run properly (like API keys and service URLs). They're stored in an encrypted file (`.env.gpg`) that requires a passphrase to decrypt. You can also override these by adding your own credentials in Colab Secrets.

**Langfuse**: A dashboard tool that displays and analyzes your evaluation results. It's a web-based interface you can access in your browser.

**Worksheet Tab**: The individual sheets within a Google Sheets document. You can see them at the bottom of your Google Sheets as tabs (like "Sheet1", "Sheet2").

***

**Need help?** Contact the team if you encounter any issues or have questions about the evaluation process.
