# 🎯 Lead Scoring Prediction App

A machine learning-powered web application to predict lead conversion probability and prioritize sales efforts.

## 🚀 Features

- Upload CSV files with lead data
- Get instant conversion probability predictions
- Download results with lead scores
- Visual score distribution
- Color-coded priority levels

## 📦 Installation

### Local Setup

1. Clone the repository:
```bash
git clone <your-repo-url>
cd lead-scoring-app
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Generate sample training data (optional):
```bash
python create_sample_data.py
```

4. Train the model:
```bash
python train_model.py
```

5. Run the app:
```bash
streamlit run app.py
```

## 📊 Required CSV Format

Your CSV file should contain the following columns:

| Column | Type | Example Values |
|--------|------|----------------|
| Email_Source | Text | Google, Facebook, Direct, Referral, LinkedIn |
| Contacted | Text | Yes, No |
| Location | Text | Mumbai, Delhi, Bangalore |
| Profession | Text | Student, Working Professional, Unemployed |
| Course_Interest | Text | Data Science, Web Development, AI/ML |

## 🌐 Deployment

### Deploy to Streamlit Cloud

1. Push your code to GitHub (make sure `.pkl` files are included)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click "New app"
4. Select your repository
5. Set main file path to `app.py`
6. Click "Deploy"

## 📁 Project Structure

```
lead-scoring-app/
├── app.py                  # Streamlit web app
├── train_model.py          # Model training script
├── create_sample_data.py   # Sample data generator
├── requirements.txt        # Python dependencies
├── best_model.pkl         # Trained model (generated)
├── scaler.pkl             # Feature scaler (generated)
├── label_encoders.pkl     # Label encoders (generated)
├── .gitignore             # Git ignore file
└── README.md              # This file
```

## 🎯 Model Performance

The app uses the best performing model from:
- Logistic Regression
- Random Forest
- Gradient Boosting

Model selection is based on ROC-AUC score.

## 📝 License

MIT License

## 👤 Author

Your Name

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!