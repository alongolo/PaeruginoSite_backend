from fastapi import FastAPI, Depends
from starlette.requests import Request
from fastapi.middleware.cors import CORSMiddleware;
import uvicorn
from app.api.api_v1.routers.genes import genes_router
from app.api.api_v1.routers.isolation import isolation_router
from app.api.api_v1.routers.strains import strains_router
from app.api.api_v1.routers.defense_systems import defense_systems_router
from app.api.api_v1.routers.statistics import statistics_router

from app.core import config
from app.db.session import SessionLocal

from app.api.api_v1.routers.cluster import cluster_router

app = FastAPI(
    title=config.PROJECT_NAME, docs_url="/api/docs", openapi_url="/api",
    description="Pseudomonas Aeruginosa Web Application"
)

# app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=['bad_subtree', 'bad_systems']
)


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request.state.db = SessionLocal()
    response = await call_next(request)
    request.state.db.close()
    return response


app.include_router(genes_router, prefix="/api/v1/genes", tags=["genes"])
app.include_router(strains_router, prefix="/api/v1/strains", tags=["strains"])
app.include_router(cluster_router, prefix="/api/v1/cluster", tags=["cluster"])
app.include_router(statistics_router, prefix="/api/v1/statistics", tags=["statistics"])
app.include_router(defense_systems_router, prefix="/api/v1/defense", tags=["defense_systems"])
app.include_router(isolation_router, prefix="/api/v1/isolation", tags=["isolation"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", reload=True, reload_dirs=["./api", "./db"], port=8800)
