import json
import vk_api

from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id


# ============================================================
# НАСТРОЙКИ
# ============================================================

TOKEN = "vk1.a.Efw0X7zBaULZCW1Nue-9l43ZzkyCryQzDxY6hkI3Xvy9ikOxlU_3NGaaq2Ju-_4dOxbY7kw9bDjXy3BUep633qbKEXPbQB_zv0Y3OyY6Qn4KhK6oJPUMo1F9hadG6rz32U_gR8M2DsNskDCat3DM8EsrxYBNlcTf3XxvuCi3p9qclsz4WEXuwWtAMzy3qi31lC6YGyvHulsxRHVhAlZTrQ"
GROUP_ID = 239491424


# ============================================================
# ПОДКЛЮЧЕНИЕ VK
# ============================================================

def main():

    print("Запуск бота...")

    vk_session = vk_api.VkApi(token=TOKEN)
    vk = vk_session.get_api()

    print("VK API: подключение установлено")

    longpoll = VkBotLongPoll(vk_session, GROUP_ID)

    print("Long Poll: подключение установлено")
    print("Бот запущен. Ожидаю сообщения...")


    # ========================================================
    # ХРАНЕНИЕ ПРОГРЕССА ПОЛЬЗОВАТЕЛЕЙ
    # ========================================================

    user_progress = {}


    # ========================================================
    # КЛАВИАТУРЫ
    # ========================================================

    def get_keyboard(step):

        kb = VkKeyboard(one_time=False)

        if step == 1:

            kb.add_button(
                "Услуги",
                color=VkKeyboardColor.POSITIVE,
                payload=json.dumps({"command": "uslugi"})
            )

            kb.add_line()

            kb.add_button(
                "Товары",
                color=VkKeyboardColor.NEGATIVE,
                payload=json.dumps({"command": "tovary"})
            )

            kb.add_line()

            kb.add_button(
                "Обучение",
                color=VkKeyboardColor.SECONDARY,
                payload=json.dumps({"command": "obuchenie"})
            )


        elif step == 2:

            kb.add_button(
                "Быстрые продажи",
                color=VkKeyboardColor.POSITIVE,
                payload=json.dumps({"command": "prodazhi"})
            )

            kb.add_line()

            kb.add_button(
                "Прогрев",
                color=VkKeyboardColor.NEGATIVE,
                payload=json.dumps({"command": "progrev"})
            )

            kb.add_line()

            kb.add_button(
                "Активация базы",
                color=VkKeyboardColor.SECONDARY,
                payload=json.dumps({"command": "aktivaciya"})
            )


        elif step == 3:

            kb.add_button(
                "Минимум ресурсов",
                color=VkKeyboardColor.POSITIVE,
                payload=json.dumps({"command": "min"})
            )

            kb.add_line()

            kb.add_button(
                "Средне",
                color=VkKeyboardColor.NEGATIVE,
                payload=json.dumps({"command": "mid"})
            )

            kb.add_line()

            kb.add_button(
                "Максимум",
                color=VkKeyboardColor.SECONDARY,
                payload=json.dumps({"command": "max"})
            )


        elif step == 4:

            kb.add_button(
                "🔄 Пройти заново",
                color=VkKeyboardColor.SECONDARY,
                payload=json.dumps({"command": "restart"})
            )

            kb.add_line()

            kb.add_button(
                "🚀 Внедрить под ключ",
                color=VkKeyboardColor.POSITIVE,
                payload=json.dumps({"command": "consult"})
            )

        return kb.get_keyboard()


    # ========================================================
    # ОТПРАВКА СООБЩЕНИЯ
    # ========================================================

    def send_msg(user_id, text, step=None):

        params = {
            "user_id": user_id,
            "message": text,
            "random_id": get_random_id()
        }

        if step is not None:
            params["keyboard"] = get_keyboard(step)

        vk.messages.send(**params)


    # ========================================================
    # НАЧАЛО ТЕСТА
    # ========================================================

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


    # ========================================================
    # РЕЗУЛЬТАТ
    # ========================================================

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


    # ========================================================
    # ОСНОВНОЙ ЦИКЛ
    # ========================================================

    for event in longpoll.listen():

        try:

            if event.type != VkBotEventType.MESSAGE_NEW:
                continue


            # Для MESSAGE_NEW vk_api предоставляет данные сообщения
            # в event.obj.message
            msg = event.obj.message

            user_id = msg.from_id
            text = (msg.text or "").strip().lower()

            payload = msg.get("payload")
            cmd = None


            # ------------------------------------------------
            # ЧИТАЕМ PAYLOAD КНОПКИ
            # ------------------------------------------------

            if payload:

                if isinstance(payload, str):

                    try:
                        payload = json.loads(payload)
                    except (ValueError, TypeError):
                        payload = None


                if isinstance(payload, dict):
                    cmd = payload.get("command")


            print(
                "Сообщение:",
                "user_id =", user_id,
                "text =", repr(text),
                "command =", repr(cmd)
            )


            # ------------------------------------------------
            # НАЧАТЬ / ПОВТОРИТЬ
            # ------------------------------------------------

            if text == "начать" or cmd == "restart":

                start_test(user_id)
                continue


            # ------------------------------------------------
            # КОНСУЛЬТАЦИЯ
            # ------------------------------------------------

            if cmd == "consult":

                send_msg(
                    user_id,
                    "🚀 Отлично!\n\n"
                    "Напишите мне в личные сообщения, и обсудим "
                    "настройку вашей воронки:\n"
                    "https://vk.me/club239491424"
                )

                continue


            # ------------------------------------------------
            # ЕСЛИ ПОЛЬЗОВАТЕЛЬ ЕЩЁ НЕ НАЧИНАЛ ТЕСТ
            # ------------------------------------------------

            if user_id not in user_progress:

                send_msg(
                    user_id,
                    "Чтобы начать тест, напишите «Начать»."
                )

                continue


            step = user_progress[user_id]["step"]


            # =================================================
            # ШАГ 1
            # =================================================

            if step == 1:

                if cmd not in {
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


                user_progress[user_id]["product"] = cmd
                user_progress[user_id]["step"] = 2


                send_msg(
                    user_id,
                    "Какая главная цель запуска?",
                    2
                )


            # =================================================
            # ШАГ 2
            # =================================================

            elif step == 2:

                if cmd not in {
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


                user_progress[user_id]["goal"] = cmd
                user_progress[user_id]["step"] = 3


                send_msg(
                    user_id,
                    "Сколько ресурсов (времени и денег) готовы вложить?",
                    3
                )


            # =================================================
            # ШАГ 3
            # =================================================

            elif step == 3:

                if cmd not in {
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


                user_progress[user_id]["resources"] = cmd


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


            # =================================================
            # ШАГ 4
            # =================================================

            elif step == 4:

                send_msg(
                    user_id,
                    "Тест уже завершён.\n\n"
                    "Если хотите пройти его ещё раз, "
                    "нажмите «Пройти заново».",
                    4
                )


        except Exception as error:

            print("ОШИБКА ПРИ ОБРАБОТКЕ СООБЩЕНИЯ:")
            print(repr(error))


# ============================================================
# ЗАПУСК
# ============================================================

if __name__ == "__main__":

    try:
        main()

    except Exception as error:

        print("КРИТИЧЕСКАЯ ОШИБКА ПРИ ЗАПУСКЕ:")
        print(repr(error))
