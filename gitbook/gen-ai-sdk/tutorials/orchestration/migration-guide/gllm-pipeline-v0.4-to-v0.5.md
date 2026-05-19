# GLLM Pipeline v0.4 to v0.5

Several legacy parameters and classes in GLLM Pipeline v0.4 have been deprecated. Backward compatibility will be **removed** in the upcoming version `v0.5.0`. Please review this migration guide to ensure a smooth transition.

{% hint style="info" %}
Note: If you've set the GLLM Pipeline dependency in your app as `>=0.4.0, <0.5.0`, you don't have to do this migration immediately, as you're locked to `v0.4.x`. You will only migrate to `0.5.0` when you choose to do so by updating your dependency to `>=0.5.0`.

However, it's still recommended to do so ASAP to be able to access new features that will be added in the future.
{% endhint %}

## Step Functions

### Deprecated Parameters Removed

The following deprecated parameters have been removed from step functions (`step()`, `conditional()`, `toggle()`, `subgraph()`):

| Removed Parameter    | Replacement              |
| -------------------- | ------------------------ |
| `input_state_map`    | `input_map`              |
| `runtime_config_map` | `input_map`              |
| `fixed_args`         | `input_map` with `Val()` |

#### **Before (v0.4):**

```python
from gllm_pipeline import step, conditional, toggle, subgraph

# Using legacy parameters
my_step = step(
    MyComponent(),
    input_state_map={"query": "user_input"},
    runtime_config_map={"model": "model_config"},
    fixed_args={"temperature": 0.7},
    output_state="result",
)

toggle_step = toggle(
    condition,
    feature_step,
    input_state_map={"value": "input"},
    runtime_config_map={"threshold": "threshold_config"},
    fixed_args={"strict_mode": True},
    output_state="feature_status",
)
```

#### **After (v0.5):**

```python
from gllm_pipeline import step, conditional, toggle, subgraph
from gllm_pipeline.types import Val

# Using unified input_map
my_step = step(
    MyComponent(),
    input_map={
        "query": "user_input",           # Maps from pipeline state
        "model": "model_config",          # Maps from runtime config
        "temperature": Val(0.7),          # Fixed value
    },
    output_state="result",
)

toggle_step = toggle(
    condition,
    feature_step,
    input_map={
        "value": "input",
        "threshold": "threshold_config",
        "strict_mode": Val(True),
    },
    output_state="feature_status",
)
```

## Caching Configuration

#### `cache_store` and `cache_config` Replaced with `cache`

The separate `cache_store` and `cache_config` parameters have been consolidated into a single `cache` parameter using `CacheConfig`.

#### **Before (v0.4):**

```python
from gllm_cache import RedisCache

my_step = step(
    MyComponent(),
    input_map={"query": "input"},
    output_state="result",
    cache_store=RedisCache(...),
    cache_config={"ttl": 3600},
)
```

#### **After (v0.5):**

```python
from gllm_cache import RedisCache
from gllm_pipeline.types import CacheConfig

my_step = step(
    MyComponent(),
    input_map={"query": "input"},
    output_state="result",
    cache=CacheConfig(store=RedisCache(...), ttl=3600),
)
```

This applies to all step functions and pipeline builder methods:

* `step()`
* `conditional()`
* `toggle()`
* `subgraph()`
* `parallel()`
* Pipeline builder's `when()`, `switch()`, `parallel()`

## Pipeline Invocation

#### `context` Parameter Added

A new `context` parameter has been added to `Pipeline.invoke()` for passing runtime context separately from configuration flags.

#### **Before (v0.4):**

```python
# Runtime context was passed via config
result = await pipeline.invoke(
    initial_state,
    config={
        "debug_state": True,
        "user_id": "123",        # Runtime context mixed with config
        "session_data": {...},   # Runtime context mixed with config
    },
)
```

#### **After (v0.5):**

```python
# Separate config flags from runtime context
result = await pipeline.invoke(
    initial_state,
    config={"debug_state": True},  # Config flags only
    context={
        "user_id": "123",
        "session_data": {...},
    },
)
```

{% hint style="warning" %}
Passing runtime context via `config` still works in v0.5 but will emit a deprecation warning. Please migrate to using the `context` parameter.
{% endhint %}

## Router

### Optional Dependencies

Some of the dependencies have been made optional to allow user opt out installing dependencies for unused modules. Below is the list of extra package to use alongside with the corresponding modules.

<table><thead><tr><th>Extra Package Name</th><th width="255.888916015625">Required by</th><th width="352.333251953125">Module Location</th></tr></thead><tbody><tr><td><code>inference</code></td><td><code>EMInvokerEncoder</code></td><td><code>gllm_pipeline.router.backend.aurelio.encoders.em_invoker_encoder</code></td></tr><tr><td><code>aurelio</code></td><td><code>LangchainEmbeddingsEncoder</code></td><td><code>gllm_pipeline.router.backend.aurelio.encoders.langchain_encoder</code></td></tr><tr><td><code>aurelio</code></td><td><code>TEIEncoder</code></td><td><code>gllm_pipeline.router.backend.aurelio.encoders.tei_encoder</code></td></tr><tr><td><code>aurelio-azure</code></td><td><code>AzureAISearchAurelioIndex</code></td><td><code>gllm_pipeline.router.backend.aurelio.index.azure_ai_search_aurelio_index</code></td></tr><tr><td><code>aurelio-datastore</code></td><td><code>DataStoreAdapterIndex</code></td><td><code>gllm_pipeline.router.backend.aurelio.index.data_store_adapter_index</code></td></tr><tr><td><code>aurelio</code></td><td><code>BaseAurelioIndex</code></td><td><code>gllm_pipeline.router.backend.aurelio.index.aurelio_index</code></td></tr><tr><td><code>inference</code></td><td><code>LMBasedRouter</code></td><td><code>gllm_pipeline.router.lm_based_router</code></td></tr></tbody></table>

### Backend Adapter Pattern

{% hint style="success" %}
**This is NOT a breaking change.** The backend adapter pattern is a new architectural pattern introduced in v0.5. Existing code continues to work without modifications.
{% endhint %}

The backend adapter pattern provides a **pluggable architecture** for router backends. All adapters implement the `BaseAdapter` interface with an `async route()` method.

#### Semantic Router: Aurelio Backend

**Before (v0.4):**

```python
from gllm_pipeline.router.aurelio_semantic_router import AurelioSemanticRouter
from gllm_inference.builder import build_em_invoker
from gllm_pipeline.router.backend.aurelio.encoders.em_invoker_encoder import EMInvokerEncoder

em_invoker = build_em_invoker("openai/text-embedding-3-small", credentials="sk-...")
encoder = EMInvokerEncoder(em_invoker)
router = AurelioSemanticRouter(
    default_route="general",
    valid_routes={"greeting", "help", "general"},
    encoder=encoder,
    route_examples={
        "greeting": ["hi", "hello", "hey"],
        "help": ["help me", "assist", "support"],
    }
)
route = await router.route("hello there")  # Returns "greeting"
```

**After (v0.5):**

```python
from gllm_pipeline.router import SemanticRouter
from gllm_inference.builder import build_em_invoker

em_invoker = build_em_invoker("openai/text-embedding-3-small", credentials="sk-...")
router = SemanticRouter.aurelio(
    default_route="general",
    valid_routes={"greeting", "help", "general"},
    encoder=em_invoker,
    route_examples={
        "greeting": ["hi", "hello", "hey"],
        "help": ["help me", "assist", "support"],
    }
)
route = await router.route("hello there")  # Returns "greeting"
```

#### Semantic Router: Native Backend

**Before (v0.4):**

<pre class="language-python"><code class="lang-python">from gllm_pipeline.router import SimilarityBasedRouter
from gllm_inference.builder import build_em_invoker

em_invoker = build_em_invoker("openai/text-embedding-3-small", credentials="sk-...")
<strong>router = SimilarityBasedRouter(
</strong>    default_route="general",
    valid_routes={"greeting", "help", "general"},
    em_invoker=em_invoker,
    route_examples={
        "greeting": ["hi", "hello", "hey"],
        "help": ["help me", "assist", "support"],
    },
    similarity_threshold=0.7
)
route = await router.route("hello there")  # Returns "greeting"
</code></pre>

**After (v0.5):**

```python
from gllm_pipeline.router import SemanticRouter
from gllm_inference.builder import build_em_invoker

em_invoker = build_em_invoker("openai/text-embedding-3-small", credentials="sk-...")
router = SemanticRouter.native(
    default_route="general",
    valid_routes={"greeting", "help", "general"},
    em_invoker=em_invoker,
    route_examples={
        "greeting": ["hi", "hello", "hey"],
        "help": ["help me", "assist", "support"],
    },
    similarity_threshold=0.7
)
route = await router.route("hello there")  # Returns "greeting"
```



#### LM Based Router: Native Backend

**Before (v0.4):**

```python
from gllm_pipeline.router import LMBasedRouter
from gllm_inference.request_processor import LMRequestProcessor
from gllm_inference.prompt_builder import PromptBuilder
from gllm_inference.builder import build_lm_invoker

lm_invoker = build_lm_invoker("openai/gpt-4o-mini", credentials="sk-...")
prompt_builder = PromptBuilder(
    system_template="Classify into: greeting, help, or general",
    user_template="{input}"
)
processor = LMRequestProcessor(lm_invoker=lm_invoker, prompt_builder=prompt_builder)
router = LMBasedRouter(
    lm_request_processor=processor,
    default_route="general",
    valid_routes={"greeting", "help", "general"}
)
route = await router.route("hello there")  # Returns route from LM
```

**After (v0.5):**

<pre class="language-python"><code class="lang-python">from gllm_pipeline.router import LMBasedRouter
from gllm_inference.request_processor import LMRequestProcessor
from gllm_inference.prompt_builder import PromptBuilder
from gllm_inference.builder import build_lm_invoker

lm_invoker = build_lm_invoker("openai/gpt-4o-mini", credentials="sk-...")
prompt_builder = <a data-footnote-ref href="#user-content-fn-1">PromptBuilder</a>(
    system_template="Classify into: greeting, help, or general",
    user_template="{input}"
)
processor = LMRequestProcessor(lm_invoker=lm_invoker, prompt_builder=prompt_builder)
router = <a data-footnote-ref href="#user-content-fn-2">LMBasedRouter.native</a>(
    lm_request_processor=processor,
    default_route="general",
    valid_routes={"greeting", "help", "general"}
)
route = await router.route("hello there")  # Returns route from LM
</code></pre>

## Type Hints

Enhanced type hints have been added across pipeline components. While this doesn't require code changes, you may see new type checking warnings if your IDE or type checker is strict. Review and update your type annotations as needed.

[^1]: 

[^2]: changed line
