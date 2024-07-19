
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from . import models, schemas
from .database import SessionLocal, engine
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token

models.Base.metadata.create_all(bind=engine)
app = Flask(__name__)
jwt = JWTManager(app)

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    # Verify credentials (implementation omitted)
    if is_valid_credentials(username, password):
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "Bad username or password"}), 401

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/workflows/", response_model=schemas.Workflow)
def create_workflow(workflow: schemas.WorkflowCreate, db: Session = Depends(get_db)):
    db_workflow = models.Workflow(**workflow.dict())
    db.add(db_workflow)
    db.commit()
    db.refresh(db_workflow)
    return db_workflow

@app.get("/workflows/{workflow_id}", response_model=schemas.Workflow)
def read_workflow(workflow_id: int, db: Session = Depends(get_db)):
    db_workflow = db.query(models.Workflow).filter(models.Workflow.id == workflow_id).first()
    if db_workflow is None:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return db_workflow

@app.post("/workflows/{workflow_id}/steps/", response_model=schemas.WorkflowStep)
def create_workflow_step(
    workflow_id: int, step: schemas.WorkflowStepCreate, db: Session = Depends(get_db)
):
    db_step = models.WorkflowStep(**step.dict(), workflow_id=workflow_id)
    db.add(db_step)
    db.commit()
    db.refresh(db_step)
    return db_step