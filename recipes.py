import requests
from config import API_URL


def get_random_recipe():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()  #
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к API: {e}")
        return None, None, None

    try:
        data = response.json()
        meal = data.get('meals', [{}])[0]  # Если 'meals' нет, то будет пустой список и не вызовет ошибку

        name = meal.get('strMeal', 'Неизвестное название')
        instructions = meal.get('strInstructions', 'Инструкция отсутствует')
        image_url = meal.get('strMealThumb', 'Изображение отсутствует')

        return name, instructions, image_url
    except (ValueError, KeyError) as e:
        print(f"Ошибка при обработке данных: {e}")
        return None, None, None
