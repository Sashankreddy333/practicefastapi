from fastapi import FastAPI,Path,HTTPException,Query
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
@app.get('/sort')
def getsorted(sortby:str=Query(...,description="what it should be sorted by"),orderby:str=Query("asc",description="sort in asc or desc")):
    values=["height","weight","bmi"]
    if sortby not in values:
        raise HTTPException(status_code=404,detail=f"{sortby} not in {values}")
    if orderby not in ["asc","des"]:
        raise HTTPException(status_code=404,detail=f"{orderby} not in asc or des")
    reversed=False
    if orderby=="des":
        reversed=True
    loadeddata=load_data()
    sortedvalues=sorted(loadeddata.values(),key=lambda x:x[sortby],reverse=reversed)
    return sortedvalues
        