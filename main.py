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
        return "response" in answer
    except requests.exceptions.HTTPError as e:
        return f"Ошибка запроса: {e}"
    except ValueError as e:
        return f"{e}"
    except KeyError:
        return "Ошибка: неожиданный формат ответа от API."


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
        return f"Сокращенная ссылка: {short_link}"
    except requests.exceptions.HTTPError as e:
        return f"Ошибка запроса: {e}"
    except ValueError as e:
        return f"{e}"
    except KeyError:
        return "Ошибка: неожиданный формат ответа от API."


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
        return f"Количество кликов: {link_stats}"
    except requests.exceptions.HTTPError as e:
        return f"Ошибка запроса: {e}"
    except ValueError as e:
        return f"{e}"
    except KeyError:
        return "Ошибка: неожиданный формат ответа от API."


def main(token, link):
    if is_shorten_link(token, link):
        return count_clicks(token, link)
    else:
        return shorten_link(token, link)


if __name__ == "__main__":
    load_dotenv()
    vk_token = os.getenv("VK_TOKEN")
    user_input = input("Введите ссылку: ")
    result = main(vk_token, user_input)
    print(result)
    