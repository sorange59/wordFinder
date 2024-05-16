import requests
from bs4 import BeautifulSoup

def read_paths_from_file(filename):
    try:
        with open(filename, 'r') as file:
            paths = [line.strip() for line in file.readlines()]
        return paths
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return []

def find_word_on_webpages(base_url, paths, target_word):
    for path in paths:
        # Construct the full URL
        url = base_url + path

        # Fetch the webpage content
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find all occurrences of the target word
            occurrences = soup.find_all(string=lambda t: target_word in t)

            # Display each occurrence along with its section
            for occ in occurrences:
                section = occ.parent
                print(f"\033[92mThe word '{target_word}' was found on the webpage: {url}\033[0m")
                print()
                print(f"\033[92m{section}")
                print(f"\033[92m{'*' * 50}")
                print()
                print()
        else:
            print(f"\033[91mFailed to fetch the webpage: {url}")

# Example usage
url2Use = input("Enter the website (e.g., google.com): ")
target_word = input("Enter the word to find: ")

base_url = "https://" + url2Use
filename = "paths.txt"

paths = read_paths_from_file(filename)
if paths:
    find_word_on_webpages(base_url, paths, target_word)

