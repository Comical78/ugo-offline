import requests
import os
import json
from tqdm import tqdm
from colorama import Fore, Style, init
import pyfiglet

# Initialize colorama for colored terminal output
init(autoreset=True)

# URL for map data
MAP_DATA_URL = "https://static.resquared.studio/maps/map_index.json"
MAP_INDEX_JSON = "map_index.json"
LOCAL_MAP_INDEX_JSON = "local_map_index.json"

# Function to print "SPARGAT" using ASCII art in large red letters
def print_spargat():
    ascii_art = pyfiglet.figlet_format("SPARGAT")
    print(f"{Fore.RED}{Style.BRIGHT}{ascii_art}{Style.RESET_ALL}")

# Function to download a file with a progress bar
def download_file(url, filename):
    try:
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get('Content-Length', 0))  # Get file size in bytes
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                # Use tqdm to show the download progress
                with tqdm(total=total_size, unit='B', unit_scale=True, desc=filename, colour='green') as progress_bar:
                    for chunk in response.iter_content(1024):
                        if chunk:  # Write each chunk of data to the file
                            f.write(chunk)
                            progress_bar.update(len(chunk))
            print(f"{Fore.GREEN}Downloaded: {filename} - {total_size / (1024 * 1024):.2f} MB")
            return filename  # Return filename after successful download
        else:
            print(f"{Fore.RED}Error downloading {filename} from {url}")
            return None
    except Exception as e:
        print(f"{Fore.RED}Download error for {filename}: {e}")
        return None

# Function to fetch the map data from the original URL and save it to map_index.json
def fetch_map_data():
    try:
        response = requests.get(MAP_DATA_URL)
        if response.status_code == 200:
            map_data = response.json()
            # Save the map data to map_index.json
            with open(MAP_INDEX_JSON, 'w') as f:
                json.dump(map_data, f, indent=4)
            print(f"{Fore.BLUE}Map data saved to {MAP_INDEX_JSON}")
            return map_data
        else:
            print(f"{Fore.RED}Error fetching map data, status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"{Fore.RED}Error fetching map data: {e}")
        return None

# Function to download files based on the data in map_index.json
def download_maps(map_data):
    downloaded_files = []

    # Iterate through each map entry and download files
    for map_entry in map_data:
        # Download the .zip file if the URL is not empty
        map_zip_url = map_entry.get('mapZipUrl', '')
        if map_zip_url:
            map_zip_filename = os.path.basename(map_zip_url)
            if download_file(map_zip_url, map_zip_filename):
                downloaded_files.append(map_zip_filename)
        
        # Download the map icon (.png) if the URL is not empty
        map_icon_url = map_entry.get('mapIcon', '')
        if map_icon_url:
            map_icon_filename = os.path.basename(map_icon_url)
            if download_file(map_icon_url, map_icon_filename):
                downloaded_files.append(map_icon_filename)
    
    return downloaded_files

# Function to create 'local_map_index.json' with only filenames of downloaded files
def create_local_map_index(downloaded_files):
    with open(LOCAL_MAP_INDEX_JSON, 'w') as f:
        json.dump(downloaded_files, f, indent=4)
    print(f"{Fore.BLUE}Created '{LOCAL_MAP_INDEX_JSON}' with downloaded file names.")

# Main function
def main():
    print_spargat()  # Display "SPARGAT" in large ASCII letters
    
    # Check if map_index.json exists
    if os.path.exists(MAP_INDEX_JSON):
        print(f"{Fore.YELLOW}{MAP_INDEX_JSON} exists, loading map data...")
        with open(MAP_INDEX_JSON, 'r') as f:
            map_data = json.load(f)
    else:
        print(f"{Fore.YELLOW}{MAP_INDEX_JSON} not found, fetching data from {MAP_DATA_URL}...")
        map_data = fetch_map_data()
    
    # If map data is available, download the maps
    if map_data:
        downloaded_files = download_maps(map_data)
        if downloaded_files:
            create_local_map_index(downloaded_files)
        else:
            print(f"{Fore.RED}No files were downloaded.")
    else:
        print(f"{Fore.RED}No map data available to process.")

if __name__ == "__main__":
    main()