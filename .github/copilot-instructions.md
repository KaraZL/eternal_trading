# Project instructions

This project is an AI-assisted lending and trading platform.

The purpose is educational: the developer wants to understand both the technology and the lending/trading domain.

Tech stack:
- Backend: Python FastAPI
- Frontend: React TypeScript
- ORM: SQLAlchemy, Alembic
- Database: PostgreSQL
- AI workflow engine later: LangGraph
- Backend tests: pytest
- Frontend tests later: Vitest / React Testing Library

Architecture rules:
- Do not put business logic directly inside FastAPI route handlers.
- Use services for business workflows.
- Use Pydantic schemas for API request/response models.
- Use SQLAlchemy ORM models for persistence.
- Keep deterministic financial calculations separate from AI agents.
- AI agents may analyze, explain, and recommend, but must not directly approve loans or execute trades.
- Every critical financial action should eventually be auditable.

Domain rules:
- A Client represents a borrower or counterparty.
- A Book represents a lending or trading portfolio.
- A Loan represents money lent to a client.
- Collateral represents assets pledged to secure a loan.
- LTV means Loan-to-Value.
- Eligible collateral value = market value after haircut.
- LTV = loan amount / eligible collateral value.
- A loan breaches risk limits when LTV is above the configured threshold.

Coding style:
- Prefer explicit types.
- Write small, readable functions.
- Use clear domain names.
- Add tests for financial calculations.
- Keep the first version simple.