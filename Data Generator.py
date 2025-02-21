import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta

# Initialize Faker for realistic data generation
fake = Faker()

# Function to generate a random project ID with numbers and underscores
def generate_project_id():
    return f"{fake.random_int(min=1000, max=9999)}_{fake.random_int(min=1000, max=9999)}"

# Function to generate synthetic data
def generate_synthetic_data(num_rows=30):
    data = []
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 3, 31)

    project_demand_ranges = {}  # Dictionary to store demand range per project

    for _ in range(num_rows):
        project_id = generate_project_id()  # Assign unique project ID

        # Assign a demand range based on project ID (choose randomly)
        if project_id not in project_demand_ranges:
            project_demand_ranges[project_id] = random.choice([(50, 60), (70, 80),(90, 100),(30,40)])

        demand_low, demand_high = project_demand_ranges[project_id]  # Get the assigned range

        row = {
            "Portfolioshare": random.choice(["SE-SCT", "QA-TST", "WQ-AI", "AFRIC"]),
            "Program": fake.word(),
            "Activity name": fake.sentence(nb_words=3),
            "Project ID": project_id,
            "Project type": random.choice(["IT", "NON IT", "Development", "Maintenance"]),
            "Charging key": random.choice(["", "Key1", "Key2", "Key3"]),
            "Priority Evaluation": random.choice(["High", "Medium", "Low", ""]),
            "Activity responsible (IT)": fake.name(),
            "Activity responsible (customer)": fake.name(),
            "Sponsor business unit (customer)": fake.company(),
            "Project region": random.choice(["USA", "IND", "EUR", "ASIA"]),
            "Planned start": start_date,
            "Planned finish": end_date,
            "Total": random.randint(500, 10000),
            "Published Forecast (F)": random.randint(500, 10000),
            "Demand (D)": random.randint(500, 10000),
            "Supply (S)": random.randint(500, 10000),
            "F vs. S": random.randint(-5000, 5000),
            "D vs. S": random.randint(-5000, 5000),
            "Capacity Demand (BAC)": random.randint(500, 10000),
        }

        # Add monthly data for 3 years (2023, 2024)
        for year in [2023, 2024]:
            for month in ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]:
                row[f"{month} {year} Published Forecast (F) (Day)"] = random.randint(10, 100)

                # Generate Demand within assigned range (ensuring <= 10 variation)
                base_demand = random.randint(demand_low, demand_high)  # Assign base demand for the project
                row[f"{month} {year} Demand (D) (Day)"] = base_demand
                
                # Generate Supply with some variation
                row[f"{month} {year} Supply (S) (Day)"] = base_demand + random.randint(-10, 10)
                
                # Calculate differences
                row[f"{month} {year} F vs. S"] = row[f"{month} {year} Published Forecast (F) (Day)"] - row[f"{month} {year} Supply (S) (Day)"]
                row[f"{month} {year} D vs. S"] = row[f"{month} {year} Demand (D) (Day)"] - row[f"{month} {year} Supply (S) (Day)"]

        data.append(row)

    return pd.DataFrame(data)

# Generate the dataset
synthetic_data = generate_synthetic_data(num_rows=30)

# Save to CSV
synthetic_data.to_csv("syntheticdata_2yconsistent.csv", index=False)
