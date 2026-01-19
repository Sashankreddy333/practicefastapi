from fastapi import FastAPI,Path,HTTPException
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
@app.get('/view/{id}')
def viewwithid(id:str=Path(...,description="get the data for the id",example="P001")):
    getview=load_data()
    if id in getview:
        return getview[id]
    raise HTTPException(status_code=404,detail="patient id not found")
        