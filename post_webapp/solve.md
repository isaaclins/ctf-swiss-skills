# Post Webapp CTF Solution

This CTF involves a Server-Side Request Forgery (SSRF) vulnerability in the "Interstellar Cargo Tracker" application. The goal is to access an internal admin page to retrieve the flag.

## 1. Understanding the Application

The application consists of two main parts:

- A primary web application (running on port 5000 internally) that provides the user interface for tracking cargo.
- A tracking service (running on port 9000 internally, named `post-tracking` in the `docker-compose.yml`) that the main application queries to get shipment details.

The main application has a `/track` endpoint that accepts a `url` parameter. This `url` is fetched by the server, leading to an SSRF vulnerability.

## 2. Identifying the Vulnerability

The relevant code in `post_webapp/app/app.py` is:

```python
@app.post("/track", response_class=HTMLResponse)
async def track_cargo(request: Request, url: str = Form(...)):
    if "localhost" in url.lower() or "127.0.0.1" in url:
        result = "<pre>Invalid tracking URL: Localhost access is not allowed.</pre>"
    else:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, timeout=10)
                # ... (rest of the code)
```

The application attempts to prevent access to `localhost` or `127.0.0.1`. However, this can be bypassed.

Additionally, there's an admin endpoint:

```python
@app.get("/admin", response_class=HTMLResponse)
async def admin(request: Request):
    client_host = request.client.host
    if client_host != "127.0.0.1" and client_host != "localhost":
        raise HTTPException(status_code=403, detail="Access denied: Admin page is restricted to localhost only")
    return templates.TemplateResponse("admin.html", {"request": request})
```

This endpoint is only accessible from `localhost`. The flag is expected to be on this page.

## 3. Exploiting the SSRF

To exploit the SSRF and access the `/admin` page of the main application (running on port 5000 internally), we need to make the main application request its own admin page.

We can bypass the `localhost` filter using an alternative IP address for localhost, such as `0.0.0.0`.

The payload URL to submit to the tracking form will be:
`http://0.0.0.0:5000/admin`

## 4. Steps to Retrieve the Flag

1.  **Navigate to the application**: Open the Interstellar Cargo Tracker page (e.g., `https://cyberskills.ch:5002`).
2.  **Go to Track Cargo**: Access the tracking functionality. The example URL provided is `http://post-tracking:9000/shipments/123`.
3.  **Intercept the Request (Optional but Recommended)**: Use a tool like Burp Suite to intercept the POST request to `/track`.
4.  **Modify the `url` parameter**:
    - If intercepting, change the value of the `url` parameter in the request body to `http://0.0.0.0:5000/admin`.
    - If not intercepting, you can try to input this URL directly into the form, although some forms might have client-side validation that makes this tricky. The screenshot shows the URL being part of the Referer and as the `url` parameter in the POST body.
5.  **Submit the Request**: Send the modified request.
6.  **View the Response**: The response should contain the content of the `/admin` page, including the flag.

If the `admin.html` template simply renders a flag, the content returned in the `<pre>` tags will be the HTML of that admin page.

For example, using `curl` to simulate the POST request from your machine, assuming the vulnerable server is at `https://cyberskills.ch:5002`:

```bash
curl -X POST https://cyberskills.ch:5002/track \
-d "url=http://0.0.0.0:5000/admin"
```

This command sends a POST request to the `/track` endpoint with the crafted URL. The server will then fetch `http://0.0.0.0:5000/admin` internally and return its content.

The flag should be visible in the response from this command.
