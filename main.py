from scrape_all import AllInOneScraper
from csv_creator import CsvCreator
from recommender_update import run_recommender_embeddings_update
from website_launch import website_launch_main
#%%
if __name__ == "__main__":
    # USE THE EXACT PACKAGE VERSIONS SPECIFIED IN requirements.txt
    # (pip installing the newest version of packages is CONFIRMED to sometimes break the code)
    # For example, newest Pandas version might be incompatible with the provided .pkl data files

    # Scrape all data from DTU's websites and save it to scraped_data folder
    AllInOneScraper.run_all_scrape_scripts() # THIS TAKES HOURS. Async url scraping is NOT IMPLEMENTED

    # Take data from scraped_data folder and clean+format+parse it.
    # Then, save it as csv file to website/static folder
    CsvCreator.create_csv() # This requires scraped_data, obtained via the above code

    # Recreate embeddings for the recommender based on the most recent scraped course data
    run_recommender_embeddings_update()

    # Launch website, using data from the csv file created above
    website_launch_main()
