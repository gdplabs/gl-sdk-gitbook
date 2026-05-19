# Discover

The Discover page helps you explore and understand your application's performance patterns by providing comprehensive insights into queries, datasets, and performance metrics across your entire system. It lets you discover and analyze both **Errors** (Issue) and **Transactions** (Trace).

<figure><img src="../../../../.gitbook/assets/unknown (66).png" alt=""><figcaption></figcaption></figure>

<figure><img src="../../../../.gitbook/assets/unknown (67).png" alt=""><figcaption></figcaption></figure>

This is how you can use Discover to view comprehensive performance data to analyze trends and identify patterns across your application.

1. Go to **sidebar > Explore > Discover.**
2. On the first page, you can see aggregated performance metrics based on your filters, along with time series visualizations of key performance indicators.

<figure><img src="../../../../.gitbook/assets/unknown (68).png" alt="" width="563"><figcaption></figcaption></figure>

3. We also can filter based on attributes of error and transactions. There is a limitation for transaction filters, it can’t filter based on span attributes.

<figure><img src="../../../../.gitbook/assets/unknown (31).png" alt="" width="563"><figcaption></figcaption></figure>

4. After your filter applied, the list will be updated.

<figure><img src="../../../../.gitbook/assets/unknown (32).png" alt="" width="563"><figcaption></figcaption></figure>

5. You can also export the data, but it will take time to compile it and sentry will email it to you for the download link, the document will be in `.csv` format

<figure><img src="../../../../.gitbook/assets/unknown (33).png" alt="" width="445"><figcaption></figcaption></figure>

6. After you find your desired event, you can analyze it by clicking on it. If the event is an Error, you will be redirected to its [Issue Details page](issues.md#issue-details). If it is a Transaction, you will be taken to the [Trace Details page](traces.md#trace-details).
