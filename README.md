# DTU Course Analyzer

## Website link
[(Link to Website)](https://dtucourseanalyzer.pythonanywhere.com)

## How to run the website locally
1. Clone/Download the repository. Ensure you have Python installed.
2. Pip install the python modules listed in requirements.txt (Python 3.11.7 or later is recommended).
3. Run website_launch.py and then visit http://127.0.0.1:5000 in your webbrowser.
4. (OPTIONAL) The repository already contains scraped data. To re-scrape the data from DTU's servers, run main.py

## About this GitHub repository
This repository contains all the code related to my hobby project, the "DTU Course Analyzer" website (not to be confused with the [Google Chrome Extension of the same name](https://chromewebstore.google.com/detail/dtu-course-analyzer/bimhgdngikcnelkhjindmdghndfmdcde)). I started the project several years ago and have only recently made it public. While the code is open-source, this was always intended to be a solo project. Be aware that if you delve into the code, you may find it complex and challenging to understand. The repository hasn't been "cleaned" for public consumption, so you should expect to find numerous leftover files with no real purpose. Most of the code was written when I was new to programming – if I were to start the project today, I would have organized things differently. Nevertheless, the code works and behaves as intended, and I've refactored and maintained it to make scraping and updating the data as straightforward as possible (for me at least). Simply run main.py to scrape the data and launch a local version of the website. For now I consider the project to be finished. However, I plan on keeping the site updated with the most recent data. If the website receives a lot of traffic, I'll consider improving its performance.

# Copy-paste of Website's FAQ section
<img src="https://dtucourseanalyzer.pythonanywhere.com/static/assets/brand/me.png" alt="Brand Image" width="180">

## Who are you?
I am Jonatan Rasmussen, a danish student studying Human-Centered AI (MSc) at DTU. This website is my hobby project. I am not paid by, or affiliated with, DTU's administration.

## What is this site?
This website contains public course data for DTU's courses. It also offers more in-depth search filters than the official DTU websites as well as evaluation summaries and overviews.

## How do I use the website?
In the 'Home' tab, use the filter to search for whichever courses you are interested in. Click on any Course Card to see in-depth data for that specific course.

## Why did you make this?
I started the project back in 2019 because I liked the DTUCourseAnalyzer Chrome extension (I am NOT its author) but its data was out of date. Yes, even back in 2019 it used outdated data. Back then I was also new to programming, so it was a fun personal project. Initially, I just wanted to collect all the data in a big spreadsheet. Over time however, I collected more and more data and I wanted to make it browsable via a website. It is my goal that people can use this site to find and discover high-quality courses.

## How long did this take to make?
200 hours would be my rough estimate. I have written 9.000 lines of Python, 6.000 lines of HTML and 5.000 lines of C#, totalling 20.000 lines of code (LOC). This is all on my Github.

## Is the data up to date?
The most recent data is from the Summer Exams 2024. So yes, it is quite up-to-date. Fetching new data from DTU's websites is something I do via scripts that I manually need to run. So expect new data to be added to this website 1-2 times per year.

## How did you get the data?
I use [this site](https://kurser.dtu.dk/archive/volumes) to scrape all the course numbers. Then I use a Python script to go to `https://kurser.dtu.dk/course/01001`, `https://kurser.dtu.dk/course/01002`, and so on to scrape course data for all the 1700+ DTU courses. Note that I am not using an API, nor have I had any contact with DTU's administration.

## Can I get your raw data file(s)?
You can find the data on my GitHub. From here, it is possible to download all the data as one huge CSV: [CSV Files](https://github.com/JonatanRasmussen/dtu-course-browser/tree/main/website/static/csv_files).

## What are your future plans for this website?
I don't really know honestly. If this website starts to become popular I want to host it somewhere better than pythonanywhere.com. I don't have a lot of time these days, so don't expect a lot of new features. I will however continue to update it with new data for as long as possible.

## Can you make a similar website for KU / AAU / SDU / RUC / (insert other university)?
Sadly this is not going to happen. The course data is completely different for non-DTU courses. I would have to re-write all of my code.

## I have found a bug!
That is not a question. Jokes aside, email me at s183649@dtu.dk or report it on my [GitHub](https://github.com/JonatanRasmussen/dtu-course-browser) (I'm kinda new to running an open-source project however, so don't expect too much).

## How can I contact you?
Email me at s183649@dtu.dk.

## Give me a fun fact
I'm the creator of the YouTube video [Best of Mat 1](https://www.youtube.com/watch?v=fUqA4bgRa5w), currently sitting at 12,000+ views.

## Show me something cool!
Sure, take a look at the subpage [/wip](https://dtucourseanalyzer.pythonanywhere.com/wip) for a behind-the-scenes sneak peek of the website design process!

## May I leave now?
Yes. [(Return to Home Page)](https://dtucourseanalyzer.pythonanywhere.com)