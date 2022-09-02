
# Real-life examples
Here are some real-life examples of solving captchas, both with a synchronous client and asynchronous.
By default, all examples use 2captcha.com.

## Prerequisites
- The `httpx` (with HTTP/2 support) and `lxml` packages must be installed before running the examples:

```pip install httpx[http2] lxml```

- You must also specify your API key:
  - either through an environment variable (`API_KEY_2CAPTCHA`);
  - or directly in the code (replace the `<PLACE_YOUR_API_KEY_HERE>` line with the key value).

- For the reCAPTCHA v2 Enterprise examples, you must specify the proxy address (in the format `http://<LOGIN>:<PASSWORD>@<PROXY_ADDRESS>:<PORT>`) using the `HTTP_PROXY_SERVER` environment variable.

## Proxy usage example
See examples on reCAPTCHA v2 Enterprise.
