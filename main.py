from fastapi import Depends, FastAPI

from models import Student

from database import session,engine

from sqlalchemy.orm import Session

import database_models


app = FastAPI()


database_models.Base.metadata.create_all(bind=engine)


@app.get("/")
def main():
    return "Hello, Welcome to Student Crud Api"


students = [
    Student( id = 1, name = 'sadhik', age = 23 ),
    Student( id = 2, name = 'hemanth', age = 25 ),
    Student( id = 3, name = 'bhanu', age = 27 ),
]

def get_db() :
    db = session()
    
    try :
        yield db
    
    finally : 
        db.close()
    


@app.get("/students")
def getAllStudents(db : Session = Depends(get_db)) :
    
    db_students = db.query(database_models.Student).all()    
    return db_students


@app.get("/students/{id}")
def getStudentById(id : int, db : Session = Depends(get_db)) :
    db_student = db.query(database_models.Student).filter(database_models.Student.id == id).first()
    
    if db_student :
        return db_student
    
    
    return "Student Not Found"


@app.post("/students")
def addStudent(student : Student, db : Session = Depends(get_db)):
    
    db.add(database_models.Student(**student.model_dump()))
    
    db.commit()
    
    return "student added successfully"


@app.put("/students/{id}")
def updateStudentById(id : int,student : Student,  db : Session = Depends(get_db)) :
    db_student = db.query(database_models.Student).filter(database_models.Student.id == id).first()
    
    if db_student :
        db_student.age = student.age
        db.commit()
        
        return "Student age updated Successfully"
    
    return "Student Not Found, Check Once"


@app.delete("/students")
def deleteAllStudents(db:Session = Depends(get_db)) :
    
    db.query(database_models.Student).delete()
    
    db.commit()
    
    return "All students deleted Successfully"
    


@app.delete("/students/{id}")
def deleteStudentById(id : int, db : Session = Depends(get_db)) :
    
    db_student = db.query(database_models.Student).filter(database_models.Student.id == id).first()
    
    if db_student : 
        
        db.delete(db_student)
        db.commit()
        return "Student deleted successfully"
    
    return "Student Not Found"
    

