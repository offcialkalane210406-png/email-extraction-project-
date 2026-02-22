import pandas as pd
import requests
from bs4 import BeautifulSoup
import time

# -----------------------------
# CONFIG
# -----------------------------
INPUT_FILE = "hospitals.xlsx"
OUTPUT_FILE = "hyderabad_hospital_websites.xlsx"
CITY_FILTER = "hyderabad"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

TIMEOUT = 6        # prevents hanging
SLEEP_TIME = 1     # prevents blocking

# -----------------------------
# LOAD & FILTER DATA
# -----------------------------
df = pd.read_excel(INPUT_FILE)

df = df[df["City"].str.lower().str.contains(CITY_FILTER, na=False)]
df = df.reset_index(drop=True)

# -----------------------------
# WEBSITE EXTRACTION
# -----------------------------
website_links = []

for idx, hospital in enumerate(df["Hospital Name"], start=1):
    print(f"[{idx}/{len(df)}] Searching website for: {hospital}")

    website = "Not Found"

    try:
        query = f"{hospital} Hyderabad official website"
        search_url = "https://www.bing.com/search?q=" + query.replace(" ", "+")

        response = requests.get(
            search_url,
            headers=HEADERS,
            timeout=TIMEOUT
        )

        soup = BeautifulSoup(response.text, "html.parser")

        for a in soup.select("li.b_algo h2 a"):
            link = a.get("href")
            if link and link.startswith("http"):
                website = link
                break

    except Exception:
        website = "Error"

    website_links.append(website)
    time.sleep(SLEEP_TIME)

# -----------------------------
# EXPORT (ONLY WEBSITE LINKS)
# -----------------------------
output_df = pd.DataFrame({
    "Website": website_links
})

output_df.to_excel(OUTPUT_FILE, index=False)

print("\nDONE.")
print(f"File created: {OUTPUT_FILE}")
