
import pandas as pd
import requests
import json


def visit_url(url, subject):
    print("Download: %s" % subject)
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36"}
    res = requests.get(url=url, headers=headers)
    json_cont = json.loads(res.text)
    data = json_cont["data"]
    title = []
    rank_display = []
    for num in range(len(data)):
        title.append(data[num]["title"])
        rank_display.append(data[num]["rank_display"])
    items_dict = dict(zip(title, rank_display))
    print("%d items are downloaded!" % len(data))
    return items_dict


def save_deal_items(items_original, sub):

    universities = ["Subject",
                    "Beihang University (former BUAA)",
                    "Northwestern Polytechnical University",
                    "Nanjing University of Aeronautics and Astronautics",
                    "Beijing Institute of Technology",
                    "Nanjing University of Science and Technology",
                    "‎Harbin Engineering University",
                    "University of Electronic Science and Technology of China",
                    "Xidian University",
                    "Beijing University of Posts and Telecommunications",
                    "Northeastern University (China)",
                    "University of Science and Technology Beijing",
                    "Beijing Jiaotong University",
                    "Xi’an Jiaotong University",
                    "Hohai University",
                    "Georgia Institute of Technology",
                    "University of Waterloo",
                    "Technische Universität Dresden",
                    "Vienna University of Technology",
                    "Politecnico di Milano",
                    "Carnegie Mellon University"]
    temp = []
    for u in universities:
        if u in items_original.keys():
            temp.append((u, items_original[u]))
        else:
            temp.append((u, None))
    subject = {"Subject": sub}
    items = {**dict(temp), **subject}
    write_to_file(items, universities)
    return


def write_to_file(item, fieldnames):
    """
    save to csv file
    :param item: the dictionary item
    :return: None
    """
    import csv
    import os
    save_path = r"./QSRanking.csv"
    with open(save_path, mode='a', encoding='utf_8', newline='') as f:
        # "a" - Append - Opens a file for appending, creates the file if it does not exist
        # use encoding=utf_8 to make sure it will not Garble
        # use the way of DictWrite to write
        w = csv.DictWriter(f, fieldnames=fieldnames)
        # if the file is empty, then write the headers
        file_is_empty = os.stat(save_path).st_size == 0
        if file_is_empty:
            w.writeheader()
        w.writerow(item)
    return




if __name__ == "__main__":

    json_urls = pd.read_csv("./subject_json_url.csv")
    for sub, url in zip(json_urls["subject"], json_urls["json_url"]):
        items_dict = visit_url(url, sub)
        save_deal_items(items_dict, sub)
