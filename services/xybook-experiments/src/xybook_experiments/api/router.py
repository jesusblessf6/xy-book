from fastapi import APIRouter, HTTPException, status

api_router = APIRouter(prefix="/api/experiments")


@api_router.get("/", tags=["experiments"])
async def list_experiments():
    raise HTTPException(status.HTTP_501_NOT_IMPLEMENTED, "Not implemented in Phase 0")


@api_router.post("/", status_code=201, tags=["experiments"])
async def create_experiment():
    raise HTTPException(status.HTTP_501_NOT_IMPLEMENTED, "Not implemented in Phase 0")


@api_router.get("/{experiment_id}", tags=["experiments"])
async def get_experiment(experiment_id: str):
    raise HTTPException(status.HTTP_501_NOT_IMPLEMENTED, "Not implemented in Phase 0")


# Reports sub-router
reports_router = APIRouter(prefix="/api/reports", tags=["reports"])


@reports_router.get("/")
async def list_reports():
    raise HTTPException(status.HTTP_501_NOT_IMPLEMENTED, "Not implemented in Phase 0")


@reports_router.get("/{report_id}")
async def get_report(report_id: str):
    raise HTTPException(status.HTTP_501_NOT_IMPLEMENTED, "Not implemented in Phase 0")
