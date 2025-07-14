import os
import csv
import requests
import time
import re

# --- Configuration ---
# Make sure this matches the name of your CSV file.
CSV_FILENAME = "arxiv_survey_results.csv" 
# The folder where PDFs will be saved.
OUTPUT_FOLDER = "phase1"
# Column names in your CSV file.
URL_COLUMN = 'url'
TITLE_COLUMN = 'title'

def sanitize_filename(filename):
    """
    Cleans a string to be a valid filename.
    Removes illegal characters and limits length.
    """
    # Remove illegal characters for most file systems
    sanitized = re.sub(r'[\\/*?:"<>|]', "", filename)
    # Replace spaces with underscores
    sanitized = sanitized.replace(' ', '_')
    # Limit filename length to avoid issues (e.g., 150 chars)
    return sanitized[:150]

# --- Main Script ---

# 1. Create the output folder if it doesn't exist
try:
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    print(f"📁 Output folder '{OUTPUT_FOLDER}' is ready.")
except OSError as e:
    print(f"Error creating directory {OUTPUT_FOLDER}: {e}")
    exit()

# 2. Check if the CSV file exists
if not os.path.exists(CSV_FILENAME):
    print(f"❌ Error: The file '{CSV_FILENAME}' was not found.")
    print("Please make sure the script is in the same directory as your CSV file.")
    exit()

# 3. Read the CSV and download PDFs
papers_to_download = []
with open(CSV_FILENAME, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        papers_to_download.append(row)

print(f"\nFound {len(papers_to_download)} papers in the CSV to process.")

for i, paper in enumerate(papers_to_download):
    title = paper.get(TITLE_COLUMN, f"untitled_paper_{i}")
    url = paper.get(URL_COLUMN)
    for file in os.listdir(OUTPUT_FOLDER):
        if file.startswith(f"arxiv_{i+1}"):
            print(f"✅ SKIPPING: File already exists at '{file}'")
            continue
    if not url:
        print(f"⚠️ SKIPPING: No URL found for title: '{title}'")
        continue

    # Create a safe filename from the title with download order index
    safe_filename = f"arxiv_{i+1}_{sanitize_filename(title)}.pdf"
    output_path = os.path.join(OUTPUT_FOLDER, safe_filename)

    print(f"\n[{i+1}/{len(papers_to_download)}] Processing: {title}")

    # Check if the file already exists to avoid re-downloading
    if os.path.exists(output_path):
        print(f"✅ SKIPPING: File already exists at '{output_path}'")
        continue

    try:
        # Download the PDF
        print(f"   Downloading from: {url}")
        response = requests.get(url, timeout=30) # 30-second timeout
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

        # Save the PDF to the file
        with open(output_path, 'wb') as pdf_file:
            pdf_file.write(response.content)
        print(f"   ✅ Success! Saved to '{output_path}'")

    except requests.exceptions.RequestException as e:
        print(f"   ❌ FAILED to download. Error: {e}")

    # Be polite to arXiv's servers by waiting between requests
    time.sleep(2)

print("\n🎉 Download process complete!")