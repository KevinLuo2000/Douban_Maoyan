from bs4 import BeautifulSoup
import requests
import csv
import time

if __name__ == "__main__":
    with open('maoyan.csv', 'w', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['TOP', '影片名称', '影片链接', '电影评分', '上映时间', '导演', '主演', '剧情简介'])
        # proxies = {'http': 'http://124.235.145.79:80', 'https': 'https://114.113.126.83:80'}
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)'
                                 ' Chrome/52.0.2743.116 Safari/537.36'}
        i = 0
        pics = []
        for page in range(10):
            # for page in range(1):
            page_number = i * 10
            url_begin = 'http://maoyan.com/board/4?offset={}'.format(str(page_number))
            wb_data = requests.get(url_begin, headers=headers)
            soup = BeautifulSoup(wb_data.text, 'lxml')
            actors = []
            titles = []
            urls = []
            ranks = []
            rating_nums = []
            times = []
            # 不用它了，直接创建空list再一次次extend
            '''
            if i == 0:
                titles = soup.select('li > div > div > div > a[href]')
                pics = soup.select('img[class="board-img"]')
                urls = soup.select('div > div > div > p > a')
                ranks = soup.select('dl > dd > i')
                rating_nums = soup.select('div > div > span[class="rating_num"]')
                times = soup.select('div > p > span')
            '''
            titles.extend(soup.select('#app > div > div > div.main > dl > dd > div > div > '
                                      'div.movie-item-info > p.name > a'))
            pics.extend(soup.select('#app > div > div > div.main > dl > dd > a > img.board-img'))
            urls.extend(soup.select('#app > div > div > div.main > dl > dd > div > div'
                                    ' > div.movie-item-info > p.name > a'))
            ranks.extend(soup.select('#app > div > div > div.main > dl > dd > i'))
            rating_nums.extend(soup.select('#app > div > div > div.main > dl > dd >'
                                           ' div > div > div.movie-item-number.score-num > p'))
            times.extend(soup.select('#app > div > div > div.main > dl > dd > div >'
                                     ' div > div.movie-item-info > p.releasetime'))
            actors.extend(soup.select('#app > div > div > div.main > dl > dd > div > div >'
                                      ' div.movie-item-info > p.star'))
            i = i + 1
            datas = []
            infos = []
            summaries = []

            for rank, title, url, rating_num, time, actor in zip(ranks, titles, urls, rating_nums, times, actors):
                '''data =[
                     rank.get_text(),
                     title.get_text(),
                     "http://maoyan.com"+url.get('href'),
                     rating_num.get_text(),
                     time.get_text().strip("上映时间："),
                     actor.get_text().strip().strip("\n")n
                ]'''
                # print(data)
                wb_data1 = requests.get("http://maoyan.com" + url.get('href'), headers=headers)
                soup1 = BeautifulSoup(wb_data1.text, 'lxml')
                director = soup1.select(
                    '#app > div > div.main-content > div > div.tab-content-container >'
                    ' div.tab-desc.tab-content.active > div:nth-of-type(2) > div.mod-content >'
                    ' div > div:nth-of-type(1) > ul > li > div > a')[
                    0].get_text()
                # screenwriter = soup1.select('#info > span:nth-of-type(2) > span.attrs')[0].get_text()

                # info = soup1.select('#info')[0].get_text().strip()
                # writer.writerows(info)
                # if str(soup1).find('展开全部') != -1:
                summary = soup1.select('span[class="dra"]')[0].get_text()
                # print(director, summary)
                # else:
                #    summary = "".join(soup1.select('#link-report > span:nth-of-type(1)')[0].get_text().split())
                f.write("{},{},{},{},{},{},{},{}\n".format(rank.get_text(), title.get_text(),
                                                           "http://maoyan.com" + url.get('href'), rating_num.get_text(),
                                                           time.get_text().strip("上映时间："), director.strip(),
                                                           actor.get_text().replace(',', ' ').strip().strip("主演："),
                                                           summary.strip()))
                # f.write(pic.get('src'))
                # writer.writerows(summary)
                # time.sleep(3)
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
            response = requests.get(url='h' + pic.get('data-src').strip('@160w_220h_1e_1c'), headers=headers,
                                    stream=True)
            with open('/Users/kevinluo/Desktop/Douban_Maoyan/maoyan_images/' + str(j) + '.jpg', 'wb') as f_:
                # 以字节流的方式写入，每128个流遍历一次，完成后为一张照片
                for data_ in response.iter_content(128):
                    f_.write(data_)
            j = j + 1
