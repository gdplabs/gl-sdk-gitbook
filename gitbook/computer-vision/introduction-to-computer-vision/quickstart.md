---
icon: play
---

# Quickstart

## Quickstart

We'll cover how to get started with one of our SDKs and make your first API request.

Before you can make requests to the GLAIR Vision API, you must obtain an **API Key**, **username**, and **password**. For now, you can obtain them by contacting us via [hi\[at\]glair.ai](mailto:hi@glair.ai) or via our representative for your company. In the future, we will release a dashboard to make it easier for you to manage your credentials.

### Choose Your SDK <a href="#choose-your-sdk" id="choose-your-sdk"></a>

Before making your first API request, you need to choose which SDK to use. In the following section, we provide code samples for NodeJS, Java, Go, and cURL.

```bash
# Install the GLAIR Vision NodeJS SDK
# Requires Node.js v18 or higher.
npm install --save @glair/vision
```



### Making Your First API Request <a href="#making-your-first-api-request" id="making-your-first-api-request"></a>

After picking your preferred SDK, you are ready to make your first call to the GLAIR Vision API. Below is an example of how to call the KTP endpoint using our SDKs.

```js
import { Vision } from '@glair/vision';

const vision = new Vision({
  apiKey: 'api-key',
  username: 'username',
  password: 'password',
});

// The SDK supports various image input types: file path, base64, or Blob/File
await vision.ocr.ktp({ image: '/path/to/image/KTP.jpg' });
```

### Making Request Without SDK <a href="#making-request-without-sdk" id="making-request-without-sdk"></a>

If you prefer not to use our SDKs, you can still do it yourself. Just with a little more boilerplate.

```js
// Install the required dependencies: 'npm install --save node-fetch form-data-encoder formdata-node'
// Save the code as 'index.mjs' and run it by executing 'node index.mjs'
import fetch from 'node-fetch';
import { FormDataEncoder } from 'form-data-encoder';
import { FormData, Blob } from 'formdata-node';
import { fileFromPath } from 'formdata-node/file-from-path';

const url = 'https://api.vision.glair.ai/ocr/v1/ktp';
const basicAuth = 'Basic ' + btoa('USERNAME' + ':' + 'PASSWORD');
const apiKey = 'API_KEY';

const data = new FormData();
data.append('image', await fileFromPath('/path/to/image/KTP.jpeg'));
const encoder = new FormDataEncoder(data);

const config = {
  method: 'POST',
  headers: {
    Authorization: basicAuth,
    'x-api-key': apiKey,
  },
  body: new Blob(encoder, { type: encoder.contentType }),
};

const response = await fetch(url, config);
console.log(await response.json());
```

### What's Next? <a href="#whats-next" id="whats-next"></a>

Great, you're now set up with an SDK and have made your first API request. Here are a few links that might be handy as you venture further into the GLAIR Vision API:

* [Learn about the different error codes in GLAIR Vision API](https://docs.glair.ai/vision/errors)
* [Check out the KTP endpoint](https://docs.glair.ai/vision/ktp)
* [Learn how to create passive liveness session to access our prebuilt web pages](https://docs.glair.ai/vision/passive-liveness-sessions)
