import subprocess
import sys


def install_requirement():
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]
        )
        print("\nRequirements are successfully installed!!!\n")
    except subprocess.CalledProcessError:
        print("\nError installing requirements. Please make sure 'pip' is installed.\n")


install_requirement()
if install_requirement():
    print("YES")

import requests
from bs4 import BeautifulSoup
import selenium
import pandas as pd
import os
import re
import keyboard
import time


def crawl():
    keyword = input("請輸入要查詢的歌名:")
    url = f"https://mojim.com/{keyword}.html?t3"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.3",
        "Cookie": "FCNEC=%5B%5B%22AKsRol-8k0P1SisPTFN60Drm0ayypgEb_s7xJxm33TwFrn0rC6c9MYU2vpCubEGGS3lQFwtvUENWAoT1RERQPI9VY5ZG0DteWs8MkOoSFBn4-ittvUF_L5dr2F4JHavcWEfbY15QHthhPotrYp8G-fOzzvGgGUQGnA%3D%3D%22%5D%5D; __gads=ID=b8df721b0b25f8b6:T=1701914625:RT=1702017063:S=ALNI_Ma2xBLZ77Ifea-tMipFEvAaualTVg; __gpi=UID=00000ca64ee972fa:T=1701914625:RT=1702017063:S=ALNI_MYYKJ5G0SPjjgNwJbfoLAyhIyzPNg; PHPSESSID=kp9fatpa0rj5hs63th7cm6714h",
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    songs = soup.find("table", class_="iB")
    data_list = []

    sequence_list = songs.find_all("span", class_="mxsh_ss1")
    singer_list = songs.find_all("span", class_="mxsh_ss2")
    source_list = songs.find_all("span", class_="mxsh_ss3")
    song_name_list = songs.find_all("span", class_="mxsh_ss4")

    # get the data and put it in the data_table
    data_table = []
    for i in range(len(sequence_list)):
        if sequence_list[i].text == " ":
            sequence_list[i] = "編號"
        else:
            sequence_list[i] = sequence_list[i].text
    data_table.append(sequence_list)

    for i in range(len(singer_list)):
        singer_list[i] = singer_list[i].text
        singer_list[0] = "歌手"
    data_table.append(singer_list)

    for i in range(len(source_list)):
        source_list[i] = source_list[i].text
        source_list[0] = "專輯來源"
    data_table.append(source_list)

    for i in range(len(song_name_list)):
        song_name_list[i] = song_name_list[i].text.split(".")
        song_name_list[i] = song_name_list[i][-1]
        song_name_list[0] = "歌名"
    data_table.append(song_name_list)

    hrefs = soup.find("dl", class_="mxsh_dl0")
    hrefs = hrefs.find_all("dd")
    href_list = []
    for href in hrefs:
        href = href.find("span", class_="mxsh_ss4")
        if href:
            a_element = href.find("a")
            if a_element:
                link = a_element.get("href")
                link = f"https://mojim.com{link}"
                href_list.append(link)
    data_table.append(href_list)

    # use pandas to save tshe data
    flag = 0
    print("\n")
    while not flag:
        want_to_save = input("是否保存查詢檔案:歌名.xlsx(YES/NO)").upper()
        print(want_to_save)
        if want_to_save == "NO":
            flag = 1
        elif want_to_save == "YES":
            flag = 1
            dir_name = "Data"
            if not os.path.exists(f"MOJIM_SONG/{dir_name}"):
                os.mkdir(f"MOJIM_SONG/{dir_name}")
            df = pd.DataFrame(data_table)
            file_path = f"MOJIM_SONG/{dir_name}/{keyword}.xlsx"
            df.to_sexcel(file_path, index=False, engine="openpyxl")
        else:
            print("重新輸入")

    # print out the options
    print("\n", "=" * 80, "\n")
    for i in range(len(sequence_list)):
        print(
            f"{sequence_list[i]}: {singer_list[i]} ; {song_name_list[i]} ; {source_list[i]}"
        )
    print("\n", "=" * 80, "\n")

    # update the url and get the response again(also update the soup)

    options = int(input("請輸入欲查詢的編號:"))
    url = href_list[options - 1]
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    print("\n", "=" * 80, "\n")
    # print(soup)
    lyrics = str(soup.find("dd", class_="fsZx3"))
    lyrics = lyrics.replace("<br/>", "\n")
    lyrics = lyrics.split("\n\n\n\n")[0]
    lyrics = re.sub(r"更多更詳盡歌詞.*?</a>", "", lyrics)
    lyrics = re.sub(r"<dd.*?>", "", lyrics)
    lyrics = re.sub(r"<ol>.*?</ol>", "", lyrics)
    lyrics = lyrics.replace("</dd>", "")
    print(f"{lyrics}")
    print("\n", "=" * 80, "\n")


while True:
    opt = int(input("請輸入選項:\n1. 查詢\n2. 退出\n>>"))
    if opt == 1:
        crawl()
    elif opt == 2:
        print("使用者退出")
        break
    else:
        print("輸入錯誤")
