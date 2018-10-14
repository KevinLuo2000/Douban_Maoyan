from bs4 import BeautifulSoup
import requests
import csv
import time

if __name__ == "__main__":
    with open('douban.csv', 'w', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['TOP', '影片名称', '影片链接', '电影评分', '一句话短评', '导演', '编剧', '主演', '剧情简介'])
        # proxies = {'http': 'http://124.235.145.79:80', 'https': 'https://114.113.126.83:80'}
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)'
                                 ' Chrome/52.0.2743.116 Safari/537.36',
                   'Referer': 'https://movie.douban.com/top250'
                   }
        i = 0
        pics = []
        for page in range(10):
            # for page in range(1):
            page_number = i * 25
            url_begin = 'http://movie.douban.com/top250?start={}'.format(str(page_number))
            wb_data = requests.get(url_begin, headers=headers)
            soup = BeautifulSoup(wb_data.text, 'lxml')
            titles = []
            urls = []
            ranks = []
            rating_nums = []
            quotes = []
            # 不用它了，直接创建空list再一次次extend
            '''
            if i == 0:
                titles = soup.select('li > div > div > div > a[href]')
                pics = soup.select('img[width="100"]')
                urls = soup.select('li > div > div > div > a[href]')
                ranks = soup.select('div > em')
                rating_nums = soup.select('div > div > span[class="rating_num"]')
                quotes = soup.select('div > p > span')
            '''
            titles.extend(soup.select('li > div > div > div > a[href]'))
            pics.extend(soup.select('img[width="100"]'))
            urls.extend(soup.select('li > div > div > div > a[href]'))
            ranks.extend(soup.select('div > em'))
            rating_nums.extend(soup.select('div > div > span[class="rating_num"]'))
            quotes.extend(soup.select('div > p > span'))
            i = i + 1
            datas = []
            infos = []
            summaries = []

            for title, url, rank, rating_num, quote in zip(titles, urls, ranks, rating_nums, quotes):
                '''data = {
                    rank.get_text(),
                    " ".join(title.get_text().split()),
                    pic.get('src'),
                    url.get('href'),
                    rating_num.get_text(),
                    quote.get_text()
                }'''
                # writer.writerows(data)
                wb_data1 = requests.get(url.get('href'), headers=headers)
                soup1 = BeautifulSoup(wb_data1.text, 'lxml')
                director = soup1.select('a[rel="v:directedBy"]')[0].get_text()
                if url.get('href').find('26430107') == -1:
                    screenwriter = soup1.select('#info > span:nth-of-type(2) > span.attrs')[0].get_text()
                    actor = " ".join(soup1.select('#info > span.actor > span.attrs')[0].get_text().split())
                else:
                    screenwriter = ''
                    actor = ''
                info = soup1.select('#info')[0].get_text().strip()
                # writer.writerows(info)
                if str(soup1).find('展开全部') != -1:
                    summary = "".join(soup1.select('span[class="all hidden"]')[0].get_text().split())
                else:
                    summary = "".join(soup1.select('#link-report > span:nth-of-type(1)')[0].get_text().split())
                f.write("{},{},{},{},{},{},{},{},{}\n".format(rank.get_text(), " ".join(title.get_text().split()),
                                                              url.get('href'), rating_num.get_text(), quote.get_text(),
                                                              director, screenwriter, actor, summary))
                # f.write(pic.get('src'))
                # writer.writerows(summary)
                time.sleep(3)
                '''
                datas.append(data)
                infos.append(info)
                summaries.append(summary)
                '''
                # print(info)
                # print(summary)
                # print("导演:", director)
                # print("编剧:", screenwriter)
                # print("主演：", actor)

        j = 1
        for pic in pics:
            response = requests.get(url=pic.get('src'), headers=headers, stream=True)
            with open('/Users/kevinluo/Desktop/Douban_Maoyan/douban_images/' + str(j) + '.jpg', 'wb') as f_:
                # 以字节流的方式写入，每128个流遍历一次，完成后为一张照片
                for data_ in response.iter_content(128):
                    f_.write(data_)
            j = j + 1
