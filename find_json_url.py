
import requests
import pandas as pd
import re


def json_url(subject, url):
    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36"}
    res = requests.get(url=url, headers=headers)
    link = res.headers["link"]
    # regular expression
    pattern = re.compile(".*?node/(.*?)>.*?")
    number = pattern.findall(link)
    json_url = "https://www.topuniversities.com/sites/default/files/qs-rankings-data/" + number[0] + ".txt"

    item_dict = {"subject": subject, "json_url": json_url}
    write_to_file(item_dict)


def write_to_file(item):
    """
    save to csv file
    :param item: the dictionary item
    :return: None
    """
    import csv
    import os
    save_path = r"./subject_json_url.csv"
    with open(save_path, mode='a', encoding='utf_8', newline='') as f:
        # "a" - Append - Opens a file for appending, creates the file if it does not exist
        # use encoding=utf_8 to make sure it will not Garble
        fieldnames = ["subject", "json_url"]
        # use the way of DictWrite to write
        w = csv.DictWriter(f, fieldnames=fieldnames)
        # if the file is empty, then write the headers
        file_is_empty = os.stat(save_path).st_size == 0
        if file_is_empty:
            w.writeheader()
        w.writerow(item)
    return


if __name__ == "__main__":

    subject_urls = pd.read_csv("./subject_url.csv")
    front_url = "https://www.topuniversities.com"
    for sub, part_url in zip(subject_urls["Subject"], subject_urls["partial_url"]):
        url = front_url+part_url
        json_url(sub, url)
