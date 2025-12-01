import pandas as pd
import numpy as np

# For reproducibility
np.random.seed(42)

# Number of employees
num_employees = 500

# Departments
departments = ['IT', 'Sales', 'HR', 'Finance', 'Marketing', 'Operations']

# Skills
skills = ['Python', 'Excel', 'Communication', 'Leadership', 'Data Analysis', 'Project Management']

# Trainings
trainings = ['Python Basics', 'Advanced Excel', 'Effective Communication', 
             'Leadership Workshop', 'Data Analysis 101', 'Project Management Mastery']

# Example employee names
names = ['Alice', 'Bob', 'Charlie', 'David', 'Eva', 'Frank', 'Grace', 'Hannah', 'Ian', 'Julia']
employee_names = [np.random.choice(names) for _ in range(num_employees)]

# Generate dataset
data = []
for i in range(1, num_employees + 1):
    emp_id = f"E{i:04d}"
    dept = np.random.choice(departments)
    
    skill_levels = {skill: np.random.randint(1, 6) for skill in skills}
    
    completed_trainings = np.random.choice(trainings, size=np.random.randint(1, 4), replace=False)
    
    data.append({
        'EmployeeID': emp_id,
        'Employee': employee_names[i-1],
        'Department': dept,
        **skill_levels,
        'TrainingsCompleted': ", ".join(completed_trainings)
    })

# Create DataFrame and save
df = pd.DataFrame(data)
df.to_csv('employee_data_full.csv', index=False)

print("Dataset created with shape:", df.shape)
print(df.head(10))
