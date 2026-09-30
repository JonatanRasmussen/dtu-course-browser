#%%

import os
import json
import time
import requests
import re

from utils import Utils
from website.global_constants.config import Config
from website.global_constants.file_name_consts import FileNameConsts


class OrbitImageDownloader:

    # --- FEATURE FLAG ---
    # Set to True if you want to overwrite images that already exist in the folder.
    # Set to False to skip downloading images you already have.
    REDOWNLOAD_EXISTING_IMAGES = False

    @staticmethod
    def download_images():
        """Reads the scraped orbit JSON and downloads all images to the scraped_images folder."""
        academic_year = Config.website_current_year
        json_file_name = f"{FileNameConsts.orbit_json}_{academic_year[0:4]}_{academic_year[5:9]}"
        json_path = f"{FileNameConsts.scraped_data_folder_name}/{json_file_name}.json"

        print(f"Starting image download for academic year {academic_year}...")

        # 1. Load the JSON file
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                orbit_dict = json.load(f)
        except FileNotFoundError:
            print(f"Error: Could not find {json_path}. Please run OrbitScraper first.")
            return

        # 2. Ensure the output directory exists
        output_folder = FileNameConsts.scraped_images_folder_name
        Utils.create_folder(output_folder)

        total_images = len(orbit_dict)
        downloaded_count = 0
        skipped_count = 0
        failed_count = 0

        # 3. Iterate and download
        for i, (teacher_name, image_url) in enumerate(orbit_dict.items(), 1):
            if not image_url:
                print(f"[{i}/{total_images}] Skipping {teacher_name}: No URL provided.")
                skipped_count += 1
                continue

            # Determine file extension based on URL
            ext = ".png" if "no-portrait" in image_url else ".jpg"

            # Sanitize teacher name for the filesystem (remove invalid characters, replace spaces with underscores)
            safe_name = re.sub(r'[\\/*?:"<>|]', "", teacher_name).replace(" ", "_")
            file_path = os.path.join(output_folder, f"{safe_name}{ext}")

            # Check if we should skip
            if os.path.exists(file_path) and not OrbitImageDownloader.REDOWNLOAD_EXISTING_IMAGES:
                print(f"[{i}/{total_images}] Skipping {teacher_name}: Image already exists.")
                skipped_count += 1
                continue

            # Download the image
            print(f"[{i}/{total_images}] Downloading {teacher_name}...")
            try:
                response = requests.get(image_url, stream=True, timeout=10)
                response.raise_for_status()

                with open(file_path, 'wb') as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
                downloaded_count += 1

                # Be polite to the server
                time.sleep(0.2)

            except requests.exceptions.RequestException as e:
                print(f"[{i}/{total_images}] Failed to download {teacher_name}: {e}")
                failed_count += 1

        print("\n--- Download Summary ---")
        print(f"Total processed: {total_images}")
        print(f"Successfully downloaded: {downloaded_count}")
        print(f"Skipped (already existed or no URL): {skipped_count}")
        print(f"Failed: {failed_count}")
        print("------------------------\n")

    """
    Key Features:
    Sanitization: Windows and Linux file systems hate characters like ?, <, >, |, :, *, /. The script uses regex (re.sub) to strip these out and replaces spaces with underscores so Morten Mørup becomes Morten_Mørup.jpg.
    Dynamic Extensions: It checks if the URL contains no-portrait to save it as a .png, otherwise it saves it as a .jpg.
    Streaming Download: It uses stream=True and iter_content to write the image directly to disk in chunks, which is the safest and most memory-efficient way to download binary files in Python.
    Politeness: Includes a small time.sleep(0.2) to ensure you don't accidentally DDoS the Orbit image server while downloading ~1000 images.
    """


#%%
if __name__ == "__main__":
    OrbitImageDownloader.download_images()