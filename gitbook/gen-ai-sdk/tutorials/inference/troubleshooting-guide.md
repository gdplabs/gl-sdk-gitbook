---
icon: triangle-exclamation
---

# Troubleshooting Guide

This guide explains common errors you may encounter when using the gllm-inference library and how to resolve them.

## Error Reference

### ProviderInvalidArgsError

**What it means:** You've provided invalid model parameters, malformed requests, or incorrect structure to the model provider.

**Common causes:**

* Invalid parameter types or values
* Malformed request structure
* Missing required parameters
* Incorrect schema format for structured outputs

**How to fix:**

1. Check the API reference for your specific invoker to verify parameter names and types
2. Validate your request structure matches the expected format
3. Ensure all required parameters are provided
4. For structured outputs, verify your Pydantic model or JSON schema is valid

***

### ContextOverflowError

**What it means:** Your input size exceeds the model's maximum context length limit.

**Common causes:**

* Input text is too long for the model
* Including too many messages in conversation history
* Large attachments (documents, images) that consume tokens
* Insufficient token budget for both input and output

**How to fix:**

1. Reduce the input size by summarizing or truncating content
2. Limit conversation history to recent messages only
3. Break large documents into smaller chunks
4. Check the model's context window size in the supported models documentation
5. Consider using a model with a larger context window

***

### ProviderAuthError

**What it means:** Authorization failed due to API key issues. Your credentials are invalid, missing, or don't have the required permissions.

**Common causes:**

* Invalid or expired API key
* API key not set in environment variables
* API key belongs to wrong organization or account
* Insufficient permissions for the requested operation
* Typo in API key

**How to fix:**

1. Verify your API key is correct and not expired
2. Check that the API key is set in the correct environment variable:
   * OpenAI: `OPENAI_API_KEY`
   * Anthropic: `ANTHROPIC_API_KEY`
   * Google: `GOOGLE_API_KEY`
   * Azure OpenAI: `AZURE_OPENAI_API_KEY`
3. Ensure the API key has the required permissions
4. For organization-specific keys, verify the organization is correct
5. Regenerate the API key if you suspect it's compromised

***

### ProviderRateLimitError

**What it means:** You've exceeded the rate limit for API requests. The model provider is throttling your requests due to too many calls in a short time.

**Common causes:**

* Too many requests sent in a short time window
* Batch processing without proper delays
* Concurrent requests exceeding provider limits
* Free tier account with lower rate limits

**How to fix:**

1. Implement exponential backoff
2. Add delays between requests
3. Use batch invocation for bulk processing (cheaper and respects rate limits)
4. Upgrade to a higher tier account if on free tier
5. Distribute requests over a longer time period

***

### ProviderInternalError

**What it means:** An unexpected server-side error occurred at the model provider. This is not caused by your code.

**Common causes:**

* Temporary service outage at the provider
* Server-side bug or issue
* Provider maintenance or deployment
* Overloaded provider infrastructure

**How to fix:**

1. Wait a few moments and retry (the SDK automatically retries with `RetryConfig`)
2. Check the provider's status page for known issues
3. If the error persists, contact the provider's support
4. Increase retry attempts and timeout values

***

### ProviderOverloadedError

**What it means:** The model provider's engine is currently overloaded and cannot process your request.

**Common causes:**

* Provider experiencing high traffic
* Too many concurrent requests
* Provider maintenance or scaling issues
* Sudden spike in usage

**How to fix:**

1. Wait and retry later (automatic with `RetryConfig`)
2. Reduce concurrent request volume
3. Use batch invocation to spread requests over time
4. Check provider status page for ongoing issues
5. Consider using an alternative model or provider temporarily

***

### ModelNotFoundError

**What it means:** The specified model could not be found. The model ID is invalid or the model is not available.

**Common causes:**

* Typo in model ID
* Model has been deprecated or removed
* Model is not available in your region or account
* Model name changed in a new version

**How to fix:**

1. Check the supported models documentation for correct model IDs
2. Verify the model is available for your account
3. Check for model deprecation notices
4. Use the correct model enum from the library (e.g., `OpenAILM.GPT_5_NANO`)

***

### APIConnectionError

**What it means:** The client failed to connect to the model provider. This is typically a network issue.

**Common causes:**

* Network connectivity problems
* Provider service is down or unreachable
* Firewall or proxy blocking the connection
* DNS resolution issues
* Provider endpoint is incorrect

**How to fix:**

1. Check your internet connection
2. Verify the provider's service status
3. Check firewall/proxy settings
4. Try using a VPN if the provider is geographically blocked
5. Verify the correct endpoint URL is being used
6. Retry with `RetryConfig` to handle transient network issues

***

### APITimeoutError

**What it means:** The request to the model provider timed out. The provider took too long to respond.

**Common causes:**

* Provider is slow to respond
* Network latency is high
* Request is complex and takes long to process
* Timeout value is too short
* Provider is overloaded

**How to fix:**

1. Increase the timeout value in `RetryConfig`
2. Retry the request (automatic with `RetryConfig`)
3. Check if the request is too complex
4. Verify network connectivity
5. Check provider status for performance issues

***

### ProviderConflictError

**What it means:** The request could not be completed due to a conflict with the current state of the resource.

**Common causes:**

* Resource already exists
* Resource state changed during operation
* Concurrent modification of the same resource
* Invalid state transition

**How to fix:**

1. Check the current state of the resource
2. Verify the operation is valid for the current state
3. Retry the operation
4. Ensure only one process modifies the resource at a time

***

### InvokerRuntimeError

**What it means:** An error occurred during the invocation of the model. This is a general runtime error.

**Common causes:**

* Unexpected error in the invoker code
* Invalid state during invocation
* Resource exhaustion
* Incompatible configuration

**How to fix:**

1. Check the debug info in the error message for details
2. Verify your configuration is valid
3. Check available system resources
4. Review the error's `debug_info` attribute for more context
5. Enable verbose logging for more details

***

### FileOperationError

**What it means:** A file operation failed during model invocation.

**Common causes:**

* File not found or inaccessible
* Insufficient permissions to read/write file
* Disk space issues
* File is corrupted
* Invalid file path

**How to fix:**

1. Verify the file path is correct and the file exists
2. Check file permissions
3. Ensure sufficient disk space
4. Verify the file is not corrupted
5. Check that the file format is supported

***

## Getting Help

If you encounter an error:

1. **Check the error message and debug info** - The error message usually contains useful details
2. **Enable verbose logging** - Use the error's `verbose()` method to get detailed information
3. **Review the API Reference** - Check the [API documentation](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_inference/api/index.html)
4. **Check the provider's documentation** - Some errors are provider-specific
5. **Contact support** - Reach out to the development team if you need further assistance
