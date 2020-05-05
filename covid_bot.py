from bot.bot import Bot
import json
from bot.handler import MessageHandler, BotButtonCommandHandler, CommandHandler
import locale
import string
from parser_russia import parser_rus
from russia import russia
from covid import Covid
import pickle
import schedule
import time
from threading import Thread

locale.setlocale(locale.LC_ALL, "")
TOKEN = "001.2422776034.0494128324:752509167"
bot = Bot(token=TOKEN)
cov = Covid()
country_info = cov.get_data()


def sort(region):
    return region.Name


def get_string_reg(i):
    return "Статистика по " + i.Name + "\nБольных: " + i.Active + "\nБольных за сегодня: " + i.Active_today \
           + "\nСмертей: " + i.Deaths + "\nСмертей за сегодня: " + i.Deaths_today + "\nВыздоровевших: " + i.Recovered \
           + "\nВыздоровевших за сегодня: " + i.Recovered_today + "\n\n "


def get_a_ii(rus):
    result = ""
    source = "{0:n}"
    for i in rus.region:
        a = i.Name[0]
        if a < 'К':
            result += get_string_reg(i)
    return result


def get_k_n(rus):
    result = ""
    source = "{0:n}"
    for i in rus.region:
        a = i.Name[0]
        if 'О' > a > 'Й':
            result += get_string_reg(i)
    return result


def get_o_r(rus):
    result = ""
    source = "{0:n}"
    for i in rus.region:
        a = i.Name[0]
        if 'С' > a > 'Н':
            result += get_string_reg(i)
    return result


def get_s_ia(rus):
    result = ""
    source = "{0:n}"
    for i in rus.region:
        a = i.Name[0]
        if a > 'Р':
            result += get_string_reg(i)

    return result


def buttons_answer_cb(bot, event):
    if event.data['callbackData'] == "up":
        f = open('text.txt')
        n = int(f.read())
        f.close()
        source = "{0:n}"
        rus = ""
        for i in range(n, n + 5):
            name = trans(country_info[i]['country'])
            rus += "Статистика по " + name + "\nВсего случаев - " + str(
                source.format(country_info[i]['confirmed'])) + "\nЗаболело - " + str(
                source.format(country_info[i]['active'])) + "\nУмерло - " + str(
                source.format(country_info[i]['deaths'])) + "\nВыздоровело - " + str(
                source.format(country_info[i]['recovered'])) + "\n\n"

        n += 5
        f = open('text.txt', 'w')
        f.write(str(n))
        f.close()
        bot.edit_text(chat_id=event.data['message']['chat']['chatId'], msg_id=event.data['message']['msgId'], text=rus,
                      inline_keyboard_markup="{}".format(json.dumps(
                          [[{"text": "Назад", "callbackData": "down"}, {"text": "Вперед", "callbackData": "up"}]])))

    if event.data['callbackData'] == "down":
        f = open('text.txt')
        n = int(f.read())
        f.close()
        source = "{0:n}"
        rus = ""
        for i in range(n - 5, n):
            name = trans(country_info[i]['country'])
            rus += "Статистика по " + name + "\nВсего случаев - " + str(
                source.format(country_info[i]['confirmed'])) + "\nЗаболело - " + str(
                source.format(country_info[i]['active'])) + "\nУмерло - " + str(
                source.format(country_info[i]['deaths'])) + "\nВыздоровело - " + str(
                source.format(country_info[i]['recovered'])) + "\n\n"
        n -= 5
        f = open('text.txt', 'w')
        f.write(str(n))
        f.close()
        bot.edit_text(chat_id=event.data['message']['chat']['chatId'], msg_id=event.data['message']['msgId'], text=rus,
                      inline_keyboard_markup="{}".format(json.dumps(
                          [[{"text": "Назад", "callbackData": "down"}, {"text": "Вперед", "callbackData": "up"}]])))

    if event.data['callbackData'] == "call_back_id_1":
        text = "Течение COVID-19 может быть разным. У большинства инфицированных наблюдаются легкие или умеренные " \
               "симптомы.\nЧасто наблюдаемые симптомы:\n\t•повышение температуры тела;\n\t•утомляемость;\n\t•сухой " \
               "кашель.\nУ некоторых инфицированных могут также наблюдаться:\n\t•боли в мышцах и " \
               "суставах;\n\t•заложенность носа;\n\t•выделения из носа;\n\t•боль в горле;\n\t•диарея.\n\nВ среднем с " \
               "момента заражения до возникновения симптомов проходит 5-6 дней, хотя в отдельных случаях этот период " \
               "может продолжаться до 14 дней.\nЛицам с легкой симптоматикой и без сопутствующих заболеваний " \
               "рекомендуется соблюдать режим самоизоляции на дому. В случае повышения температуры тела, " \
               "появления кашля и одышки следует обратиться к врачу. Вызовите врача по телефону. "
        bot.send_text(chat_id=event.data['message']['chat']['chatId'], text=text)
    elif event.data['callbackData'] == "call_back_id_2":
        text = "Для предупреждения распространения COVID-19:\n\t•Соблюдайте правила гигиены рук. Часто мойте руки " \
               "водой с мылом или \tобрабатывайте их спиртосодержащим антисептиком для рук.\n\t•Держитесь на " \
               "безопасном расстоянии от чихающих или кашляющих людей.\n\t•Не прикасайтесь руками к глазам, " \
               "рту или носу.\n\t•При кашле или чихании прикрывайте рот и нос локтевым сгибом или платком.\n\t•Если " \
               "вы чувствуете недомогание, оставайтесь дома.\n\t•В случае повышения температуры, появлении кашля и " \
               "одышки обратитесь за \tмедицинской помощью. Вызовите врача по телефону.\n\t•Следуйте указаниям " \
               "местных органов здравоохранения.",
        bot.send_text(chat_id=event.data['message']['chat']['chatId'], text=text)
    elif event.data['callbackData'] == "Info":
        bot.send_text(chat_id=event.data['message']['chat']['chatId'],
                      text="https://coronavirus-monitor.ru/coronavirus-v-rossii/")

    elif event.data['callbackData'] == "A-Ii":
        rus = russia()
        with open('entry.pickle', 'rb') as f:
            rus.region = pickle.load(f)
        rus.region.sort(key=sort)
        bot.send_text(chat_id=event.data['message']['chat']['chatId'],
                      text=get_a_ii(rus))

    elif event.data['callbackData'] == "K-N":
        rus = russia()
        with open('entry.pickle', 'rb') as f:
            rus.region = pickle.load(f)
        rus.region.sort(key=sort)
        bot.send_text(chat_id=event.data['message']['chat']['chatId'],
                      text=get_k_n(rus))

    elif event.data['callbackData'] == "O-R":
        rus = russia()
        with open('entry.pickle', 'rb') as f:
            rus.region = pickle.load(f)
        rus.region.sort(key=sort)
        bot.send_text(chat_id=event.data['message']['chat']['chatId'],
                      text=get_o_r(rus))

    elif event.data['callbackData'] == "S-Ia":
        rus = russia()
        with open('entry.pickle', 'rb') as f:
            rus.region = pickle.load(f)
        rus.region.sort(key=sort)
        bot.send_text(chat_id=event.data['message']['chat']['chatId'],
                      text=get_s_ia(rus))
        # region
    elif event.data['callbackData'] == "01":
        bot.send_text(chat_id=event.data['message']['chat']['chatId'],
                      text="Давайте рассмотрим один «типичный» день на карантине.\n\nВы на самоизоляции, "
                           "но тут звонок в дверь...",
                      inline_keyboard_markup="{}".format(json.dumps([[{"text": "Открыть", "callbackData": "1"}],
                                                                     [{"text": "Посмотреть в глазок, спросить: «Кто "
                                                                               "там?»",
                                                                       "callbackData": "2"}],
                                                                     [{"text": "Проигнорировать",
                                                                       "callbackData": "3"}]])))
    elif event.data['callbackData'] == "00":
        bot.send_text(chat_id=event.data['message']['chat']['chatId'],
                      text="Привет, меня зовут Ковид.\nНе так давно миром завладел коронавирус. Ежедневно статистика "
                           "заражения в большинстве странах мира растёт со сверхзвуковой скоростью. Помочь своей "
                           "стране остановить пандемию может каждый из нас. Как известно, одержать победу над любым "
                           "врагом помогает максимальная информированность о нём, его действиях и слабых "
                           "точках.\nКаждый день я буду присылать тебе статистику распространения COVID-19. Спасем "
                           "планету, не выходя из дома!\nЕсли тебе скучно, а текущая ситуация наводит грусть, "
                           "то не расстраивайся и сыграй со мной в игру!\n\nСписок команд: \n /total_rus - Статистика "
                           "по России и регионам \n /country - Статистика по миру",
                      inline_keyboard_markup="{}".format(
                          json.dumps([[{"text": "Источник информации", "callbackData": "Info", "style": "attention"},
                                       {"text": "Симптомы", "callbackData": "call_back_id_1", "style": "attention"},
                                       {"text": "Профилактика", "callbackData": "call_back_id_2",
                                        "style": "attention"}],
                                      [{"text": "Начать игру", "callbackData": "01", "style": "primary"}]])))

    elif event.data['callbackData'] == "1":
        bot.send_text(chat_id=event.data['message']['chat']['chatId'],
                      text="Там мужчина без маски - вы проиграли!",
                      inline_keyboard_markup="{}".format(json.dumps([[{"text": "Начать заного", "callbackData": "01"}],
                                                                     [{"text": "Носите маску! Вы можете быть "
                                                                               "носителем даже без симптомов! ",
                                                                       "url": "https://www.youtube.com/watch?v"
                                                                              "=8gmOZqxdNFA"}],
                                                                     [{"text": "Выход", "callbackData": "00",
                                                                       "style": "attention"}]])))

    elif event.data['callbackData'] == "2":
        bot.send_text(chat_id=event.data['message']['chat']['chatId'],
                      text="За дверью стои мужчина в шортах без маски - это твой сосед, ему нужен сахар",
                      inline_keyboard_markup="{}".format(
                          json.dumps([[{"text": "Сказать, что сахара нет", "callbackData": "6"}],
                                      [{"text": "Вынести ему сахар", "callbackData": "7"}]])))

    elif event.data['callbackData'] == "6":
        bot.send_text(chat_id=event.data['message']['chat']['chatId'],
                      text="Сосед ушел, но сработала сигнализация у моего автомобиля. Его не видно из окна",
                      inline_keyboard_markup="{}".format(
                          json.dumps([[{"text": "Выйти на улицу посмотреть", "callbackData": "9"}],
                                      [{"text": "Надеть маску и выйти посмотреть", "callbackData": "10"}]])))
    elif event.data['callbackData'] == "9":
        bot.send_text(chat_id=event.data['message']['chat']['chatId'],
                      text="Вы зашли в лифт, неизвестный чихнул прямо на вас, а вы без маски((",
                      inline_keyboard_markup="{}".format(json.dumps([[{"text": "Начать заного", "callbackData": "01"}],
                                                                     [{"text": "Носите маску! Вы можете быть "
                                                                               "носителем даже без симптомов! ",
                                                                       "url": "https://www.youtube.com/watch?v"
                                                                              "=8gmOZqxdNFA"}],
                                                                     [{"text": "Выход", "callbackData": "00",
                                                                       "style": "attention"}]])))
    elif event.data['callbackData'] == "10":
        bot.send_text(chat_id=event.data['message']['chat']['chatId'],
                      text="Выясняется, что кто-то стукнул машину и уехал, есть вмятина, что делать?",
                      inline_keyboard_markup="{}".format(json.dumps([[{
                          "text": "Стало грустно, через Госуслуги сделал пропуск и пошел в магазин за мороженым",
                          "callbackData": "100"}],
                          [{"text": "Позвонить в полицию", "callbackData": "11"}],
                          [{"text": "Пойти домой", "callbackData": "12"}]])))
    elif event.data['callbackData'] == "100":
        bot.send_text(chat_id=event.data['message']['chat']['chatId'],
                      text="Здесь должна быть романтическая история и самый хеппи енд",
                      inline_keyboard_markup="{}".format(json.dumps([[{"text": "Начать заного", "callbackData": "01"}],
                                                                     [{"text": "Выход", "callbackData": "00",
                                                                       "style": "attention"}]])))
    elif event.data['callbackData'] == "11":
        bot.send_text(chat_id=event.data['message']['chat']['chatId'],
                      text="Они вас не слышат, что предпринять?",
                      inline_keyboard_markup="{}".format(json.dumps([[{
                          "text": "Немного спустить защитную маску во время разговора",
                          "callbackData": "13"}],
                          [{"text": "Начать говорить громче", "callbackData": "12"}]])))
    elif event.data['callbackData'] == "13":
        bot.send_text(chat_id=event.data['message']['chat']['chatId'],
                      text="В этот момент мимо вас пробегал Флэш - у него коронавирус, вы теперь больны",
                      inline_keyboard_markup="{}".format(json.dumps([[{"text": "Начать заного", "callbackData": "01"}],
                                                                     [{"text": "Пасхалка, Вам будет чем заняться "
                                                                               "на самоизоляции ;)",
                                                                       "url": "http://studiohd.org/serial"
                                                                              "/flehsh_50/15-1-0-223"}],
                                                                     [{"text": "Выход", "callbackData": "00",
                                                                       "style": "attention"}]])))

    elif event.data['callbackData'] == "12":
        bot.send_text(chat_id=event.data['message']['chat']['chatId'],
                      text="Вы проявили гражданскую сознательность и спасли многие жизни, Спасибо!",
                      inline_keyboard_markup="{}".format(json.dumps([[{"text": "Начать заного", "callbackData": "01"}],
                                                                     [{"text": "Оставайтесь в безопасности будучи "
                                                                               "дома)",
                                                                       "url": "https://www.kaspersky.ru/"}],
                                                                     [{"text": "Выход", "callbackData": "00",
                                                                       "style": "attention"}]])))

    elif event.data['callbackData'] == "7":
        bot.send_text(chat_id=event.data['message']['chat']['chatId'],
                      text="Сахар закончился, нужно его купить",
                      inline_keyboard_markup="{}".format(
                          json.dumps([[{"text": "Пойти в магазин за сахаром", "callbackData": "15"}],
                                      [{"text": "Выписать пропуск на поход в магазин и пойти за сахаром",
                                        "callbackData": "16"}],
                                      [{"text": "Заказать сахар в онлайн-магазине",
                                        "callbackData": "12"}],
                                      [{"text": "Выписать пропуск на поход в магазин, надеть маску и пойти за сахаром",
                                        "callbackData": "100"}]])))
    elif event.data['callbackData'] == "15":
        bot.send_text(chat_id=event.data['message']['chat']['chatId'],
                      text="Остановила полиция - нет пропуска, да еще и без маски!)",
                      inline_keyboard_markup="{}".format(json.dumps([[{"text": "Начать заного", "callbackData": "01"}],
                                                                     [{"text": "Можете ознакомиться с текущим "
                                                                               "законодательством по этому вопросу",
                                                                       "url": "http://www.consultant.ru/document"
                                                                              "/cons_doc_LAW_10699"
                                                                              "/5c403b6bfc15c73864f56d40c8a28cd51e72f86c/"}],
                                                                     [{"text": "Выход", "callbackData": "00",
                                                                       "style": "attention"}]])))
    elif event.data['callbackData'] == "16":
        bot.send_text(chat_id=event.data['message']['chat']['chatId'],
                      text="Огромный охранник смачно чихнул около вас, а вы без маски!!",
                      inline_keyboard_markup="{}".format(json.dumps([[{"text": "Начать заного", "callbackData": "01"}],
                                                                     [{"text": "Носите маску! Вы можете быть "
                                                                               "носителем даже без симптомов! ",
                                                                       "url": "https://www.youtube.com/watch?v"
                                                                              "=8gmOZqxdNFA"}],
                                                                     [{"text": "Выход", "callbackData": "00",
                                                                       "style": "attention"}]])))

    elif event.data['callbackData'] == "3":
        bot.send_text(chat_id=event.data['message']['chat']['chatId'],
                      text="Звонки повторяются...",
                      inline_keyboard_markup="{}".format(json.dumps([[{"text": "Открыть", "callbackData": "1"}],
                                                                     [{"text": "Игнор", "callbackData": "20"}]])))
    elif event.data['callbackData'] == "20":
        bot.send_text(chat_id=event.data['message']['chat']['chatId'],
                      text="Включилась сигнализация у вашего автомобиля. Его не видно из окна",
                      inline_keyboard_markup="{}".format(
                          json.dumps([[{"text": "Надеть маску и выйти посмотреть", "callbackData": "10"}],
                                      [{"text": "Выйти посмотреть", "callbackData": "9"}],
                                      [{"text": "Игнор", "callbackData": "21"}]])))
    elif event.data['callbackData'] == "21":
        bot.send_text(chat_id=event.data['message']['chat']['chatId'],
                      text="Стук в дверь продолжается, сигнализация орет, начал звонить телефон",
                      inline_keyboard_markup="{}".format(json.dumps([[{"text": "Ответить", "callbackData": "22"}],
                                                                     [{"text": "Игнор", "callbackData": "23"}]])))

    elif event.data['callbackData'] == "22":
        bot.send_text(chat_id=event.data['message']['chat']['chatId'],
                      text="Друг позвал на шашлыки",
                      inline_keyboard_markup="{}".format(json.dumps([[{"text": "Поехали!", "callbackData": "24"}],
                                                                     [{"text": "НЕТ! Остаться дома, выписать "
                                                                               "пропуск и пойти в маске в магазин "
                                                                               "за  домашним шашлычком",
                                                                       "callbackData": "100"}]])))
    elif event.data['callbackData'] == "24":
        bot.send_text(chat_id=event.data['message']['chat']['chatId'],
                      text="Ну, это совсем беды(( Вы проиграли!",
                      inline_keyboard_markup="{}".format(json.dumps([[{"text": "Начать заного", "callbackData": "01"}],
                                                                     [{"text": "Выход", "callbackData": "00",
                                                                       "style": "attention"}]])))
    elif event.data['callbackData'] == "23":
        bot.send_text(chat_id=event.data['message']['chat']['chatId'],
                      text="От постоянных шумов сильно разболелась голова, начали мерещиться зеленые человечки на "
                           "балконе...",
                      inline_keyboard_markup="{}".format(
                          json.dumps([[{"text": "Выйти к ним на балкон", "callbackData": "25"}],
                                      [{"text": "Выбежать из дома", "callbackData": "26"}],
                                      [{"text": "Надеть маску и выйти к ним на балкон", "callbackData": "27"}]])))
    elif event.data['callbackData'] == "25":
        bot.send_text(chat_id=event.data['message']['chat']['chatId'],
                      text="Они что-то бормотали на своем, потом двое достали некий прибор - вспышка...И вы в кровати -"
                           " это всего лишь сон, но балкон открыт....",
                      inline_keyboard_markup="{}".format(json.dumps([[{"text": "Начать заного", "callbackData": "01"}],
                                                                     [{"text": "Выход", "callbackData": "00",
                                                                       "style": "attention"}]])))
    elif event.data['callbackData'] == "26":
        bot.send_text(chat_id=event.data['message']['chat']['chatId'],
                      text="Сосед у двери без маски, вы тоже!!!",
                      inline_keyboard_markup="{}".format(json.dumps([[{"text": "Начать заного", "callbackData": "01"}],
                                                                     [{"text": "Выход", "callbackData": "00",
                                                                       "style": "attention"}]])))
    elif event.data['callbackData'] == "27":
        bot.send_text(chat_id=event.data['message']['chat']['chatId'],
                      text="Они, видя вашу разумность, предлагают улететь с ними",
                      inline_keyboard_markup="{}".format(json.dumps([[{"text": "Звоним в РенТВ", "callbackData": "25"}],
                                                                     [{"text": "Побрызгать на них антисептиком",
                                                                       "callbackData": "28"}],
                                                                     [{"text": "Полететь с ними",
                                                                       "callbackData": "29"}]])))
    elif event.data['callbackData'] == "28":
        bot.send_text(chat_id=event.data['message']['chat']['chatId'],
                      text="Они растворились в небытие, а вы проснулись на своей кровати...",
                      inline_keyboard_markup="{}".format(json.dumps([[{"text": "Начать заного", "callbackData": "01"}],
                                                                     [{"text": "Выход", "callbackData": "00",
                                                                       "style": "attention"}]])))
    elif event.data['callbackData'] == "29":
        bot.send_text(chat_id=event.data['message']['chat']['chatId'],
                      text="Happy end",
                      inline_keyboard_markup="{}".format(json.dumps([[{"text": "Начать заного", "callbackData": "01"}],
                                                                     [{"text": "Выход", "callbackData": "00",
                                                                       "style": "attention"}]])))
    bot.answer_callback_query(query_id=event.data['queryId'],show_alert=False, text="")

    # endregion


def get_info_about_russia(bot, event):
    bot.send_actions(chat_id=event.data['chat']['chatId'], actions=["typing"])
    source = "{0:n}"
    rus = russia()
    with open('entry.pickle', 'rb') as f:
        rus = pickle.load(f)
    cov = Covid()
    country_info = cov.get_status_by_country_name("russia")
    source = "{0:n}"
    rus = "Статистика по России: \nВсего случаев - " + str(
        source.format(country_info['confirmed'])) + "\nЗаболело - " + str(
        source.format(country_info['active'])) + "\nУмерло - " + str(
        source.format(country_info['deaths'])) + "\nВыздоровело - " + str(source.format(country_info['recovered']))

    bot.send_text(chat_id=event.from_chat,
                  text=rus + "\n\nЕсли вас интересует статистика по регионам, нажмите на кнопку, которая соответсвует "
                             "первой буквы этого региона:",
                  inline_keyboard_markup="{}".format(json.dumps([[{"text": "А-Й", "callbackData": "A-Ii"}],
                                                                 [{"text": "К-Н", "callbackData": "K-N"}],
                                                                 [{"text": "O-Р", "callbackData": "O-R"}],
                                                                 [{"text": "С-Я", "callbackData": "S-Ia"}]])))

    bot.send_actions(chat_id=event.data['chat']['chatId'], actions=[])


def message_cb(bot, event):
    if event.text == "/start":
        bot.send_text(chat_id=event.from_chat,
                      text="Привет, меня зовут Ковид.\nНе так давно миром завладел коронавирус. Ежедневно статистика "
                           "заражения в большинстве странах мира растёт со сверхзвуковой скоростью. Помочь своей "
                           "стране остановить пандемию может каждый из нас. Как известно, одержать победу над любым "
                           "врагом помогает максимальная информированность о нём, его действиях и слабых "
                           "точках.\nКаждый день я буду присылать тебе статистику распространения COVID-19. Спасем "
                           "планету, не выходя из дома!\nЕсли тебе скучно, а текущая ситуация наводит грусть, "
                           "то не расстраивайся и сыграй со мной в игру!\n\nСписок команд: \n /total_rus - Статистика "
                           "по России и регионам \n /country - Статистика по миру",
                      inline_keyboard_markup="{}".format(
                          json.dumps([[{"text": "Источник информации", "callbackData": "Info", "style": "attention"},
                                       {"text": "Симптомы", "callbackData": "call_back_id_1", "style": "attention"},
                                       {"text": "Профилактика", "callbackData": "call_back_id_2",
                                        "style": "attention"}],
                                      [{"text": "Начать игру", "callbackData": "01", "style": "primary"}]])))
    if "/country" == event.text:
        f = open('text.txt', 'w')
        f.write("5")
        f.close()
        source = "{0:n}"
        rus = ""
        for i in range(5):
            name = trans(country_info[i]['country'])
            rus += "Статистика по " + name + "\nВсего случаев - " + str(
                source.format(country_info[i]['confirmed'])) + "\nЗаболело - " + str(
                source.format(country_info[i]['active'])) + "\nУмерло - " + str(
                source.format(country_info[i]['deaths'])) + "\nВыздоровело - " + str(
                source.format(country_info[i]['recovered'])) + "\n\n"
        bot.send_text(chat_id=event.from_chat, text=rus, inline_keyboard_markup="{}".format(
            json.dumps([[{"text": "Назад", "callbackData": "down"}, {"text": "Вперед", "callbackData": "up"}]])))


def trans(str):
    str = str.strip()
    deflenght = len(str)
    filename = "land.txt"
    with open(filename, "r") as file:
        for line in file:
            n = line.rfind(str)
            if n != -1:
                str1 = line
                break
        if n == -1:
            return ('')
        else:
            str = str1.split('/')
            return str[0].title()


def pars():
    parser = parser_rus()
    parser.parser()


def send_alert():
    chats_to_send_notifications = ["752328306"]
    source = "{0:n}"
    rus = russia()
    with open('entry.pickle', 'rb') as f:
        rus = pickle.load(f)
    cov = Covid()
    country_info = cov.get_status_by_country_name("russia")
    source = "{0:n}"
    rus = "Статистика по России: \nВсего случаев - " + str(
        source.format(country_info['confirmed'])) + "\nЗаболело - " + str(
        source.format(country_info['active'])) + "\nУмерло - " + str(
        source.format(country_info['deaths'])) + "\nВыздоровело - " + str(source.format(country_info['recovered']))
    for chat in chats_to_send_notifications:
        bot.send_text(chat_id=chat,
                      text=rus + "\n\nЕсли вас интересует статистика по регионам, нажмите на кнопку, которая "
                                 "соответсвует первой буквы этого региона:",
                      inline_keyboard_markup="{}".format(json.dumps([[{"text": "А-Й", "callbackData": "A-Ii"}],
                                                                     [{"text": "К-Н", "callbackData": "K-N"}],
                                                                     [{"text": "O-Р", "callbackData": "O-R"}],
                                                                     [{"text": "С-Я", "callbackData": "S-Ia"}]])))


def run():
    schedule.every().day.at("20:00").do(pars)
    schedule.every().day.at("12:00").do(send_alert)
    while True:
        schedule.run_pending()
        time.sleep(1)


thread = Thread(target=run)
thread.start()


def main():
    TOKEN = "001.2422776034.0494128324:752509167"
    bot = Bot(token=TOKEN)

    bot.dispatcher.add_handler(MessageHandler(callback=message_cb))
    bot.dispatcher.add_handler(BotButtonCommandHandler(callback=buttons_answer_cb))
    bot.dispatcher.add_handler(CommandHandler(command="total_rus",
                                              callback=get_info_about_russia))

    bot.start_polling()

    bot.idle()


if (__name__ == "__main__"):
    main()
