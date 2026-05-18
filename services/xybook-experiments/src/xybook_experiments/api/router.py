from fastapi import APIRouter, HTTPException, status

api_router = APIRouter()


@api_router.get("/api/experiments", tags=["experiments"])
async def list_experiments():
    raise HTTPException(status.HTTP_501_NOT_IMPLEMENTED, "Not implemented in Phase 0")


@api_router.post("/api/experiments", status_code=201, tags=["experiments"])
async def create_experiment():
    raise HTTPException(status.HTTP_501_NOT_IMPLEMENTED, "Not implemented in Phase 0")


@api_router.get("/api/experiments/{experiment_id}", tags=["experiments"])
async def get_experiment(experiment_id: str):
    raise HTTPException(status.HTTP_501_NOT_IMPLEMENTED, "Not implemented in Phase 0")


@api_router.get("/api/reports", tags=["reports"])
async def list_reports():
    raise HTTPException(status.HTTP_501_NOT_IMPLEMENTED, "Not implemented in Phase 0")


@api_router.get("/api/reports/{report_id}", tags=["reports"])
async def get_report(report_id: str):
    raise HTTPException(status.HTTP_501_NOT_IMPLEMENTED, "Not implemented in Phase 0")
