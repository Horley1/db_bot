#first = main, second - additional
TOKEN = '5199364372:AAGnaM9JbpyH2_JjTpCi1zb3EN5nWUtiwmE'
#TOKEN = '5256986108:AAGuCg2FPFxltj0mvNQw_nBnk2EXhLpT67k'
URL = 'https://elbotv2.herokuapp.com/' + TOKEN
ids =  ['CAACAgIAAxkBAAEEW-piSXIVswfZpTUQbIQ2M4n9dLgIFgACwhQAAqV0-Ev2QS0_VNmeqyME',
        'CAACAgIAAxkBAAEEW-xiSXIbqRpOQI0vDbzQQn0PBDx7pwACWxQAAhEmSEiF-lHNpwsiUCME',
        'CAACAgIAAxkBAAEEW-5iSXIc47BonwABeJ9sLx3k4gLq1D0AAj0SAALdQchLDn4t5IqeVFojBA',
        'CAACAgIAAxkBAAEEW_BiSXIkR4IY0OVqm03QXES799PDxAACNRYAAmuvEUikE1iE8N-oDCME',
        'CAACAgIAAxkBAAEEW_JiSXIlmn9a_680Ap74deE8ArYrFgACMxMAAsLywEsrGmlZy3WfByME',
        'CAACAgIAAxkBAAEEW_RiSXIuNCIwyR4_Ig2XEFVWIAqDQAACGxkAAtGhIUhw4lz4b5HPpyME',
        'CAACAgIAAxkBAAEEW_ZiSXI1_0BfnIfFWHx1UO_RpHdYWAACcBYAAjieyUsSmBUapA3hySME',
        'CAACAgIAAxkBAAEEW_hiSXI4oIgep-f6XFFyHJD7EgkF5AACIhQAAvMbmUjYyqgg8AmsFSME',
        'CAACAgIAAxkBAAEEW_piSXJBRh0lnGKf9wUkIy0g5aYZeAACDQEAAlKJkSMj1EWMeMTHeyME',
        'CAACAgIAAxkBAAEEW_xiSXJDCbZ4mzyHXXCrDmIOcnDyQACFgEAAlKJkSNYRGjD1m8AATgjBA',
        'CAACAgIAAxkBAAEEW_5iSXJG7Q2WY50RYhdF3V7PFCPb1QACHAEAAlKJkSPBxyimSSWA_iME',
        'CAACAgIAAxkBAAEEXAABYklySDAiDaXPbwor0JtT6EUMJxMAAhUBAAJSiZEjgGt537i45vIjBA',
        'CAACAgIAAxkBAAEEXAJiSXJMh4vk5A-2NK31u8QqZs7qxwACHgEAAlKJkSNHWLKdRIDqeyME',
        'CAACAgIAAxkBAAEEXARiSXJO2C3ePR7NBU21X_qOFnOpWQACIAEAAlKJkSOi1WO8Nphi1yME',
        'CAACAgIAAxkBAAEEXAZiSXJRe8xXIyl2FDs9O9hVPo26sgACIgEAAlKJkSPI4ZRB58JpMyME',
        'CAACAgIAAxkBAAEEXAhiSXJTeJ6ypJI5iWqxjwABPgiEEe8AAlYAA8GcYAykqU9bWwPpESME',
        'CAACAgIAAxkBAAEEXApiSXJXNb2lSNlKYfqhoh4AAV5xI9wAAmEAA8GcYAw36GGenNSThSME',
        'CAACAgIAAxkBAAEEXAxiSXJbEb1QP8bsZW8ehI_clpzvMAACawADwZxgDJa035uTKCYzIwQ',
        'CAACAgIAAxkBAAEEXA5iSXJfszhtm7zLr9uzRvCm-Q5G8QACXAADwZxgDMTB55U4nCMLIwQ',
        'CAACAgIAAxkBAAEEXBBiSXJjKZuLBjcmBS4fMYWpJZghJwACaQADwZxgDE4zEm9SERyMIwQ',
        'CAACAgIAAxkBAAEEXBJiSXJlTfD3nWsFvchl94wkMZ3_DQACJgEAAlKJkSN1aC2WkRIrHiME',
        'CAACAgIAAxkBAAEEXBRiSXJpOfLWb0HmDHU6TxmTQXf63gACNQEAAlKJkSOy_T2Gqc2eJCME',
        'CAACAgIAAxkBAAEEXBZiSXJvo9JtBuAwHT6B5Cyfm9vfMwACMgEAAlKJkSNZdMrsEXdk9SME',
        'CAACAgIAAxkBAAEEXBhiSXJ1nU5o_qyc2bYNYJp1T9GvAQACNwEAAlKJkSPVFECnfG0SGiME',
        'CAACAgIAAxkBAAEEXBpiSXJ33lrpDKFNbn5vq6hyn5syOgACLwEAAlKJkSPELNUfKfI02yME',
        'CAACAgIAAxkBAAEEXBxiSXKHKvbE2sKW0WwSw86KQnw62wACfQADmS9LCsfb0MCpuOlOIwQ',
        'CAACAgIAAxkBAAEEXB5iSXKJKwqS7Wd-nEMa1EIdsxt0hAACewADmS9LCkEObbhRaHn8IwQ',
        'CAACAgIAAxkBAAEEXCBiSXKa6MDX2QNESrWLfFYCtMc5mAACBgsAAi8P8AZbj4rJYwbA0SME',
        'CAACAgIAAxkBAAEEXCJiSXKdGiYfhA6bnPyfy2HHAhVutgACCgsAAi8P8AaHQje1ciNWiiME',
        'CAACAgIAAxkBAAEEXCRiSXKh5Zveo-iiT48i1AcZfQ-EXQACFQsAAi8P8AaN2GW4ATIe6CME',
        'CAACAgIAAxkBAAEEXCZiSXKk8bY0iVCJIoN4Z8LOZqGC2AACEQsAAi8P8AbimyN2TCVklSME',
        'CAACAgIAAxkBAAEEXChiSXKoxDyrGrYYduiQhyu8BheobgACGAsAAi8P8AbLXyC6NEZCDSME',
        'CAACAgIAAxkBAAEEXCpiSXKr_VqIV3t7eELeIdlv5O6WkgACGwsAAi8P8AZkiYC6UpHIYSME',
        'CAACAgIAAxkBAAEEXCxiSXKtf2KMF54VE7cH03oYfPIXcwACIAsAAi8P8AYzFD78OxAgbCME',
        'CAACAgIAAxkBAAEEXC5iSXKuu7m5GLNkZIwhQVSLgK8teQACIQsAAi8P8AYi01Fg2H7WziME',
        'CAACAgIAAxkBAAEEXDBiSXKyMbkeihwquFbSTTTJD86ZqAACFAsAAi8P8AaaXjUXGr_YQiME',
        'CAACAgIAAxkBAAEEXDJiSXK5jcRTnf-dBUssqqQfl22wxQACBgADwDZPE8fKovSybnB2IwQ',
        'CAACAgIAAxkBAAEEXDRiSXK6zDbfI-1bsbM22xneD8JIhgACHwADwDZPE-Q4M_eEUpmSIwQ',
        'CAACAgIAAxkBAAEEXDZiSXK-Kt8UtcxS4EW_jwOxZWfTMgACDAADwDZPE-LPI__Cd5-8IwQ',
        'CAACAgIAAxkBAAEEXDhiSXLB1euRD2h2J0MxVSUAAXQxzbIAAhIAA8A2TxMzvJ4BLpUHNyME',
        'CAACAgIAAxkBAAEEXDpiSXLDSHuAQdSWdMeLN—2qloLoQACHAADwDZPE8GCGtMs_g7hIwQ',
        'CAACAgIAAxkBAAEEXDxiSXLF3embyK9WNFqB7E65kJHxBwACIAADwDZPE_QPK7o-X_TPIwQ',
        'CAACAgIAAxkBAAEEXD5iSXLKmge9xchd9UQK05HWPJi5PAAC0wUAApb6EgU-blRJYnI9SSME',
        'CAACAgIAAxkBAAEEXEBiSXLMED1u0OnkSgjQqsA3McwERAAC4AUAApb6EgWbFgFwLZQU2SME',
        'CAACAgIAAxkBAAEEXEJiSXLPtkao7LbXcRNDCL2LDBocagAC5gUAApb6EgX7jn22HxOAsSME',
        'CAACAgIAAxkBAAEEXERiSXMW0pVj9yoP-JIBpvWnP4NS1gACVhMAAtLeyUt7_BaVb-O_iyME']



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


phrases = ["Я не знаю такой команды(((. Напиши: /start",
    "Извини, тебе нужно написать: /start",
    "Мдааммм... Напиши: /start уже",
    "Блин, не трать мою оперативку и напиши: /start",
    "Ты вообще в порядке? Что ты пишешь?",
    "Мдаммммммм.. Напиши уже : /start",
    "Я тебе говорю! Напиши : /start , и спи спокойной",
    "Почему нельзя просто написать : /start ?"]

db_name = 'dft0ot5oh53gat'
db_user = 'fpgvrquayzkmpl'
db_pass = 'be29ae63278b02f6de70c261d907afae93390f4630602a9db37a9506466314df'
db_host = 'ec2-54-228-97-176.eu-west-1.compute.amazonaws.com'

mon = {"01":"января", "02":"февраля", "03":"марта", "04":"апреля", "05":"мая", "06":"июня", "07":"июля", "08":"августа", "09":"сентября", "10":"октября", "11":"ноября", "12":"декабря"}
sub = {"Алгебра":"алгебре", "Биология":"биологии", "География":"географии", "Геометрия":"геометрии","Иностранный язык (английский)":"английскому языку","Информатика":"информатике",
       "История России. Всеобщая история":"истории России и всеобщей истории","Литература":"литературе", "Обществознание":"обществознанию","Практикум":"практикуму","Практикум по решению задач по физике" :"практикум по физике",
       "Русский язык":"русскому языку","Технология":"технологии","Физика":"физике","Физкультура":"физкультуре","Химия":"химии"}

start_period = '20220328'
end_period = '20220530'
next_periods = []
#TODO: fix periods in config