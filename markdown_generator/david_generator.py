import os
import pandas as pd

# Define input CSV file
csv_file = "david_publications.csv"  # Update with actual CSV file name

# Define output directory (Ensure it exists before writing files)
output_dir = "../_publications"
os.makedirs(output_dir, exist_ok=True)

# Read CSV file and remove invalid characters
try:
    with open(csv_file, "r", encoding="utf-8", errors="ignore") as f:  # "ignore" removes bad characters
        df = pd.read_csv(f)
    print("Successfully read CSV (invalid characters removed).")
except Exception as e:
    print(f"Error reading CSV: {e}")
    exit(1)

# Function to clean and format filenames
def clean_filename(title, max_length=80):
    """Cleans a title to be used as a filename, ensuring it is not too long."""
    title = str(title) if pd.notna(title) else "untitled"  # Convert to string and handle NaN
    filename = "".join(c for c in title if c.isalnum() or c in (" ", "_", "-")).rstrip().replace(" ", "-").lower()
    return filename[:max_length]  # Truncate long filenames

# Function to escape special characters for YAML
def escape_yaml(text):
    """Ensures all text is a string and removes non-ASCII characters."""
    if pd.isna(text):  # Handle NaN values
        return ""
    return str(text).encode("ascii", "ignore").decode()  # Convert to string & remove non-ASCII characters

# Generate markdown files
for index, row in df.iterrows():
    # Ensure 'Year' is treated as a string and handle float years (like 2025.0)
    year = str(row["Year"]).split(".")[0] if pd.notna(row["Year"]) else "unknown"

    # Convert title to string and clean it for the filename
    filename_slug = clean_filename(row["Title"], max_length=80)  # Limit length
    md_filename = f"{year}-{filename_slug}.md"

    # Ensure full path uses forward slashes (Windows fix)
    md_filepath = os.path.join(output_dir, md_filename).replace("\\", "/")

    # Construct markdown content
    markdown_content = f"""---
title: "{escape_yaml(row['Title'])}"
collection: publications
permalink: /publication/{filename_slug}
year: "{year}"
group: "{escape_yaml(row['Group'])}"
venue: "{escape_yaml(row['Venue'])}"
category: "{escape_yaml(row['Category'])}"
published_link: "{escape_yaml(row.get('Published Link', ''))}"
pdf: "{escape_yaml(row.get('PDF', ''))}"
apa_citation: "{escape_yaml(row['APA Citation'])}"
co-authors:
  - "{escape_yaml(row.get('Co-Author1', ''))}"
  - "{escape_yaml(row.get('Co-Author2', ''))}"
  - "{escape_yaml(row.get('Co-Author3', ''))}"
  - "{escape_yaml(row.get('Co-Author4', ''))}"
  - "{escape_yaml(row.get('Co-Author5', ''))}"
  - "{escape_yaml(row.get('Co-Author6', ''))}"
---
"""

    # Ensure output directory exists before writing (Redundant check for safety)
    os.makedirs(output_dir, exist_ok=True)

    # Write markdown file
    with open(md_filepath, "w", encoding="utf-8") as f:
        f.write(markdown_content)

    print(f"Generated: {md_filepath}")

print("Markdown generation complete.")
