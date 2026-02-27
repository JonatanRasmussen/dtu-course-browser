import os
import gzip
import re
import pandas as pd
import time
from datetime import datetime
from pathlib import Path


# ==========================================
# 1. CONFIGURATION
# ==========================================
BASE_DIR = Path(__file__).resolve().parent
LOG_DIRECTORY = BASE_DIR / "logs" / "manual_webhost_logs" / "access"

# Set your time range here (Format: 'YYYY-MM-DD HH:MM:SS')
# Note: PythonAnywhere logs are in UTC time.
START_DATE = '2026-02-18 00:00:00'
END_DATE   = '2026-02-28 23:59:59'

# Define what constitutes a bot/crawler in the User-Agent string
BOT_KEYWORDS = 'bot|spider|crawl|slurp|chatgpt|amazon|bing|yandex|semrush|ahrefs|openai|seo'

# ==========================================
# 2. LOG PARSING SETUP
# ==========================================
# Regex pattern to match PythonAnywhere's extended Nginx combined log format
# Example: 130.226.161.92 - -[26/Feb/2026:14:28:02 +0000] "GET /course/1234 HTTP/1.1" 200 ...
LOG_PATTERN = re.compile(
    r'^(?P<ip>[\d\.]+)\s+-\s+-\s+\[(?P<timestamp>.*?)\]\s+'
    r'"(?P<method>[A-Z]+)\s+(?P<path>.*?)\s+HTTP/.*?"\s+'
    r'(?P<status>\d+)\s+(?P<size>\d+)\s+'
    r'"(?P<referrer>.*?)"\s+"(?P<user_agent>.*?)"'
)

def load_logs(directory):
    print(f"Loading log files from: {directory}...")
    start_time = time.time()

    data = []
    line_number = 0
    files_processed = 0
    total_lines = 0
    total_matches = 0

    if not os.path.exists(directory):
        print(f"Error: Could not find directory {directory}")
        return pd.DataFrame()

    files = os.listdir(directory)
    print(f"Found {len(files)} files in directory.\n")

    for file_index, filename in enumerate(files, start=1):
        filepath = os.path.join(directory, filename)

        if filename.endswith('.gz'):
            f = gzip.open(filepath, 'rt', encoding='utf-8', errors='ignore')
        elif ('access' and '.log') in filename:
            f = open(filepath, 'r', encoding='utf-8', errors='ignore')
        else:
            continue

        files_processed += 1
        print(f"[{file_index}/{len(files)}] Processing: {filename}")

        with f:
            for line_number, line in enumerate(f, start=1):
                total_lines += 1

                match = LOG_PATTERN.search(line)
                if match:
                    data.append(match.groupdict())
                    total_matches += 1

                # Print progress every 100,000 lines
                if line_number % 100_000 == 0:
                    elapsed = time.time() - start_time
                    print(
                        f"   {line_number:,} lines read "
                        f"(Total: {total_lines:,}) | "
                        f"Matches: {total_matches:,} | "
                        f"Elapsed: {elapsed:.1f}s"
                    )

        print(f"   Finished {filename} ({line_number:,} lines)\n")

    total_time = time.time() - start_time
    print("="*50)
    print(f"Finished loading {files_processed} files.")
    print(f"Total lines processed: {total_lines:,}")
    print(f"Total matched entries: {total_matches:,}")
    print(f"Total time: {total_time:.1f} seconds")
    print("="*50 + "\n")

    return pd.DataFrame(data)

# ==========================================
# 3. DATA PROCESSING & ANALYSIS
# ==========================================
def analyze_logs():
    # Load raw data
    df = load_logs(LOG_DIRECTORY)
    if df.empty:
        return

    # Convert the timestamp string (e.g. "26/Feb/2026:14:28:02 +0000") to a real datetime object
    print("Parsing dates (this might take a few seconds)...")
    df['timestamp'] = pd.to_datetime(df['timestamp'], format='%d/%b/%Y:%H:%M:%S %z', errors='coerce')

    # Filter out any rows where the date couldn't be parsed
    df = df.dropna(subset=['timestamp'])

    # Make our START and END dates timezone-aware (UTC) to match the logs
    start_dt = pd.to_datetime(START_DATE).tz_localize('UTC')
    end_dt   = pd.to_datetime(END_DATE).tz_localize('UTC')

    # Apply the Date/Time filter
    mask_time = (df['timestamp'] >= start_dt) & (df['timestamp'] <= end_dt)
    df_filtered = df.loc[mask_time]

    if df_filtered.empty:
        print(f"No traffic found between {START_DATE} and {END_DATE}.")
        return

    # Separate Humans from Bots
    mask_bots = df_filtered['user_agent'].str.contains(BOT_KEYWORDS, case=False, na=False)
    df_bots = df_filtered[mask_bots]
    df_humans = df_filtered[~mask_bots]

    # Filter out static files (.png, .css, .js, .ico) so we only see real page visits
    mask_static = df_humans['path'].str.contains(r'\.(?:png|jpg|css|js|ico|woff2?)$|^/static/', case=False, regex=True)
    df_human_pages = df_humans[~mask_static]

    # ==========================================
    # 4. PRINT REPORTS
    # ==========================================
    print("="*50)
    print(f"TRAFFIC REPORT: {START_DATE} to {END_DATE}")
    print("="*50)

    total_hits = len(df_filtered)
    bot_hits = len(df_bots)
    human_page_views = len(df_human_pages)
    unique_human_ips = df_humans['ip'].nunique()

    print(f"Total Server Hits:  {total_hits:,} (includes bots and images)")
    print(f"Bot/Crawler Hits:   {bot_hits:,} ({bot_hits/total_hits*100:.1f}%)")
    print(f"Human Page Views:   {human_page_views:,} (excluding static files)")
    print(f"Est. Unique Humans: {unique_human_ips:,} (based on unique IP addresses)\n")

    print("--- TOP 10 VIEWED PAGES ---")
    top_pages = df_human_pages['path'].value_counts().head(10)
    print(top_pages.to_string())
    print()

    print("--- TOP 10 SEARCHED COURSES ---")
    mask_courses = df_human_pages['path'].str.startswith('/course/')
    top_courses = df_human_pages[mask_courses]['path'].value_counts().head(10)

    # Clean up the output to just show the course ID
    top_courses.index = top_courses.index.str.replace('/course/', '')
    print(top_courses.to_string())
    print("\n" + "="*50)

if __name__ == "__main__":
    analyze_logs()