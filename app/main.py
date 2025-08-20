from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def root():
    return {'message': 'HRM-BE API is running 🚀'}
