"""
P2IS Image Lab - Serveur auto-contenu
Sert l'API FastAPI ET le frontend React (build statique) sur le meme port 8002.
L'utilisateur n'a besoin que de Python - pas de Node.js.
"""
import sys
import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Ajouter le repertoire courant dans sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from api.routes import router

app = FastAPI(title="P2IS Image Web Tool")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes API
app.include_router(router, prefix="/api")

# Servir le build statique React (dossier dist/)
DIST_DIR = Path(__file__).parent / "dist"

if DIST_DIR.exists():
    # Monter les assets (JS, CSS, images...)
    app.mount("/assets", StaticFiles(directory=str(DIST_DIR / "assets")), name="assets")

    # Toutes les autres routes -> index.html (SPA React Router)
    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        index = DIST_DIR / "index.html"
        return FileResponse(str(index))

    @app.get("/")
    async def serve_root():
        return FileResponse(str(DIST_DIR / "index.html"))
else:
    @app.get("/")
    async def no_frontend():
        return {
            "error": "Frontend non compile. Lance 'npm run build' dans web_ui/ d'abord.",
            "docs": "http://127.0.0.1:8002/docs"
        }

if __name__ == "__main__":
    import uvicorn
    import webbrowser
    import threading
    import time

    def open_browser():
        time.sleep(2)
        webbrowser.open("http://127.0.0.1:8002")

    threading.Thread(target=open_browser, daemon=True).start()
    uvicorn.run("server_image:app", host="127.0.0.1", port=8002, reload=False)
