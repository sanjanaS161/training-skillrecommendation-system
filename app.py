import streamlit as st
import pandas as pd
import numpy as np

# Load dataset
df = pd.read_csv('employee_data_full.csv')

st.set_page_config(page_title="Training Dashboard", layout="wide")
st.title("🚀 Employee Training & Skills Dashboard")
st.markdown("This dashboard highlights skill gaps of employees and recommends training programs to improve their skills.")

# Department filter
department = st.selectbox("Select Department", ["All"] + list(df['Department'].unique()))
if department != "All":
    df = df[df['Department'] == department]

# Color-code skills
def color_skills(val):
    if val <= 1:
        color = '#8B0000'  # dark red = critical
    elif val <= 2:
        color = 'red'      # low
    elif val <= 4:
        color = 'orange'   # medium
    else:
        color = 'green'    # high
    return f'background-color: {color}'

skill_columns = ['Python', 'Excel', 'Communication', 'Leadership', 'Data Analysis', 'Project Management']

# Mapping skills to trainings
skill_to_training = {
    'Python': 'Python Basics',
    'Excel': 'Advanced Excel',
    'Communication': 'Effective Communication',
    'Leadership': 'Leadership Workshop',
    'Data Analysis': 'Data Analysis 101',
    'Project Management': 'Project Management Mastery'
}
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.ensemble import RandomForestClassifier

# Prepare training labels
# Convert TrainingsCompleted to list
df['TrainingsCompletedList'] = df['TrainingsCompleted'].str.split(', ')

# We will predict the next training (for simplicity, pick one missing training)
def next_training(row):
    for training in skill_to_training.values():
        if training not in row['TrainingsCompletedList']:
            return training
    return "No training needed"

df['NextTraining'] = df.apply(next_training, axis=1)

# Features: skill levels
X = df[skill_columns]
y = df['NextTraining']

# Train simple Random Forest
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X, y)

# Function to predict next training for any employee
def predict_training(row):
    features = row[skill_columns].values.reshape(1, -1)
    return clf.predict(features)[0]

# Apply prediction (optional: only for demo)
df['PredictedNextTraining'] = df.apply(predict_training, axis=1)

# Show in dashboard
st.subheader("ML Predicted Next Training for Employees")
st.write(df[['EmployeeID', 'Employee', 'Department'] + skill_columns + ['PredictedNextTraining']].head(20))

# Recommend trainings
def recommend_training(row):
    recs = [training for skill, training in skill_to_training.items() if row[skill] <= 2]
    return ", ".join(recs) if recs else "No training needed"

df['RecommendedTraining'] = df.apply(recommend_training, axis=1)

# --- Layout: Two columns ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Employee Skill Table")
    st.markdown("This table shows the current skill levels of each employee. Skills are color-coded: dark red = critical, red = low, orange = medium, green = high.")
    st.write(df.style.applymap(lambda x: color_skills(x) if isinstance(x, (int,float)) else '', subset=skill_columns))

with col2:
    st.subheader("Training Demand Overview")
    st.markdown("This chart shows the number of employees who need each training based on skill gaps. It helps HR prioritize training programs.")

    all_recommendations = df['RecommendedTraining'].str.split(', ').explode()
    training_count = all_recommendations.value_counts()
    st.bar_chart(training_count)

# --- Search employee ---
st.subheader("🔍 Search Employee")
st.markdown("You can search for any employee by ID or name to see their skill levels and recommended trainings.")
search_emp = st.text_input("Enter Employee ID or Name:")
if search_emp:
    search_results = df[df['EmployeeID'].str.contains(search_emp, case=False) | df['Employee'].str.contains(search_emp, case=False)]
    if not search_results.empty:
        st.write(search_results[['EmployeeID', 'Employee', 'Department'] + skill_columns + ['RecommendedTraining']])
    else:
        st.warning("No employee found!")

# --- Highlight critical skill gaps ---
st.subheader("Critical Skill Gaps (Skill ≤1)")
st.markdown("This table shows employees who have at least one critical skill gap (skill level ≤1). Immediate training is recommended for these employees.")
critical_employees = df[df[skill_columns].le(1).any(axis=1)]
st.write(critical_employees[['EmployeeID', 'Employee', 'Department'] + skill_columns])
