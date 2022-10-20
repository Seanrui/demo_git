import requests
from fake_useragent import UserAgent


class Web_spider:
    def __init__(self):
        self.headers1 = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
        self.headers = {
            'User-Agent': UserAgent().random,
        }

    def get_response(self, url):
        """
        获取数据的方法
        :param url:
        :return:
        """
        response = requests.get(url=url, headers=self.headers)
        print(self.headers)
        return response

    def data_parser(self, response):
        """
        数据解析的方法
        :param response:
        :return:
        """
        print(response.status_code)
        print(response.text)

    def run(self, url):
        """
        运行的方法
        :param url:
        :return:
        """
        response = self.get_response(url)
        self.data_parser(response)


if __name__ == '__main__':
    url = 'https://www.baidu.com'
    Web_spider().run(url)
