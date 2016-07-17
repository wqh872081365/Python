# 爬取拉勾网 http://www.lagou.com

使用scrapy框架实现爬取拉勾网所提供的职位信息，数据保存方式有Json和MySQL。
数据包含职位提供的主要信息，比如工作位置，学历要求，工作年限，薪酬待遇，公司规模，工作详情等等。

使用：

命令行进入项目的根目录，执行下列命令启动spider:

scrapy crawl lagou_job

输出：

items.json 文件。

MySQL保存数据。

# 需要重要的库 

scrapy

MySQLdb


__author__ = 'wangqihui'
