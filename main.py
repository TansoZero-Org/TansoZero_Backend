from fastapi import FastAPI
from routers import dashboard, contract, energy, efficiency,region
from fastapi.middleware.cors import CORSMiddleware
    
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(dashboard.router)
app.include_router(contract.router)
app.include_router(energy.router)
app.include_router(efficiency.router)
app.include_router(region.router)

@app.get("/")
def read_root():
    return {"message": "ㅎㅇ"}
