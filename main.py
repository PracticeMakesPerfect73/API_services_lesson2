import requests
import os
from dotenv import load_dotenv
from urllib.parse import urlparse
import argparse

def is_shorten_link(token, link):
    api_url = 'https://api.vk.ru/method/utils.getLinkStats'
    key = urlparse(link).path.strip('/')
    params = {"access_token": token,
              "key": key,
              "v": "5.199"
              }
    response = requests.get(api_url, params=params)
    response.raise_for_status()
    answer = response.json()
    return "response" in answer


def shorten_link(token, link):
    api_url = 'https://api.vk.ru/method/utils.getShortLink'
    params = {"access_token": token,
              "url": link,
              "v": "5.199"
              }
    response = requests.get(api_url, params=params)
    response.raise_for_status()
    answer = response.json()
    short_link = answer["response"]["short_url"]
    return short_link


def count_clicks(token, link):
    api_url = 'https://api.vk.ru/method/utils.getLinkStats'
    key = urlparse(link).path.strip('/')
    params = {"access_token": token,
              "key": key,
              "v": "5.199"
              }
    response = requests.get(api_url, params=params)
    response.raise_for_status()
    answer = response.json()
    link_stats = answer["response"]["stats"][0]["views"]
    return link_stats


def main():
    load_dotenv()
    vk_token = os.environ["VK_TOKEN"]
    parser = argparse.ArgumentParser(description="VK URL Shortener & Click Counter")
    parser.add_argument("link", help="Ссылка для сокращения или проверки кликов")
    args = parser.parse_args()

    user_input = args.link
    try:
        if is_shorten_link(vk_token, user_input):
            clicks = count_clicks(vk_token, user_input)
            print(f"По вашей ссылке перешли {clicks} раз")
        else:
            short_link = shorten_link(vk_token, user_input)
            print(f"Сокращенная ссылка: {short_link}")
    except requests.exceptions.HTTPError as e:
        print(f"Ошибка запроса: {e}")
    except ValueError as e:
        print(f"{e}")
    except KeyError:
        print("Ошибка: неожиданный формат ответа от API.")


if __name__ == "__main__":
    main()
