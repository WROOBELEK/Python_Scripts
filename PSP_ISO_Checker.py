import os
import zlib
import requests
from tabulate import tabulate
import re

# URL for the database
ISO_URL = "https://raw.githubusercontent.com/libretro/libretro-database/master/metadat/no-intro/Sony%20-%20PlayStation%20Portable.dat"
PSN_URL = "https://raw.githubusercontent.com/libretro/libretro-database/master/metadat/no-intro/Sony%20-%20PlayStation%20Portable%20(PSN).dat"
GAME_PATH = r"C:\Provide\Your\ISOs\Path\Here"

def magicText(text, hex, bold=False, italic=False, underline=False):
    boldCode = 1 if bold else 0
    italicCode = 3 if italic else 0
    underlineCode = 4 if underline else 0

    red = int(hex[1:3], 16)
    green = int(hex[3:5], 16)
    blue = int(hex[5:7], 16)
    return f"\033[{boldCode};{italicCode};{underlineCode};38;2;{red};{green};{blue}m{text}\033[00m"

def fetch_crc32_database(url, type="defualt"):
    """Fetch and parse CRC32 values from the database."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.text
        # Parse CRC32 values from the database using regex
        crc32_set = set(re.findall(r'\bcrc\s([0-9A-Fa-f]{8})\b', data))
        print(f"Database {type} loaded: {len(crc32_set)} CRC32 checksums found.")
        return {crc.upper() for crc in crc32_set}
    except Exception as e:
        print(f"Error fetching {type} database: {e}")
        return set()

def calculate_crc32(file_path):
    """Calculate the CRC32 checksum of a file."""
    try:
        with open(file_path, 'rb') as file:
            checksum = 0
            while chunk := file.read(8192):
                checksum = zlib.crc32(chunk, checksum)
            return format(checksum & 0xFFFFFFFF, '08X')  # Format as an 8-character hex string
    except Exception as e:
        return f"Error: {e}"

def database_checker(directory, iso_crc32_set, psn_crc32_set):
    """Calculate CRC32 checksums for all files in a directory and check against the database."""
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            crc32 = calculate_crc32(file_path)
            if crc32 in iso_crc32_set:
                status = magicText("ISO", "#00FF00", bold=True)
            elif crc32 in psn_crc32_set:
                status = magicText("PSN", "#006FCD", bold=True)
            else:
                status = magicText("No", "#FF0000", bold=True)
            print(f"{magicText(file, "#FFFF00", bold=True)} {magicText("||", "#00FFFF")} CRC32: {crc32} {magicText("||", "#00FFFF")} In Database: {status}")

def main():
    print(magicText("PSP ISO/PSN CRC32 Checker\n", "#00FF00", bold=True, italic=True, underline=True))
    if not os.path.isdir(GAME_PATH):
        print("Error: Invalid directory. Please provide a valid path.")
        return
    
    iso_crc32_set = fetch_crc32_database(ISO_URL, "ISO")
    psn_crc32_set = fetch_crc32_database(PSN_URL, "PSN")

    print("\nCalculating CRC32 checksums and checking against the databases...\n")
    database_checker(GAME_PATH, iso_crc32_set, psn_crc32_set)

if __name__ == "__main__":
    main()
