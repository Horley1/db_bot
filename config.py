TOKEN = 'ENTER YOUR TOKEN HERE'
URL = 'ENTER YOUR URL WEBHOOK HERE' + TOKEN
ids =  ["CAACAgIAAxkBAAED5jliB622rYVv8eZEJhSU02AfXY6HEwACCwEAAlKJkSNKMfbkP3tfNSME",
        "CAACAgIAAxkBAAED5jtiB627ZWPy4SQYjXy4mT_uxr7f5wACWwADwZxgDNjYPseA8L6OIwQ",
        "CAACAgIAAxkBAAED5j1iB62_gxfmocZbsXvbUzcQb7TPIwACOgEAAlKJkSM5H9SlIyE44CME",
        "CAACAgIAAxkBAAED5j9iB63DmQEWgUnRjDBTEEQsfkYMCAACzxEAAuEYmEsMb6jvCfEBdyME",
        "CAACAgIAAxkBAAED5kFiB63Ilk6JvzNNOIq7F7Hzxx2VuAACYgYAAhyS0gPTMsh9l1U6gyME",
        "CAACAgIAAxkBAAED5kNiB63LuHof3amiyGPSXdqGbLh4FgACYgADmS9LCloe14FkpNDVIwQ",
        "CAACAgIAAxkBAAED5kViB63csm1btKnuXSmFmPiL8hU5vgAC-Q4AAnR3SUk1h3fnp2LZciME",
        "CAACAgIAAxkBAAED5kdiB63hBeLSzwH40RBUPab2AVkBowACZwADlJzpD1nBv1K_IDCPIwQ",
        "CAACAgIAAxkBAAED5kliB63sf_Vsgctp1Tgcs-Ww-mxVIwACNhAAAkk9sEvXsNAN-3e9DCME",
        "CAACAgIAAxkBAAED5ktiB637ln0jH8tK3UCioMEoR-6r5gACKBEAAlcaSUmOXFDqGGG_MSME",
        "CAACAgIAAxkBAAED5k1iB638ecKCOss-CZYRoc0ucI-iXQACDxAAAk8CUUlrHZ307_CsCCME",
        "CAACAgIAAxkBAAED5k9iB64CzjUv_WYuVfknv5EaDrFz9QACMBUAAj_uSEniPAtGDDckRyME",
        "CAACAgIAAxkBAAED0c1h_vsDtZR 101Gk1N0fPWN8oEHmLwACBwADVnU5LboLuKwYEpiCIwQ",
        "CAACAgIAAxkBAAED0c9h_vwkMIJ-E5iXn6raMpLlLoVikAACrQMCAAFji0YM1YXYfa8fXZIjBA",
        "CAACAgIAAxkBAAED0dFh_vw6qGWW9v4pM0J8ngrT2i9gpQACbwADlJzpD_cN0109W4HOIwQ",
        "CAACAgIAAxkBAAED0dNh_vxDz0xMkR4Xh0mFH-U2PJZi3AACMxAAAhWWSUlBydiAaLsldCME",
        "CAACAgIAAxkBAAED_W1iFhGDX2dgNq7efPXHhB0AAbxaVNIAAoYSAAIIiQlIXPiKu0maM08jBA",
        "CAACAgIAAxkBAAED_W9iFhGHzYAtds1abtH_7Tp4jnzttAACvhMAAlyQGUixvwABbzUoBYMjBA",
        "CAACAgIAAxkBAAED_XFiFhGO13mV0CGs-lKEqUkZ-0RFsQAC-BUAAsRBGUi6RYdDxSXHNiME",
        "CAACAgIAAxkBAAED_XNiFhGijjWl0xVU5d_nqjycohwUawAC3QEAAj-xbAPALZx9xn1brSME",
        "CAACAgIAAxkBAAED_XdiFhGsHA6MByN7eJJyYvn8ZBWGWAAC5BEAArI8oUtV1SedduTDUyME",
        "CAACAgIAAxkBAAED_XliFhGtw0c_pXJgYRMBwAT_UJVBBwACahQAAhxlyEtuBRQphTfNqSME",
        "CAACAgIAAxkBAAED_XtiFhGyu7aEW5Sg1pEYU6ePsE3bIAACWxUAAp-JmUstG3BndZxZqiME",
        "CAACAgIAAxkBAAED_X1iFhG0G07vVfmbwg-qRVdTrmD6_QACEAADRStcFjJsCA7R3GWCIwQ",
        "CAACAgIAAxkBAAED_X9iFhHFI87uFfJnLfi1MSy-e8z2aQACUwkAAnlc4gnTg5_qPcJpeyME",
        "AACAgIAAxkBAAED_YNiFhHyYrCBRGUyriIai54-w6Q_EAACDhQAAl8pOUjpCPT3YNeWISME",
        "CAACAgIAAxkBAAED_YViFhHzpRKt8k10dzWOQWbnpWSTsQACwhQAAqV0-Ev2QS0_VNmeqyME",
        "CAACAgIAAxkBAAED_YdiFhH3iepQvomw9rE-vdiovZ91nwACZxgAAsFqEEge3vxXKuWFGSME",
        "CAACAgIAAxkBAAED_YliFhH9Bjx83BLLPILRuus2mhAS7wACiBcAAhcJIUgX6I8AAY6fNxgjBA",
        "CAACAgIAAxkBAAED_YtiFhH_7vEh69Ktd2kibejHDwkOMwACzhcAAjSdIEiIEbgpyCdqGCME",
        "CAACAgIAAxkBAAED_Y1iFhIOrVHZfxaHorUWX1VRcjZqMwAC_hEAAkNhyUsXQJqa2HnLdiME",
        "CAACAgIAAxkBAAED_Y9iFhIVSq2E7jyO7z--23m8CXlqUQACdxIAAr1BCUhrfC2MNLR0ziME"]

agree = ["CAACAgIAAxkBAAEEDXxiIld2n2kBTRiecPL4yWAGv-C4wgACXRgAAg1MOEgoCfq_PJ5zKCME",
         "CAACAgIAAxkBAAEEDX5iIleCN9dODPXbjksE7opKAAEiy7MAAhYMAALn6rFJM9pxG82qStAjBA",
         "CAACAgQAAxkBAAEEDYBiIleP0fN0JpiDpYM3hHASy75vPAAC6gEAApUkhCIh1qk9Eg3wxiME",
         "CAACAgIAAxkBAAEEDYJiIleeCqQOSjeLVhdUoFFf69IUvgAC1RAAAkYYSUrRLe7CNv_0DCME",
         "CAACAgIAAxkBAAEEDYRiIleu74-49169KbC3FI1dWjcuHgACygQAAhyS0gM_ER5qcnge7iME",
         "CAACAgIAAxkBAAEEDYZiIlfBe_iEYrfnUQrNoJkaJzTpMQACfQADmS9LCsfb0MCpuOlOIwQ",
         "CAACAgIAAxkBAAEEDYhiIlfHCKdfdmLCxmXenRZPnyocyQACyxIAApf9SEl0G3pXyFU9LiME",
         "CAACAgIAAxkBAAEEDYpiIlfL_0lmjvbu9mgT_f_o1qfeeQACWAADlJzpD_14E4scLipgIwQ",
         "CAACAgIAAxkBAAEEDY5iIlfTaO7E3JxoKgFFob0TgvrCfwAC6AQAAvPyjj-be41RjBUoYyME",
         "CAACAgIAAxkBAAEEDZBiIlfWm0j4a5CtBrSgO6c4vbHM8wACVAADX8p-C_ToNjLl5Er_IwQ",
         "CAACAgIAAxkBAAEEDZJiIlfnOngQ55VXzGxSCD1H7NwZvwACwgMAAuSsUQ-2lANp-uCBWSME",
         "CAACAgIAAxkBAAEEDZRiIlfzB0Z8s5xBiL6kNUQK8W2RMQACBQADRIw6N_kJEwa-onktIwQ",
         "CAACAgIAAxkBAAEEDZZiIlgCQ4jTbLQdAfzxXpwysuVaBQACVwADuRtZC7Tl71Hzx6JfIwQ"]


phrases = ["Я не знаю такой команды(((. Для регистрации напиши: /reg",
    "Ты вообще нормальый?? Напиши: /reg и не позорься!",
    "Мдааммм.... Вообще не шарит... Напиши: /reg уже",
    "Блин, не трать мою оперативку и напиши: /reg"
    "Слыш ты! Давай иди ругайся! Я уже устал тратить свой время!",
    "Я не понял, ты вообще адекват? Что ты пишешь?",
    "Давай иди от сюда! И чтобы я тебя больше не видел!!!",
    "Иди гуляй васек!!!!!!",
    "Мдаммммммм.. Шкет, иди гуляй!",
    "Братан, я тебе говорю! Напиши : /reg , и спи спокойной",
    "Почему нельзя просто написать : /reg ?",
    "ЕСЛИ БУДЕШЬ ПИСАТЬ ФИГНЮ???<!!! Я тебя забаню!!!!!!",
    "НАПИШИ: /reg !!",
    "Пока.",
    "Не пиши мне больше.",
    "УХАДИ!!!!",
    "удали интеренет"]

db_name = 'YOUR DATABASE NAME'
db_user = 'YOUR DATABASE USER'
db_pass = 'YOUR DATABASE PASSWORD'
db_host = 'YOUR DATABASE HOST'

mon = {"01":"января", "02":"февраля", "03":"марта", "04":"апреля", "05":"мая", "06":"июня", "07":"июля", "08":"августа", "09":"сентября", "10":"октября", "11":"ноября", "12":"декабря"}
sub = {"Алгебра":"алгебре", "Биология":"биологии", "География":"географии", "Геометрия":"геометрии","Иностранный язык (английский)":"английскому языку","Информатика":"информатике",
       "История России. Всеобщая история":"истории России и всеобщей истории","Литература":"литературе", "Обществознание":"обществознанию","Практикум":"практикуму","Практикум по решению задач по физике" :"практикум по физике",
       "Русский язык":"русскому языку","Технология":"технологии","Физика":"физике","Физкультура":"физкультуре","Химия":"химии"}

