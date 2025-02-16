import requests
import os
from dotenv import load_dotenv


def is_shorten_link(token, link):
    api_url = 'https://api.vk.ru/method/utils.getLinkStats'
    key = link.split('/')[-1]
    params = {"access_token": token,
              "key": key,
              "v": "5.199"
              }
    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        answer = response.json()
        if "response" in answer:
            return True
        else:
            return False
    except requests.exceptions.HTTPError as e:
        print(f"Ошибка запроса: {e}")
    except ValueError as e:
        print(f"{e}")
    except KeyError:
        print("Ошибка: неожиданный формат ответа от API.")
    return False


def shorten_link(token, link):
    api_url = 'https://api.vk.ru/method/utils.getShortLink'
    params = {"access_token": token,
              "url": link,
              "v": "5.199"
              }
    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        answer = response.json()
        short_link = answer["response"]["short_url"]
        print(f'Сокращенная ссылка: {short_link}')
        return short_link
    except requests.exceptions.HTTPError as e:
        print(f"Ошибка запроса: {e}")
    except ValueError as e:
        print(f"{e}")
    except KeyError:
        print("Ошибка: неожиданный формат ответа от API.")
    return False


def count_clicks(token, link):
    api_url = 'https://api.vk.ru/method/utils.getLinkStats'
    key = link.split('/')[-1]
    params = {"access_token": token,
              "key": key,
              "v": "5.199"
              }
    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        answer = response.json()
        link_stats = answer["response"]["stats"][0]["views"]
        print(f'Количество кликов: {link_stats}')
        return link_stats
    except requests.exceptions.HTTPError as e:
        print(f"Ошибка запроса: {e}")
    except ValueError as e:
        print(f"{e}")
    except KeyError:
        print("Ошибка: неожиданный формат ответа от API.")
    return False


def main(token, link):
    if is_shorten_link(token, link):
        count_clicks(token, link)
    else:
        shorten_link(token, link)


if __name__ == "__main__":
    load_dotenv()
    vk_token = os.getenv("VK_TOKEN")
    user_input = input("Введите ссылку: ")
    main(vk_token, user_input)
