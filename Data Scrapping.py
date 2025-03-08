import requests
from bs4 import BeautifulSoup
import pandas as pd
import random
import time

# ------------------ Books to Scrape -----------------
def scrape_books(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        books = []

        for book in soup.find_all('article', class_='product_pod'):
            title = book.h3.a['title']
            price = book.find('p', class_='price_color').text
            stock = "In Stock" if "In stock" in book.find('p', class_='instock availability').text else "Out of Stock"
            rating = book.p['class'][1]  # Extract rating (e.g., 'Three' for 3-star)
            details_url = "https://books.toscrape.com/catalogue/" + book.h3.a['href']

            # Fetch additional details (description, category, and product info)
            details_response = requests.get(details_url)
            details_soup = BeautifulSoup(details_response.text, 'html.parser')

            description_tag = details_soup.select_one("#product_description ~ p")
            description = description_tag.text.strip() if description_tag else "No description available"
            category = details_soup.select("ul.breadcrumb li a")[-1].text.strip()

            # Extract product information table
            product_info = {}
            table_rows = details_soup.select("table tr")
            for row in table_rows:
                key = row.th.text.strip()
                value = row.td.text.strip()
                product_info[key] = value

            books.append({
                'Title': title,
                'Price': price,
                'Stock Status': stock,
                'Rating': rating,
                'Category': category,
                'Description': description,
                'UPC': product_info.get('UPC', 'N/A'),
                'Product Type': product_info.get('Product Type', 'N/A'),
                'Price (excl. tax)': product_info.get('Price (excl. tax)', 'N/A'),
                'Price (incl. tax)': product_info.get('Price (incl. tax)', 'N/A'),
                'Tax': product_info.get('Tax', 'N/A'),
                'Availability': product_info.get('Availability', 'N/A'),
                'Number of reviews': product_info.get('Number of reviews', 'N/A')
            })

        return books

    except requests.exceptions.RequestException as e:
        print(f"Error fetching books: {e}")
        return []

# Scrape first 5 pages
base_url = 'https://books.toscrape.com/catalogue/page-{}.html'
all_books = []

for page in range(1, 6):
    url = base_url.format(page)
    all_books.extend(scrape_books(url))
    time.sleep(1)  # Prevent overloading the server

# Save to CSV
books_df = pd.DataFrame(all_books)
books_df.to_csv("books_with_product_info.csv", index=False)
print("Books data saved to books_with_product_info.csv")


# ------------------ Quotes to Scrape ------------------
def scrape_quote_authors():
    base_url = "http://quotes.toscrape.com/page/{}/"
    authors = {}

    page = 1
    while len(authors) < 10 and page <= 10:
        try:
            url = base_url.format(page)
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            for quote in soup.find_all("div", class_="quote"):
                author_tag = quote.find("small", class_="author")
                author_name = author_tag.text if author_tag else None

                author_link = quote.find("a")["href"] if quote.find("a") else None
                if author_name and author_link and author_name not in authors:
                    author_url = "http://quotes.toscrape.com" + author_link
                    author_response = requests.get(author_url)
                    author_soup = BeautifulSoup(author_response.text, "html.parser")

                    name = author_soup.find("h3", class_="author-title").text.strip()
                    dob = author_soup.find("span", class_="author-born-date").text.strip()
                    nationality = author_soup.find("span", class_="author-born-location").text.replace("in", "").strip()
                    description = author_soup.find("div", class_="author-description").text.strip()

                    authors[name] = {
                        "Name": name,
                        "Date of Birth": dob,
                        "Nationality": nationality,
                        "Description": description
                    }

                    if len(authors) >= 10:
                        break
            page += 1
            time.sleep(1)  # Prevent rapid requests

        except requests.exceptions.RequestException as e:
            print(f"Error fetching quotes: {e}")
            break

    return list(authors.values())

# Scrape and save authors
authors_data = scrape_quote_authors()
authors_df = pd.DataFrame(authors_data)
authors_df.to_csv("authors.csv", index=False)
print("Authors data saved to authors.csv")


# ------------------ Wikipedia Scraper ------------------
def scrape_random_wikipedia():
    try:
        url = "https://en.wikipedia.org/wiki/Special:Random"
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.find("h1", id="firstHeading").text.strip()
        paragraphs = soup.select("p")
        content = "\n".join(p.text.strip() for p in paragraphs[:3] if p.text.strip())  # First 3 meaningful paragraphs

        return {
            "Title": title,
            "Content": content
        }

    except requests.exceptions.RequestException as e:
        print(f"Error fetching Wikipedia: {e}")
        return {"Title": "Error", "Content": "Failed to fetch content"}

# Scrape a random Wikipedia page
random_wiki_page = scrape_random_wikipedia()
print(f"\nWikipedia Page: {random_wiki_page['Title']}\n")
print(random_wiki_page["Content"])

