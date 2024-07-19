
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Workflow(Base):
    __tablename__ = 'workflows'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    created_at = Column(DateTime)
    steps = relationship("WorkflowStep", back_populates="workflow")

class WorkflowStep(Base):
    __tablename__ = 'workflow_steps'

    id = Column(Integer, primary_key=True, index=True)
    workflow_id = Column(Integer, ForeignKey('workflows.id'))
    name = Column(String)
    order = Column(Integer)
    ai_model = Column(String)
    input_data = Column(String)
    output_data = Column(String)
    workflow = relationship("Workflow", back_populates="steps")

class AIModel(Base):
    __tablename__ = 'ai_models'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    type = Column(String)  # e.g., 'classification', 'regression', etc.
    parameters = Column(String)  # JSON string of model parameters
    performance_metric = Column(Float)