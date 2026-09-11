import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import json

# ВСТАВЬ СЮДА СВОЙ КЛЮЧ (тот, который ты получила при создании приложения)
TOKEN = 'a86ca9afa86ca9afa86ca9afd6ab2f3f5aaa86ca86ca9afc2cda087435b2bb49feaab31'
GROUP_ID = '-236661576'

vk_session = vk_api.VkApi(token=TOKEN)
vk = vk_session.get_api()

# Бот сам включит Longpoll API при запуске
clean_id = GROUP_ID.replace('-', '')
try:
    vk.groups.setLongPollSettings(group_id=clean_id, enabled=True, api_version="5.199")
    print("Longpoll API включен автоматически!")
except Exception as e:
    print(f"Ошибка при включении Longpoll: {e}")

longpoll = VkBotLongPoll(vk_session, clean_id)

user_progress = {}

def get_keyboard(step):
    kb = VkKeyboard(one_time=False)
    if step == 1:
        kb.add_button('Услуги', color=VkKeyboardColor.POSITIVE, payload=json.dumps({"command": "uslugi"}))
        kb.add_line()
        kb.add_button('Товары', color=VkKeyboardColor.NEGATIVE, payload=json.dumps({"command": "tovary"}))
        kb.add_line()
        kb.add_button('Обучение', color=VkKeyboardColor.SECONDARY, payload=json.dumps({"command": "obuchenie"}))
    elif step == 2:
        kb.add_button('Быстрые продажи', color=VkKeyboardColor.POSITIVE, payload=json.dumps({"command": "prodazhi"}))
        kb.add_line()
        kb.add_button('Прогрев', color=VkKeyboardColor.NEGATIVE, payload=json.dumps({"command": "progrev"}))
        kb.add_line()
        kb.add_button('Активация базы', color=VkKeyboardColor.SECONDARY, payload=json.dumps({"command": "aktivaciya"}))
    elif step == 3:
        kb.add_button('Минимум ресурсов', color=VkKeyboardColor.POSITIVE, payload=json.dumps({"command": "min"}))
        kb.add_line()
        kb.add_button('Средне', color=VkKeyboardColor.NEGATIVE, payload=json.dumps({"command": "mid"}))
        kb.add_line()
        kb.add_button('Максимум', color=VkKeyboardColor.SECONDARY, payload=json.dumps({"command": "max"}))
    elif step == 4:
        kb.add_button('🔄 Пройти заново', color=VkKeyboardColor.SECONDARY, payload=json.dumps({"command": "restart"}))
        kb.add_line()
        kb.add_button('🚀 Внедрить под ключ', color=VkKeyboardColor.POSITIVE, payload=json.dumps({"command": "consult"}))
    return kb.get_keyboard()

def send_msg(user_id, text, step=None):
    kb = get_keyboard(step) if step else None
    vk.messages.send(user_id=user_id, message=text, random_id=0, keyboard=kb)

for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        msg = event.obj.message
        user_id = msg['from_id']
        text = msg.get('text', '').lower()
        
        if 'payload' in msg and msg['payload']:
            payload = json.loads(msg['payload'])
            cmd = payload.get('command')
            
            if cmd == 'restart' or text == 'начать':
                user_progress[user_id] = {'step': 1}
                send_msg(user_id, "🎮 Привет! Давай подберем идеальную механику запуска. Что вы продаете?", 1)
                
            elif cmd == 'consult':
                send_msg(user_id, "Отлично! Напишите мне в личные сообщения, и мы обсудим настройку вашей воронки: https://vk.me/club239491424")
                
            elif user_id in user_progress:
                step = user_progress[user_id]['step']
                
                if step == 1:
                    user_progress[user_id]['product'] = cmd
                    user_progress[user_id]['step'] = 2
                    send_msg(user_id, "Какая главная цель запуска?", 2)
                    
                elif step == 2:
                    user_progress[user_id]['goal'] = cmd
                    user_progress[user_id]['step'] = 3
                    send_msg(user_id, "Сколько ресурсов (времени/денег) готовы вложить?", 3)
                    
                elif step == 3:
                    product = user_progress[user_id]['product']
                    goal = user_progress[user_id]['goal']
                    
                    if product == 'uslugi' and goal == 'prodazhi':
                        result = "🔥 ВАША МЕХАНИКА: БЛИЦ-АУКЦИОН\n\n ПЛАН ДЕЙСТВИЙ:\nДень 1: Пост-анонс с интригой («Завтра разыграем услугу за полцены»).\nДень 2: Сбор заявок в рассылку. Ограничение: только 10 мест.\nДень 3: Запуск аукциона в чате. Кто дал последнюю ставку за 5 минут — забирает.\n\n"
                    elif product == 'tovary':
                        result = " ВАША МЕХАНИКА: ТАЙНЫЙ ЯЩИК\n\n📝 ПЛАН ДЕЙСТВИЙ:\nШаг 1: Собрать 3 варианта боксов (Эконом, Стандарт, Премиум).\nШаг 2: Сфотографировать только «намеки» на содержимое.\nШаг 3: Анонс в сторис и пост. Продажа только через личные сообщения.\n\n"
                    else:
                        result = "🗺️ ВАША МЕХАНИКА: КАРТА СОКРОВИЩ\n\n📝 ПЛАН ДЕЙСТВИЙ:\nЭтап 1: Выдаем бесплатный чек-лист за подписку.\nЭтап 2: Серия из 3 прогревающих писем с пользой.\nЭтап 3: Открываем продажу основного продукта со скидкой «для своих».\n\n"
                    
                    result += "🚀 ХОТИТЕ ВНЕДРИТЬ ЭТО ПОД КЛЮЧ?\nНе тратьте время на настройку бота и рассылок. Напишите мне, и я соберу эту автоворонку для вашего бизнеса: https://vk.me/club239491424"
                    
                    send_msg(user_id, result, 4)
        
        elif text == 'начать':
            user_progress[user_id] = {'step': 1}
            send_msg(user_id, " Привет! Давай подберем идеальную механику запуска. Что вы продаете?", 1)
