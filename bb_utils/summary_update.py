import requests

class ArticleUpdater:
    def __init__(self, base_url):
        self.base_url = base_url
        self.list_endpoint = 'generate-summary/'
        self.detail_endpoint = 'generate-summary/{}/'
        self.trigger_endpoint = 'translate-summary-trigger/'

    def get_articles(self):
        response = requests.get(self.base_url + self.list_endpoint)
        if response.status_code == 200:
            return response.json()
        else:
            print("Failed to retrieve articles with empty summary.")
            return []

    ## TODO: By Niraj matere
    def generate_summary(self, description_dict):
        return {
            1: "this is the updated summary"
        }

    def update_article(self, article):
        article_id = article['id']
        endpoint = self.detail_endpoint.format(article_id)

        response = requests.put(self.base_url + endpoint, json=article)
        if response.status_code == 200:
            print(f"Article {article_id} updated successfully.")
        else:
            print(f"Failed to update article {article_id}.")

    def process_articles(self):
        articles = self.get_articles()
        if articles:
            description_dict = {}
            for article in articles:
                description_dict[article['id']] = article['description']
            
            summary_dict = self.generate_summary(description_dict)

            for article in articles:
                article['summary'] = summary_dict[article['id']]
                self.update_article(article)
        else:
            print("No articles with empty summary found.")

    def schedule_translation(self):
        response = requests.get(self.base_url + self.trigger_endpoint)
        if response.status_code == 200:
            print("Translation of summaries to Hindi initiated on the remote server.")
        else:
            print("Failed to trigger translation of summaries to Hindi on the remote server.")

if __name__ == '__main__':
    base_url = 'http://68.183.82.126/api/'

    updater = ArticleUpdater(base_url)
    updater.process_articles()
    updater.schedule_translation()
