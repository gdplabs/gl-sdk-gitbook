---
icon: brain-circuit
---

# Fine Tuning

## What is a Fine Tuning ?

Fine tuning is a process that adapts a pre-trained model to perform better on specific tasks or domains by training it on a smaller, specialized dataset.This ensures that the model’s responses are more accurate, relevant, and tailored to particular use cases or requirements. The fine-tuning techniques used in our SDK include:

1. [**Supervised Fine Tuning**](supervised-fine-tuning-sft.md) - training models using labeled input-output pairs to achieve task-specific performance improvements.
2. [**Group Relative Policy Optimization (GRPO)**](group-relative-policy-optimization-grpo.md) - A reinforcement learning-based method that trains models to maximize reward functions across groups of candidate responses. This enables models to learn preference-aligned behaviors directly from reward signals instead of relying on explicit input-output pairs.
3. [**Direct Preference Optimization (DPO)**](direct-preference-optimization-dpo.md) - A stable and efficient alignment method that optimizes models using paired preference data (chosen vs rejected responses). Unlike reinforcement learning approaches that require a separate reward model, DPO directly adjusts the model to increase the likelihood of generating preferred outputs.

## Why we should used our SDK?

Our SDK transforms the complex process of large language model customization into a streamlined, production-ready workflow that helps users fine-tune LLM models efficiently. It eliminates engineering bottlenecks while delivering state-of-the-art training capabilities. The key advantages that make our SDK the preferred choice include:

1. **Unified Training Interface** - Provides a single, consistent API for multiple training methods including Supervised Fine-Tuning (SFT), Group Relative Policy Optimization (GRPO), and Direct Preference Optimization (DPO). This allows seamless switching between techniques without rewriting pipelines.
2. **Collaborative Data Management** - Enables real-time collaboration by supporting both local CSV files and Google Sheets. Data scientists and non-technical team members can update datasets instantly without code changes or deployments.
3. **Simplified Configuration** - Replaces complex, nested configurations with a flat, readable YAML structure and robust validation. This approach reduces setup time, prevents common errors, and makes experiments reproducible and easy to manage.
4. **Real-Time Training Observability** - Multiple monitoring options including structured JSONL logs, TensorBoard integration, and rich console output for immediate visibility into training metrics and resource usage.
