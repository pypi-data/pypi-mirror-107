import requests

from bs4 import BeautifulSoup


class WebCrawler:

    def __init__(self, path_init_web):
        self.path_init_web = path_init_web
    
    def crawl_the_web(self):
        """ Crawl the web """
        site_html_res = requests.get(self.path_init_web)
        site_html = BeautifulSoup(site_html_res.text, 'html.parser')
        result = []
        for link in site_html.find_all('a'):
            result.append(link.get('href'))
        return result
