import os.path
import time
import fitz # contians in pymupdf
import requests
from lxml import etree

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/93.0.4577.82 Safari/537.36 ',
    'cookie': '',  # your cookie
    'Connection': 'close'
}

# 设置代理
proxies = {
    'http': 'http://127.0.0.1:7890',
    'https': 'http://127.0.0.1:7890',
}

# 经过测试,通过网页下载最高分辨率图片时,下载十张左右后后续图片分辨率会变成低分辨率,加上header_img可解决.head_img中影响下载分辨率参数不详,目前是all-in
header_img = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'cookie': '', # your cookie
    'pragma': 'no-cache',
    'referer': 'https://e-hentai.org/g/944656/0c2120f188/',
    'sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'
}

# 下载用header
header_download = {
    'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'close',
    'Pragma': 'no-cache',
    'Referer': 'https://e-hentai.org/',
    'sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Sec-Fetch-Dest': 'image',
    'Sec-Fetch-Mode': 'no-cors',
    'Sec-Fetch-Site': 'cross-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'
}


def getHTML(url):
    global proxies
    global header
    get_html = ''
    while get_html == '':
        try:
            get_html = requests.get(url, headers=header, proxies=proxies).content.decode('utf-8')
        except requests.exceptions.SSLError:
            print('Connection refused by target server...sleep 1s')
            time.sleep(1)
            continue
        except requests.exceptions.ProxyError:
            print('Connection refused by proxy server...sleep 1s')
            time.sleep(1)
            continue

    return etree.HTML(get_html)


def getIMGHTML(url, header_img):
    global proxies
    get_html = ''
    while get_html == '':
        try:
            get_html = requests.get(url, headers=header_img, proxies=proxies).content.decode('utf-8')
        except requests.exceptions.SSLError:
            print('Connection refused by target server...sleep 1s')
            time.sleep(1)
            continue
        except requests.exceptions.ProxyError:
            print('Connection refused by proxy server...sleep 1s')
            time.sleep(1)
            continue

    return etree.HTML(get_html)


def pageGraber(g_url, pageCount):
    global header_img
    page_url_list = []
    # page starts from zero
    page_url = g_url + '?p={}'
    page_no = 0
    while page_no < pageCount:
        print(page_url.format(page_no) + ' grabbing img_html_url')
        page_html = getIMGHTML(page_url.format(page_no), header_img)
        page_url_list.extend(page_html.xpath('//*[@id="gdt"]/div/a/@href'))
        page_no += 1
    return page_url_list


def imgUrlGraber(page_url_list):
    global header_img
    img_url_list = []
    for page_url in page_url_list:
        img_html = getIMGHTML(page_url, header_img)
        img_url = img_html.xpath('//*[@id="img"]/@src')[0]
        img_url_list.append(img_url)
        print('get_img_url:' + img_url)
    return img_url_list


def downloadImages(title, img_url_list, path):
    global header_download
    # 以title为名新建文件夹
    img_dir = str(os.path.join(path, title)).replace('|', '_')
    os.makedirs(img_dir)
    for img_url in img_url_list:
        count = 0
        resp = None
        while count < 5:
            try:
                resp = requests.get(url=img_url, headers=header_download, proxies=proxies)
                break
            except:
                count += 1
                print('error occured {} times,sleep 1s...'.format(count))
                time.sleep(1)
                continue
        img_name = img_url.split('/')[-1]
        with open(img_dir + '\\' + img_name, 'wb+') as f:
            f.write(resp.content)
    return img_dir


# 获取域名为https://gotbjbqvnxfkunugorzh.hath.network中的图片有时间限制,目前采用抓到url后立即下载,以免失效
def imgUrlGraberAndDownload(page_url_list, title, path):
    def downloadImg(_img_url, _img_dir):
        count = 0
        resp = None
        while count < 5:
            try:
                resp = requests.get(url=_img_url, headers=header_download, proxies=proxies)
                break
            except:
                count += 1
                print('error occured {} times,sleep 1s...'.format(count))
                time.sleep(1)
                continue
        img_name = _img_url.split('/')[-1]
        with open(_img_dir + '\\' + img_name, 'wb+') as f:
            f.write(resp.content)

    # 以title为名新建文件夹
    img_dir = str(os.path.join(path, title)).replace('|', '_')
    os.makedirs(img_dir)
    global header_img
    # todo 多线程改造提高效率
    for page_url in page_url_list:
        # 获取url
        img_html = getIMGHTML(page_url, header_img)
        img_url = img_html.xpath('//*[@id="img"]/@src')[0]
        print('get_img_url:' + img_url)
        # 下载图片
        downloadImg(img_url, img_dir)
        print('down')
    return img_dir


def downloadByPage(g_url, html):
    # 默认排列 4行 大图 一页20张
    pageCount = int(
        int(html.xpath('/html/body/div[2]/div[3]/div[1]/div[3]/table/tr[6]/td[2]')[0].text.split(' ')[0]) / 20) + 1
    global header_img
    header_img['referer'] = g_url
    page_url_list = pageGraber(g_url, pageCount)
    title = html.xpath('//*[@id="gn"]')[0].text
    return imgUrlGraberAndDownload(page_url_list=page_url_list, title=title, path='D:\\temp')

    # 使用上面的方法 抓到url后马上下载,以免失效
    # img_url_list = imgUrlGraber(page_url_list)
    # return downloadImages(title=title, img_url_list=img_url_list, path='D:\\temp')


def downloadByTorrent(g_url, html):
    # todo 种子下载
    pass


def ehentaiDownloader(g_url):
    # 判断是否有种子文件
    html = getHTML(g_url)
    num = int(str(html.xpath('/html/body/div[2]/div[3]/div[3]/p[3]/a')[0].text)[18:-1])
    print('num=%d' % num)
    if num == 0:
        # 没种子通过页面图片下载
        print('通过页面下载')
        return downloadByPage(g_url, html)
    else:
        # 有种子通过种子下载
        print('通过种子下载')
        return downloadByTorrent(g_url, html)


def get_info(url):
    # todo 获取分页信息
    html = getHTML(url)
    info = []
    for div in html.xpath('/html/body/div[2]/form/div[2]/div'):
        href = div.xpath('./div/div/a')[0].attrib['href']
        title = div.xpath('./div/div/a/span')[0].text
        info.append((title, href))
    return info


# jpg转pdf
def convert(img_dir):
    if not img_dir:
        print('img_dir not exist')
        return
    doc = fitz.open()
    img_name_list = os.listdir(img_dir)
    total = len(img_name_list)
    count = 0
    for file_name in img_name_list:
        count += 1
        if not file_name.endswith('.jpg'):
            continue
        img_ab_path = img_dir + '\\' + file_name
        imgdoc = fitz.open(img_ab_path)
        imgbytes = imgdoc.convert_to_pdf()
        imgpdf = fitz.open('pdf', imgbytes)
        doc.insert_pdf(imgpdf)
        print('{}/{}'.format(count, total))

    pdf_name = img_dir.split('\\')[-1] + '.pdf'
    doc.save(os.path.join(img_dir, pdf_name))
    doc.close()


if __name__ == '__main__':
    # todo 获取所有收藏url
    # url = 'https://e-hentai.org/favorites.php'
    # info = get_info(url)

    # 下载单个图集
    g_url = 'https://e-hentai.org/g/944656/0c2120f188/'
    img_dir_ = ehentaiDownloader(g_url)
    # 转换为pdf
    convert(img_dir_)
