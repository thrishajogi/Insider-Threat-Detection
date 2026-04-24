# 🔐 Insider Threat Detection System

An AI-based insider threat detection system that uses machine learning and real-time monitoring to identify suspicious user behavior.

## 🚀 Features

- Machine Learning-based risk prediction (Random Forest)
- Risk scoring (Low / Medium / High)
- Real-time dashboard using Streamlit
- High-risk alert system
- Camera-based user presence detection
- Role-based access (Admin / Viewer)

## 🧠 Tech Stack

- Python
- Scikit-learn
- Pandas, NumPy
- Streamlit
- OpenCV

## 📊 How it Works

1. User behavior data is analyzed using a trained ML model
2. The model predicts whether activity is malicious
3. Risk levels are assigned (Low / Medium / High)
4. A live dashboard displays alerts and activity
5. Camera verifies user presence for access control

## ▶️ Run the Project

```bash
pip install -r requirements.txt
streamlit run app.py