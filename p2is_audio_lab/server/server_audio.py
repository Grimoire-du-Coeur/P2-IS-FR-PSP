import sys
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router

app = FastAPI(title="P2IS Audio Web Tool")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

DIST_DIR = Path(__file__).parent / "dist"
if DIST_DIR.exists():
    app.mount("/assets", StaticFiles(directory=str(DIST_DIR / "assets")), name="assets")

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        path = DIST_DIR / full_path
        if path.is_file():
            return FileResponse(path)
        return FileResponse(DIST_DIR / "index.html")


if __name__ == "__main__":
    import uvicorn
    
    import webbrowser
    import threading
    import time
    def open_browser():
        time.sleep(1.5)
        webbrowser.open("http://127.0.0.1:8001")
    threading.Thread(target=open_browser, daemon=True).start()
    uvicorn.run("server_audio:app", host="127.0.0.1", port=8001, reload=False)

