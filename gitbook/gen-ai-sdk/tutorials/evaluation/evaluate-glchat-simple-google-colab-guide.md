---
hidden: true
---

# 📑 Evaluate GLChat - Simple Google Colab Guide

### What is This?

This guide helps you test how well **GLChat** answers questions. You'll provide test questions and see how accurately your selected chatbot responds. The evaluation runs automatically in **Google Colab** (a free online tool that works in your web browser) and shows you detailed results about the chatbot's performance. This guide is simpler because there is **no customization needed**, we will use all the default settings.

**What you'll accomplish:**

* Test the chatbot with your own questions and scenarios
* Get scores showing how well the chatbot performs
* View detailed analysis of each answer in a dashboard

***

### 1. Before You Start

Make sure you have:

* Access to Google Account (@gdplabs.id)
* Access to the [shared drive folder](https://drive.google.com/drive/u/0/folders/1per1tZBH9DDQ_0jfsIwNgFbEL5fp-JAi)

#### Check Langfuse Service

Before running the evaluation, check that you can open the Langfuse dashboard at https://langfuse.obrol.id/

* If you see a "503 Service Temporarily Unavailable" error, the service needs to be turned on
* **Contact the evals team** to turn on the service for you
* **Note:** The service automatically turns off at 23:59 WIB. If you need to run tests after that time, contact the evals team to turn it on again

***

### 2. Prepare Your Dataset

You need to create a Google Sheets document with your test questions and information.

#### Step 1: Create Your Google Sheets

1. Create a new Google Sheets document
2. Add your test data following the required format (see below)
3. Upload your Google Sheets to our [datasets folder](https://drive.google.com/drive/u/0/folders/1hmSVTstuqNzAdzeBNmoC3XQgpFmNXJt_) on Google Drive

#### Step 2: Dataset Requirements

Your Google Sheets must use specific column names so the system can read your data correctly.

**Important:** See the [Prepare Your Dataset](https://gdplabs.gitbook.io/sdk/tutorials/evaluation/evaluate-glchat-tutorial#step-2-prepare-your-dataset) section in our GitBook for the complete list of required column names and examples.

***

### 3. Prepare Attachments (Skip if You Don't Have Any)

If your evaluation includes file attachments (like images, PDFs, or documents):

1. Create your own folder in [this Google Drive folder](https://drive.google.com/drive/u/0/folders/1lqVxajjQ3bklY7ITS82fyDDAsuQN6trq)
2. Upload all your attachments to that folder
3. You'll need the folder ID later (see step 4 below)

***

### 4. Fill the Configuration Form

In the Google Colab notebook, you'll find a form section. Fill in these fields:

#### Required Fields

* **`google_sheets_id`**: The ID of your Google Sheets document
  * **How to find it**: Look at your Google Sheets URL in your browser's address bar
  * It looks like: `https://docs.google.com/spreadsheets/d/15oQq2HOM02qP3_ZLm4AStB7fqAhoGlshhkOsOFXCSK8/edit`
  * Copy the long string between `/d/` and `/edit`
  * Example: `15oQq2HOM02qP3_ZLm4AStB7fqAhoGlshhkOsOFXCSK8`
* **`worksheet_name`**: The name of the worksheet tab in your Google Sheets
  * **How to find it**: Look at the bottom of your Google Sheets. You'll see tabs (like "Sheet1", "Sheet2", or a custom name)
  * Copy the exact name of the tab you want to evaluate
  * Example: `glchat_test_data` or `Sheet1`
* **`user_id`**: Your user ID
  * Example: `tester_eval1@glair.ai`

#### Optional Fields (You Can Leave These Empty)

* **`chatbot_id`**: The chatbot ID you want to test
  * If you leave this empty, it will use `general-purpose` automatically
* **`model_name`**: The model name you want to test
  * If you leave this empty, it will use `GPT 5 Mini` automatically
* **`attachments_gdrive_folder_id`**: The Google Drive folder ID where your attachments are stored (only if you have attachments)
  * **How to find it**: Look at your Google Drive folder URL
  * It looks like: `https://drive.google.com/drive/folders/1sY7a7yZiAfMlM0ozXlEnzb4EbN84sl2N`
  * Copy the long string after `/folders/`
  * If you leave this empty and have attachments in the [general folder](https://drive.google.com/drive/u/0/folders/1sY7a7yZiAfMlM0ozXlEnzb4EbN84sl2N), it will use that folder automatically

***

### 5. Run the Evaluation

1. In the Google Colab notebook, click **"Runtime"** in the top menu bar
2. Select **"Run all"** from the dropdown menu
3. Wait for the evaluation to complete (this may take several minutes)

The notebook will run everything automatically from top to bottom.

#### What to Expect During Execution

You may be asked to do the following:

**a. Google Drive Access**

* You may be asked to allow access to your Google Drive
* Click the URL that appears, sign in with your Google account (@gdplabs.id), and follow the steps

**b. Google Cloud Login**

* You may see a URL asking you to sign in
* Click the URL, sign in with your Google account (@gdplabs.id)
* After signing in, copy the URL from your browser and paste it back into the notebook where prompted
* Press Enter to continue

**c. Passphrase (Password)**

* You will be asked for a passphrase (password) to unlock the configuration
* Enter the passphrase when prompted
* **If you don't know the passphrase, ask the evals team**

**Note:** Just follow the prompts and do what they ask. The system will guide you through each step.

***

### 6. View Your Results

After the evaluation completes, you can view your results at:

**Langfuse Dashboard** - https://langfuse.obrol.id/

**What is Langfuse?** Langfuse is a web-based dashboard (like a website) where you can see and analyze your evaluation results. It shows you detailed information about how well the chatbot performed.

Your results will show:

* Individual scores for each question
* Overall performance metrics
* Detailed breakdowns of each answer

You can filter and explore the results using the Langfuse website. For more information on how to use the dashboard, see the [View Evaluation Results in Langfuse](https://gdplabs.gitbook.io/sdk/tutorials/evaluation/evaluate-glchat-tutorial#step-6-view-evaluation-results-in-langfuse) section in our GitBook.

### Important Notes

**Default Settings:**

* Your results will be saved to the `glchat_beta` project in Langfuse
* The system uses the evals team's settings for Google Sheets and GLChat
* You don't need to change any of these settings - they're already configured

***

### Quick Reference

**What is Google Colab?** A free online tool that lets you run code in your web browser. You don't need to install anything on your computer - just open it in your browser.

**What is a Worksheet Tab?** The individual sheets within a Google Sheets document. You can see them at the bottom of your Google Sheets as tabs (like "Sheet1", "Sheet2").

**What is Langfuse?** A dashboard tool (website) that shows your evaluation results. You can access it in your web browser.

***

**Need help?** Contact the evals team if you encounter any issues or have questions about the evaluation process.
