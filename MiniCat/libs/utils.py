# !/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:
# Author: Vincent<vincent8280@outlook.com>
#         http://wax8280.github.io
# Created on 2017/10/10 9:52
import datetime
import time
import heapq
import os
import random
import re
import yaml
import hashlib
import platform

from functools import wraps


def md5string(x):
    return hashlib.md5(x.encode()).hexdigest()


def singleton(cls):
    instances = {}

    @wraps(cls)
    def getinstance(*args, **kw):
        if cls not in instances:
            the_instances = cls(*args, **kw)
            instances[cls] = the_instances
            return the_instances
        else:
            return instances[cls]

    return getinstance


def load_config(path):
    try:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return yaml.load(f)
        except UnicodeDecodeError:
            with open(path, 'r') as f:
                return yaml.load(f)
    except FileNotFoundError:
        return {}


def write_config(path, d):
    # path所在的目录
    if not os.path.exists(os.path.split(path)[0]):
        os.makedirs((os.path.split(path)[0]))

    dump_string = yaml.dump(d)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(dump_string)


def get_system():
    return platform.system()


def find_file(rootdir, pattern):
    finded = []
    for i in os.listdir(rootdir):
        if not os.path.isdir(os.path.join(rootdir, i)):
            if re.search(pattern, i):
                finded.append(os.path.join(rootdir, i))
    return finded


def write(folder_path, file_path, content, mode='wb'):
    path = os.path.join(folder_path, file_path)
    if not os.path.exists(os.path.split(path)[0]):
        try:
            os.makedirs((os.path.split(path)[0]))
        except FileExistsError:
            pass
    with open(path, mode) as f:
        f.write(content)


def codes_write(folder_path, file_path, content, mode='wb'):
    path = os.path.join(folder_path, file_path)
    if not os.path.exists(os.path.split(path)[0]):
        os.makedirs((os.path.split(path)[0]))
    with open(path, mode) as f:
        f.write(content)


def format_file_name(file_name, a=''):
    file_name = re.sub(r'[ \\/:*?"<>→|+\r\n]', '', file_name)

    if a:
        # 文件名太长无法保存mobi
        if len(file_name) + len(a) + 2 > 55:
            _ = 55 - len(a) - 2 - 3
            file_name = file_name[:_] + '...（{}）'.format(a)
        else:
            file_name = file_name + '（{}）'.format(a)
    else:
        if len(file_name) > 55:
            _ = 55 - 3
            file_name = file_name[:_] + '...'
        else:
            file_name = file_name
    return file_name


def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    return str(text)


def read_file_to_list(path):
    try:
        with open(path, 'r') as f:
            return [i.strip() for i in list(f.readlines())]
    except FileNotFoundError as e:
        return str(e)
    except Exception as e:
        return str(e)


def check_config(main_config, script_config, config_name, logger):
    if config_name not in script_config:
        if config_name in main_config:
            script_config.update({config_name: main_config.get(config_name)})
        else:
            logger.log_it("在配置文件中没有发现'{}'项，请确认主配置文件中或脚本配置文件中存在该项。".format(config_name), 'ERROR')
            os._exit(0)


def split_list(the_list, window):
    return [the_list[i:i + window] for i in range(0, len(the_list), window)]


def random_char(c):
    return [chr(random.choice(list(set(range(65, 123)) - set(range(91, 97))))) for i in range(c)]


def get_next_datetime_string(data_string: str, format_string: str, days: int, prev=False) -> str:
    now_datatime = datetime.datetime.strptime(data_string, format_string)
    if prev:
        return (now_datatime - datetime.timedelta(days=days)).strftime(format_string)
    else:
        return (now_datatime + datetime.timedelta(days=days)).strftime(format_string)


def compare_datetime_string(data_stringA: str, data_stringB: str, format_string: str) -> bool:
    """return true if data_stringA is bigger or equal"""
    return datetime.datetime.strptime(data_stringA, format_string) >= datetime.datetime.strptime(data_stringB,
                                                                                                 format_string)


def get_datetime_string(format_string: str) -> str:
    return datetime.datetime.fromtimestamp(time.time()).strftime(format_string)


class PriorityList(list):
    """
    >>> a = PriorityList()
    >>> a.priority_push([150, ['t5', 't6']])
    >>> print(a)
    [[150, ['t5', 't6']]]
    >>> a.priority_push([50, ['t1', 't2']])
    >>> print(a)
    [[50, ['t1', 't2']], [150, ['t5', 't6']]]
    >>> a.priority_push([100, ['t3', 't4']])
    >>> print(a)
    [[50, ['t1', 't2']], [150, ['t5', 't6']], [100, ['t3', 't4']]]
    >>> print(a.priority_pop())
    [50, ['t1', 't2']]
    >>> print(a)
    [[100, ['t3', 't4']], [150, ['t5', 't6']]]
    """

    def priority_pop(self):
        # lowest is first
        try:
            return heapq.heappop(self)
        except IndexError:
            return None

    def priority_push(self, item):
        heapq.heappush(self, item)


def make_string_to_dict(string: str) -> dict:
    '''
    accept: application/json, text/plain, */*
    Accept-Encoding: gzip, deflate, br
    Accept-Language: zh-CN,zh;q=0.9
    Connection: keep-alive
    Cookie: q_c1=8badf742c835456fbfbdfacda8f64451|1507800445000|1507800445000; _zap=087347ce-032e-4e9d-8ba0-960d04f97509; z_c0="2|1:0|10:1520348373|4:z_c0|92:Mi4xekg5b0FBQUFBQUFBc0t0NVlBZ19EU1lBQUFCZ0FsVk4xZnFMV3dCWFoybkpxSExQcE1Hc3ZFNlg1LXF4RE5Ga2pn|2c9b200ea3be31f742835d7085b9c4a88477e3329e1932cb894dc68194b001f6"; _xsrf=e43b63cf-b3d5-4dbf-a07d-1168b6415541; d_c0="AMBm1dy_6A2PTl40-bnOfe-TCLzxBm5pvn8=|1531737851"; q_c1=8badf742c835456fbfbdfacda8f64451|1531737851000|1507800445000; tgw_l7_route=1c2b7f9548c57cd7d5a535ac4812e20e
    Host: www.zhihu.com
    Referer: https://www.zhihu.com/people/labixiaoxing/answers?page=1
    User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36
    X-Requested-With: Fetch
    X-UDID: AMBm1dy_6A2PTl40-bnOfe-TCLzxBm5pvn8=
    :param str:
    :return:
    '''

    d = {}
    l = string.strip().split('\n')

    for each in l:
        split_each = each.strip().split(': ')
        d[split_each[0]] = split_each[1]

    return d


if __name__ == '__main__':
    a = '''
        accept: application/json, text/plain, */*
    Accept-Encoding: gzip, deflate, br
    Accept-Language: zh-CN,zh;q=0.9
    Connection: keep-alive
    Cookie: q_c1=8badf742c835456fbfbdfacda8f64451|1507800445000|1507800445000; _zap=087347ce-032e-4e9d-8ba0-960d04f97509; z_c0="2|1:0|10:1520348373|4:z_c0|92:Mi4xekg5b0FBQUFBQUFBc0t0NVlBZ19EU1lBQUFCZ0FsVk4xZnFMV3dCWFoybkpxSExQcE1Hc3ZFNlg1LXF4RE5Ga2pn|2c9b200ea3be31f742835d7085b9c4a88477e3329e1932cb894dc68194b001f6"; _xsrf=e43b63cf-b3d5-4dbf-a07d-1168b6415541; d_c0="AMBm1dy_6A2PTl40-bnOfe-TCLzxBm5pvn8=|1531737851"; q_c1=8badf742c835456fbfbdfacda8f64451|1531737851000|1507800445000; tgw_l7_route=1c2b7f9548c57cd7d5a535ac4812e20e
    Host: www.zhihu.com
    Referer: https://www.zhihu.com/people/labixiaoxing/answers?page=1
    User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36
    X-Requested-With: Fetch
    X-UDID: AMBm1dy_6A2PTl40-bnOfe-TCLzxBm5pvn8=   
      '''
    d = {}
    l = a.strip().split('\n')

    for each in l:
        split_each = each.strip().split(': ')
        d[split_each[0]] = split_each[1]
