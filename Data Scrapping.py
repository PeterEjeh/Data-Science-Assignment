#Books to Scrape 

import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to scrape book details
def scrape_books(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    books = []

    for book in soup.find_all('article', class_='product_pod'):
        title = book.h3.a['title']
        price = book.find('p', class_='price_color').text
        stock = book.find('p', class_='instock availability').text.strip()
        rating = book.p['class'][1]  # e.g., 'Three' for 3-star rating
        books.append({
            'Title': title,
            'Price': price,
            'Stock Status': stock,
            'Rating': rating
        })
    return books

# Scrape the first 5 pages
base_url = 'http://books.toscrape.com/catalogue/page-{}.html'
all_books = []

for page in range(1, 6):  # First 5 pages
    url = base_url.format(page)
    all_books.extend(scrape_books(url))

# Convert to DataFrame
books_df = pd.DataFrame(all_books)
print(books_df.head())


 # Quotes to Scrape 

import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to scrape quotes and authors
def scrape_quotes():
    url = 'http://quotes.toscrape.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    authors = set()

    for quote in soup.find_all('div', class_='quote'):
        author = quote.find('small', class_='author').text
        authors.add(author)

    # Scrape author details
    author_details = []
    for author in list(authors)[:10]:  # Limit to 10 authors
        author_url = f'http://quotes.toscrape.com/author/{author.replace(" ", "-")}/'
        response = requests.get(author_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        name = soup.find('h3', class_='author-title').text
        nationality = soup.find('span', class_='author-born-location').text
        description = soup.find('div', class_='author-description').text.strip()
        dob = soup.find('span', class_='author-born-date').text

        author_details.append({
            'Name': name,
            'Nationality': nationality,
            'Description': description,
            'Date of Birth': dob
        })

    return author_details

# Scrape and display
quotes_df = pd.DataFrame(scrape_quotes())
print(quotes_df.head())


# Wikipedia Scrapper

import requests
from bs4 import BeautifulSoup

# Function to scrape a random Wikipedia page
def scrape_random_wikipedia():
    url = 'https://en.wikipedia.org/wiki/Special:Random'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    title = soup.find('h1', id='firstHeading').text
    content = soup.find('div', class_='mw-parser-output').text.strip()[:500]  # First 500 characters

    return {
        'Title': title,
        'Content': content
    }

# Scrape and display
random_page = scrape_random_wikipedia()
print(f"Title: {random_page['Title']}")
print(f"Content: {random_page['Content']}")