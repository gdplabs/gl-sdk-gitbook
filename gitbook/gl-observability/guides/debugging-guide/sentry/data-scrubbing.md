# Data Scrubbing

Sentry has a server-side data scrubbing feature to protect sensitive information from malicious actors. The feature is enabled by default and recommended to be used. It offers default scrubbing rules and you can also add custom rules to scrub additional data. These privacy rules can be configured at the project level for individual applications or at the organization level to apply the same rules across all projects.

## Data Scrubbing

### Setting Page Location

Data scrubbing settings can be found by following these steps:

1. Go to **Sidebar > Settings > Projects** and select the project.

<figure><img src="../../../../.gitbook/assets/image (51).png" alt=""><figcaption></figcaption></figure>

2. Go to **Sidebar > Privacy and Security** to open the Data Scrubbing settings.

<figure><img src="../../../../.gitbook/assets/image (52).png" alt=""><figcaption></figcaption></figure>

### Scrubbing Rules

Sentry has a default scrubbing rules and you can add more custom rules to scrub sensitive data. These are the Sentry scrubbing rules:

1. Credit card number value, detected using regex patterns.
2. Span fields with sensitive keys, all values are redacted when the field name matches:
   1. password
   2. secret
   3. passwd
   4. api\_key
   5. apikey
   6. auth
   7. credentials
   8. mysql\_pwd
   9. privatekey
   10. private\_key
   11. token
   12. bearer
3.  Span fields and values specified on settings. To set it, open the Data Scrubbing setting page and add the fields name or values to **Additional Sensitive Fields** field. Separate each value by a newline.

    <figure><img src="../../../../.gitbook/assets/image (53).png" alt=""><figcaption></figcaption></figure>
4. Advance data scrubbing rules. You can specify what fields and condition the rule will be applied. To set it, follow these steps:
   1. Open the Data Scrubbing setting page.
   2.  Look for **Advanced Data Scrubbing** table and click **Add Rule** button. it will open the rules form.

       <figure><img src="../../../../.gitbook/assets/image (55).png" alt="" width="480"><figcaption></figcaption></figure>
   3.  Choose the method, what will the redacted value converted to.

       <figure><img src="../../../../.gitbook/assets/image (56).png" alt="" width="420"><figcaption></figcaption></figure>
   4.  Choose the data type. If the data type is matched with the value, it will be redacted. Choose **Anything** to always redact the field value.

       <figure><img src="../../../../.gitbook/assets/image (57).png" alt=""><figcaption></figcaption></figure>
   5.  Choose the field. To make it simple inserting the field names, find a trace that contains the field on any spans and copy the trace transaction ID. Then click on **Use event ID for auto-completion**, it will open a form to search fields based on the trace transaction ID.

       <figure><img src="../../../../.gitbook/assets/image (60).png" alt=""><figcaption></figcaption></figure>
   6. Verify the specified field according to the scrubbing rules on new incoming traces. The data should be redacted if the rules are fulfilled.
