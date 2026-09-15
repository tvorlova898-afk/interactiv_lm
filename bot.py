import json
import vk_api

from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id


# =========================
# НАСТРОЙКИ
# =========================

TOKEN = 'vk1.a.Efw0X7zBaULZCW1Nue-9l43ZzkyCryQzDxY6hkI3Xvy9ikOxlU_3NGaaq2Ju-_4dOxbY7kw9bDjXy3BUep633qbKEXPbQB_zv0Y3OyY6Qn4KhK6oJPUMo1F9hadG6rz32U_gR8M2DsNskDCat3DM8EsrxYBNlcTf3XxvuCi3p9qclsz4WEXuwWtAMzy3qi31lC6YGyvHulsxRHVhAlZTrQ'
GROUP_ID = 239491424


# =========================
# ПОДКЛЮЧЕНИЕ К VK
# =========================

vk_session = vk_api.VkApi(token=TOKEN)
vk = vk_session.get_api()

print("VK API: подключение установлено")


# =========================
# LONG POLL
# =========================

try:
    longpoll = VkBotLongPoll(vk_session, GROUP_ID)
    print("✅ Long Poll: подключение установлено")
except Exception as e:
    print("❌ Ошибка подключения Long Poll:")
    print(e)
    raise


# =========================
# СОСТОЯНИЕ ПОЛЬЗОВАТЕЛЕЙ
# =========================

user_progress = {}


# =========================
# КЛАВИАТУРЫ
# =========================

def get_keyboard(step):

    kb = VkKeyboard(one_time=False)

    if step == 1:

        kb.add_button(
            'Услуги',
            color=VkKeyboardColor.POSITIVE,
            payload=json.dumps({"command": "uslugi"})
        )

        kb.add_line()

        kb.add_button(
            'Товары',
            color=VkKeyboardColor.NEGATIVE,
            payload=json.dumps({"command": "tovary"})
        )

        kb.add_line()

        kb.add_button(
            'Обучение',
            color=VkKeyboardColor.SECONDARY,
            payload=json.dumps({"command": "obuchenie"})
        )

    elif step == 2:

        kb.add_button(
            'Быстрые продажи',
            color=VkKeyboardColor.POSITIVE,
            payload=json.dumps({"command": "prodazhi"})
        )

        kb.add_line()

        kb.add_button(
            'Прогрев',
            color=VkKeyboardColor.NEGATIVE,
            payload=json.dumps({"command": "progrev"})
        )

        kb.add_line()

        kb.add_button(
            'Активация базы',
            color=VkKeyboardColor.SECONDARY,
            payload=json.dumps({"command": "aktivaciya"})
        )

    elif step == 3:

        kb.add_button(
            'Минимум ресурсов',
            color=VkKeyboardColor.POSITIVE,
            payload=json.dumps({"command": "min"})
        )

        kb.add_line()

        kb.add_button(
            'Средне',
            color=VkKeyboardColor.NEGATIVE,
            payload=json.dumps({"command": "mid"})
        )

        kb.add_line()

        kb.add_button(
            'Максимум',
            color=VkKeyboardColor.SECONDARY,
            payload=json.dumps({"command": "max"})
        )

    elif step == 4:

        kb.add_button(
            '🔄 Пройти заново',
            color=VkKeyboardColor.SECONDARY,
            payload=json.dumps({"command": "restart"})
        )

        kb.add_line()

        kb.add_button(
            '🚀 Внедрить под ключ',
            color=VkKeyboardColor.POSITIVE,
            payload=json.dumps({"command": "consult"})
        )

    return kb.get_keyboard()


# =========================
# ОТПРАВКА СООБЩЕНИЯ
# =========================

def send_msg(user_id, text, step=None):

    keyboard = get_keyboard(step) if step else None

    vk.messages.send(
        user_id=user_id,
        message=text,
        random_id=get_random_id(),
        keyboard=keyboard
    )


# =========================
# НАЧАЛО ТЕСТА
# =========================

def start_test(user_id):

    user_progress[user_id] = {
        'step': 1
    }

    send_msg(
        user_id,
        "🎮 Привет! Давай подберём идеальную механику запуска.\n\n"
        "Что вы продаёте?",
        1
    )


# =========================
# РЕЗУЛЬТАТ
# =========================

def get_result(product, goal, resources):

    # Услуги + быстрые продажи
    if product == 'uslugi' and goal == 'prodazhi':

        result = (
            "🔥 ВАША МЕХАНИКА: БЛИЦ-АКЦИЯ\n\n"
            "Если вы продаёте услуги и хотите получить "
            "быстрый результат, вам подойдёт механика "
            "короткого предложения с ограниченным сроком "
            "и понятным действием.\n\n"
            "Главная задача — не перегружать человека "
            "длинным прогревом, а быстро довести его "
            "до решения."
        )

    # Товары
    elif product == 'tovary':

        result = (
            "🎁 ВАША МЕХАНИКА: ТАЙНЫЙ ЯЩИК\n\n"
            "Для товаров хорошо работает механика, "
            "в которой человеку интересно узнать, "
            "что именно он получит.\n\n"
            "Здесь можно использовать подборки, "
            "квиз, ограниченные предложения или "
            "механику неожиданного выбора."
        )

    # Обучение + прогрев
    elif product == 'obuchenie' and goal == 'progrev':

        result = (
            "🗺️ ВАША МЕХАНИКА: КАРТА СОКРОВИЩ\n\n"
            "Для образовательного продукта лучше "
            "сначала провести человека через несколько "
            "понятных шагов и показать ценность результата.\n\n"
            "Ваша задача — дать человеку почувствовать: "
            "«Я уже двигаюсь к результату»."
        )

    # Активация базы
    elif goal == 'aktivaciya':

        result = (
            "⚡ ВАША МЕХАНИКА: ПОВТОРНЫЙ СТАРТ\n\n"
            "Если главная задача — оживить существующую "
            "базу, не обязательно сразу продавать.\n\n"
            "Лучше вернуть внимание через простое "
            "действие: выбор, мини-тест, полезный материал "
            "или персональную рекомендацию."
        )

    # Остальные варианты
    else:

        result = (
            "🧩 ВАША МЕХАНИКА: МАРШРУТ К РЕЗУЛЬТАТУ\n\n"
            "В вашем случае лучше всего подойдёт механика, "
            "которая сначала определяет ситуацию человека, "
            "а затем предлагает ему следующий шаг.\n\n"
            "Это позволяет не отправлять всем одно и то же "
            "предложение, а подстраивать путь под запрос."
        )

    # Учитываем ресурсы
    if resources == 'min':

        result += (
            "\n\n💡 Ресурсов немного — значит, "
            "механику стоит делать максимально простой: "
            "один сценарий, минимум ручной работы "
            "и понятная точка продажи."
        )

    elif resources == 'mid':

        result += (
            "\n\n💡 При среднем объёме ресурсов можно "
            "добавить сегментацию и несколько вариантов "
            "сценария в зависимости от ответов."
        )

    elif resources == 'max':

        result += (
            "\n\n💡 При большом объёме ресурсов можно "
            "собрать полноценную автоматизированную "
            "воронку с несколькими ветками и "
            "дополнительными точками взаимодействия."
        )

    result += (
        "\n\n🚀 Хотите внедрить эту механику под ключ?"
    )

    return result


# =========================
# ОБРАБОТКА СООБЩЕНИЙ
# =========================

for event in longpoll.listen():

    try:

        if event.type != VkBotEventType.MESSAGE_NEW:
            continue

        msg = event.obj.message

        user_id = msg['from_id']

        text = msg.get('text', '').strip().lower()

        # -------------------------
        # Получаем payload
        # -------------------------

        payload = msg.get('payload')
        cmd = None

        if payload:

            try:

                if isinstance(payload, str):
                    payload = json.loads(payload)

                if isinstance(payload, dict):
                    cmd = payload.get('command')

            except (json.JSONDecodeError, TypeError, AttributeError):

                cmd = None

        print(
            f"📩 Сообщение от {user_id}: "
            f"text='{text}', command='{cmd}'"
        )

        # -------------------------
        # Перезапуск
        # -------------------------

        if text == 'начать' or cmd == 'restart':

            start_test(user_id)
            continue

        # -------------------------
        # Кнопка консультации
        # -------------------------

        if cmd == 'consult':

            send_msg(
                user_id,
                "🚀 Отлично!\n\n"
                "Напишите мне в личные сообщения, "
                "и обсудим, как такую механику можно "
                "внедрить под ключ:\n"
                "https://vk.me/club239491424"
            )

            continue

        # -------------------------
        # Если пользователь ещё
        # не начал тест
        # -------------------------

        if user_id not in user_progress:

            send_msg(
                user_id,
                "Чтобы начать тест, напишите «Начать»."
            )

            continue

        # -------------------------
        # Текущий шаг
        # -------------------------

        step = user_progress[user_id]['step']

        # =========================
        # ШАГ 1
        # =========================

        if step == 1:

            allowed = {
                'uslugi',
                'tovary',
                'obuchenie'
            }

            if cmd not in allowed:

                send_msg(
                    user_id,
                    "Пожалуйста, выберите один из вариантов.",
                    1
                )

                continue

            user_progress[user_id]['product'] = cmd
            user_progress[user_id]['step'] = 2

            send_msg(
                user_id,
                "Какая главная цель запуска?",
                2
            )

        # =========================
        # ШАГ 2
        # =========================

        elif step == 2:

            allowed = {
                'prodazhi',
                'progrev',
                'aktivaciya'
            }

            if cmd not in allowed:

                send_msg(
                    user_id,
                    "Пожалуйста, выберите один из вариантов.",
                    2
                )

                continue

            user_progress[user_id]['goal'] = cmd
            user_progress[user_id]['step'] = 3

            send_msg(
                user_id,
                "Сколько ресурсов "
                "(времени и денег) готовы вложить?",
                3
            )

        # =========================
        # ШАГ 3
        # =========================

        elif step == 3:

            allowed = {
                'min',
                'mid',
                'max'
            }

            if cmd not in allowed:

                send_msg(
                    user_id,
                    "Пожалуйста, выберите один из вариантов.",
                    3
                )

                continue

            user_progress[user_id]['resources'] = cmd

            product = user_progress[user_id]['product']
            goal = user_progress[user_id]['goal']
            resources = user_progress[user_id]['resources']

            result = get_result(
                product,
                goal,
                resources
            )

            user_progress[user_id]['step'] = 4

            send_msg(
                user_id,
                result,
                4
            )

        # =========================
        # ШАГ 4
        # =========================

        elif step == 4:

            send_msg(
                user_id,
                "Тест уже завершён.\n\n"
                "Если хотите пройти его ещё раз, "
                "нажмите «Пройти заново»."
                ,
                4
            )

    except Exception as e:

        print("❌ Ошибка обработки сообщения:")
        print(repr(e))
