# Service 
from fastapi import FastAPI
from . import routers


# FastAPI app instance
app = FastAPI()


# Include all routers
app.include_router(routers.router, prefix='/admin', tags=[])


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app=app, host='0.0.0.0', port='8000')
