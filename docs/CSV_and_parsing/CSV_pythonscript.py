import csv

csv_file_name = "Documents\GitHub\LabConnect\docs\CSV_and_parsing\CSVtest.csv"


data = []  # List to store rows of data

try:
    # Storing the data
    with open(csv_file_name, mode="r", newline="") as file:
        reader = csv.reader(file)
        headers = next(reader)  # Read the first row as headers

        for row in reader:
            data.append(row)

    # Printing the data
    with open(csv_file_name, mode="r", newline="") as file:
        reader = csv.reader(file)
        data = list(reader)
        headers = data[0]
        rows = data[1:]

        # Calculate column widths for formatting
        column_widths = [max(len(cell) for cell in col) for col in zip(*data)]

        # Print headers
        header_line = " | ".join(
            f"{header:^{width}}" for header, width in zip(headers, column_widths)
        )
        separator = "-" * len(header_line)
        print(separator)
        print(header_line)
        print(separator)

        # Print data
        for row in rows:
            row_line = " | ".join(
                f"{cell:<{width}}" for cell, width in zip(row, column_widths)
            )
            print(row_line)

        print(separator)

except FileNotFoundError:
    print(f"The file '{csv_file_name}' was not found.")
except Exception as e:
    print(f"An error occurred: {e}")
