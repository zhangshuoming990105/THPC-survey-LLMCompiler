import csv
import os

# --- Configuration ---
# Update these filenames to match your files exactly.
ARXIV_CSV = "arxiv_survey_results.csv"
GOOGLE_SCHOLAR_CSV = "google_scholar_results_with_status.csv"
OUTPUT_CSV = "phase2_to_be_categorized.csv"

# --- Main Script ---
print("🚀 Starting CSV finalization process...")

merged_data = []
seen_titles = set()

# 1. Read and process the arXiv CSV
try:
    with open(ARXIV_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            title = row.get('title', '').strip()
            # Normalize title for duplicate checking
            normalized_title = title.lower()
            
            if title and normalized_title not in seen_titles:
                # Extract the year from the 'date-year' column (e.g., '2023-10-25')
                year = row.get('date-year', '')[:4]
                merged_data.append({'title': title, 'year': year})
                seen_titles.add(normalized_title)
    print(f"✅ Read {len(merged_data)} unique papers from '{ARXIV_CSV}'")
except FileNotFoundError:
    print(f"⚠️ WARNING: arXiv file not found at '{ARXIV_CSV}'. Skipping.")

# 2. Read and process the Google Scholar CSV
initial_count = len(merged_data)
try:
    with open(GOOGLE_SCHOLAR_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            title = row.get('title', '').strip()
            normalized_title = title.lower()
            
            if title and normalized_title not in seen_titles:
                year = row.get('year', '')
                merged_data.append({'title': title, 'year': year})
                seen_titles.add(normalized_title)
    print(f"✅ Read {len(merged_data) - initial_count} unique new papers from '{GOOGLE_SCHOLAR_CSV}'")
except FileNotFoundError:
    print(f"⚠️ WARNING: Google Scholar file not found at '{GOOGLE_SCHOLAR_CSV}'. Skipping.")

# 3. Prepare the final data with new columns
output_rows = []
for index, paper in enumerate(merged_data, start=1):
    output_rows.append({
        'index': index,
        'relevant': '', # Placeholder for your 'yes' or 'no'
        'comment': '',  # Placeholder for your categories
        'title': paper['title'],
        'year': paper['year']
    })

# 4. Write the result to the final CSV file
if output_rows:
    final_fieldnames = ['index', 'relevant', 'comment', 'title', 'year']
    try:
        with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=final_fieldnames)
            writer.writeheader()
            writer.writerows(output_rows)
        print(f"\n🎉 Success! Merged and finalized {len(output_rows)} papers into '{OUTPUT_CSV}'.")
    except IOError as e:
        print(f"\n❌ Error writing to file: {e}")
else:
    print("\nNo data was processed. Output file was not created.")