import json

def extract_paper_author_ids(input_file, output_file):
    """
    Extract paper ID and author ID pairs from a JSON file and write to a text file.

    :param input_file: Path to the input JSON file with multiple paper records.
    :param output_file: Path to the output text file for storing paper-author ID pairs.
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
            data = json.load(infile)  # Load the entire JSON data

            # Iterate over each record (paper) in the dataset
            for record in data:
                paper_id = record.get('id')  # Unique paper ID
                authors = record.get('authors', [])

                # Iterate over each author in the paper
                for author in authors:
                    author_id = author.get('id')

                    # Skip if author ID is empty or None
                    if not author_id:
                        continue

                    # Write the paper ID and author ID pair to the output file
                    outfile.write(f"{paper_id} {author_id}\n")

        print(f'Paper-author ID pairs have been written to {output_file}')

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
extract_paper_author_ids('AMiner-Citation_2014_2024.json', 'paper_author.txt')
