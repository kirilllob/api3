import requests
from urllib.parse import urlparse
import os
import argparse
from dotenv import load_dotenv 


def shorten_link(token, long_url):
    url = 'https://api.vk.ru/method/utils.getShortLink'
    params = {"v": 5.199, "url": long_url}
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()["response"]["short_url"]


def count_clics(token, short_link):
    url = 'https://api.vk.ru/method/utils.getLinkStats'
    params = {
        "v": 5.236,
        "interval": "forever",
        "key": short_link,
        "extended": 0
    }
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()["response"]["stats"]


def main():
    load_dotenv()
    token = os.environ['VK_TOKEN']
    parser = argparse.ArgumentParser(description='эта программа, которая позволяет посчитать клики по ссылкам')
    parser.add_argument('--url', type=str, help='введите ссылку')
    args = parser.parse_args()
    parsed_url = urlparse(args.url)
    parsed_split_url = "".join(parsed_url.path.split("/"))
    try:
        if parsed_url.netloc == "vk.cc":
            print("Количество кликов по ссылке:",
                  count_clics(token, parsed_split_url)[0]["views"])
        else:
            print("сокращёная ссылка:", shorten_link(token, args.url))
    except requests.exceptions.HTTPError:
        print("проверьте вашу ссылку")


if __name__ == "__main__":
    main()
