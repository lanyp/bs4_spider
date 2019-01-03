from bs4 import BeautifulSoup
import requests
import json
import random

# bs4爬取巴比特社区
class Bs4_spider(object):
    def __init__(self):
        self.url = 'http://8btc.com/forum-61-{}.html'
        # 常用浏览器user-agent列表
        self.agent_list = [
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60",
            "Opera/8.0 (Windows NT 5.1; U; en)",
            "Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50",
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0",
            "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
            "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36"
        ]
        # 主页信息列表
        self.data_list = []
        # 详情页信息列表
        self.detail_list = []

    # 获取数据
    def get_response(self, url):
        headers = {
            'User-Agent': random.choice(self.agent_list)
        }
        # 发送请求返回数据
        response = requests.get(url, headers=headers)
        # 获取content得到bytes类型数据
        data = response.content
        return data

    # 解析标题数据
    def parse_data_list(self, data):
        # 创建对象
        soup = BeautifulSoup(data, 'lxml')
        # 根据类选择器,获取标题,返回列表
        title_list = soup.select('.xst')
        for title in title_list:
            data_dic = {}
            data_dic['title'] = title.get_text()
            # data_dic['url'] = title['href']
            data_dic['detail_url'] = title.get('href')
            self.data_list.append(data_dic)

    # 详情页数据解析
    def parse_detail_list(self, data):
        # 创建对象
        soup = BeautifulSoup(data, 'lxml')
        # 问题
        # question = soup.select('#thread_subject')[0].get_text()
        author_id = soup.select('a[class="name_uinfo"]')[0].get_text()
        question = soup.find(id='thread_subject').get_text()
        description = None
        # 问题描述
        description_table = soup.select('table[class="mt20"]')
        if description_table != None and len(description_table) > 0:
            if description_table[0].select('.t_f') != None and len(description_table[0].select('.t_f')) > 0:
                # 去掉字符串中的空格,换行符等其他多余符号
                description_str_list = description_table[0].select('.t_f')[0].stripped_strings
                for string in description_str_list:
                    description = string
        # 回复信息列表
        answer_box_list = soup.select('.info-box')
        answer_list = []
        for info in answer_box_list:
            info_dic = {'user_id': '', 'answer_info': ''}
            if info.select('.xw1') != None and len(info.select('.xw1')) > 0:
                info_dic['user_id'] = info.select('.xw1')[0].get_text()
            if info.select('.t_f') != None and len(info.select('.t_f')) > 0:
                # 去掉字符串中的空格,换行符等其他多余符号
                answer_info_list = info.select('.t_f')[0].stripped_strings
                for string in answer_info_list:
                    info_dic['answer_info'] = string
            answer_list.append(info_dic)

        # 详情页字典
        detail_dic = {
            'author_id': author_id,
            'question': question,
            'description': description,
            'answer_list': answer_list
        }
        # 详情页列表
        self.detail_list.append(detail_dic)

    # 获取页码链接
    def get_page_href_list(self, data):
        # 创建对象
        soup = BeautifulSoup(data, 'lxml')
        # 分页控件
        page_div_list = soup.select('div[class="pg"]')
        # 页码链接集合
        page_href_list = []
        if page_div_list != None and len(page_div_list) == 2:
            page_element_list = page_div_list[1].select('a')
            for item in page_element_list:
                if item.get_text() != 1 or item.get_text() != '1':
                    page_href_list.append(item['href'])

        return page_href_list

    # 保存数据
    def save_data(self, data, file_path):
        data_str = json.dumps(data, ensure_ascii=False)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(data_str)

    # 执行
    def execute(self, start_page=1, end_page=2):
        '''

        :param start_page: 起始页
        :param end_page: 结束页
        :return:
        '''
        # 抓取主页帖子标题
        for i in range(start_page, end_page):
            url = self.url.format(i)
            # 获取主页数据
            data = self.get_response(url)
            # 解析主页数据
            self.parse_data_list(data)
        # 保存主页数据
        self.save_data(self.data_list, 'title.json')

        # 抓取帖子详情页信息
        for data in self.data_list:
            first_detail_page__url = data['detail_url']
            # 获取详情页数据
            first_detail_page_data = self.get_response(first_detail_page__url)
            if first_detail_page_data != None:
                # 解析详情页数据
                self.parse_detail_list(first_detail_page_data)
                page_href_list = self.get_page_href_list(first_detail_page_data)
                for page_href in page_href_list:
                    other_detail_page_data = self.get_response(page_href)
                    if other_detail_page_data != None:
                        self.parse_detail_list(other_detail_page_data)

        self.save_data(self.detail_list, 'detail.json')


# 程序入口
if __name__ == '__main__':
    spider = Bs4_spider()
    spider.execute(1, 3)
