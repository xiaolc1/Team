import json

def extract_venue_author_ids(input_file, output_file, venue_mapping_file):
    """
    Extract venue (mapped to a unique ID) and author ID pairs from a JSON file containing multiple paper records.
    Each venue ID along with the author IDs from the papers will be written to a text file.
    Additionally, save the venue to ID mapping to another file.

    :param input_file: Path to the input JSON file with multiple paper records.
    :param output_file: Path to the output text file for storing the venue ID-author ID pairs.
    :param venue_mapping_file: Path to the output text file for storing the venue to ID mapping.
    """
    venue_to_id = {}  # Dictionary to map venue names to unique IDs
    current_id = 1  # Start assigning IDs from 1

    try:
        with open(input_file, 'r', encoding='utf-8') as infile, \
             open(output_file, 'w', encoding='utf-8') as outfile:
            data = json.load(infile)  # Load the entire JSON data

            # Iterate over each record (paper) in the dataset
            for record in data:
                venue = record.get('venue')
                if venue:  # Check if venue is not None or empty
                    venue = venue.strip()  # Safely call strip() because venue is not None
                    if venue not in venue_to_id:
                        venue_to_id[venue] = current_id
                        current_id += 1
                    venue_id = venue_to_id[venue]

                    authors = record.get('authors', [])  # Get the list of authors
                    # Iterate over each author in the paper
                    for author in authors:
                        author_id = author.get('id')
                        if author_id:  # Ensure author ID is present
                            # Write the venue ID and author ID pair to the output file
                            outfile.write(f"{venue_id} {author_id}\n")

        # After processing all records, save the venue to ID mapping
        with open(venue_mapping_file, 'w', encoding='utf-8') as mapfile:
            for venue, vid in venue_to_id.items():
                mapfile.write(f"{venue} && {vid}\n")

        print(f'Venue-author ID pairs have been written to {output_file}')
        print(f'Venue to ID mapping has been written to {venue_mapping_file}')

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
extract_venue_author_ids('AMiner-Citation_2014_2024.json', 'venue_author.txt', 'venue_id_mapping.txt')


