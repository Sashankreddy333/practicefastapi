from fastapi import FastAPI
app=FastAPI()

@app.get('/')
def get():
    return {"message":"hello world"}
@app.get('/sum')
def sum():
    return {"message":"sum is displayed"}
