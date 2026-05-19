# Session Replays

The Replays page allows you to watch video playbacks of user sessions to diagnose how errors occur. Note that this feature is available only for frontend or UI applications.

<figure><img src="../../../../.gitbook/assets/unknown (35).png" alt=""><figcaption></figcaption></figure>

## How to Debug

This is how you can use Replays page to debug errors in your UI app.

1. Go to **sidebar > Explore > Replays**
2. Select the project you want to look into

<figure><img src="../../../../.gitbook/assets/unknown (36).png" alt="" width="358"><figcaption></figcaption></figure>

3. Filter by the environment name and when it takes place.

<figure><img src="../../../../.gitbook/assets/image (8).png" alt="" width="390"><figcaption></figcaption></figure>

4. Search for specific replays based on attributes like transaction attributes, click fields, tags, and more.

<figure><img src="../../../../.gitbook/assets/unknown (37).png" alt="" width="563"><figcaption></figcaption></figure>

5. You can click the replays to see a replay video and additional information about the error.

## Replay Details

The replay details include a video showcasing the user's actions on the UI app that result in an error. Alongside the video, the page contains additional contexts about the error.

<figure><img src="../../../../.gitbook/assets/unknown (38).png" alt=""><figcaption></figcaption></figure>

### Breadcrumbs

Breadcrumbs provides history and timeline leading to an error. It contains event information like click events and UI components it interacts with.

<figure><img src="../../../../.gitbook/assets/unknown (39).png" alt=""><figcaption></figcaption></figure>

### Console

The Console section displays a list of logs inside the browser console.

<figure><img src="../../../../.gitbook/assets/unknown (40).png" alt=""><figcaption></figcaption></figure>

### Network

The Network section provides a detailed log of all HTTP requests made by the browser during the session. For each request, you can see crucial information like the HTTP method, response status code, and path, which helps you quickly identify failed API calls or slow network performance.

<figure><img src="../../../../.gitbook/assets/unknown (41).png" alt=""><figcaption></figcaption></figure>

### Errors

The Errors section displays a list of related Issues. This guide also provided detailed information about [Issue Details](issues.md#issue-details).

<figure><img src="../../../../.gitbook/assets/unknown (42).png" alt=""><figcaption></figcaption></figure>

### Tags

The Tags section displays a list of additional information that might be useful for debugging like the browser name, browser version, and more.

<figure><img src="../../../../.gitbook/assets/unknown (43).png" alt=""><figcaption></figcaption></figure>
