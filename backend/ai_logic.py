
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np

def train_model(data, target, model_type='random_forest'):
    X_train, X_test, y_train, y_test = train_test_split(data, target, test_size=0.2, random_state=42)
    
    if model_type == 'random_forest':
        model = RandomForestClassifier(n_estimators=100, random_state=42)
    else:
        raise ValueError(f"Unsupported model type: {model_type}")
    
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    return model, accuracy

def save_model(model, filename):
    joblib.dump(model, filename)

def load_model(filename):
    return joblib.load(filename)

def predict(model, input_data):
    return model.predict(input_data)

# Usage in API route (main.py)

@app.post("/train_model/")
def train_ai_model(training_data: schemas.TrainingData, db: Session = Depends(get_db)):
    data = np.array(training_data.data)
    target = np.array(training_data.target)
    
    model, accuracy = train_model(data, target, model_type=training_data.model_type)
    
    model_filename = f"{training_data.model_type}_{training_data.name}.joblib"
    save_model(model, model_filename)
    
    db_model = models.AIModel(
        name=training_data.name,
        type=training_data.model_type,
        parameters=str(model.get_params()),
        performance_metric=accuracy
    )
    db.add(db_model)
    db.commit()
    
    return {"message": "Model trained successfully", "accuracy": accuracy}

@app.post("/predict/")
def make_prediction(prediction_request: schemas.PredictionRequest, db: Session = Depends(get_db)):
    db_model = db.query(models.AIModel).filter(models.AIModel.name == prediction_request.model_name).first()
    if db_model is None:
        raise HTTPException(status_code=404, detail="Model not found")
    
    model_filename = f"{db_model.type}_{db_model.name}.joblib"
    model = load_model(model_filename)
    
    input_data = np.array(prediction_request.input_data).reshape(1, -1)
    prediction = predict(model, input_data)
    
    return {"prediction": prediction.tolist()}