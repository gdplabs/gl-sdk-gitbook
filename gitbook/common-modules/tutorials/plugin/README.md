---
icon: puzzle-piece-simple
cover: >-
  https://images.unsplash.com/photo-1612611741189-a9b9eb01d515?crop=entropy&cs=srgb&fm=jpg&ixid=M3wxOTcwMjR8MHwxfHNlYXJjaHwyfHxwdXp6bGV8ZW58MHx8fHwxNzY4MTkyMDU2fDA&ixlib=rb-4.1.0&q=85
coverY: 0
---

# Plugin

GL Plugin is a flexible plugin-based architecture that allows you to build modular and extensible applications. It provides a robust framework for managing plugins, handling dependencies, and injecting services.

<figure><img src="../../../.gitbook/assets/plugin (1).png" alt=""><figcaption><p>The Plugin Architecture. <a href="https://www.mermaidchart.com/play?utm_source=mermaid_live_editor&#x26;utm_medium=toggle#pako:eNqdlG2PmkAQx7_KBpO-kssB5xMvmorASaKJgfZVbcweLEpdF7vg3dHLffcOT6ugp7lioszMb-Y_O7vrm-THAZF0SZblJfNjFkZrfckQojiLD6mOCN0uWREMafzibzBP0XcDiOTwtOZ4v0HObk9_LqX8h-wIS3EaxWwp_cqrlM9i6gCwoId1xNAUs4ASXqQ1KUVASTOgfhTQzgKEBae9Pc7KMHCPM1S-N0vMj53NMcNrwhtxz4W4R_hz5BPkknWUpDxrLc44X5yBE9KkTqCzYDEK0XzRFZqtFvMV1F7df5Nl9CONaPSXJChmBMUc7WJOkCx_zdVFCnBTnCBcBDy38k-NvBYUgl0oi1mvKSiRAD1lVQ2nYgsUSOUDUEFfYDfyL63M8FzI8Nxj7QknOIU-q5ElTQGBFwJ3yGG_iZ-e0HcXVSC_WIMjOivnnFzoqpoqwLquLwj2N7VHAYe3zWpTbZpa05yDOf5zwJXtuWC7MexbXd5oOZq2T3GSmCREfr5RYUSp3gnDsAunJ94SvaNpWvUuv0RButHV_WsrM4JDUWeO8o9IHo1GzWTlLDlvHbWZbu0JcAL3mONMZ3Cearfeeehb5mTYrVRNy7ZtsPyYxhxaHgytwbilk6_48zq23RsNhI5tm7bVEzpDS1W1fkun2Mj_EDIMrTc-Clm2aRyF7L6mmi0hOAKfl9EGD-ZgUstYqmXY9snc8mApk6QZJeJPSeSbvXt46rN7cvPfkH_gz0RHNGIEc_SOBCIu9BWmusnXCfUmoV0lxO2_jig3CfUmod0YiXNzvTlysYr0_g-A_SYa">Mermaid Link</a>.</p></figcaption></figure>

### Core Components <a href="#core-components" id="core-components"></a>

**Plugin Manager**

The central orchestrator for plugins. It manages:

* Registration, instantiation, and retrieval of plugins.
* Ensures that each plugin is paired with its handler and that all dependencies are injected before use.
* Handles service registration

**Service Registry**

A container for all services

* Handles registration and retrieval of service instances
* Handles dependency injection
* Maps service types to their implementations

{% hint style="warning" %}
Note: You don't need to create your own Service Registry - it's automatically created and assigned into the Manager!
{% endhint %}

**Plugin Handler**

The **Handler** is your customization point for _how_ plugins behave. It serves two purposes:

* **Service Injection**: Define what services your plugins receive via `create_injections()`. This is where the Service Registry's power flows into your plugins.
* **Lifecycle Control**: The `initialize_plugin()` method lets you run setup logic when a plugin is instantiated.

In the diagram, notice how Plugin Handler Impl sits in the middle—it extends the base, receives service injections, and handles multiple plugins.

Interface for providing services to plugins

* Creates service injections through create\_injections
* Initializes plugin-specific resources
* Can be extended for different types of plugins (e.g., HTTP handlers, Pipelines)

**Plugin**

**Plugins** are where your actual functionality lives. The `@Plugin.for_handler()` decorator binds a plugin to its handler, establishing the relationship shown in the diagram (Handler → "Handles" → Plugins).

This is pure polymorphism in action—extend the base, define your metadata, and add whatever methods your use case requires.

All plugins must inherit from the `Plugin` base class.

* Has basic metadata (name, description, version)
* Receives injected services automatically
* Can be extended with specific functionality
