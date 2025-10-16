
class UrlLoaded:
    def __init__(self):
        self.urls_list = self.load_processed_urls()

    def load_processed_urls(self):
        try:
            with open('processed_urls.txt', 'r') as f:
                return [line.strip() for line in f.readlines()]
        except FileNotFoundError:
            return []