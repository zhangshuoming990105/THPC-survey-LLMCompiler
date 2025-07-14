import csv
import os

# --- Configuration ---
# The CSV file you want to clean and sort.
INPUT_CSV = "phase2_to_be_categorized.csv" 
# The name of the final, polished output file.
OUTPUT_CSV = "phase2_to_be_categorized_deduplicated.csv"

# --- Main Script ---

# 1. Check if the input file exists
if not os.path.exists(INPUT_CSV):
    print(f"❌ Error: The file '{INPUT_CSV}' was not found.")
    exit()

# 2. Read the data and remove duplicates
print(f"Reading data from '{INPUT_CSV}'...")
# We use a dictionary with normalized titles as keys to automatically handle duplicates.
# The last entry for any given title will be the one that's kept.
unique_papers = {} 
original_row_count = 0

with open(INPUT_CSV, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        original_row_count += 1
        title = row.get('title', '').strip()
        if title:
            # Normalize title for accurate duplicate checking
            normalized_title = title.lower()
            unique_papers[normalized_title] = row

print(f"Processed {original_row_count} rows. Found {len(unique_papers)} unique papers.")

# 3. Convert the dictionary of unique papers back to a list
cleaned_rows = list(unique_papers.values())

# 4. Sort the cleaned list alphabetically by title
print("Sorting the unique papers by title...")
cleaned_rows.sort(key=lambda row: row['title'].lower())

# 5. Write the cleaned and sorted data to a new file
if cleaned_rows:
    # Get headers from the first row of the cleaned data
    fieldnames = cleaned_rows[0].keys()
    try:
        with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(cleaned_rows)
        print(f"\n🎉 Success! Saved {len(cleaned_rows)} cleaned and sorted papers to '{OUTPUT_CSV}'.")
    except IOError as e:
        print(f"\n❌ Error writing to file: {e}")
else:
    print("\nNo data to process. Output file was not created.")