import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def extract_links_from_div(url, class_name, ignore_domains):
    """
    Fetches the page at the given URL and extracts links from a specified div with a given class name,
    while ignoring links from specified domains.
    
    :param url: URL of the page to fetch
    :param class_name: The class name of the div to search within (e.g., 'downloadz')
    :param ignore_domains: A list of domain strings to ignore in the extracted links
    :return: List of extracted links
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the div with the specified class name
        div = soup.find('div', class_=class_name)
        if not div:
            print(f"No div with class '{class_name}' found on {url}")
            return []

        # Extract all anchor tags within the div
        links = [a['href'] for a in div.find_all('a', href=True)]
        
        # Filter out links from the ignored domains
        filtered_links = []
        for link in links:
            domain = urlparse(link).netloc
            if all(ignored not in domain for ignored in ignore_domains):
                filtered_links.append(link)
        
        return filtered_links

    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return []

def main(file_path, output_path, class_name, ignore_domains):
    """
    Reads a list of URLs from a text file and extracts links from a specific div with a given class name.

    :param file_path: Path to the text file containing URLs
    :param output_path: Path to the output text file to save extracted links
    :param class_name: The class name of the div to extract links from
    :param ignore_domains: List of domain strings to ignore in the extracted links
    """
    try:
        with open(file_path, 'r') as file:
            urls = [line.strip() for line in file if line.strip()]

        all_links = []
        for url in urls:
            links = extract_links_from_div(url, class_name, ignore_domains)
            all_links.extend(links)
            print(f"Extracted {len(links)} valid links from {url}")

        # Save the filtered links to the output file
        with open(output_path, 'w') as output_file:
            for link in all_links:
                output_file.write(f"{link}\n")
        
        print(f"\nTotal valid links extracted: {len(all_links)}")
        print(f"Links have been saved to {output_path}")

    except FileNotFoundError:
        print(f"File not found: {file_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python extract_links.py <input_file_path> <output_file_path>")
    else:
        input_file_path = sys.argv[1]
        output_file_path = sys.argv[2]
        class_name = "downloadz"  # The class name of the div element you want to search within
        ignore_domains = ["bit.ly", "nitroflare.com", "fileblade.com"]  # Domains to ignore
        main(input_file_path, output_file_path, class_name, ignore_domains)
