# -*- coding:utf-8 -*-
# !/usr/bin/env python

import requests
import re
import pandas as pd


def title_scrapy() -> pd.DataFrame:

    df = pd.DataFrame(
        dict(
            catg=["中间bar", "中间bar", "金象任务", "金象任务", "果园", "果园", "果园", "签到", "签到", "签到"],
            urls=["https://m.fenxianglife.com/fms/100004/552812/index.html",
                  "https://m.fenxianglife.com/fms/100004/3e0704/index.html",
                  "https://m.fenxianglife.com/fms/100004/bebf44/index.html",
                  "https://m.fenxianglife.com/fms/100004/8ceb00/index.html",
                  "https://m.fenxianglife.com/fms/100004/74a2e9/index.html",
                  "https://m.fenxianglife.com/fms/100004/5e7254/index.html",
                  "https://m.fenxianglife.com/fms/100004/0a7d50/index.html",
                  "https://m.fenxianglife.com/fms/100004/584d90/index.html",
                  "https://m.fenxianglife.com/fms/100004/e9aad0/index.html",
                  "https://m.fenxianglife.com/fms/100004/6f4eb4/index.html"]
        )
    )
    titles = []

    for i in df["urls"]:
        r = requests.get(url=i)
        r.encoding = "utf-8"
        title = re.findall(r"<title>(.*?)</title>", r.text)[0]
        titles.append(title)

    df["titles"] = titles

    return df


if __name__ == "__main__":
    pass
