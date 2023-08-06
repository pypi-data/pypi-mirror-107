# -*- coding:utf-8 -*-
# !/usr/bin/env python

import pandas as pd
import os
import random

from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem

from configparser import ConfigParser

# dict to df
df_dict = dict(
    app_name=["粉象生活", "蜜源", "骑士卡", "花生日记", "好省", "福袋生活"],
    app_id=["1383296825", "1262351972", "1436462010", "1390240947", "1332598333", "1463740455"],
    rank_analysis=[
        "dSB1TixkdUh9SldKdQ5cCitwf1BpZ0hDaQIFUz1vVAlXWzdccBMfUUBAFxZWVg90FVAABAMBBQUGAFwODSQXBw==",
        "dSB1TixkdUh9WmlJdR5iQCtgVRhpZ0hDaQIFUz1vVAlXWzdccBMfUUBAFxZWVg90FVAABAMBBQYCClQBCCQXBw==",
        "dSB1TixkdUh+dH0CdiBuQSlwcxZpZ0hDaQIFUz1vVAlXWzdccBMfUUBAFxZWVg90FVAABAMBBQYDAFQCASQXBw==",
        "dSB1TixkdUh9SltHdQ5mTytgZ1JpZ0hDaQIFUz1vVAlXWzdccBMfUUBAFxZWVg90FVAABAMBBQYFAFwHDCQXBw==",
        "dSB1TixkdUh9Sn1JdjBcDClOextpZ0hDaQIFUz1vVAlXWzdccBMfUUBAFxZWVg90FVAABAMBBQAJCVUFDSQXBw==",
        "dSB1TixkdUh+dGlKdh5mTypwY1BpZ0hDaQIFUz1vVAlXWzdccBMfUUBAFxZWVg90FVAABQQIBQkBD1ICDCQXBw=="
    ],
    appinfo_analysis=[
        "dTB5AixKeQV+WldJdjN5TSQXGQBAQB9RQEBZVgJYeEcFBlQIBAcEAggJAFd3G1U=",
        "dTB9BCxafQF9ZFsDdQl5TSQXGQBAQB9RQEBZVgJYeEcFBlQIBAcEBAgIDlJ3G1U=",
        "dTBlTC9aYQJ9WnFIdSN5TSQXGQBAQB9RQEBZVgJYeEcFBlQIBAcEBgMED1F3G1U=",
        "dTB5Ayx0eQB9dFsAdlZ5TSQXGQBAQB9RQEBZVgJYeEcFBlcJBQYCAAkGDFB3G1U=",
        "dTB5TCxaZQV/dH1KdVZ5TSQXGQBAQB9RQEBZVgJYeEcFBlcJBQYBCAkED1J3G1U=",
        "dTBlBCxKUwB9dGEBdjN5TSQXGQBAQB9RQEBZVgJYeEcFBlcJBQYBBgEIC1B3G1U="
    ]
)
APP_DF = pd.DataFrame(df_dict)

# random user_agent
software_names = [SoftwareName.CHROME.value]
operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]
user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)
USER_AGENT = user_agent_rotator.get_random_user_agent()


# database path
def set_database_path(database_name):
    return os.path.join(os.path.dirname(__file__), "db/{}".format(database_name))


# sleep time
SLEEP_TIME = random.random() * 10 / 2

# email and umeng account


if "config.ini" in os.listdir(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))):
    cfg = ConfigParser()
    cfg.read(os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + r"\config.ini", encoding="utf-8-sig")
    USERNAME = cfg.get("email_account", "user_name")
    PASSWORD = cfg.get("email_account", "pass_word")
    APIKEY = cfg.get("umeng_api_info", "api_key")
    APISECURITY = cfg.get("umeng_api_info", "api_security")
    APPKEYS = [cfg.get("umeng_api_info", "ios_app_keys"), cfg.get("umeng_api_info", "android_app_keys")]
else:
    print("Not Exists config.ini")

# chromedrive
CHROMEDRIVER_PATH = os.path.join(os.path.dirname(__file__),
                                 r"file/{}".format("chromedriver.exe" if os.name == "nt" else "chromedriver"))
