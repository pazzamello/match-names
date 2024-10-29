# A simple Hello World program in Python
print("Hello, World!")
# BYD
# Canadian solar

def check_company_names(csv_file_path):
    """
    Read CSV file and check if first column contains similar matches to BYD or Canadian solar
    using fuzzy string matching. Returns list of matching company names found.
    """
    import csv
    from fuzzywuzzy import fuzz  # You'll need to: pip install fuzzywuzzy python-Levenshtein
    
    target_companies = ['BYD', 'Canadian solar']
    matches = []
    SIMILARITY_THRESHOLD = 80  # Adjust this value (0-100) to be more or less strict
    
    try:
        with open(csv_file_path, 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader, None)  # Skip header row if exists
            
            for row in csv_reader:
                if row:
                    company_name = row[0].lower()  # Convert to lowercase for better matching
                    # Track matches for this company name
                    match_count = 0
                    matched_company = None
                    
                    for target in target_companies:
                        ratio = fuzz.ratio(company_name, target.lower())
                        partial_ratio = fuzz.partial_ratio(company_name, target.lower())
                        
                        print(f"Comparing '{company_name}' with '{target.lower()}':")
                        print(f"  Ratio: {ratio}")
                        print(f"  Partial Ratio: {partial_ratio}")
                        print(f"  Threshold: {SIMILARITY_THRESHOLD}")
                        
                        if ratio >= SIMILARITY_THRESHOLD or partial_ratio >= SIMILARITY_THRESHOLD:
                            match_count += 1
                            matched_company = row[0]
                            print(f"  MATCH FOUND! Company: {row[0]}")
                            
                            if match_count > 1:  # If we match multiple targets, skip this company
                                print(f"  Multiple matches found - skipping {row[0]}")
                                match_count = 0  # Reset match count to exclude this company
                                matched_company = None
                                break
                        print("---")
                    
                    # Only add to matches if we matched exactly one target company
                    if match_count == 1:
                        matches.append(matched_company)
                        print(f"Added to matches: {matched_company}\n")
                    
        # Save matches to a new CSV file
        output_file = 'matching_companies.csv'
        with open(output_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Matching Company Name'])  # Header
            writer.writerows([[company] for company in matches])
        print(f"Matching companies saved to {output_file}")
        
        return matches
    except FileNotFoundError:
        print(f"Error: File {csv_file_path} not found")
        return []
    except Exception as e:
        print(f"Error reading CSV file: {str(e)}")
        return []

# Create test CSV file
def create_test_csv(filename='test_companies.csv'):
    """Create a sample CSV file with company names for testing."""
    import csv
    
    # Sample company data with variations and other companies
    companies = [
        ["BYD Company Limited"],
        ["BYD Electronics"],
        ["Build Your Dreams (BYD)"],
        ["Canadian Solar Inc."],
        ["Canadian Solar Solutions"], 
        ["CanadianSolar Technologies"],
        ["Tesla, Inc."],
        ["First Solar"],
        ["Byd automotive"],
        ["Canadian solar panels ltd"],
        ["Sunpower Corporation"],
        ["candian solar"],  # Intentional misspelling
        ["B Y D Electric"],
        ["Solar Canadian | BYD "],
    ]

    try:
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Company Name"])  # Header
            writer.writerows(companies)
        print(f"CSV file '{filename}' has been created successfully!")
        return True
    except Exception as e:
        print(f"Error creating CSV file: {str(e)}")
        return False

# Example usage:
if __name__ == "__main__":
    csv_filename = 'test_companies.csv'
    if create_test_csv(csv_filename):
        matching_companies = check_company_names(csv_filename)
        print("\nMatching companies found:", matching_companies)
