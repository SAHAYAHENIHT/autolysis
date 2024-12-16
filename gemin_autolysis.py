import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from dotenv import load_dotenv
import google.generativeai as genai

# Step 1: Load Environment Variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  # Renamed for clarity
if not GEMINI_API_KEY:
    raise EnvironmentError("GEMINI_API_KEY environment variable is not set.")

# Step 2: Handle Command-line Arguments
if len(sys.argv) != 2:
    raise ValueError("Usage: uv run autolysis.py <dataset.csv>")
filename = sys.argv[1]

# Step 3: Load and Explore the Dataset
try:
    # Attempt to read the file with UTF-8 encoding
    df = pd.read_csv(filename)
except UnicodeDecodeError:
    print("UTF-8 decoding failed. Trying alternative encodings...")

    # Retry with common alternative encodings
    encodings = ['latin1', 'ISO-8859-1', 'cp1252', 'utf-16', 'utf-32']
    for encoding in encodings:
        try:
            df = pd.read_csv(filename, encoding=encoding)
            print(f"Successfully loaded the dataset using {encoding} encoding.")
            break
        except Exception as e:
            print(f"Failed with {encoding}: {e}")
    else:
        raise ValueError("Failed to load the dataset with common encodings. Please check the file encoding.")

print("\nDataset loaded successfully!")
print("Columns in the dataset:", df.columns.tolist())
print("\nBasic Statistics:")
print(df.describe(include='all'))

# Step 4: Perform Basic Analysis
print("\nMissing Values:")
print(df.isnull().sum())

# Select only numerical columns for correlation
numeric_columns = df.select_dtypes(include=['number'])
correlation_matrix = numeric_columns.corr()

print("Correlation Matrix (numerical columns):")
print(correlation_matrix)

# Step 6: Visualizations and Folder Creation

# Define output folder as 'gemini_dataset'
output_folder = f"gemini_{os.path.splitext(os.path.basename(filename))[0]}"


# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# 1. Correlation Matrix Heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title("Correlation Matrix Heatmap")
plt.tight_layout()
heatmap_file = os.path.join(output_folder, "correlation_matrix.png")
plt.savefig(heatmap_file)
plt.show()

# 2. Distribution of Numerical Columns (Histograms for each numerical column)
numeric_columns.hist(bins=15, figsize=(15, 10), edgecolor='black')
plt.suptitle('Distribution of Numerical Columns')
plt.tight_layout()
histogram_file = os.path.join(output_folder, "distribution_histograms.png")
plt.savefig(histogram_file)
plt.show()

# 3. Pairplot (Scatter plot matrix) for numerical columns
sns.pairplot(numeric_columns)
plt.suptitle('Pairplot of Numerical Columns', y=1.02)
plt.tight_layout()
pairplot_file = os.path.join(output_folder, "pairplot.png")
plt.savefig(pairplot_file)
plt.show()

# Step 5: Integrate LLM for Suggestions (using Gemini API)

# Replace 'YOUR_API_KEY' with your actual Gemini API key
genai.configure(api_key=GEMINI_API_KEY)  # Use environment variable for API key

# Choose the appropriate model (e.g., "gemini-pro" or "gemini-flash")
model = genai.GenerativeModel("gemini-pro")  # Adjust model name based on your needs

# Prepare the prompt with data insights
prompt = f"Analyze the following dataset:\nColumns: {list(df.columns)}\nSummary: {df.describe(include='all')}"

try:
    # Call the generate_content method without max_tokens if not supported
    response = model.generate_content(prompt)
    suggestions = response.text

    print("\nLLM Suggestions (using Gemini):")
    print(suggestions)

except Exception as e:
    print("\nFailed to fetch suggestions from the LLM:", e)
    suggestions = ""

# Step 6: Generate README.md
description = f"The dataset contains the following columns: {', '.join(df.columns)}."
insights = "Based on the analysis, here are the main insights:\n" + suggestions
implications = "These findings suggest the following actions:\n - Further exploration of key variables.\n - Addressing missing values.\n - Implementing suggested analyses."

# Generate README content
readme_content = f"""
# Analysis Report

## Dataset Overview
{description}

## Key Insights
{insights}

## Implications
{implications}

## Visualizations
![Correlation Matrix](correlation_matrix.png)
![Distribution of Numerical Columns](distribution_histograms.png)
![Pairplot of Numerical Columns](pairplot.png)
"""

# Define the README file path
readme_file = os.path.join(output_folder, "README.md")

# Save the README file
with open(readme_file, "w") as file:
    file.write(readme_content)

print(f"\nREADME.md generated successfully: {readme_file}")
