import csv

def read_csv_file(file_name):
    """Reads data from a CSV file."""
    try:
        with open(file_name, mode="r", newline="") as file:
            reader = csv.reader(file)
            headers = next(reader)  
            data = [row for row in reader]  
            return headers, data
    except FileNotFoundError:
        print(f"The file '{file_name}' was not found.")
        return None, None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None

def print_csv_data(headers, data):
    """Prints CSV data in a formatted manner."""
    if headers and data:
        # Calculate column widths for formatting
        column_widths = [max(len(cell) for cell in col) for col in zip(headers, *data)]
        
        # Print headers
        header_line = " | ".join(f"{header:^{width}}" for header, width in zip(headers, column_widths))
        separator = "-" * len(header_line)
        print(separator)
        print(header_line)
        print(separator)
        
        # Print data
        for row in data:
            row_line = " | ".join(f"{cell:<{width}}" for cell, width in zip(row, column_widths))
            print(row_line)
        
        print(separator)

def main():
    """Main function to execute CSV parsing."""
    csv_file_name = "Documents\GitHub\LabConnect\docs\CSV_and_parsing\CSVtest.csv"
    headers, data = read_csv_file(csv_file_name)
    if headers and data:
        print_csv_data(headers, data)

if __name__ == "__main__":
    main()
