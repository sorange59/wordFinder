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

        try:
            # Fetch the webpage content
            response = requests.get(url)
            response.raise_for_status()

            # Parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find all occurrences of the target word
            occurrences = soup.find_all(string=lambda text: target_word.lower() in text.lower())

            if occurrences:
                print(f"\033[92mThe word '{target_word}' was found on the webpage: {url}\033[0m\n")
                for occ in occurrences:
                    section = occ.parent
                    print(f"{section.get_text(strip=True)}")
                    print(f"\033[92m{'*' * 50}\033[0m\n")
        except requests.RequestException as e:
            print(f"\033[91mFailed to fetch the webpage: {url}\033[0m")
            print(f"Error: {e}\n")

# Example usage
url2Use = input("Enter the website (e.g., https://google.com): ")
target_word = input("Enter the word to find: ")

base_url = url2Use
filename = "paths.txt"

paths = read_paths_from_file(filename)
if paths:
    find_word_on_webpages(base_url, paths, target_word)
