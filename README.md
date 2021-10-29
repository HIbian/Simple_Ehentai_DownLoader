# Simple_Ehentai_DownLoader
a simple ehentai downloader with jpg 2 pdf

[中文介绍](README中文.md)

## Environment

* python3.8

## How to use

* before you start,there are some tips.
  * the quality of images you download depends on what you set in e-hentai personal settings.

1. clone this project using `git clone https://github.com/HIbian/Simple_Ehentai_DownLoader.git` or other way you like.
2. open the project folder and run `pip install -r requiements.txt`.
3. copy your cookie to header which is in `SimpleEhentaiDownloader.py line 10 and line 26`.
4. if you use proxy , change it in line 15.or keep it empty
5. copy the url which manga you like,and paste into line 255.
6. don't forget change the download file directory in line 186.
7. run`python SimpleEhentaiDownloader.py` and you'll get a folder with images and a pdf file.