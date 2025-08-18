from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth, files, chat, pricing


def create_app() -> FastAPI:
    app = FastAPI(title="DocuTalk API", version="1.0.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/health")
    async def health():
        return {"status": "ok"}

    app.include_router(auth.router)
    app.include_router(files.router)
    app.include_router(chat.router)
    app.include_router(pricing.router)

    return app


app = create_app()

