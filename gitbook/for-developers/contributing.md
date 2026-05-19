---
hidden: true
icon: code-merge
---

# Contributing

This page provides the general guidelines for contributing to the Gen AI SDK.

## Requirements

Below are the requirements needed to contribute to the Gen AI SDK.

1.  **Python 3.11+**

    Although not required, it is recommended to use [Miniconda](https://docs.anaconda.com/free/miniconda/index.html) to manage python environments.
2.  **uv 0.5.0+**

    Please refer to the [installation guide](https://docs.astral.sh/uv/getting-started/installation/). After installing, close and re-open the terminal window for the changes to take effect.
3.  **gcloud CLI**

    Please refer to the [installation guide](https://cloud.google.com/sdk/docs/install). After installing, please run `gcloud auth login` to authorize gcloud to access the Cloud Platform with Google user credentials.

## Getting Started

Below are the step-by-step guideline to setup a development environment for a Gen AI SDK module:

{% stepper %}
{% step %}
Go to the module directory by running `cd libs/gllm-<module_name>`. Optionally, the `gllm-<module_name>` module folder can also be opened using an IDE (e.g. Cursor).
{% endstep %}

{% step %}
Configure uv permission to access Google Cloud repositories. These permissions can expire. If you get authorization errors after a while, please simply rerun these commands.

```bash
export UV_INDEX_GEN_AI_INTERNAL_USERNAME=oauth2accesstoken
export UV_INDEX_GEN_AI_INTERNAL_PASSWORD="$(gcloud auth print-access-token)"
export UV_INDEX_GEN_AI_USERNAME=oauth2accesstoken
export UV_INDEX_GEN_AI_PASSWORD="$(gcloud auth print-access-token)"
```
{% endstep %}

{% step %}
Install the module dependencies.

```bash
make install
```
{% endstep %}

{% step %}
Install pre-commit hooks. This will make sure our code is compliant with the style guide before committing.

```
pre-commit install --config ../../.pre-commit-config.yaml
```
{% endstep %}
{% endstepper %}

## Test Files

The test files for each module are located in the `gllm-<module_name>/tests` directory, which further contains 2 subdirectories:

1. `unit_tests`: Contains the unit tests for the module.
2. `integration_tests`: Contains the integration tests for the module.

Any prerequisites and setup required to run the integration tests must be put in the respective module's `README.md` file.

To run the tests, please use:

```bash
make test
```

To see the coverage report, please use:

```bash
uv run coverage report -i -m --skip-empty
```

## Dependencies Management

Below are the conventions for the Gen AI SDK modules dependencies management:

1. Arrangements:
   1. Dependencies must be sorted alphabetically by default.
   2. Dependencies may be grouped if necessary.
   3.  Dependencies should be arranged as follows:

       ```toml
       python = ">=3.11,<3.xx"

       gllm-<package_name> = { version = "^0.x.0", source = "gen-ai-internal" }

       <other_package_name> = "^x.y.z"
       ```
2. To modify the dependencies for the module, either:
   1. Manually update the `pyproject.toml` file, then run `make update`
   2.  Use uv commands:

       1. To add package: `uv add <package_name>`.
       2. To remove package: `uv remove <package_name>`.
       3. To update package: `uv sync --upgrade`.

       After using uv commands, please adjust the package ordering accordingly.
3. After modifying dependencies, please make sure to commit the updated `uv.lock`.
4. Versioning:
   1. For stable packages (major version >= 1), please use `^x.y.z`, e.g. `pandas = "^2.2.3"`.
   2. For unstable packages (major version = 0), please use `>=0.y.z,<0.y+1.z`, e.g. `fastapi = ">=0.115.0,<0.116.0"`.
   3. If necessary, package can be locked strictly to a specific version, e.g. `transformers = "4.46.1"`. However, please be careful as this may cause version conflict between modules.

## Code Convention

Below are the code convention for the Gen AI SDK:

1. For general code convention, please refer to the [Python Style Guide](https://docs.google.com/document/d/1uRggCrHnVfDPBnG641FyQBwUwLoFw0kTzNqRm92vUwM/edit?usp=sharing).
2. Modules are located in the `libs` directory. Each module has its own directory with the following structure:
   1. `<snake_case_module_name>`: contains the source code for the module.
   2. `tests`: contains the tests for the module.
   3. `pyproject.toml`: contains the configuration for the module.
   4. `uv.lock`: contains the dependencies for the module.
   5. `README.md`: contains the documentation for the module.
3. For logging, please use our [logger manager](https://github.com/GDP-ADMIN/gl-sdk/blob/main/libs/gllm-core/gllm_core/utils/logger_manager.py):
   1.  For function logging, define the logger outside of the function:

       ```python
       logger = LoggerManager().get_logger()

       def my_function():
           logger.info("This is an info")
           logger.warning("This is a warning")
           logger.error("This is an error")
       ```
   2.  For class logging, please set the logger as a protected attribute:

       ```python
       class MyClass:
           def __init__():
               self._logger = LoggerManager().get_logger()

           def method():
               self._logger.info("This is an info")
               self._logger.warning("This is a warning")
               self._logger.error("This is an error")
       ```
4. For deprecation, please use our [deprecated decorator](https://github.com/GDP-ADMIN/gl-sdk/blob/main/libs/gllm-core/gllm_core/utils/imports.py#L63).
   1.  To deprecate a function, simply add the decorator:

       ```python
       @deprecated(deprecated_in="0.1.20", removed_in="0.2.0")
       def deprecated_function():
           pass
       ```
   2.  To deprecate a class, add the decorator to the constructor:

       ```python
       class DeprecatedClass:
           @deprecated(deprecated_in="0.1.20", removed_in="0.2.0")
           def __init__():
               pass
       ```
5. For optional packages, please use our [check optional packages](https://github.com/GDP-ADMIN/gl-sdk/blob/main/libs/gllm-core/gllm_core/utils/imports.py#L16) util as follows:
   1.  To use an optional package in a function, put the checker and import in the function:

       ```python
       def my_function():
           check_optional_packages("package", extras="extra")
           from package import Module
           return Module(...)
       ```
   2.  To use an optional package in a class, put the checker and import in the class constructor:

       ```python
       class MyClass:
           def __init__():
               check_optional_packages("package", extras="extra")
               from package import Module
               self.module = Module(...)
       ```

## AI Feedback

To enhance tracking of AI usage, facilitate early issue identification, and continuously refine our development process, all future Pull Requests (PRs) are required to contain structured AI Feedback comments from both the author and the reviewer.

### Overview

The AI Feedback system tracks:

1. **Author Feedback** - Which AI suggestions were True Positives (TP) or False Positives (FP), including impact levels and models/prompts used
2. **Reviewers Feedback** - Which AI models were used for review and any issues caught by reviewers that AI missed
3. **Review Responsiveness** - Time from PR open until first START REVIEW
4. **Active Review Window** - Duration of human review from first START REVIEW to merge
5. **End-to-End PR Cycle Time** - Total time from PR open to merge

For detailed guidelines, examples, and complete documentation, please refer to the [AI Feedback Guide](https://docs.google.com/document/d/1U5xAoXjV9d0cuoky8g0y2WYH8dSZiir6GoIg-5Lv0Bg/edit?tab=t.0).

## Contributing General Flow

The general steps for contributing to the Gen AI SDK are as follows:<br>

{% stepper %}
{% step %}
Create a new branch from `main`.
{% endstep %}

{% step %}
Work on the branch to apply the changes.
{% endstep %}

{% step %}
Commit the changes. If any dependency are modified, please dont forget to also commit the `uv.lock` file.
{% endstep %}

{% step %}
Push the changes.
{% endstep %}

{% step %}
Create a PR. The PR description should contain the following:

1. **Description**: Brief description on what the PR is about.
2. **Changes**: Bulleted list of specific modifications and their purpose.
3. **How to Test**: Provide a brief guidelines for the reviewers to verify the changes.
{% endstep %}

{% step %}
Request for reviews:

1. At least 2 approval are required in order to merge the PR, 1 on which should be from the Gen AI SDK team. Please communicate with the Gen AI SDK team whenever help is needed for PR reviews.

{% endstep %}

{% step %}
Merge the PR. Please always use `Squash and Merge`.
{% endstep %}

{% step %}
Add AI Feedback comments. To enhance tracking of AI usage, facilitate early issue identification, and continuously refine our development process, all PRs are required to contain structured AI Feedback comments from both the author and the reviewer.

**For Author (1 comment per PR):**
- Add a comment **after merging the PR** documenting which AI suggestions were True Positives (TP) or False Positives (FP)
- Include impact level (High, Medium, Low) for each suggestion
- Document the AI models and prompts used during development
- Use this for lessons learned and improvement suggestions
{% endstep %}

{% step %}
Create a release for the merged changes:

1. Go to the [Draft a new release](https://github.com/GDP-ADMIN/gl-sdk/releases/new) page.
2. Click on `Choose a Tag`.
3. The tag name should follow the following convention:
   1. Format: `gllm_<package_name>-v<major>.<minor>.<patch>`.
   2. The version should be updated as follows:
      1. If your changes contain breaking changes, please bump the minor version.
      2. Otherwise, please bump the patch version.
   3. For example, say you've just made changes to the [GLLM Core](https://github.com/GDP-ADMIN/gl-sdk/tree/main/libs/gllm-core) module, and its current latest tag is `gllm_core-v0.2.5` (The latest tag should be visible when you start typing the tag name):
      1. If your changes contain breaking changes, please create `gllm_core-v0.3.0`.
      2. Otherwise, please create `gllm_core-v0.2.6`.
4. Click on `Generate release note` and adjust the message accordingly.
5. Click on `Publish release` to create the release.
{% endstep %}

{% step %}
Verifying build:

1. After creating the release, go to the [Build binary](https://github.com/GDP-ADMIN/gl-sdk/actions/workflows/build-binary.yml) page.
2. Find the recent release's build.
3. Please make sure that all jobs are executed successfully, which means the changes are ready to be used.

{% hint style="danger" %}
If there are any failing builds, please consult to the Gen AI SDK team or the DSO team, as unattended failing builds may result in versioning problem in the future due to missing build.
{% endhint %}
{% endstep %}
{% endstepper %}

## Creating New Package

{% hint style="warning" %}
Coming soon!
{% endhint %}

## Github Issues

For feature request or bug report, feel free to [open a Github issue](https://github.com/GDP-ADMIN/gl-sdk/issues).

## Static Code Analysis

When creating a Pull Request and a commit is pushed to GitHub, it will trigger an SCA job.

1. To request access to the SCA report, please fill out [this ticket form](https://infragdplabs.ladesk.com/submit_ticket) by including the project keys of each modules.
2. You can check the project key in `./sonar-project.properties` of each module (example: [gllm-core](https://github.com/GDP-ADMIN/gl-sdk/blob/main/libs/gllm-core/sonar-project.properties#L1)).<br>
