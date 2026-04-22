import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.api.router import api_router
from app.core.config import settings

def create_app() -> FastAPI:
    """Application factory for the Document Assistant."""
    app = FastAPI(title=settings.APP_NAME)

    # Include API routes
    app.include_router(api_router)

    # Setup static files
    # Check if static dir exists, if not create it
    if not os.path.exists(settings.STATIC_DIR):
        os.makedirs(settings.STATIC_DIR, exist_ok=True)

    app.mount("/static", StaticFiles(directory=settings.STATIC_DIR), name="static")

    @app.get("/")
    async def serve_ui():
        """Serves the main frontend application."""
        return FileResponse(f"{settings.STATIC_DIR}/index.html")

    return app

app = create_app()
