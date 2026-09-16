import json
import sys
import traceback

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id


TOKEN = "vk1.a.Efw0X7zBaULZCW1Nue-9l43ZzkyCryQzDxY6hkI3Xvy9ikOxlU_3NGaaq2Ju-_4dOxbY7kw9bDjXy3BUep633qbKEXPbQB_zv0Y3OyY6Qn4KhK6oJPUMo1F9hadG6rz32U_gR8M2DsNskDCat3DM8EsrxYBNlcTf3XxvuCi3p9qclsz4WEXuwWtAMzy3qi31lC6YGyvHulsxRHVhAlZTrQ"
GROUP_ID = 239491424

LOG_FILE = "/app/data/bot.log"


# ============================================================
# ЛОГИРОВАНИЕ
# ============================================================

def log(message):
    message = str(message)

    # В рабочий лог Bothost
    try:
        sys.stderr.write(message + "\n")
        sys.stderr.flush()
    except Exception:
        pass

    # Дополнительно в файл
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(message + "\n")
            f.flush()
    except Exception:
        pass


# ============================================================
# ЗАПУСК
# ============================================================

log("========================================")
log("ЗАПУСК БОТА")
log("========================================")

try:

    log("Версия vk_api: " + getattr(vk_api, "__version__", "unknown"))

    log("Создаю VK-сессию...")

    vk_session = vk_api.VkApi(token=TOKEN)
    vk = vk_session.get_api()

    log("VK API: подключение создано")

    log("Подключаю Bots Long Poll...")

    longpoll = VkBotLongPoll(
        vk_session,
        GROUP_ID
    )

    log("Bots Long Poll: подключение установлено")
    log("БОТ ЗАПУЩЕН. ОЖИДАЮ СООБЩЕНИЯ.")

except Exception as e:

    log("!!! ОШИБКА ЗАПУСКА !!!")
    log("Тип: " + type(e).__name__)
    log("Ошибка: " + str(e))
    log(traceback.format_exc())

    raise


# ============================================================
# СОСТОЯНИЕ ПОЛЬЗОВАТЕЛЕЙ
# ============================================================

user_progress = {}


# ============================================================
# КЛАВИАТУРА
# ============================================================

def get_keyboard(step):

    kb = VkKeyboard(one_time=False)

    if step == 1:

        kb.add_button(
            "Услуги",
            color=VkKeyboardColor.POSITIVE,
            payload=json.dumps({
                "command": "uslugi"
            })
        )

        kb.add_line()

        kb.add_button(
            "Товары",
            color=VkKeyboardColor.NEGATIVE,
            payload=json.dumps({
                "command": "tovary"
            })
        )

        kb.add_line()

        kb.add_button(
            "Обучение",
            color=VkKeyboardColor.SECONDARY,
            payload=json.dumps({
                "command": "obuchenie"
            })
        )

    elif step == 2:

        kb.add_button(
            "Быстрые продажи",
            color=VkKeyboardColor.POSITIVE,
            payload=json.dumps({
                "command": "prodazhi"
            })
        )

        kb.add_line()

        kb.add_button(
            "Прогрев",
            color=VkKeyboardColor.NEGATIVE,
            payload=json.dumps({
                "command": "progrev"
            })
        )

        kb.add_line()

        kb.add_button(
            "Активация базы",
            color=VkKeyboardColor.SECONDARY,
            payload=json.dumps({
                "command": "aktivaciya"
            })
        )

    elif step == 3:

        kb.add_button(
            "Минимум ресурсов",
            color=VkKeyboardColor.POSITIVE,
            payload=json.dumps({
                "command": "min"
            })
        )

        kb.add_line()

        kb.add_button(
            "Средне",
            color=VkKeyboardColor.NEGATIVE,
            payload=json.dumps({
                "command": "mid"
            })
        )

        kb.add_line()

        kb.add_button(
            "Максимум",
            color=VkKeyboardColor.SECONDARY,
            payload=json.dumps({
                "command": "max"
            })
        )

    elif step == 4:

        kb.add_button(
            "🔄 Пройти заново",
            color=VkKeyboardColor.SECONDARY,
            payload=json.dumps({
                "command": "restart"
            })
        )

        kb.add_line()

        kb.add_button(
            "🚀 Внедрить под ключ",
            color=VkKeyboardColor.POSITIVE,
            payload=json.dumps({
                "command": "consult"
            })
        )

    return kb.get_keyboard()


# ============================================================
# ОТПРАВКА СООБЩЕНИЯ
# ============================================================

def send_msg(user_id, text, step=None):

    log("Пытаюсь отправить сообщение пользователю: " + str(user_id))

    try:

        # Сначала отправляем БЕЗ клавиатуры.
        # Это специально: проверяем сам messages.send.
        result = vk.messages.send(
            user_id=user_id,
            message=text,
            random_id=get_random_id()
        )

        log("messages.send БЕЗ КЛАВИАТУРЫ: УСПЕШНО")
        log("Ответ VK: " + repr(result))

    except Exception as e:

        log("========================================")
        log("ОШИБКА VK ПРИ messages.send")
        log("Тип: " + type(e).__name__)
        log("str: " + str(e))
        log("repr: " + repr(e))

        if hasattr(e, "code"):
            log("КОД VK: " + str(e.code))

        if hasattr(e, "error"):
            log("ДАННЫЕ VK: " + repr(e.error))

        log(traceback.format_exc())
        log("========================================")

        raise

    # Если клавиатура не нужна — всё.
    if step is None:
        return

    # Теперь отдельно проверяем отправку клавиатуры.
    try:

        keyboard = get_keyboard(step)

        log("Клавиатура сформирована")
        log("Keyboard: " + repr(keyboard))

        result = vk.messages.send(
            user_id=user_id,
            message=text,
            random_id=get_random_id(),
            keyboard=keyboard
        )

        log("messages.send С КЛАВИАТУРОЙ: УСПЕШНО")
        log("Ответ VK: " + repr(result))

    except Exception as e:

        log("========================================")
        log("ОШИБКА VK ПРИ messages.send С КЛАВИАТУРОЙ")
        log("Тип: " + type(e).__name__)
        log("str: " + str(e))
        log("repr: " + repr(e))

        if hasattr(e, "code"):
            log("КОД VK: " + str(e.code))

        if hasattr(e, "error"):
            log("ДАННЫЕ VK: " + repr(e.error))

        log(traceback.format_exc())
        log("========================================")

        raise


# ============================================================
# НАЧАЛО ТЕСТА
# ============================================================

def start_test(user_id):

    user_progress[user_id] = {
        "step": 1
    }

    send_msg(
        user_id,
        "🎮 Привет! Давай подберём идеальную механику запуска.\n\n"
        "Что вы продаёте?",
        1
    )


# ============================================================
# РЕЗУЛЬТАТ
# ============================================================

def get_result(product, goal, resources):

    if product == "uslugi" and goal == "prodazhi":

        result = (
            "🔥 ВАША МЕХАНИКА: БЛИЦ-АКЦИЯ\n\n"
            "Если вы продаёте услуги и хотите получить быстрый "
            "результат, вам подойдёт короткое предложение с "
            "понятным действием и ограниченным сроком."
        )

    elif product == "tovary":

        result = (
            "🎁 ВАША МЕХАНИКА: ТАЙНЫЙ ЯЩИК\n\n"
            "Для товаров хорошо работает механика, в которой "
            "человеку интересно узнать, что именно он получит. "
            "Это может быть подборка, квиз или специальное предложение."
        )

    elif product == "obuchenie" and goal == "progrev":

        result = (
            "🗺️ ВАША МЕХАНИКА: КАРТА СОКРОВИЩ\n\n"
            "Для образовательного продукта хорошо провести человека "
            "через несколько понятных шагов и показать ценность результата."
        )

    elif goal == "aktivaciya":

        result = (
            "⚡ ВАША МЕХАНИКА: ПОВТОРНЫЙ СТАРТ\n\n"
            "Если задача — оживить существующую базу, можно вернуть "
            "внимание через простой выбор, мини-тест, полезный материал "
            "или персональную рекомендацию."
        )

    else:

        result = (
            "🧩 ВАША МЕХАНИКА: МАРШРУТ К РЕЗУЛЬТАТУ\n\n"
            "В вашем случае подойдёт механика, которая сначала "
            "определяет ситуацию человека, а затем предлагает "
            "ему следующий шаг."
        )

    if resources == "min":

        result += (
            "\n\n💡 Ресурсов немного — делаем механику простой: "
            "один сценарий, минимум ручной работы и понятная точка продажи."
        )

    elif resources == "mid":

        result += (
            "\n\n💡 При среднем объёме ресурсов можно добавить "
            "сегментацию и несколько вариантов сценария."
        )

    elif resources == "max":

        result += (
            "\n\n💡 При большом объёме ресурсов можно собрать "
            "полноценную автоматизированную воронку с несколькими ветками."
        )

    result += "\n\n🚀 Хотите внедрить эту механику под ключ?"

    return result


# ============================================================
# ОСНОВНОЙ ЦИКЛ
# ============================================================

for event in longpoll.listen():

    try:

        if event.type != VkBotEventType.MESSAGE_NEW:
            continue

        # Для MESSAGE_NEW в vk_api 11.10.1
        # сообщение находится в event.message.
        message = event.message

        if not message:
            log("MESSAGE_NEW получено, но event.message пустой")
            continue

        user_id = message.get("from_id")
        peer_id = message.get("peer_id")
        text = (message.get("text") or "").strip().lower()

        payload = message.get("payload")

        command = None

        if payload:

            try:

                if isinstance(payload, str):
                    payload = json.loads(payload)

                if isinstance(payload, dict):
                    command = payload.get("command")

            except (
                json.JSONDecodeError,
                TypeError,
                AttributeError
            ):

                command = None

        log("----------------------------------------")
        log("ВХОДЯЩЕЕ СООБЩЕНИЕ")
        log("user_id: " + str(user_id))
        log("peer_id: " + str(peer_id))
        log("text: " + repr(text))
        log("payload: " + repr(payload))
        log("command: " + repr(command))
        log("----------------------------------------")

        # ----------------------------------------------------
        # НАЧАТЬ / ЗАНОВО
        # ----------------------------------------------------

        if text == "начать" or command == "restart":

            start_test(user_id)
            continue

        # ----------------------------------------------------
        # КОНСУЛЬТАЦИЯ
        # ----------------------------------------------------

        if command == "consult":

            send_msg(
                user_id,
                "🚀 Отлично!\n\n"
                "Напишите мне в личные сообщения, и обсудим "
                "настройку вашей воронки:\n"
                "https://vk.me/club239491424"
            )

            continue

        # ----------------------------------------------------
        # ПОЛЬЗОВАТЕЛЬ ЕЩЁ НЕ НАЧАЛ ТЕСТ
        # ----------------------------------------------------

        if user_id not in user_progress:

            send_msg(
                user_id,
                "Чтобы начать тест, напишите «Начать»."
            )

            continue

        step = user_progress[user_id]["step"]

        # ----------------------------------------------------
        # ШАГ 1
        # ----------------------------------------------------

        if step == 1:

            if command not in {
                "uslugi",
                "tovary",
                "obuchenie"
            }:

                send_msg(
                    user_id,
                    "Пожалуйста, выберите один из вариантов.",
                    1
                )

                continue

            user_progress[user_id]["product"] = command
            user_progress[user_id]["step"] = 2

            send_msg(
                user_id,
                "Какая главная цель запуска?",
                2
            )

        # ----------------------------------------------------
        # ШАГ 2
        # ----------------------------------------------------

        elif step == 2:

            if command not in {
                "prodazhi",
                "progrev",
                "aktivaciya"
            }:

                send_msg(
                    user_id,
                    "Пожалуйста, выберите один из вариантов.",
                    2
                )

                continue

            user_progress[user_id]["goal"] = command
            user_progress[user_id]["step"] = 3

            send_msg(
                user_id,
                "Сколько ресурсов (времени и денег) готовы вложить?",
                3
            )

        # ----------------------------------------------------
        # ШАГ 3
        # ----------------------------------------------------

        elif step == 3:

            if command not in {
                "min",
                "mid",
                "max"
            }:

                send_msg(
                    user_id,
                    "Пожалуйста, выберите один из вариантов.",
                    3
                )

                continue

            user_progress[user_id]["resources"] = command

            result = get_result(
                user_progress[user_id]["product"],
                user_progress[user_id]["goal"],
                user_progress[user_id]["resources"]
            )

            user_progress[user_id]["step"] = 4

            send_msg(
                user_id,
                result,
                4
            )

        # ----------------------------------------------------
        # ШАГ 4
        # ----------------------------------------------------

        elif step == 4:

            send_msg(
                user_id,
                "Тест уже завершён.\n\n"
                "Если хотите пройти его ещё раз, "
                "нажмите «Пройти заново».",
                4
            )

    except Exception as e:

        log("========================================")
        log("ОШИБКА ОБРАБОТКИ СОБЫТИЯ")
        log("Тип: " + type(e).__name__)
        log("str: " + str(e))
        log("repr: " + repr(e))

        if hasattr(e, "code"):
            log("КОД VK: " + str(e.code))

        if hasattr(e, "error"):
            log("ДАННЫЕ VK: " + repr(e.error))

        log(traceback.format_exc())
        log("========================================")
