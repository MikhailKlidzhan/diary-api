from fastapi import FastAPI
from .api import api_router


app = FastAPI(
    title='Diary App',
    description='A diary app with CRUD operations',
    version='0.1.0'
)


app.include_router(api_router)


@app.get('/')
async def root() -> dict[str, str]:
    return {'message': 'Welcome to Diary API'}


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
