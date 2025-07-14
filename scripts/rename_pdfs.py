import os
import csv
import re

# --- Configuration ---
PDF_FOLDER_PATH = "/Users/zhangshuoming/Desktop/THPC-survey-LLMCompiler/phase2_filtered"
INPUT_CSV = "phase3_filtered.csv"
OUTPUT_CSV = "phase3_renamed.csv"

# --- Helper Function ---
def sanitize_filename(filename):
    """Cleans a string to make it a valid filename."""
    sanitized = re.sub(r'[\\/*?:"<>|]', "", filename)
    sanitized = sanitized.replace(' ', '_')
    return sanitized[:150]

# --- Main Script ---

# 1. Validate paths
if not os.path.isdir(PDF_FOLDER_PATH):
    print(f"❌ Error: Folder not found at '{PDF_FOLDER_PATH}'")
    exit()
if not os.path.exists(INPUT_CSV):
    print(f"❌ Error: CSV file not found at '{INPUT_CSV}'")
    exit()

# 2. Read CSV data into a dictionary for easy lookup
csv_data = {}
try:
    with open(INPUT_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames
        if '\ufeffindex' not in headers:
            print(f"\n❌ CRITICAL ERROR: Found headers {headers}, but required column 'index' was not found.")
            exit()
        for row in reader:
            csv_data[row['\ufeffindex']] = row
    print(f"✅ Successfully read {len(csv_data)} rows from '{INPUT_CSV}'.")
except Exception as e:
    print(f"❌ An error occurred reading the CSV: {e}")
    exit()

# 3. Iterate through PDF files and rename them
print("\nStarting PDF renaming process...")
renamed_count = 0
unmatched_files = []

for old_filename in os.listdir(PDF_FOLDER_PATH):
    if old_filename.lower().endswith('.pdf'):
        try:
            # --- IMPROVED PARSING LOGIC ---
            # This now correctly handles names like 'aa_17.pdf' and 'aa_17_title.pdf'
            base_name, _ = os.path.splitext(old_filename)
            parts = base_name.split('_')
            file_index = parts[1]
            # --- END IMPROVEMENT ---

            if file_index in csv_data:
                paper_title = csv_data[file_index]['title']
                sanitized_title = sanitize_filename(paper_title)
                new_filename = f"{file_index}_{sanitized_title}.pdf"
                
                old_path = os.path.join(PDF_FOLDER_PATH, old_filename)
                new_path = os.path.join(PDF_FOLDER_PATH, new_filename)
                
                if old_path != new_path:
                    os.rename(old_path, new_path)
                    print(f"✅ Renamed '{old_filename}' to '{new_filename}'")
                else:
                    print(f"➡️ Filename '{old_filename}' is already correct. Skipping.")

                csv_data[file_index]['path'] = new_path
                renamed_count += 1
            else:
                unmatched_files.append(old_filename)
        except IndexError:
            print(f"⚠️ Warning: Could not parse index from '{old_filename}'. Skipping.")
            unmatched_files.append(old_filename)
        except Exception as e:
            print(f"❌ An error occurred while processing '{old_filename}': {e}")
            unmatched_files.append(old_filename)

print(f"\nRenamed {renamed_count} files successfully.")
if unmatched_files:
    print("\n⚠️ The following files could not be matched or renamed:")
    for fname in unmatched_files:
        print(f"  - {fname}")

# 4. Write the updated data to a new CSV file
updated_rows = list(csv_data.values())
if updated_rows:
    fieldnames = list(updated_rows[0].keys())
    try:
        with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(updated_rows)
        print(f"\n🎉 Success! Regenerated CSV with paths at '{OUTPUT_CSV}'.")
    except IOError as e:
        print(f"\n❌ Error writing to new CSV file: {e}")
else:
    print("\nNo data was processed to write to the new CSV.")