import json

def extract_citation_network(input_file, output_file):
    """
    Extract a citation network from a JSON file containing multiple paper records.
    Each paper along with its referenced papers' IDs will be written to a text file.

    :param input_file: Path to the input JSON file with multiple paper records.
    :param output_file: Path to the output text file for storing the citation pairs.
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
            data = json.load(infile)  # Load the entire JSON data

            # Iterate over each record (paper) in the dataset
            for record in data:
                paper_id = record.get('id')  # Unique paper ID
                references = record.get('references', [])  # List of referenced paper IDs

                # Iterate over each reference in the paper
                for ref_id in references:
                    # Write the paper ID and reference ID pair to the output file
                    outfile.write(f"{paper_id} {ref_id}\n")

        print(f'Citation network pairs have been written to {output_file}')

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
extract_citation_network('AMiner-Citation_2014_2024.json', 'paper_paper.txt')
