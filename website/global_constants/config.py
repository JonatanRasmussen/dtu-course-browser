

class Config:
    course_semesters = ['E20', 'F21', 'E21', 'F22', 'E22', 'F23', 'E23', 'F24', 'E24', 'F25', 'E25', 'F26']
    course_years = '2025-2026' # If changing this, re-run scrape_course_numbers.py
    data_null_value = None  #type: ignore
    data_decimal_precision = 2
    data_percental_precision = 1

    website_current_year = "2025-2026"
    website_last_updated = "07/08/2025"

    # feature flags for scraping
    feature_flag_scrape_archive = True
    feature_flag_scrape_evals = True
    feature_flag_scrape_grades = True
    feature_flag_scrape_info = True
