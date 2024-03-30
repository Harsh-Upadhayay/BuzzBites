import subprocess
from query_generators import generate_queries
import os
from loguru import logger

def run_spider(spider_name, query, time_frame=''):
    # Construct the command to execute
    command = f"scrapy crawl {spider_name} -a query='{query}' -a time_frame='{time_frame}'"

    # Execute the command and wait for it to complete
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")

if __name__ == '__main__':
    queries = generate_queries()
    os.chdir('/home/harsh/BuzzBites/scraping')
    for query in queries:
        run_spider('google_search', query)
        logger.info(f"Finished crawling query: {query}")
        
        # break  # Remove this line if you want to crawl all queries
