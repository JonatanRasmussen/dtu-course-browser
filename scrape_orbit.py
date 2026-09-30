#%%

import time
import urllib.parse
import requests
import html
import re
from requests.exceptions import Timeout, RequestException
import pandas as pd

from utils import Utils
from website.global_constants.config import Config
from website.global_constants.dtu_consts import DtuConsts
from website.global_constants.file_name_consts import FileNameConsts


class OrbitScraper:

    DEFAULT_IMAGE_URL = "https://orbit.dtu.dk/assets/no-portrait-473c6d005990baa1f418d9c668dcd4ec.png"

    # Quick and dirty blacklist for teachers we know are missing/gone
    MISSING_LIST = [
        "Stig Christian Herluf S Andersen",
        "Mette Harrestrup",
        "Aske Unger",
        "Ida Stub Johansson",
        "Andrea Nadal Pellisé",
        # The following are not missing, but have an invalid picture
    ]

    # Teachers who use external/personal emails in the course base that won't match their DTU Orbit alias
    SKIP_EMAIL_CHECK = [
        "Thomas Ulrik Stepnicka",
        "Lene Fischer"
    ]

    # Manual overrides for teachers whose Orbit URLs heavily deviate from the standard format.
    MANUAL_MAPPING = {
        "Lesia Marie-Jeanne M Mitridati": "lesia-mitridati",
        "Carl Christian Berggreen": "christian-berggreen",
        "Carlos Guillermo Acevedo Rocha": "carlos-g-acevedo-rocha",
        "Jonas Ove Philip Eliasson": "jonas-eliasson",
        "Sona Tomaškovicová": "sonia-tomaškovicová",
        "Philip Thomas Lanken C Clausen": "philip-thomas-lanken-conradsen-clausen",
        "Lenka Tetkova": "lenka-tetková",
        "Ying Li": "jason-li-ying",
        "Bodean Bue Gervang": "bo-gervang",
        "Seyyedjalal Kazempour": "jalal-kazempour",
        "Coraline Yvonne Solange Lapre": "coraline-lapre",
        "Nikolay Akopian": "nika-akopian",
        "Hanna Katarina Lilith J Rosvall": "hanna-katarina-lilith-johansson",
        "Mei Lee Ling": "meilee-ling"
    }

    @staticmethod
    def quick_test_scrape_for_debugging_please_ignore():
        """ Do a quick scrape to see if the code works."""
        course_numbers = ['01001', '02402']  # Example of valid courses
        academic_year = '2023-2024'  # Example of valid academic year
        file_name = f"{FileNameConsts.orbit_json}_test"
        OrbitScraper.scrape_orbit(course_numbers, academic_year, file_name)

    @staticmethod
    def scrape_orbit(course_numbers, academic_year, file_name):
        """Scrape DTU Orbit for course responsible images."""
        print(f'Webscrape of Orbit will now begin for academic year {academic_year}...')

        info_file_name = f"{FileNameConsts.info_df}_{academic_year[0:4]}_{academic_year[5:9]}"

        try:
            info_df = Utils.load_scraped_csv(info_file_name)
        except FileNotFoundError:
            message = f"{file_name}: Could not find {info_file_name}.csv. Ensure InfoScraper has run first."
            Utils.logger(message, "Error", FileNameConsts.scrape_log_name)
            return {}

        teacher_columns = [
            DtuConsts.dtu_name_of_main_responsible,
            DtuConsts.dtu_name_of_co_responsible_1,
            DtuConsts.dtu_name_of_co_responsible_2,
            DtuConsts.dtu_name_of_co_responsible_3,
            DtuConsts.dtu_name_of_co_responsible_4
        ]

        # Extract unique teacher names and map them to their expected email aliases
        unique_teachers = set()
        teacher_aliases = {}
        filtered_df = info_df[info_df[FileNameConsts.df_index].isin(course_numbers)]

        for col in teacher_columns:
            if col in filtered_df.columns:
                names = filtered_df[col].dropna().unique()
                for name in names:
                    clean_name = html.unescape(str(name).strip())
                    if clean_name != DtuConsts.dtu_no_data_for_responsible and clean_name != "":
                        unique_teachers.add(clean_name)

        # Build a dictionary of expected email aliases for each teacher
        for teacher_name in unique_teachers:
            aliases = set()
            mask = (
                (filtered_df.get(DtuConsts.dtu_name_of_main_responsible) == teacher_name) |
                (filtered_df.get(DtuConsts.dtu_name_of_co_responsible_1) == teacher_name) |
                (filtered_df.get(DtuConsts.dtu_name_of_co_responsible_2) == teacher_name) |
                (filtered_df.get(DtuConsts.dtu_name_of_co_responsible_3) == teacher_name) |
                (filtered_df.get(DtuConsts.dtu_name_of_co_responsible_4) == teacher_name)
            )
            teacher_rows = filtered_df[mask]

            for _, row in teacher_rows.iterrows():
                text_to_search = ""
                if "Responsible" in row.index and pd.notna(row["Responsible"]):
                    text_to_search += str(row["Responsible"]) + " "
                if "Course co-responsible" in row.index and pd.notna(row["Course co-responsible"]):
                    text_to_search += str(row["Course co-responsible"]) + " "

                found_emails = re.findall(r'([a-zA-Z0-9._-]+)@', text_to_search)
                for e in found_emails:
                    aliases.add(e.lower())

            teacher_aliases[teacher_name] = aliases

        orbit_dict = {}
        iteration_count = 0
        session = requests.Session()

        for teacher_name in unique_teachers:
            iteration_count += 1

            # 1. Check Blacklist
            if teacher_name in OrbitScraper.MISSING_LIST:
                orbit_dict[teacher_name] = ""
                OrbitScraper._print_progress(iteration_count, len(unique_teachers), file_name)
                continue

            # 2. Determine which name variations to try
            names_to_try = []
            if teacher_name in OrbitScraper.MANUAL_MAPPING:
                names_to_try.append(OrbitScraper.MANUAL_MAPPING[teacher_name])
            else:
                names_to_try.append(teacher_name.lower().replace(' ', '-'))
                for fallback in OrbitScraper._generate_name_fallbacks(teacher_name):
                    names_to_try.append(fallback.lower().replace(' ', '-'))

            expected_aliases = teacher_aliases.get(teacher_name, set())
            image_url = ""
            match_found = False

            # 3. Try fetching the image for each name variation
            for formatted_name in names_to_try:

                # Try the base name
                success, img = OrbitScraper._check_profile(session, formatted_name, expected_aliases, teacher_name, file_name)
                if success:
                    image_url = img
                    match_found = True
                    break

                # Try the "-2" variant immediately if the base name failed (either 404 or wrong email)
                success, img = OrbitScraper._check_profile(session, formatted_name + "-2", expected_aliases, teacher_name, file_name)
                if success:
                    image_url = img
                    match_found = True
                    break

                time.sleep(0.5)

            # 4. If all fallbacks failed
            if not match_found:
                message = f"{file_name}, {teacher_name}: Page not found on Orbit (404) after trying all fallbacks."
                Utils.logger(message, "Warning", FileNameConsts.scrape_log_name)
                image_url = OrbitScraper.DEFAULT_IMAGE_URL

            orbit_dict[teacher_name] = image_url

            OrbitScraper._print_progress(iteration_count, len(unique_teachers), file_name)
            time.sleep(0.5)

        if len(file_name) != 0:
            Utils.save_dct_as_json(file_name, orbit_dict)

        print('Webscrape of Orbit is now completed! Check log for details.\n')
        return orbit_dict

    @staticmethod
    def _check_profile(session, slug, expected_aliases, teacher_name, file_name):
        """
        Helper method to fetch a profile, check for 404, verify email, and extract image.
        Returns (True, image_url) if successful, (False, None) if it fails.
        """
        encoded_name = urllib.parse.quote(slug)
        page_source = OrbitScraper._fetch_orbit_page_source(session, encoded_name, teacher_name, file_name, False)

        if OrbitScraper._is_404(page_source):
            return False, None

        # Verify Email (unless skipped)
        if teacher_name not in OrbitScraper.SKIP_EMAIL_CHECK:
            orbit_alias = OrbitScraper._extract_orbit_email_alias(page_source)
            # If we have expected aliases and the profile has an alias, they must match
            if expected_aliases and orbit_alias and orbit_alias not in expected_aliases:
                return False, None

        # Match found!
        image_url = OrbitScraper._parse_image_url(page_source, teacher_name, file_name)
        return True, image_url

    @staticmethod
    def _generate_name_fallbacks(teacher_name):
        """
        Generate fallback names by omitting the last name, the first name,
        and then middle names one by one.
        """
        parts = teacher_name.split()
        fallbacks = []

        if len(parts) > 1:
            # 1. Omit the last name
            fallbacks.append(" ".join(parts[:-1]))
            # 2. Omit the first name
            fallbacks.append(" ".join(parts[1:]))

        if len(parts) > 2:
            # 3. Omit middle names one by one
            for i in range(1, len(parts) - 1):
                fallback_parts = parts[:i] + parts[i+1:]
                fallbacks.append(" ".join(fallback_parts))

        return fallbacks

    @staticmethod
    def _fetch_orbit_page_source(session, encoded_name, original_name, file_name, is_timeout):
        """Fetch the HTML of the Orbit person page."""
        try:
            url = f"https://orbit.dtu.dk/en/persons/{encoded_name}/"
            response = session.get(url, timeout=10, headers={"Accept-Language": "en"})
            return response.text
        except requests.exceptions.RequestException:
            if not is_timeout:
                time.sleep(5)
                return OrbitScraper._fetch_orbit_page_source(session, encoded_name, original_name, file_name, True)
            return ""

    @staticmethod
    def _is_404(page_source):
        """Check if the page source represents a 404 Not Found page."""
        return "Page not found" in page_source or "The page does not exist" in page_source

    @staticmethod
    def _extract_orbit_email_alias(page_source):
        """Extract the email alias from the Orbit page source."""
        if 'class="email">' in page_source:
            try:
                alias = page_source.split('class="email">')[1].split('<')[0].strip().lower()
                return alias
            except IndexError:
                pass
        return None

    @staticmethod
    def _parse_image_url(page_source, teacher_name, file_name):
        """Parse the image URL from the Orbit page source."""
        if "files-asset/" in page_source:
            split_source = page_source.split("files-asset/")[1]
            image_id = split_source.split(".")[0]
            full_url = f"https://orbit.dtu.dk/files-asset/{image_id}.jpg?w=160&f=webp"

            message = f"Scraped Orbit image for {teacher_name}: {full_url}"
            Utils.logger(message, "Log", FileNameConsts.scrape_log_name)
            return full_url

        elif "no-portrait-" in page_source:
            message = f"Scraped Orbit image for {teacher_name}: {OrbitScraper.DEFAULT_IMAGE_URL} (No portrait)"
            Utils.logger(message, "Log", FileNameConsts.scrape_log_name)
            return OrbitScraper.DEFAULT_IMAGE_URL

        else:
            message = f"{file_name}, {teacher_name}: 'files-asset/' and 'no-portrait' not found on valid page."
            Utils.logger(message, "Error", FileNameConsts.scrape_log_name)
            return OrbitScraper.DEFAULT_IMAGE_URL

    @staticmethod
    def _print_progress(iteration_count, total_count, file_name):
        """Helper to print progress to console."""
        if iteration_count % 50 == 0 or iteration_count in [1, 2, 5, 10]:
            print(f'{file_name}: {iteration_count} of {total_count} teachers have been scraped')

#%%
if __name__ == "__main__":
    OrbitScraper.quick_test_scrape_for_debugging_please_ignore()