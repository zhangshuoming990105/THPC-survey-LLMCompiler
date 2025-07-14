import csv
from scholarly import scholarly

# --- Configuration ---
SEARCH_QUERY = '(("large language model" OR "LLM" OR "transformer") AND ("compiler" OR "compilation" OR "code optimization")) OR ("neural compilation")'
OUTPUT_FILENAME = "google_scholar_results.csv"

# --- Main Script ---

print(f"🔬 Starting GENERAL search on Google Scholar with query: '{SEARCH_QUERY}'")
print("Note: This process can be slow as it scrapes the website directly.")

try:
    search_results_generator = scholarly.search_pubs(SEARCH_QUERY)
except Exception as e:
    print(f"❌ An initial error occurred. This might be due to a network issue or Google blocking the request: {e}")
    exit()

papers_to_write = []
results_limit = 300 

for i, paper in enumerate(search_results_generator):
    if i >= results_limit:
        print(f"\nReached the limit of {results_limit} papers processed.")
        break
        
    try:
        pub_year = paper.get('bib', {}).get('pub_year')
        
        if pub_year and int(pub_year) >= 2020:
            paper_data = {
                'title': paper.get('bib', {}).get('title'),
                'authors': ', '.join(paper.get('bib', {}).get('author', [])),
                'year': pub_year,
                'venue': paper.get('bib', {}).get('venue'),
                'url': paper.get('pub_url')
            }
            papers_to_write.append(paper_data)
            print(f"Found relevant paper: {paper_data['title']}")

    except Exception as e:
        print(f"Could not process a paper. Error: {e}")

print(f"\n✅ Found {len(papers_to_write)} relevant papers since 2020.")

# --- Sort the results by year (most recent first) ---
# This is the new line that performs the sorting.
papers_to_write.sort(key=lambda p: int(p.get('year', 0)), reverse=True)
print("📑 Results have been sorted by year.")

# --- Write to CSV File ---
if papers_to_write:
    fieldnames = ['title', 'authors', 'year', 'venue', 'url']
    
    try:
        with open(OUTPUT_FILENAME, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(papers_to_write)
            
        print(f"💾 Successfully saved sorted results to '{OUTPUT_FILENAME}'")
    except IOError as e:
        print(f"Error: Could not write to file. {e}")
else:
    print("No papers found matching the criteria. No CSV file was created.")