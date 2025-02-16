import requests
import os
from dotenv import load_dotenv
from urllib.parse import urlparse


def make_request(api_url, params):
    response = requests.get(api_url, params=params)
    response.raise_for_status()
    return response.json()


def is_shorten_link(token, link):
    api_url = 'https://api.vk.ru/method/utils.getLinkStats'
    key = urlparse(link).path.strip('/')
    params = {"access_token": token,
              "key": key,
              "v": "5.199"
              }
    answer = make_request(api_url, params)
    return "response" in answer


def shorten_link(token, link):
    api_url = 'https://api.vk.ru/method/utils.getShortLink'
    params = {"access_token": token,
              "url": link,
              "v": "5.199"
              }
    answer = make_request(api_url, params)
    short_link = answer["response"]["short_url"]
    return short_link


def count_clicks(token, link):
    api_url = 'https://api.vk.ru/method/utils.getLinkStats'
    key = urlparse(link).path.strip('/')
    params = {"access_token": token,
              "key": key,
              "v": "5.199"
              }
    answer = make_request(api_url, params)
    link_stats = answer["response"]["stats"][0]["views"]
    return link_stats


def main():
    load_dotenv()
    vk_token = os.environ["VK_TOKEN"]
    user_input = input("Введите ссылку: ")
    try:
        if is_shorten_link(vk_token, user_input):
            clicks = count_clicks(vk_token, user_input)
            print(f"Количество кликов: {clicks}")
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
