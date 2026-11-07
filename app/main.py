from fastapi import FastAPI
from app.api.access_grants import router as access_grants_router
from app.api.employees import router as employees_router
from app.api.audit_logs import router as audit_logs_router
from fastapi.middleware.cors import CORSMiddleware
from app.api.access_reviews import (
    router as access_reviews_router
)
app = FastAPI(
    title="AegisAI",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    employees_router,
    prefix="/api",
    tags=["Employees"]
)
app.include_router(
    access_grants_router,
    prefix="/api",
    tags=["Access Grants"]
)
app.include_router(
    audit_logs_router,
    prefix="/api",
    tags=["Audit Logs"]
)
app.include_router(
    access_reviews_router,
    prefix="/api",
    tags=["Access Reviews"]
)

from app.api.roles import router as roles_router
app.include_router(
    roles_router,
    prefix="/api",
    tags=["Roles"]
)

from app.api.authorization import router as authorization_router

app.include_router(
    authorization_router,
    prefix="/api",
    tags=["Authorization"]
)
from app.api.access_requests import router as access_requests_router

app.include_router(
    access_requests_router,
    prefix="/api",
    tags=["Access Requests"]
)

from app.api.resources import (
    router as resources_router
)

app.include_router(
    resources_router,
    prefix="/api",
    tags=["Resources"]
)

from app.api.dashboard import (
    router as dashboard_router
)

app.include_router(
    dashboard_router,
    prefix="/api",
    tags=["Dashboard"]
)

@app.get("/")
def root():
    return {"message": "AegisAI IAM Platform"}


@app.get("/health")
def health():
    return {"status": "healthy"}