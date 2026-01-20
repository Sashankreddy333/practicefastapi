from fastapi import FastAPI,Path,HTTPException,Query
import json
from fastapi.responses import JSONResponse

from pydantic import BaseModel,computed_field,Field
from typing import Annotated,Literal,Optional
app=FastAPI()
class patient(BaseModel):
    id:Annotated[str,Field(..., description="the patient id")]
    name:Annotated[str,Field(...,description="patient name")]
    city:Annotated[str,Field(...,description="patient living city",max_length=20)]
    age:Annotated[int,Field(...,gt=0,lt=100,description="patient age")]
    gender:Annotated[Literal['male','female','others'],Field(...,description="patient gender")]
    height:Annotated[float,Field(...,gt=0,description="patient height")]
    weight:Annotated[float,Field(...,gt=0,description="patient weight")]
    @computed_field
    @property
    def bmi(self)->float:
        return round(self.height/self.weight,2)
    @computed_field
    @property
    def verdict(self)->str:
        if self.bmi<18.5:
            return "Underweight"
        elif self.bmi<30:
            return "Normal"
        else:
            return "Obese"
class update_patient(BaseModel):
    id:Annotated[Optional[str],Field(default=None,description="the patient id")]
    name:Annotated[Optional[str],Field(default=None,description="patient name")]
    city:Annotated[Optional[str],Field(default=None,description="patient living city",max_length=20)]
    age:Annotated[Optional[int],Field(default=None,gt=0,lt=100,description="patient age")]
    gender:Annotated[Optional[Literal['male','female','others']],Field(default=None,description="patient gender")]
    height:Annotated[Optional[float],Field(default=None,gt=0,description="patient height")]
    weight:Annotated[Optional[float],Field(default=None,gt=0,description="patient weight")]

def load_data():
    with open('patients.json','r') as f:
        patientdata=json.load(f)
        return patientdata
def save_data(data):
    with open('patients.json','w') as f:
        json.dump(data,f)
@app.post('/create')
def create_patient(patient:patient):
    data=load_data()
    if patient.id in data:
        raise HTTPException(status_code=400,detail="file already exists")
    data[patient.id]=patient.model_dump(exclude=["id"])
    save_data(data)
    return JSONResponse(status_code=201,content={"message":"data added successfully"})
@app.put('/edit/{patientid}') 
def update_data(patientid:str,new_data_point:update_patient):
    data=load_data()
    if patientid not in data:
        raise HTTPException(status_code=400,detail="patient id not found")
    old_data=data[patientid]
    new_data=new_data_point.model_dump(exclude_unset=True)
    for key ,val in new_data.items():
        old_data[key]=val
    old_data["id"]=patientid
    old_data_update=patient(**old_data)
    updated_data_point=old_data_update.model_dump(exclude="id")
    data[patientid]=updated_data_point
    save_data(data)
    return JSONResponse(status_code=201,content={"message":"successfully updated"})
    
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
@app.delete("/delete/{patientid}")
def delete_data(patientid:str):
    data=load_data()
    if patientid not in data:
        raise HTTPException(status_code=400,detail="id not found")
    del data[patientid]
    save_data(data)
    return JSONResponse(status_code=201,content={"message":"deleted successfully"})