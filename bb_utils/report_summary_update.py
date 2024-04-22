import requests

class ArticleUpdater:
    def __init__(self, base_url):
        self.base_url = base_url
        self.list_endpoint = 'generate-summary-report/'
        self.detail_endpoint = 'generate-summary-report/{}/'

    def get_reports(self):
        response = requests.get(self.base_url + self.list_endpoint)
        if response.status_code == 200:
            return response.json()
        else:
            print("Failed to retrieve reports with empty summary.")
            return []

    ## TODO: By Niraj matere
    def generate_summary(self, description_dict):
        return {
            1: "this is the updated summary"
        }

    def update_report(self, article):
        report_id = article['id']
        endpoint = self.detail_endpoint.format(report_id)

        response = requests.put(self.base_url + endpoint, json=article)
        if response.status_code == 200:
            print(f"Report {report_id} updated successfully.")
        else:
            print(f"Failed to update report {report_id}.")

    def process_reports(self):
        reports = self.get_reports()
        if reports:
            description_dict = {}
            for report in reports:
                description_dict[report['id']] = report['description']
            
            summary_dict = self.generate_summary(description_dict)

            for report in reports:
                report['summary'] = summary_dict[report['id']]
                self.update_report(report)
        else:
            print("No reports with empty summary found.")

if __name__ == '__main__':
    base_url = 'http://68.183.82.126/api/'

    updater = ArticleUpdater(base_url)
    updater.process_reports()