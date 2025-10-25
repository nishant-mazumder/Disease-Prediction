import pickle
import numpy as np
from django.conf import settings
import os


def load_model(model_name):
    """Load a pickle model from the ml_models directory."""
    model_path = os.path.join(settings.ML_MODELS_PATH, f"{model_name}.pkl")
    try:
        with open(model_path, 'rb') as file:
            model = pickle.load(file)
        return model
    except FileNotFoundError:
        raise FileNotFoundError(f"Model file {model_path} not found")
    except Exception as e:
        raise Exception(f"Error loading model {model_name}: {str(e)}")


def predict_diabetes(data):
    """Predict diabetes using the diabetes model."""
    model = load_model('diabetes_model2')
    
    # Convert input data to numpy array
    # features = np.array([
    #     data['pregnancies'],
    #     data['glucose'],
    #     data['blood_pressure'],
    #     data['skin_thickness'],
    #     data['insulin'],
    #     data['bmi'],
    #     data['diabetes_pedigree_function'],
    #     data['age']
    # ]).reshape(1, -1)
    features = np.array([
    int(data['pregnancies']),                   
    float(data['glucose']),                    
    float(data['blood_pressure']),              
    float(data['skin_thickness']),             
    float(data['insulin']),                     
    float(data['bmi']),                         
    float(data['diabetes_pedigree_function']),   
    int(data['age'])                            
    ]).reshape(1, -1)

    
    # Make prediction
    prediction = model.predict(features)[0]
    probability = model.predict_proba(features)[0]
    
    result = "Diabetic" if prediction == 1 else "Non-Diabetic"
    confidence = max(probability) * 100
    
    return {
        'prediction': result,
        'confidence': round(confidence, 2),
        'probability_positive': round(probability[1] * 100, 2),
        'probability_negative': round(probability[0] * 100, 2)
    }


def predict_heart_disease(data):
    """Predict heart disease using the heart disease model."""
    model = load_model('heart_disease_model')
    
    # Convert input data to numpy array
    # features = np.array([
    #     data['age'],
    #     data['sex'],
    #     data['cp'],
    #     data['trestbps'],
    #     data['chol'],
    #     data['fbs'],
    #     data['restecg'],
    #     data['thalach'],
    #     data['exang'],
    #     data['oldpeak'],
    #     data['slope'],
    #     data['ca'],
    #     data['thal']
    # ]).reshape(1, -1)
    features = np.array([
    int(data['age']),
    int(data['sex']),
    int(data['cp']),
    float(data['trestbps']),
    float(data['chol']),
    int(data['fbs']),
    int(data['restecg']),
    float(data['thalach']),
    int(data['exang']),
    float(data['oldpeak']),
    int(data['slope']),
    int(data['ca']),
    int(data['thal'])
    ]).reshape(1, -1)

    
    # Make prediction
    prediction = model.predict(features)[0]
    probability = model.predict_proba(features)[0]
    
    result = "Heart Disease" if prediction == 1 else "No Heart Disease"
    confidence = max(probability) * 100
    
    return {
        'prediction': result,
        'confidence': round(confidence, 2),
        'probability_positive': round(probability[1] * 100, 2),
        'probability_negative': round(probability[0] * 100, 2)
    }


def predict_parkinsons(data):
    """Predict Parkinson's disease using the Parkinson's model."""
    model = load_model('parkinsons_model2')
    
    # Convert input data to numpy array
    # features = np.array([
    #     data['fo'],
    #     data['fhi'],
    #     data['flo'],
    #     data['jitter_percent'],
    #     data['jitter_abs'],
    #     data['rap'],
    #     data['ppq'],
    #     data['ddp'],
    #     data['shimmer'],
    #     data['shimmer_db'],
    #     data['apq3'],
    #     data['apq5'],
    #     data['apq'],
    #     data['dda'],
    #     data['nhr'],
    #     data['hnr'],
    #     data['rpde'],
    #     data['dfa'],
    #     data['spread1'],
    #     data['spread2'],
    #     data['d2'],
    #     data['ppe']
    # ]).reshape(1, -1)
    features = np.array([
    float(data['fo']),
    float(data['fhi']),
    float(data['flo']),
    float(data['jitter_percent']),
    float(data['jitter_abs']),
    float(data['rap']),
    float(data['ppq']),
    float(data['ddp']),
    float(data['shimmer']),
    float(data['shimmer_db']),
    float(data['apq3']),
    float(data['apq5']),
    float(data['apq']),
    float(data['dda']),
    float(data['nhr']),
    float(data['hnr']),
    float(data['rpde']),
    float(data['dfa']),
    float(data['spread1']),
    float(data['spread2']),
    float(data['d2']),
    float(data['ppe'])
    ]).reshape(1, -1)

    
    # Make prediction
    prediction = model.predict(features)[0]
    probability = model.predict_proba(features)[0]
    
    result = "Parkinson's Disease" if prediction == 1 else "No Parkinson's Disease"
    confidence = max(probability) * 100
    
    return {
        'prediction': result,
        'confidence': round(confidence, 2),
        'probability_positive': round(probability[1] * 100, 2),
        'probability_negative': round(probability[0] * 100, 2)
    }
