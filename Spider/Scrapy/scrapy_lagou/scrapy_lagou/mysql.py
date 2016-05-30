#!/usr/bin/env python
# -*- coding:utf-8 -*-

import MySQLdb


def repeat_test(db, cursor):
    # 确认无重复项
    sql = """SELECT * FROM lagou_jobs WHERE positionId in (SELECT positionId FROM lagou_jobs group by positionId having count(positionId) > 1)"""

    cursor.execute(sql)
    db.commit()

    # results = cursor.fetchall()
    # print [unicode(str(x).decode('utf-8')) for x in results[0]]
    print cursor.fetchall()


def chinese_test(db, cursor):
    # 确认中文在mysql没有问题,在python中输入可以直接用中文,输出有问题,为unicode编码,但是单个输出是中文

    sql = """SELECT * FROM lagou_jobs WHERE idlagou_jobs = '%d'""" % (316)
    cursor.execute(sql)
    db.commit()
    results = cursor.fetchall()
    # print [unicode(str(x).decode('utf-8')) for x in results[0]]
    print results[0]


def salary_average(db, cursor):
    # 1、python在各个城市的最低薪资的平均值
    # 结果 一共[207, 209, 61, 111, 77, 15, 12, 3, 0, 0, 7, 45]条，平均值=[11.64, 13.0, 10.03, 10.38, 8.09, 7.4, 8.17, 8.0, 0, 0, 6.57, 7.27]
    # [[25, 11.64, 2], [25, 13.0, 2], [20, 10.03, 2], [20, 10.38, 1], [15, 8.09, 2], [15, 7.4, 3], [15, 8.17, 4], [8, 8.0, 8], [0, 0, 0], [0, 0, 0], [10, 6.57, 4], [12, 7.27, 2]]
    # 第一条就够
    citys = ['上海', '北京', '杭州', '深圳', '广州', '南京', '苏州', '天津', '无锡', '宁波', '厦门', '成都']  # 爬取城市
    average = {}
    average_list = []
    max_list = []
    min_list = []
    for city in citys:

        sql1 = """SELECT salaryMin FROM lagou_jobs WHERE city = '%s'AND (positionName LIKE '%s' OR positionName LIKE '%s')""" % (city, '%Python%', '%python%')
        cursor.execute(sql1)
        db.commit()
        result = []
        results1 = cursor.fetchall()
        for number in range(len(results1)):
            result.append(int(results1[number][0].replace('k', '')))
            # print result
        print len(result)

        sql2 = """SELECT count(*) FROM lagou_jobs WHERE city = '%s'AND (positionName LIKE '%s' OR positionName LIKE '%s')""" % (city, '%Python%', '%python%')
        cursor.execute(sql2)
        db.commit()
        results2 = cursor.fetchall()
        results2 = int(results2[0][0])
        # print [unicode(str(x).decode('utf-8')) for x in results[0]
        print results2

        if results2 > 0:
            average[city] = float(sum(result))/float(results2)
            average[city] = round(average[city], 2)
            max_list.append(max(result))
            min_list.append(min(result))
        else:
            average[city] = 0
            max_list.append(0)
            min_list.append(0)

        average_list.append(average[city])

    # print average
    # print average_list
    return [[x, average_list[k], min_list[k]] for k, x in enumerate(max_list)]


def main():
    db = MySQLdb.connect("localhost", "root", "password", "lagou_job", charset='utf8')
    cursor = db.cursor()
    salary = salary_average(db, cursor)
    print salary
    cursor.close()
    db.close()

if __name__ == '__main__':
    main()

