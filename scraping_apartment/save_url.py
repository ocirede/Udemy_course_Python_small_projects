class SaveUrl:
    def __init__(self, filename='processed_urls.txt'):
        self.filename = filename

    def save_url(self, url):
        """Append a URL to the file."""
        with open(self.filename, 'a') as f:
            f.write(url + '\n')
        print(f"✅ URL saved: {url}")

