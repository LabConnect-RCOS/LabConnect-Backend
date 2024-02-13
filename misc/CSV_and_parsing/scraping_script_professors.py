import requests
from bs4 import BeautifulSoup

# Send an HTTP request to the URL
response = requests.get("https://faculty.rpi.edu/search")

# Check for a valid response (HTTP Status Code 200)
if response.status_code == 200:
    # Parse the HTML content using Beautiful Soup
    soup = BeautifulSoup(response.content, "html.parser")

    # Locate the data you're interested in
    # For example, if the professor data is in a table:
    table = soup.find("table", {"class": "professor-data"})

    # Iterate through the table rows
    for row in table.find_all("tr")[1:]:  # Skip header row
        columns = row.find_all("td")
        professor_name = columns[0].text
        department = columns[1].text
        # ... and so on for other columns

        print(f"{professor_name}, {department}")
else:
    print(f"Failed to retrieve page with status code: {response.status_code}")
