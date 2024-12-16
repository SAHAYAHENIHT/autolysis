import os
import sys
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import openai

# Initialize OpenAI API
openai.api_base = "https://aiproxy.sanand.workers.dev/openai/"
openai.api_key = os.environ.get("eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjIzZjIwMDUwNzZAZHMuc3R1ZHkuaWl0bS5hYy5pbiJ9.5QMcbJqvYakIV_5_JaAvpETvFUu4JfVSIK2iw2JEd1E")

def load_data(filename):
    """Load CSV data into a Pandas DataFrame."""
    try:
        # Try reading the file with a different encoding
        data = pd.read_csv(filename, encoding='latin1')  # Use 'latin1' or 'ISO-8859-1'
        print(f"Loaded dataset: {filename}")
        return data
    except Exception as e:
        print(f"Error loading dataset: {e}")
        sys.exit(1)

def basic_analysis(data):
    """Perform basic analysis and return insights."""
    summary = data.describe(include="all").transpose()
    missing_values = data.isnull().sum()
    return summary, missing_values

def visualize_data(data, output_dir):
    """
    Generate visualizations based on the dataset.
    This includes a heatmap of correlations and other relevant visualizations.
    """
    # Filter only numeric columns for correlation matrix
    numeric_data = data.select_dtypes(include=['number'])  # Select only numeric columns
    
    if numeric_data.empty:
        print("No numeric data found for correlation matrix.")
        return

    # Plot correlation heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(numeric_data.corr(), annot=True, cmap="coolwarm")
    heatmap_path = os.path.join(output_dir, "correlation_heatmap.png")
    plt.title("Correlation Heatmap")
    plt.savefig(heatmap_path)
    plt.close()
    print(f"Correlation heatmap saved to {heatmap_path}")

    # Example of other visualizations (modify as needed)
    # Distribution plot for each numeric column
    for col in numeric_data.columns:
        plt.figure(figsize=(8, 6))
        sns.histplot(data[col].dropna(), kde=True, bins=30)
        plt.title(f"Distribution of {col}")
        distribution_path = os.path.join(output_dir, f"{col}_distribution.png")
        plt.savefig(distribution_path)
        plt.close()
        print(f"Distribution plot for {col} saved to {distribution_path}")


def generate_story(data, summary, missing_values, output_dir):
    """Use AI Proxy to generate a Markdown story."""
    columns_info = str(data.dtypes)
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a data analyst assistant."},
                {"role": "user", "content": f"Analyze this dataset. Columns: {columns_info}, Missing Values: {missing_values}. Summary: {summary}."}
            ],
        )
        story = response['choices'][0]['message']['content']
    except Exception as e:
        story = f"Failed to generate story: {e}"

    # Write the story to README.md
    with open(f"{output_dir}/README.md", "w") as file:
        file.write(story)

def main():
    if len(sys.argv) != 2:
        print("Usage: uv run autolysis.py <dataset.csv>")
        sys.exit(1)

    # Get dataset filename
    filename = sys.argv[1]
    dataset_name = filename.split('.')[0]
    output_dir = f"./{dataset_name}"

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    # Load data
    data = load_data(filename)

    # Basic analysis
    summary, missing_values = basic_analysis(data)

    # Visualize data
    visualize_data(data, output_dir)

    # Generate story
    generate_story(data, summary, missing_values, output_dir)

if __name__ == "__main__":
    main()
