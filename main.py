import pickle
import os.path
from random import randint, choice

"""
* Хранилище в файле
* В настройки "автосохранение"
* Статус банка и хранилища в файле
"""
lvlupcost = [25, 30, 35, 40]

statesfile = "playerinfo.data"

checkfile = os.path.exists(f'{statesfile}')
if checkfile:
    with open(statesfile, 'rb') as f:
        loadeddata = pickle.load(f)
        autoload = loadeddata["autoload"]

class Player:
    def __init__(self):
        
        # стартовая сумма денег
        self.startmoney = 35
        
        # "общие" переменные
        self.money = self.startmoney
        self.winstreak = 0
        self.bet = 0
        self.rate = 0
        
        # банк (142-194)
        self.bankcoins = 0
        self.bankstatus = "НЕ ПОСТРОЕН"
        
        # настройки
        self.autoloadstat = "ВЫКЛ"
        
        # для сохранения/загрузки прогресса (120-135)
        self.state = {}

        # супер-юзер (102-107)
        self.gm = 0
        self.status = ""

        # переменные для "монеточки" (31-100)
        self.coin = 0
        self.buyHelp = None
        self.CFgames = []
        self.CFlist_status = ""
        
        # переменные для "камень ножницы бумага"
        self.kanobubot = 0
        self.KNBgames = []
        self.KNBlist_status = ""
        
        # хранилище
        self.storagedmoney = 0
        self.putmoney = 0
        self.storagelimit = 25
        self.storagestatus = "НЕ ПОСТРОЕН"
        self.storagelvl = 1
        self.storagelvlup = 40

    def coinflip(self):
        print("Коинфлип (или же монеточка) - все зависит от вашей удачи.")
        print("Поставьте ставку, и если вы победите, вы получите в 2 раза больше")
        print("Если проиграете, вы потеряете ту сумму, которую вложили.")
        print("Введите 0 для возвращения в меню.")
        while True:
            print("\nВаша ставка? {%s}" % self.money)

            try:
                self.rate = int(input(">>> "))
            except ValueError:
                self.rate = 0

            if self.rate == 0:
                break
            if self.rate > self.money:
                print("У вас мало денег для такой ставки!")
            else:
                if self.rate == self.money:
                    print("Видимо, вы очень смелый человек, раз решили потратить сразу все деньги...")
                self.bet = int(input("\nОрел или решка? (1/2)\n>>> "))
                self.coin = randint(1, 2)
                if self.coin == self.bet:
                    self.money += self.rate
                    # +1 к винстрику
                    if self.winstreak < 0:
                        self.winstreak = 0
                    elif self.winstreak >= 0:
                        self.winstreak += 1

                    print(f"Вы победили! Ваш приз - {self.rate * 2}.\nВаш баланс - {self.money}.\n")
                    print(f"Ваш винстрик - {self.winstreak}")
                    self.CFgames.append("(+%(win)s) {Баланс %(money)s}" % {"win": self.rate, "money": self.money})
                else:
                    print("К сожалению, вы проиграли.")
                    if self.winstreak >= 10:
                        print(f"Но так как у вас есть {self.winstreak}, вы можете потратить 10 ед., что-бы вернуть свои деньги.")
                        i = input("Согласны? (y/n)")
                        if i == 'y':
                            self.buyHelp = True
                            self.winstreak -= 10
                            print("Вы не потратили свои деньги.")
                            print(f"Ваш винстрик - {self.winstreak}")
                            self.CFgames.append("(Купил 2 шанс) {Баланс %s}" % self.money)
                        else:
                            self.buyHelp = False
                    else:
                        self.buyHelp = False

                    if not self.buyHelp:
                        self.money -= self.rate
                        print(f"Ваш баланс - {self.money} (-{self.rate})")
                        # обнуление/-1 к винстрику
                        if self.winstreak <= 0:
                            self.winstreak -= 1
                        elif self.winstreak > 0:
                            self.winstreak = 0
                            
                        print(f"Ваш винстрик - {self.winstreak}")
                        self.CFgames.append("(-%(lose)s) {Баланс %(money)s}" % {"lose": self.rate, "money": self.money})
                    if self.money > 0:
                        print("Сыграем еще раз? (y/n)")
                        i = input(">>> ")
                        if i == 'n':
                            break
                        else:
                            print("Продолжаем!\n")

                    else:
                        print("У вас 0 денег.")
                        break

            # coin = 0
            self.bet = 0
            self.rate = 0

    def op(self):
        self.gm = 1
        self.money = 1000000
        self.winstreak = 5000
        self.status = "[АКТИВИРОВАНО]"
        print("Super-User активирован!")

    # история coinflip игр
    def CFreplays(self):
        if self.CFgames == []:
            print("\nНеактивировано. Сыграйте 1 игру в CF.\n")
        else:
            self.CFlist_status = "[Активно!]"
            count = 0
            for j in self.CFgames:
                count += 1
                print(f"{count}. {j}")
                
    def KNBreplays(self):
        if self.KNBgames == []:
            print("\nНеактивировано. Сыграйте 1 игру в KNB.\n")
        else:
            self.KNBlist_status = "[Активно!]"
            count = 0
            for j in self.KNBgames:
                count += 1
                print(f"{count}. {j}")

    def savestate(self):
        self.states = {
            "money": self.money,
            "winstreak": self.winstreak,
            "coins": self.bankcoins,
            "status": self.status,
            "autoload": self.autoloadstat,
            "bankstatus": self.bankstatus,
            "storagestatus": self.storagestatus,
            "storagelevel": self.storagelvl,
            "storagelimit": self.storagelimit,
            "storagedmoney": self.storagedmoney
        }

        with open(statesfile, "wb") as file:
            pickle.dump(self.states, file)

        print("\nПрогресс сохранен!\n")

    def loadstate(self):
        with open(statesfile, 'rb') as file:
            loadeddata = pickle.load(file)

        self.money = loadeddata["money"]
        self.winstreak = loadeddata["winstreak"]
        self.bankcoins = loadeddata["coins"]
        self.status = loadeddata["status"]
        self.autoloadstat = loadeddata["autoload"]
        self.bankstatus = loadeddata["bankstatus"]
        self.storagestatus = loadeddata["storagestatus"]
        self.storagelvl = loadeddata["storagelevel"]
        self.storagelimit = loadeddata["storagelimit"]
        self.storagedmoney = loadeddata["storagedmoney"]
        print("\nПрогресс загружен!\n")
        
    def bank(self):
        while True:
            print("Выберите функцию:")
            print("1. Обменять деньги на монеты {20 денег -> 1 монета}")
            print("2. Обменять винстрик на монеты {3 винстрика -> 1 монета}")
            print("3. Обменять монеты на деньги {1 монета -> 15 денег}")
            print("4. Обменять монеты на винстрик {1 монета -> 3 винстрика}")
            print("5. Что за банк?")
            print("6. Выйти")
            print(f"Запас ваших монеток в банке - {self.bankcoins}")

            try:
                act = int(input(">>> "))
            except ValueError:
                act = False
        
            if act == 1:
                if self.money >= 20:
                    self.money -= 20
                    self.bankcoins += 1
                    print(f"Вы купили 1 монету. {self.bankcoins}")
                    print(f"Ваш баланс - {self.money}")
                else:
                    print(f"У вас мало денег для покупки монет.\nНакопите еще {25 - self.money}")
        
            elif act == 2:
                if self.winstreak >= 3:
                    self.winstreak -= 3
                    self.bankcoins += 1
                    print(f"Вы купили 1 монету. {{self.backcoins}}")
                    print(f"Ваш винстрик - {self.winstreak}")
                else:
                    print(f"У вас мало винстрика для покупки монет! Накопите еще {5 - self.winstreak}")
                
            elif act == 3:
                if self.bankcoins >= 1:
                    self.bankcoins -= 1
                    self.money += 15
                    print(f"Вы обменяли 1 монету на 20 денег. ({self.bankcoins} монет осталось)")
                    print(f"Ваш баланс - {self.money}")
                else:
                    print("Недостаточно монет.")
                    
            elif act == 4:
                if self.bankcoins >= 1:
                    self.bankcoins -= 1
                    self.winstreak += 3
                    print(f"Вы обменяли 1 монету на 5 винстриков. ({self.bankcoins} монет осталось)")
                    print(f"Ваш винстрик - {self.winstreak}")
                else:
                    print("\nНедостаточно монет\n")
            
            elif act == 5:
                print("\nЭто банк, в котором вы можете обменивать свои ресурсы на монеты. Монеты - накопительная валюта, и она будет лежать в банке бесконечно.\n")
            
            else:
                break
                
    def setings(self):
        while True:
            print(f"1. Автозагрузка {self.autoloadstat}")

            try:
                setsettings = int(input(">>> "))
            except ValueError:
                setsettings = False

            if setsettings == 1 and self.autoloadstat == "ВЫКЛ":
                self.autoloadstat = "ВКЛ"
            elif setsettings == 1 and self.autoloadstat == "ВКЛ":
                self.autoloadstat = "ВЫКЛ"
            else:
                break
    
    def resetprogress(self):
        print("\nВы точно хотите сбросить прогресс? y/n || д/н")
        act = input(">>> ")
        if act == "y" or act == "д":
            self.money = self.startmoney
            self.winstreak = 0
            self.bankcoins = 1
            self.status = ""
            self.CFgames = []
            self.CFlist_status = ""
            self.KNBgames = []
            self.KNBlist_status = ""
            self.storagelimit = 25
            self.storagelvl = 1
            self.storagedmoney = 0
            self.bankstatus = "НЕ ПОСТРОЕН"
            self.storagestatus = "НЕ ПОСТРОЕН"
            print("Прогресс успешно сброшен.")
        else:
            pass
    
    def games(self):
        while True:
            print("1. Коинфлип")
            print("2. Камень-ножницы-бумага")

            try:
                act = int(input(">>> "))
            except ValueError:
                act = False

            if act == 1:
                user.coinflip()
            elif act == 2:
                user.kanobu()
            else:
                break
    
    def kanobu(self):
        print("КаНоБу (камень-ножницы-бумага).")
        print("Приз увеличен до х3.")
        print("При проигрыше, нельзя вернуть свои деньги.")
        print("Введите 0 для выхода в меню.")
        
        while True:
            print("Какая будет ставка? {%s}" % self.money)
            self.rate = int(input(">>> "))
            if self.rate > self.money:
                print("У вас нет таких денег!")
            elif self.rate == 0:
                break
            else:
                while True:
                    print("\n1. Камень")
                    print("2. Ножницы")
                    print("3. Бумага\n")
                    self.bet = int(input(">>> "))
                    if self.bet > 0 and self.bet < 4:
                        break
                    else:
                        print("\n\nНеверный ввод\n\n")
                
                self.kanobubot = randint(1, 3)
                if self.bet == self.kanobubot:
                    print("Ничья!")
                    print("Вы не потратили деньги и винстрик.")
                    self.KNBgames.append(f"НИЧЬЯ (Баланс{self.money})")
                elif self.bet == 1 and \
                    self.kanobubot == 2 or \
                    self.bet == 2 and \
                    self.kanobubot == 3 or \
                    self.bet == 3 and \
                    self.kanobubot == 1:
                    self.money += self.rate * 3
                    # +1 к винстрику
                    if self.winstreak < 0:
                        self.winstreak = 0
                    elif self.winstreak >= 0:
                        self.winstreak += 1
                    print("Победа!")
                    print(f"Ваш баланс - {self.money} (+{self.rate * 3})")
                    print(f"Ваш винстрик - {self.winstreak}")
                    self.KNBgames.append(f"ПОБЕДА (Баланс: {self.money} (+{self.rate})")
                    
                elif self.bet == 1 and \
                    self.kanobubot == 3 or \
                    self.bet == 2 and \
                    self.kanobubot == 1 or \
                    self.bet == 3 and \
                    self.kanobubot == 2:
                        self.money -= self.rate
                        # обнуление/-1 к винстрику
                        if self.winstreak <= 0:
                            self.winstreak -= 1
                        elif self.winstreak > 0:
                            self.winstreak = 0
                        
                        print("Вы проиграли!")
                        print(f"Ваш баланс - {self.money} (-{self.rate})")
                        print(f"Ваш винстрик - {self.winstreak}")
                        self.KNBgames.append(f"ПОРАЖЕНИЕ (Баланс: {self.money} (-{self.rate})")
        
    def replays(self):
        while True:
            print(f"\n\n1. КоинФлип игры {self.CFlist_status}")
            print(f"2. КаНоБу игры {self.KNBlist_status}")

            try:
                act = int(input(">>> "))
            except ValueError:
                act = False

            if act == 1:
                self.CFreplays()
            elif act == 2:
                self.KNBreplays()
            else:
                break
                
    def storage(self):
        while True:
            print("1. Положить деньги")
            print("2. Забрать деньги")
            print("3. Прокачать хранилище")
            print("4. Что за хранилище?")
            print(f"Ваш баланс - {self.storagedmoney}/{self.storagelimit}")
            act = int(input(">>> "))
            if act == 1:
                print(f"Сколько вы хотите положить? ({self.money})")
                print("Введите 0 для возвращения в меню.")

                try:
                    self.putmoney = int(input(">>> "))
                except ValueError:
                    self.putmoney = False

                if self.putmoney <= 0:
                    break
                    
                elif self.putmoney > self.money:
                    print("Мало денег для такой суммы.\n")
                elif self.putmoney == 0:
                    break
                        
                else:
                    if self.storagedmoney + self.putmoney > self.storagelimit:
                        print("Операция отклонена.")
                    else:
                        self.money -= self.putmoney
                        self.storagedmoney += self.putmoney
                        print(f"Вы пополнили свое хранилище на {self.putmoney}.")
                            
            elif act == 2:
                while True:
                    print("Сколько денег вы хотите забрать?")
                    print(f"Ваш баланс - {self.money}")
                    print(f"Баланс в хранилище - {self.storagedmoney}")
                    print("Введите 0 для возвразещения в меню.")

                    try:
                        self.putmoney = int(input(">>> "))
                    except ValueError:
                        self.putmoney = False

                    if self.storagelimit - self.putmoney < 0:
                        print("Операция отменена.")
                    elif self.putmoney > self.storagedmoney:
                        print("У вас мало денег в хранилище для забирания такой суммы.")
                            
                    elif self.putmoney == 0:
                        break
                            
                    else:
                        self.money += self.putmoney
                        self.storagedmoney -= self.putmoney
                        print(f"Вы пополнили свой баланс на {self.putmoney}")
                        print(f"Ваш баланс - {self.money}")
                        print(f"Баланс в хранилище - {self.storagedmoney}")
                        break
                        
            elif act == 3:
                print(f"Уровень хранилища - {self.storagelvl}")
                print(f"Повышение уровня стоит {self.storagelvlup} денег.")
                print(f"Ваш баланс - {self.money}")
                print("Будете повышать уровень? д/н")
                act = input(">>> ")
                if act == 'д':
                    if self.money >= self.storagelvlup:
                        self.money -= self.storagelvlup
                        self.storagelvl += 1
                        self.storagelimit += 15
                        self.storagelvlup += choice(lvlupcost)
                        print(f"Вы повысили уровень хранилища до {self.storagelvl}")
                        print(f"Лимит хранлища - {self.storagelimit} (+15)")
                        print(f"Ваш баланс - {self.money}")
                    else:
                        print("Мало денег.")
                        
                elif act == 'н':
                    pass
                    
            elif act == 4:
                print("В хранилище вы можете положить свои деньги, и они никуда не пропадут.")
                print("Так же, вы можете увеличивать лимит хранилища, покупая улучшения.")
                print(f"Покупая улучшение, цена поднимается на случайное число от {lvlupcost[0]} до {lvlupcost[3]}.")
                print(f"Уровень вашего хранилища - {self.storagelvl}.")
            
            else:
                break
                            
    def buildings(self):
        while True:
            print(f"\n1. Банк {self.bankstatus}")
            print(f"2. Хранилище {self.storagestatus}")

            try:
                act = int(input(">>> "))
            except ValueError:
                act = False

            if act == 1 and self.bankstatus == "НЕ ПОСТРОЕН":
                print("Постройка банка стоит 75 денег.")
                print("Построить? д/н")
                act = input(">>> ")
                if act == 'д' and self.money >= 75:
                    print("Банк построен. Теперь вы можете им пользоватся!")
                    self.bankstatus = ''
                elif act == 'д' and self.money < 75:
                    print("Нехватает денег.")
                else:
                    pass
                    
            elif act == 2 and self.storagestatus == "НЕ ПОСТРОЕН":
                print("Постройка хранилища стоит 250 денег.")
                print("Построить? д/н")
                act = input(">>> ")
                if act == 'д' and self.money >= 250:
                    print("Хранилище построено. Теперь вы можете им пользоватся!")
                    self.storagestatus = ""
                elif act == 'д' and self.money < 250:
                    print("Нехватает денег.")
                else:
                    pass
                    
            elif act == 1 and self.bankstatus == "":
                self.bank()
            
            elif act == 2 and self.storagestatus == "":
                self.storage()
                
            else:
                break

user = Player()
if checkfile and autoload == "ВКЛ":
    user.loadstate()
    
while True:
    print("Выберите функцию")
    print("1. Игры")
    print("2. Права супер-юзера %s" % user.status)
    print("3. История игр")
    print("4. Сохранить прогресс")
    print("5. Загрузить прогресс")
    print("6. Постройки")
    print("7. Настройки")
    print("8. Баланс игрока")
    print("9. Сбросить прогресс")

    try:
        act = int(input(">>> "))
    except ValueError:
        act = False

    if act == 1:
        user.games()
    elif act == 2:
        user.op()
    elif act == 3:
        user.replays()
    elif act == 4:
        user.savestate()
    elif act == 5:
        user.loadstate()
    elif act == 6:
        user.buildings()
    elif act == 7:
        user.setings()
    elif act == 8:
        print(f"\nБаланс - {user.money}")
        print(f"Винстрик - {user.winstreak}")
        if user.bankstatus == "":
            print(f"Монеты в банке - {user.bankcoins}\n")
        if user.storagestatus == "":
            print(f"Баланс в хранилище - {user.storagedmoney}")
        print()
    elif act == 9:
        user.resetprogress()
    else:
        break
