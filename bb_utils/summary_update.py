import requests

class ArticleUpdater:
    def __init__(self, base_url):
        self.base_url = base_url
        self.list_endpoint = 'generate-summary/'
        self.detail_endpoint = 'generate-summary/{}/'

    def get_articles_with_empty_summary(self):
        response = requests.get(self.base_url + self.list_endpoint)
        if response.status_code == 200:
            return response.json()
        else:
            print("Failed to retrieve articles with empty summary.")
            return []

    def generate_summary(self, description):
        return "this is the updated summary"

    def update_article_summary(self, article):
        article_id = article['id']
        endpoint = self.detail_endpoint.format(article_id)

        article_description = article['description']
        article['summary'] = self.generate_summary(article_description)

        response = requests.put(self.base_url + endpoint, json=article)
        if response.status_code == 200:
            print(f"Article {article_id} updated successfully.")
        else:
            print(f"Failed to update article {article_id}.")

    def process_articles(self):
        articles = self.get_articles_with_empty_summary()
        if articles:
            for article in articles:
                self.update_article_summary(article)
        else:
            print("No articles with empty summary found.")

if __name__ == '__main__':
    base_url = 'http://localhost:8000/api/'

    updater = ArticleUpdater(base_url)
    updater.process_articles()
