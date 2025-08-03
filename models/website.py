import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

class Website:
    def __init__(self, url):
        self.url = url
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise ValueError(f"Failed to fetch {url}: {response.status_code}")
        self.soup = BeautifulSoup(response.content, 'html.parser')

    def get_title(self):
        title = self.soup.title.string if self.soup.title else 'No title found'
        return title

    def get_content(self):
        text = self.soup.get_text(strip=True)
        if not text:
            raise ValueError(f"No content found in {self.url}")
        for irrelevant in self.soup.body(['script', 'style', 'img', 'input', 'button']):
            irrelevant.decompose()
        return text

    def get_links(self):
        links = [a['href'] for a in self.soup.find_all('a', href=True)]
        return links

    def __str__(self):
        return self.get_content()