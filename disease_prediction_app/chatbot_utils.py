import re
import random
import pandas as pd
import numpy as np
import csv
import os
from django.conf import settings
from sklearn import preprocessing
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from difflib import get_close_matches
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

class HealthChatbot:
    def __init__(self):
        self.model = None
        self.le = None
        self.symptoms_dict = {}
        self.severity_dictionary = {}
        self.description_list = {}
        self.precaution_dictionary = {}
        self.cols = None
        self.training = None
        self.quotes = [
            "⚡ Health is wealth, take care of yourself.",
            "⚡ A healthy outside starts from the inside.",
            "⚡ Every day is a chance to get stronger and healthier.",
            "⚡ Take a deep breath, your health matters the most.",
            "⚡ Remember, self-care is not selfish."
        ]
        self.symptom_synonyms = {
            "stomach ache": "stomach_pain",
            "belly pain": "stomach_pain",
            "tummy pain": "stomach_pain",
            "loose motion": "diarrhea",
            "motions": "diarrhea",
            "high temperature": "fever",
            "temperature": "fever",
            "feaver": "fever",
            "coughing": "cough",
            "throat pain": "sore_throat",
            "cold": "chills",
            "breathing issue": "breathlessness",
            "shortness of breath": "breathlessness",
            "body ache": "muscle_pain",
        }
        self.initialize_model()

    def initialize_model(self):
        """Initialize the ML model and load data"""
        try:
            # Load training data
            training_path = os.path.join(settings.BASE_DIR, 'chatbot', 'Data', 'Training.csv')
            self.training = pd.read_csv(training_path)
            
            # Clean duplicate column names
            self.training.columns = self.training.columns.str.replace(r"\.\d+$", "", regex=True)
            self.training = self.training.loc[:, ~self.training.columns.duplicated()]
            
            # Features and labels
            self.cols = self.training.columns[:-1]
            x = self.training[self.cols]
            y = self.training['prognosis']
            
            # Label Encoding
            self.le = preprocessing.LabelEncoder()
            y = self.le.fit_transform(y)
            
            # Train-test split
            x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.33, random_state=42)
            
            # Model
            self.model = RandomForestClassifier(n_estimators=300, random_state=42)
            self.model.fit(x_train, y_train)
            
            # Create symptoms dictionary
            self.symptoms_dict = {symptom: idx for idx, symptom in enumerate(self.cols)}
            
            # Load additional data
            self.load_severity_dict()
            self.load_description_list()
            self.load_precaution_dict()
            
        except Exception as e:
            print(f"Error initializing model: {e}")
            self.model = None

    def load_severity_dict(self):
        """Load symptom severity data"""
        try:
            severity_path = os.path.join(settings.BASE_DIR, 'chatbot', 'MasterData', 'symptom_severity.csv')
            with open(severity_path) as csv_file:
                for row in csv.reader(csv_file):
                    try:
                        self.severity_dictionary[row[0]] = int(row[1])
                    except:
                        pass
        except Exception as e:
            print(f"Error loading severity dictionary: {e}")

    def load_description_list(self):
        """Load symptom descriptions"""
        try:
            desc_path = os.path.join(settings.BASE_DIR, 'chatbot', 'MasterData', 'symptom_Description.csv')
            with open(desc_path) as csv_file:
                for row in csv.reader(csv_file):
                    self.description_list[row[0]] = row[1]
        except Exception as e:
            print(f"Error loading description list: {e}")

    def load_precaution_dict(self):
        """Load precaution data"""
        try:
            prec_path = os.path.join(settings.BASE_DIR, 'chatbot', 'MasterData', 'symptom_precaution.csv')
            with open(prec_path) as csv_file:
                for row in csv.reader(csv_file):
                    self.precaution_dictionary[row[0]] = [row[1], row[2], row[3], row[4]]
        except Exception as e:
            print(f"Error loading precaution dictionary: {e}")

    def extract_symptoms(self, user_input):
        """Extract symptoms from user input"""
        extracted = []
        text = user_input.lower().replace("-", " ")

        # 1. Synonym replacement
        for phrase, mapped in self.symptom_synonyms.items():
            if phrase in text:
                extracted.append(mapped)

        # 2. Exact match
        for symptom in self.cols:
            if symptom.replace("_", " ") in text:
                extracted.append(symptom)

        # 3. Fuzzy match (typo handling)
        words = re.findall(r"\w+", text)
        for word in words:
            close = get_close_matches(word, [s.replace("_", " ") for s in self.cols], n=1, cutoff=0.8)
            if close:
                for sym in self.cols:
                    if sym.replace("_", " ") == close[0]:
                        extracted.append(sym)

        return list(set(extracted))

    def predict_disease(self, symptoms_list):
        """Predict disease based on symptoms"""
        if not self.model:
            return None, 0, None
            
        input_vector = np.zeros(len(self.symptoms_dict))
        for symptom in symptoms_list:
            if symptom in self.symptoms_dict:
                input_vector[self.symptoms_dict[symptom]] = 1

        pred_proba = self.model.predict_proba([input_vector])[0]
        pred_class = np.argmax(pred_proba)
        disease = self.le.inverse_transform([pred_class])[0]
        confidence = round(pred_proba[pred_class] * 100, 2)
        return disease, confidence, pred_proba

    def get_disease_description(self, disease):
        """Get description for a disease"""
        return self.description_list.get(disease, 'No description available.')

    def get_disease_precautions(self, disease):
        """Get precautions for a disease"""
        return self.precaution_dictionary.get(disease, [])

    def get_random_quote(self):
        """Get a random empathy quote"""
        return random.choice(self.quotes)

    def get_related_symptoms(self, disease, current_symptoms):
        """Get related symptoms for a disease"""
        if self.training is None:
            return []
            
        disease_symptoms = list(self.training[self.training['prognosis'] == disease].iloc[0][:-1].index[
            self.training[self.training['prognosis'] == disease].iloc[0][:-1] == 1
        ])
        
        # Return symptoms not already mentioned
        return [symptom for symptom in disease_symptoms if symptom not in current_symptoms]

# Global chatbot instance
chatbot_instance = None

def get_chatbot():
    """Get or create chatbot instance"""
    global chatbot_instance
    if chatbot_instance is None:
        chatbot_instance = HealthChatbot()
    return chatbot_instance


