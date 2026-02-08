import requests
from bs4 import BeautifulSoup


RBI_URL = "https://www.rbi.org.in/Scripts/NotificationUser.aspx"


def scrape_rbi():
    response = requests.get(RBI_URL, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    items = soup.select("a[href*='NotificationUser.aspx']")

    results = []

    for item in items[:3]:  # limit scope for MVP
        title = item.get_text(strip=True)
        link = "https://www.rbi.org.in" + item["href"]
        results.append(
            {
                "title": title,
                "url": link,
            }
        )

    return results