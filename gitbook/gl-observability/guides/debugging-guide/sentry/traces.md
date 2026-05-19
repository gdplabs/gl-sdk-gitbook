# Traces

Trace represents the full path of a single request, from start to finish, across all connected services in your system. It is constructed from multiple spans, which is a single, timed operation within a trace and has attributes, a key-value pair, that provide additional information that can be useful for debugging. By analyzing traces, developers can understand the flow and timing of operations, helping them identify issues in code execution.

## Traces Page

The Traces page shows a list of traces and offers flexible queries and filters to help you quickly find the trace you need.

<figure><img src="../../../../.gitbook/assets/image (4) (1) (1).png" alt=""><figcaption></figcaption></figure>

## How to Debug

These steps will guide you on how to use Sentry Traces page for debugging your code:

1. Go to **sidebar > Explore > Traces.**
2. Select the project you want to look into.

<figure><img src="../../../../.gitbook/assets/unknown (21).png" alt=""><figcaption></figcaption></figure>

3. Filter by the environment name and when it takes place.

<figure><img src="../../../../.gitbook/assets/image (5).png" alt=""><figcaption></figcaption></figure>

4. Search for specific traces based on attributes like transaction name, span attributes, duration, and more.

<figure><img src="../../../../.gitbook/assets/unknown (22).png" alt="" width="563"><figcaption></figcaption></figure>

5. You can also save your custom search as a by clicking the \`**>> Advanced** button below the project select button. It will open a sidebar for setting the visualization. Then click the **Save as…** button and choose to save it as a query.

<figure><img src="../../../../.gitbook/assets/image (7).png" alt=""><figcaption></figcaption></figure>

6. After you find your desired trace, you can analyze spans to understand the time taken by various parts of your application, helping you optimize performance.

## Trace Details

Once you select a trace, you will be directed to the **Trace Details** page. Here, you will find a comprehensive breakdown of the trace and its spans, visualized in a Gantt chart.

<figure><img src="../../../../.gitbook/assets/unknown (23).png" alt=""><figcaption></figcaption></figure>

Clicking on a specific span in the chart will reveal the span information such as:

1. General Data

<figure><img src="../../../../.gitbook/assets/unknown (24).png" alt=""><figcaption></figcaption></figure>

2. Additional Data

<figure><img src="../../../../.gitbook/assets/unknown (25).png" alt=""><figcaption></figcaption></figure>

3. Trace Data

<figure><img src="../../../../.gitbook/assets/unknown (26).png" alt="" width="526"><figcaption></figcaption></figure>

4. Body

<figure><img src="../../../../.gitbook/assets/unknown (27).png" alt="" width="529"><figcaption></figcaption></figure>

5. Headers

<figure><img src="../../../../.gitbook/assets/unknown (28).png" alt="" width="527"><figcaption></figcaption></figure>

6. Tags & Context

<figure><img src="../../../../.gitbook/assets/unknown (29).png" alt="" width="519"><figcaption></figcaption></figure>

7. Database Query

<figure><img src="../../../../.gitbook/assets/unknown (30).png" alt="" width="563"><figcaption></figcaption></figure>

## Make Searching Trace Easier

Traces page's search feature allows querying a trace based on span attribute values. Adding more searchable span and its attributes makes it easier to find a specific trace. You can follow this #to add more span from a third-party library.
