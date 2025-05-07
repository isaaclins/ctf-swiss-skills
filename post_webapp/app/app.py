from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import httpx
import json
import uvicorn

app = FastAPI()

app.mount("/templates", StaticFiles(directory="templates"), name="templates")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/track", response_class=HTMLResponse)
async def track_page(request: Request, url: str = None):
    return templates.TemplateResponse("track.html", {"request": request, "result": "", "url": url or ""})

@app.post("/track", response_class=HTMLResponse)
async def track_cargo(request: Request, url: str = Form(...)):
    if "localhost" in url.lower() or "127.0.0.1" in url:
        result = "<pre>Invalid tracking URL: Localhost access is not allowed.</pre>"
    else:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, timeout=10)
                response.raise_for_status()
                content = response.text
                try:
                    data = json.loads(content)
                    content = json.dumps(data, indent=2)
                except json.JSONDecodeError:
                    pass
        except httpx.TimeoutException:
            content = "Request timed out after 10 seconds"
        except httpx.RequestError as e:
            content = f"Error fetching URL: {str(e)}"
        result = f"<pre>{content}</pre>"
    
    return templates.TemplateResponse("track.html", {"request": request, "result": result, "url": url})

@app.get("/admin", response_class=HTMLResponse)
async def admin(request: Request):
    client_host = request.client.host
    if client_host != "127.0.0.1" and client_host != "localhost":
        raise HTTPException(status_code=403, detail="Access denied: Admin page is restricted to localhost only")
    return templates.TemplateResponse("admin.html", {"request": request})

@app.get("/services", response_class=HTMLResponse)
async def services(request: Request):
    return templates.TemplateResponse("services.html", {"request": request})

@app.get("/shipments", response_class=HTMLResponse)
async def shipments(request: Request):
    return templates.TemplateResponse("shipments.html", {"request": request})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)