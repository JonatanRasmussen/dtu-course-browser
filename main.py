from scrape_masterscript import run_all_scrape_scripts
from csv_creator import csv_creator_main
from website_launch import website_launch_main
#%%
if __name__ == "__main__":
    # Scrape all data from DTU's websites and save it to scraped_data folder
    # Note that this uses Selenium Webbrowser
    run_all_scrape_scripts() # THIS TAKES HOURS. Async url scraping is NOT IMPLEMENTED

    # Take data from scraped_data folder and clean+format+parse it.
    # Then, save it as csv file to website/static folder
    csv_creator_main() # This requires scraped_data, obtained via the above code

    # Launch website, using data from the csv file created above
    website_launch_main()
