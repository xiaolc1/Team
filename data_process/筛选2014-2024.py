import json


def filter_papers(input_file, output_file, start_year, end_year, chunk_size=1000):
    """
    Filter papers within the specified year range from a large JSON file.

    :param input_file: Path to the input JSON file.
    :param output_file: Path to the output JSON file.
    :param start_year: Start year for filtering.
    :param end_year: End year for filtering.
    :param chunk_size: Number of records to read in each chunk.
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
            outfile.write('[')  # Start of JSON array
            first_record = True  # To handle commas between records

            while True:
                lines = []
                for _ in range(chunk_size):
                    line = infile.readline()
                    if not line:
                        break
                    lines.append(line.strip())

                if not lines:
                    break

                for line in lines:
                    record = json.loads(line)
                    if start_year <= record['year'] <= end_year:
                        if not first_record:
                            outfile.write(',\n')
                        json.dump(record, outfile)
                        first_record = False

            outfile.write(']')  # End of JSON array
            print(f'Filtered records have been written to {output_file}')

    except Exception as e:
        print(f"An error occurred: {e}")


# Usage example
filter_papers('AMiner-Citation-network-V15.json',
              '../../team_predict/AMiner/data_process/AMiner-Citation-network-2014-2024.json', 2014, 2024)
