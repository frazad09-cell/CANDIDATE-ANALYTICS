# 💼 Candidate Analytics — HR Job Placement Prediction

> End-to-end **Data Analytics + Machine Learning + Streamlit** project for analyzing candidate performance and job placement outcomes.

## 📌 Project Overview

This project analyzes candidate academic performance, skills, experience, interview performance, and employment-related factors. It covers the complete workflow from data cleaning and exploratory analysis to machine-learning classification, MySQL integration, and an executive Streamlit dashboard.

## 🎯 Objectives

- Understand factors associated with candidate placement outcomes
- Clean and preprocess HR candidate data
- Perform statistical relationship analysis and EDA
- Engineer meaningful academic, interview, skills, and readiness features
- Compare multiple classification algorithms
- Store engineered data in MySQL
- Present key HR metrics in an interactive Streamlit dashboard

## 🔄 Project Workflow

```text
Raw HR Data
     ↓
Data Understanding
     ↓
Data Cleaning & Preprocessing
     ↓
Encoding & Feature Scaling
     ↓
Statistical Analysis + EDA
     ↓
Feature Engineering
     ↓
MySQL Storage
     ↓
Machine Learning
     ↓
Model Evaluation
     ↓
Streamlit HR Dashboard
```

## 🧹 Data Preprocessing

The project standardizes categorical labels, removes duplicates, handles missing numerical values with the median and categorical values with the mode, encodes categorical variables, and applies StandardScaler to numerical features.

## 🛠️ Feature Engineering

| Feature | Description |
|---|---|
| Academic Score | Average of SSC, HSC and degree percentages |
| Experience Category | Candidate experience grouping |
| Skills Match Level | Low / Medium / High skills alignment |
| Interview Score | Average of technical, aptitude and communication scores |
| Interview Performance | Interview performance band |
| Placement Readiness Score | Weighted candidate-readiness indicator |

### Placement Readiness Score

The project-defined score combines:

- Academic Score — **25%**
- Skills Match — **30%**
- Technical Score — **20%**
- Aptitude Score — **10%**
- Communication Score — **15%**

> The readiness score is an analytical business score, not a machine-learning probability.

## 🤖 Machine Learning Models

Five classification algorithms are compared:

| Model | Purpose |
|---|---|
| Logistic Regression | Baseline linear classifier |
| Decision Tree | Rule-based classification |
| Random Forest | Ensemble tree classifier |
| K-Nearest Neighbors | Distance-based classification |
| Gradient Boosting | Boosted ensemble classifier |

Primary evaluation metrics: **Accuracy, Precision, Recall and F1 Score**.

## 📊 Streamlit Dashboard

The project includes a premium **HR Placement Intelligence** dashboard with candidate filters, management insights, placement overview, adjustable high-risk threshold, KPI definitions, and candidate-data exploration.

### Executive KPIs

| KPI | Description |
|---|---|
| 👥 Total Candidates | Candidate records after cleaning/filtering |
| 🎯 Placement Rate | Percentage of candidates with placed status |
| 🤝 Job Acceptance Rate | Uses placed status as the available proxy |
| ⭐ Average Interview Score | Mean interview performance |
| 🧩 Average Skills Match | Mean skills-match percentage |
| 📉 Offer Dropout Rate | N/A because no explicit dropout field exists |
| ⚠️ High-Risk Candidates | Candidates below the selected readiness threshold |

## 🗄️ MySQL Integration

The engineered candidate dataset can be stored in MySQL using **SQLAlchemy + PyMySQL**, enabling SQL-based analysis and reporting.

## 🧰 Tech Stack

`Python` · `Pandas` · `NumPy` · `Matplotlib` · `Seaborn` · `SciPy` · `Scikit-learn` · `MySQL` · `SQLAlchemy` · `Streamlit` · `Jupyter Notebook` · `VS Code`

## 🚀 Run the Streamlit Dashboard

Place `HR.csv` and the Streamlit Python file in the same project folder.

```bash
pip install streamlit pandas numpy scikit-learn
streamlit run app.py
```

## 📁 Suggested Repository Structure

```text
CANDIDATE-ANALYTICS/
├── HR.csv
├── HR_Job_Placement_Analysis.ipynb
├── app.py
├── requirements.txt
├── README.md
└── reports/
    └── HR_Job_Placement_3_Page_Report.docx
```

## ⚠️ Dataset Notes

The current project data does not contain separate offer-acceptance or offer-dropout fields. Placement status is therefore used as the available proxy for Job Acceptance Rate, while Offer Dropout Rate is displayed as **N/A**. High-risk percentage is a configurable readiness-score business rule rather than model-predicted risk.

## ✨ Project Highlights

**End-to-End Analytics** · **Feature Engineering** · **5 ML Models** · **MySQL Integration** · **Interactive Streamlit Dashboard** · **Executive HR KPIs**

---

### 👨‍💻 Candidate Analytics Project

Built as a practical HR analytics and machine-learning portfolio project.
