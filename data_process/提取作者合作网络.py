import json
from collections import defaultdict

def extract_author_collaboration_network(input_file, output_file, min_collaborations=0):
    """
    Extract author collaboration network from a JSON file and save to a text file.
    Only includes collaborations with more than min_collaborations times and valid author IDs.

    :param input_file: Path to the input JSON file.
    :param output_file: Path to the output text file.
    :param min_collaborations: Minimum number of collaborations to include.
    """
    collaboration_counts = defaultdict(int)

    try:
        with open(input_file, 'r', encoding='utf-8') as infile:
            data = json.load(infile)

            for record in data:
                authors = record.get('authors', [])
                author_ids = [author['id'] for author in authors if author.get('id')]

                # Update collaboration counts
                for i in range(len(author_ids)):
                    for j in range(i + 1, len(author_ids)):
                        author_pair = tuple(sorted([author_ids[i], author_ids[j]]))
                        collaboration_counts[author_pair] += 1

        with open(output_file, 'w', encoding='utf-8') as outfile:
            for (author1, author2), count in collaboration_counts.items():
                if count > min_collaborations:
                    # outfile.write(f"{author1}\t{author2}\t{count}\n")
                    outfile.write(f"{author1}\t{author2}\n")

        print(f'Author collaboration network has been written to {output_file}')

    except Exception as e:
        print(f"An error occurred: {e}")

# Usage example
# extract_author_collaboration_network('data_process/ACM_conferences_2014_2024.json', 'author_collaboration_network.txt')
extract_author_collaboration_network('../../team_predict/AMiner/data_process/AMiner-Citation_2014_2024.json', 'author_author.txt')
