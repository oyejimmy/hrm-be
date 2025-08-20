import os
import shutil
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form
from starlette.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.auth.security import get_current_user, require_roles
from app.database.session import get_db
from app.modules.user.models import Department, EmployeeDocument, User
from fastapi.responses import StreamingResponse
import csv
from io import StringIO


class DepartmentCreate(BaseModel):
    name: str
    description: Optional[str] = None


class UserCreate(BaseModel):
    email: str
    full_name: str
    password: str
    role: str
    department_id: Optional[int] = None


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    designation: Optional[str] = None
    department_id: Optional[int] = None
    is_active: Optional[bool] = None


class UserOut(BaseModel):
    id: int
    email: str
    full_name: str
    role: str

    class Config:
        orm_mode = True


class DocumentCreate(BaseModel):
    title: str
    file_path: str
    description: Optional[str] = None


router = APIRouter()


@router.post("/departments", dependencies=[Depends(require_roles("admin"))])
def create_department(payload: DepartmentCreate, db: Session = Depends(get_db)):
    dept = Department(name=payload.name, description=payload.description)
    db.add(dept)
    db.commit()
    db.refresh(dept)
    return dept


@router.post("/", response_model=UserOut, dependencies=[Depends(require_roles("admin"))])
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    from app.auth.security import get_password_hash

    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(status_code=400, detail="Email already exists")
    user = User(
        email=payload.email,
        full_name=payload.full_name,
        password_hash=get_password_hash(payload.password),
        role=payload.role,
        department_id=payload.department_id,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get("/", response_model=List[UserOut], dependencies=[Depends(require_roles("admin", "manager"))])
def list_users(db: Session = Depends(get_db)):
    return db.query(User).all()


@router.get("/me")
def me(current=Depends(get_current_user)):
    return current


@router.get("/export/csv", dependencies=[Depends(require_roles("admin", "manager"))])
def export_users_csv(db: Session = Depends(get_db)):
    users = db.query(User).all()
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["id", "email", "full_name", "role", "department_id", "designation", "join_date"])
    for u in users:
        writer.writerow([u.id, u.email, u.full_name, u.role, u.department_id, u.designation, u.join_date])
    output.seek(0)
    return StreamingResponse(iter([output.getvalue()]), media_type="text/csv", headers={"Content-Disposition": "attachment; filename=employees.csv"})


@router.patch("/{user_id}", response_model=UserOut, dependencies=[Depends(require_roles("admin", "manager"))])
def update_user(user_id: int, payload: UserUpdate, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    for field, value in payload.dict(exclude_unset=True).items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return user


@router.delete("/{user_id}", dependencies=[Depends(require_roles("admin"))])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"ok": True}


@router.post("/{user_id}/documents", dependencies=[Depends(require_roles("admin", "manager", "employee"))])
def add_document(
    user_id: int,
    title: str = Form(...),
    description: Optional[str] = Form(None),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current=Depends(get_current_user),
):
    # Permission: employees can only upload for themselves; managers/admins can upload for any user
    if current.role == "employee" and current.id != user_id:
        raise HTTPException(status_code=403, detail="Cannot upload documents for other users")
    if not db.get(User, user_id):
        raise HTTPException(status_code=404, detail="User not found")
    os.makedirs("uploads", exist_ok=True)
    filename = f"{user_id}_{int(datetime.utcnow().timestamp())}_{file.filename}"
    path = os.path.join("uploads", filename)
    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    doc = EmployeeDocument(employee_id=user_id, title=title, file_path=path, description=description)
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc


@router.get("/{user_id}/documents")
def list_documents(user_id: int, db: Session = Depends(get_db)):
    return db.query(EmployeeDocument).filter(EmployeeDocument.employee_id == user_id).all()


@router.delete("/documents/{document_id}")
def delete_document(document_id: int, db: Session = Depends(get_db)):
    doc = db.get(EmployeeDocument, document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    db.delete(doc)
    db.commit()
    return {"ok": True}


class DocumentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


@router.put("/documents/{document_id}")
def update_document(document_id: int, payload: DocumentUpdate, db: Session = Depends(get_db), current=Depends(get_current_user)):
    doc = db.get(EmployeeDocument, document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    if current.role == "employee" and current.id != doc.employee_id:
        raise HTTPException(status_code=403, detail="Cannot edit others' documents")
    for field, value in payload.dict(exclude_unset=True).items():
        setattr(doc, field, value)
    db.commit()
    db.refresh(doc)
    return doc


@router.get("/documents/{document_id}/download")
def download_document(document_id: int, db: Session = Depends(get_db), current=Depends(get_current_user)):
    doc = db.get(EmployeeDocument, document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    if current.role == "employee" and current.id != doc.employee_id:
        raise HTTPException(status_code=403, detail="Cannot download others' documents")
    if not os.path.exists(doc.file_path):
        raise HTTPException(status_code=404, detail="File not found on server")
    return FileResponse(path=doc.file_path, filename=os.path.basename(doc.file_path))


