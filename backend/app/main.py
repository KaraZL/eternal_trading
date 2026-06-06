"""FastAPI application for AI-assisted lending platform."""

from fastapi import FastAPI

from .api import clients, books, loans, collateral, risk

app = FastAPI(title="Eternal Lending Platform", version="0.1.0")

# Include API routers
app.include_router(clients.router, prefix="/api/clients", tags=["clients"])
app.include_router(books.router, prefix="/api/books", tags=["books"])
app.include_router(loans.router, prefix="/api/loans", tags=["loans"])
app.include_router(collateral.router, prefix="/api/collateral", tags=["collateral"])
app.include_router(risk.router, prefix="/api/risk", tags=["risk"])


@app.get("/health")
async def health_check() -> dict:
    """Health check endpoint."""
    return {"status": "ok"}