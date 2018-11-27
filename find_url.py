
import requests
from bs4 import BeautifulSoup


def create_url():
    url = "https://www.topuniversities.com/subject-rankings/2018"
    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36"}

    res = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(res.content,"lxml")
    sub_lists = soup.find_all(class_="sub-list")
    for sub in sub_lists:
        items = sub.find_all("a")
        for item in items:
            yield {
                "Subject": item.get_text(),
                "partial_url": item["href"]
            }


def write_to_file(item):
    """
    save to csv file
    :param item: the dictionary item
    :return: None
    """
    import csv
    import os
    save_path = r"./subject_url.csv"
    with open(save_path, mode='a', encoding='utf_8', newline='') as f:
        # "a" - Append - Opens a file for appending, creates the file if it does not exist
        # use encoding=utf_8 to make sure it will not Garble
        fieldnames = ["Subject", "partial_url"]
        # use the way of DictWrite to write
        w = csv.DictWriter(f, fieldnames=fieldnames)
        # if the file is empty, then write the headers
        file_is_empty = os.stat(save_path).st_size == 0
        if file_is_empty:
            w.writeheader()
        w.writerow(item)
    return


if __name__ == "__main__":

    items = create_url()
    for item in items:
        write_to_file(item)

