import arxiv
import csv
from datetime import datetime

# --- Configuration ---
# Use the same effective query as before.
# search_query = 'ti:("large language model" OR "LLM") AND abs:("compiler" OR "optimization" OR "code generation")'
# search_query = '(ti:("large language model" OR "LLM" OR "transformer") AND abs:(compiler OR optimization OR "code generation")) OR ti:("neural compilation" OR "neural code translation")'
search_query = '(ti:("large language model" OR "LLM") AND ti:("compiler" OR "compilation" OR "code optimization")) OR ti:("neural compilation" OR "neural code translation")'
max_results_to_fetch = 200
output_filename = "arxiv_survey_results.csv"

# --- Script ---
print(f"🔬 Starting search on arXiv with query: '{search_query}'")

# Perform the search, sorting by submitted date to get recent papers.
search = arxiv.Search(
  query=search_query,
  max_results=max_results_to_fetch,
  sort_by=arxiv.SortCriterion.SubmittedDate
)

# A list to hold all the structured paper data
papers_to_write = []

# Iterate through the search results
for result in search.results():
    # We apply the date filter here, as the API fetches regardless of date.
    if result.updated.year >= 2020:
        # The 'updated' attribute holds the date of the most recent version.
        most_recent_date = result.updated.strftime('%Y-%m-%d')

        # Structure the data for each paper as a dictionary
        paper_data = {
            'title': result.title,
            'abstract': result.summary.replace('\n', ' '), # Remove newlines for cleaner CSV
            'url': result.pdf_url,
            # The 'comment' field often contains conference information.
            'comment': result.comment,
            'date-year': most_recent_date
        }
        papers_to_write.append(paper_data)

print(f"✅ Found {len(papers_to_write)} relevant papers since 2020.")

# --- Write to CSV File ---
if papers_to_write:
    # Define the column headers for the CSV file.
    fieldnames = ['title', 'abstract', 'url', 'comment', 'date-year']
    
    try:
        with open(output_filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            # Write the header row
            writer.writeheader()
            
            # Write all the paper data
            writer.writerows(papers_to_write)
            
        print(f"💾 Successfully saved results to '{output_filename}'")
    except IOError as e:
        print(f"Error: Could not write to file. {e}")
else:
    print("No papers found matching the criteria. No CSV file was created.")