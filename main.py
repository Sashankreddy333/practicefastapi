from fastapi import FastAPI
import json
app=FastAPI()
def load_data():
    with open('patients.json','r') as f:
        patientdata=json.load(f)
        return patientdata
        
@app.get('/')
def get():
    return {"message":"hello world"}
@app.get('/sum')
def sum():
    return {"message":"sum is displayed"}
@app.get('/view')
def view():
    getview=load_data()
    return getview
