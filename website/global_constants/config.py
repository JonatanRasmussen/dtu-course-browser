

class Config:
    course_semesters = ['E19', 'F20', 'E20', 'F21', 'E21', 'F22', 'E22', 'F23', 'E23', 'F24', 'E24', 'F25']
    course_years = '2024-2025/' # If changing this, re-run scrape_course_numbers.py
    data_null_value = None  #type: ignore
    data_decimal_precision = 2
    data_percental_precision = 1

    website_current_year = "2025"
    website_last_updated = "27/03/2025"

    # Selenium toggle on/off
    selenium_is_enabled = True

    # feature flags for scraping
    feature_flag_scrape_archive = True
    feature_flag_scrape_evals = True
    feature_flag_scrape_grades = True
    feature_flag_scrape_info = True
