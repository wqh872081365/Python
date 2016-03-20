#爬取http://www.dmoz.org

scrapy框架实现

爬取以下信息：

'http://www.dmoz.org/Computers/Programming/Languages/Python/Books/',

'http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/'

使用：

命令行进入项目的根目录，执行下列命令启动spider:

scrapy crawl dmoz -o items.json

该命令将采用 JSON 格式对爬取的数据进行序列化

输出items.json 文件。

参考： 

Scrapy 0.25 文档

http://scrapy-chs.readthedocs.org/zh_CN/latest/index.html    

__author__ = 'wangqihui'
