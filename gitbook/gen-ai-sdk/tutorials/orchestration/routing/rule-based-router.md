---
icon: list-check
---

# Rule-Based Router

[**`gllm-pipeline`**](https://github.com/GDP-ADMIN/gl-sdk/tree/main/libs/gllm-pipeline/gllm_pipeline/router) | **Tutorial**: [rule-based-router.md](rule-based-router.md "mention") | [API Reference](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_pipeline/api/router.html)

The **Rule-Based Router** routes queries based on keyword matching and pattern rules. It's ideal for deterministic routing logic where you want explicit control over routing decisions.

<details>

<summary>Prerequisites</summary>

This tutorial does not require external dependencies. It uses only the core routing framework.

</details>

## Installation

```bash
pip install gllm-pipeline
```

## Basic Usage

### Step 1: Define routing rules

```python
import asyncio
from gllm_pipeline.router import RuleBasedRouter
from gllm_pipeline.router.rule_based_router import RouterRule, RouterRuleset

# Define rules for each route
billing_rules = RouterRuleset(
    rules=[
        RouterRule(
            keywords=["payment", "invoice", "billing", "charge", "refund"],
            allow_substring=True,
            case_sensitive=False,
        ),
    ],
    match_all=False,  # Match any rule
)

tech_support_rules = RouterRuleset(
    rules=[
        RouterRule(
            keywords=["crash", "error", "bug", "broken", "not working"],
            allow_substring=True,
            case_sensitive=False,
        ),
    ],
    match_all=False,
)

faq_rules = RouterRuleset(
    rules=[
        RouterRule(
            keywords=["hours", "location", "contact", "help", "guide"],
            allow_substring=True,
            case_sensitive=False,
        ),
    ],
    match_all=False,
)

# Map routes to rulesets
ruleset_map = {
    "billing": billing_rules,
    "tech_support": tech_support_rules,
    "faq": faq_rules,
}
```

### Step 2: Create the router

```python
router = RuleBasedRouter(
    ruleset_map=ruleset_map,
    default_route="faq",
    valid_routes={"billing", "tech_support", "faq"},
)
```

### Step 3: Route queries

```python
# Route a single query
query = "My credit card was charged twice"
route = asyncio.run(router.route(query))
print(f"Selected route: {route}")  # Output: "billing"

# Route with filtering
route = asyncio.run(
    router.route(query, route_filter={"billing", "faq"})
)
```

## Advanced Rule Configuration

### Exact Keyword Matching

Match complete words only:

```python
exact_match_rule = RouterRule(
    keywords=["error", "bug", "crash"],
    allow_substring=False,  # Exact match only
    case_sensitive=False,
)
```

### Case-Sensitive Matching

```python
case_sensitive_rule = RouterRule(
    keywords=["API", "SDK", "HTTP"],
    allow_substring=True,
    case_sensitive=True,  # Case matters
)
```

### Input Splitting

Split input before matching:

```python
from gllm_pipeline.router.rule_based_router import RouterSplitRule

# Split by space and match first word
split_rule = RouterSplitRule(
    splitter=[" "],
    beg_index=0,
    end_index=1,
)

command_rule = RouterRule(
    keywords=["help", "support", "info"],
    allow_substring=False,
    case_sensitive=False,
    split_rule=[split_rule],
)
```

### Multiple Rules (AND/OR Logic)

```python
# All rules must match (AND logic)
strict_ruleset = RouterRuleset(
    rules=[
        RouterRule(
            keywords=["payment", "card"],
            allow_substring=True,
            case_sensitive=False,
        ),
        RouterRule(
            keywords=["failed", "declined", "error"],
            allow_substring=True,
            case_sensitive=False,
        ),
    ],
    match_all=True,  # All rules must match
)

# Any rule can match (OR logic)
loose_ruleset = RouterRuleset(
    rules=[
        RouterRule(
            keywords=["payment", "invoice", "billing"],
            allow_substring=True,
            case_sensitive=False,
        ),
        RouterRule(
            keywords=["refund", "credit"],
            allow_substring=True,
            case_sensitive=False,
        ),
    ],
    match_all=False,  # Any rule can match
)
```

## Complete Example

```python
import asyncio
from gllm_pipeline.router import RuleBasedRouter
from gllm_pipeline.router.rule_based_router import RouterRule, RouterRuleset

async def main():
    # Define comprehensive rulesets
    billing_rules = RouterRuleset(
        rules=[
            RouterRule(
                keywords=["payment", "invoice", "billing", "charge", "refund", "card", "subscription"],
                allow_substring=True,
                case_sensitive=False,
            ),
        ],
        match_all=False,
    )

    tech_support_rules = RouterRuleset(
        rules=[
            RouterRule(
                keywords=["crash", "error", "bug", "broken", "not working", "fail", "issue"],
                allow_substring=True,
                case_sensitive=False,
            ),
        ],
        match_all=False,
    )

    sales_rules = RouterRuleset(
        rules=[
            RouterRule(
                keywords=["pricing", "plan", "feature", "enterprise", "upgrade"],
                allow_substring=True,
                case_sensitive=False,
            ),
        ],
        match_all=False,
    )

    faq_rules = RouterRuleset(
        rules=[
            RouterRule(
                keywords=["hours", "location", "contact", "help", "guide", "how"],
                allow_substring=True,
                case_sensitive=False,
            ),
        ],
        match_all=False,
    )

    # Create router
    router = RuleBasedRouter(
        ruleset_map={
            "billing": billing_rules,
            "tech_support": tech_support_rules,
            "sales": sales_rules,
            "faq": faq_rules,
        },
        default_route="faq",
        valid_routes={"billing", "tech_support", "sales", "faq"},
    )

    # Test queries
    test_cases = [
        "My credit card was charged twice",
        "The app keeps crashing on startup",
        "What are your enterprise pricing options?",
        "What are your business hours?",
        "I don't understand something",
    ]

    for query in test_cases:
        route = await router.route(query)
        print(f"Query: {query}")
        print(f"Route: {route}\n")

asyncio.run(main())
```

## Configuration Options

### Alphanumeric Filtering

Only consider alphanumeric characters:

```python
rule = RouterRule(
    keywords=["error", "fail"],
    allow_substring=True,
    case_sensitive=False,
    alphanumeric_only=True,  # Ignore punctuation
)
```

### Complex Splitting Patterns

```python
from gllm_pipeline.router.rule_based_router import RouterSplitRule

# Split by multiple delimiters
multi_split_rule = [
    RouterSplitRule(splitter=[" "], beg_index=0, end_index=2),
    RouterSplitRule(splitter=["-"], beg_index=0, end_index=1),
]

rule = RouterRule(
    keywords=["error-code", "error code"],
    allow_substring=False,
    case_sensitive=False,
    split_rule=multi_split_rule,
)
```

### Route Filtering

```python
# Restrict available routes at runtime
route = asyncio.run(
    router.route(
        query,
        route_filter={"billing", "faq"}  # Must include default_route
    )
)
```

## Best Practices

1. **Keyword Selection**: Choose keywords that are specific to each route
2. **Avoid Overlap**: Minimize keyword overlap between routes
3. **Test Coverage**: Test with diverse queries including edge cases
4. **Fallback Route**: Set a sensible default for unmatched queries
5. **Maintenance**: Document rules and update as new patterns emerge
6. **Performance**: Rule-based routing is very fast; use for high-throughput scenarios

## Troubleshooting

**Routes not matching?**
- Add more keywords to the rule
- Enable substring matching if needed
- Check case sensitivity settings
- Verify split rules are working correctly

**Too many false positives?**
- Use stricter matching (exact words, case-sensitive)
- Reduce keyword overlap
- Use AND logic (match_all=True) for multiple conditions

**Ambiguous queries matching multiple routes?**
- Define rule priority (order matters)
- Use more specific keywords
- Add additional rules to disambiguate

## See Also

- [Semantic Router](semantic-router/) - Embedding-based routing
- [Similarity-Based Router](similarity-based-router.md) - Similarity-based routing
- [LM-Based Router](lm-based-router.md) - Language model-based routing
