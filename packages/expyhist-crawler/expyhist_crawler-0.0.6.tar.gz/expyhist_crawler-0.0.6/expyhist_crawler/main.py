# -*- coding:utf-8 -*-
# !/usr/bin/env python


from expyhist_crawler.decorator import save_decorator
from expyhist_crawler.setting import set_database_path

from expyhist_crawler.crawler.app_rank_crawler import AppRankScrapy


@save_decorator("app_rank", set_database_path("crawler.db"), "append")
def app_rank():

    return AppRankScrapy().get_result()


if __name__ == "__main__":
    app_rank()
