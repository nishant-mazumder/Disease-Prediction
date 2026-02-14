# 🩺 Disease Prediction System

A smart and user-friendly **disease prediction system** for diabetes, heart disease, and Parkinson’s built using **Django, SQLite, and Machine Learning**. Users can predict diseases by inputting their health parameters and also interact with a chatbot for guidance.

---

## 🎯 Objectives

- Predict the likelihood of diabetes, heart disease, and Parkinson’s using trained ML models  
- Provide a user-friendly web interface for predictions  
- Allow users to interact with a chatbot to get health guidance  
- Store user inputs and appointment data securely in a database 

---

## 🧠 Machine Learning Approach

- **Algorithms Used:** Support Vector Machine (SVM), Logistic Regression  
- **Datasets:** Publicly available datasets for diabetes, heart disease, and Parkinson’s  
- **Process:**  
  1. Collected and preprocessed datasets  
  2. Trained ML models for each disease  
  3. Integrated trained models with the Django backend to provide real-time predictions
     
---

## 🏗️ System Architecture / Workflow

1. **Frontend:** Users input their health parameters via web forms built with HTML, CSS, and JavaScript  
2. **Backend:** Django handles requests, runs predictions using the trained ML models, and interacts with the SQLite database  
3. **Database:** SQLite stores user data, prediction results, and doctor appointment details  
4. **Chatbot:** Users can chat with the trained ML models for disease guidance and additional information  
5. **Results:** Users receive predictions and advice instantly via the web interface

---

## 💻 Technologies Used

- **Frontend:** HTML, CSS, JavaScript  
- **Backend:** Django  
- **Database:** SQLite  
- **Machine Learning:** Scikit-learn (SVM, Logistic Regression)  
- **Deployment:** Local server (Django runserver)  

---

## 📊 Results

- Accurately predicts the probability of diabetes, heart disease, and Parkinson’s based on user input  
- Provides instant feedback via the web interface and chatbot  
- Enables storage and management of user data for follow-up or further analysis  

---

## ✅ Advantages

- User-friendly interface for non-technical users  
- Multi-disease prediction system in a single platform  
- Chatbot provides an interactive experience for users  
- Full-stack integration demonstrating frontend, backend, database, and ML workflow  

---

## ⚠️ Limitations

- Depends on the quality and completeness of the dataset  
- Cannot replace professional medical diagnosis  
- Limited to the input features available in the datasets  

---

## 📜 Disclaimer

This application is intended for **educational purposes only** and **should not be used as a substitute for professional medical advice or diagnosis**. Always consult a healthcare professional for accurate diagnosis and treatment.  

---

## ⚙️ Setup & Installation

1. Clone the repository:
   https://github.com/nishant-mazumder/Disease-Prediction.git

2. Create a virtual environment:
   python -m venv venv

3. Activate the virtual environment:
   .\venv\Scripts\Activate.ps1
   
4. Install dependencies
   pip install -r requirements.txt

5. Run migrations:
   python manage.py migrate

6. Start the server:
   python manage.py runserver


