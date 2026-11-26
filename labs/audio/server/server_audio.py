import sys
from pathlib import Path

# S'assurer que la racine du projet est dans sys.path quel que soit le dossier de lancement
ROOT_DIR = Path(__file__).resolve().parents[3]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from labs.audio.server.api.routes import router

app = FastAPI(title="P2IS Audio Web Tool")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")

DIST_DIR = Path(__file__).parent / "dist"
if DIST_DIR.exists():
    app.mount("/assets", StaticFiles(directory=str(DIST_DIR / "assets")), name="assets")

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        if full_path.startswith("api/"):
            raise HTTPException(status_code=404, detail="API route not found")
        path = DIST_DIR / full_path
        if path.is_file():
            return FileResponse(path)
        return FileResponse(DIST_DIR / "index.html")
else:
    @app.get("/")
    async def no_frontend():
        return {
            "error": "Frontend non compilé ou dossier dist manquant.",
            "docs": "http://127.0.0.1:8001/docs"
        }


if __name__ == "__main__":
    import uvicorn
    import webbrowser
    import threading
    import time

    def open_browser():
        time.sleep(1.5)
        webbrowser.open("http://127.0.0.1:8001")

    threading.Thread(target=open_browser, daemon=True).start()
    uvicorn.run(app, host="127.0.0.1", port=8001)
