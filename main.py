import pickle
from random import randint

statesfile = "playerinfo.data"


class Player:
    def __init__(self):
        # "общие" переменные
        self.money = 25
        self.winstreak = 0
        self.bet = 0
        self.rate = 0
        
        # банк
        self.bankcoins = 1

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

    def coinflip(self):
        print("Коинфлип (или же монеточка) - все зависит от вашей удачи.")
        print("Поставьте ставку, и если вы победите, вы получите в 2 раза больше")
        print("Если проиграете, вы потеряете ту сумму, которую вложили.")
        print("Введите 0 для возвращения в меню.")
        while True:
            print("\nВаша ставка? {%s}" % self.money)
            self.rate = int(input(">>> "))
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
            print("\nНеактивирован. Сыграйте 1 игру в CF.\n")
        else:
            self.CFlist_status = "[Активно!]"
            count = 0
            for j in self.CFgames:
                count += 1
                print(f"{count}. {j}")

    def savestate(self):
        self.states = {"money": self.money, "winstreak": self.winstreak, "coins": self.bankcoins}

        with open(statesfile, "wb") as file:
            pickle.dump(self.states, file)

        print("\nПрогресс сохранен!\n")

    def loadstate(self):
        with open(statesfile, 'rb') as file:
            loadeddata = pickle.load(file)

        self.money = loadeddata["money"]
        self.winstreak = loadeddata["winstreak"]
        self.bankcoins = loadeddata["coins"]
        print("\nПрогресс загружен!\n")
        
    def bank(self):
        print("Выберите функцию:")
        print("1. Обменять деньги на монеты {25 денег -> 1 монета}")
        print("2. Обменять винстрик на монеты {5 винстрика -> 1 монета}")
        print("3. Обменять монеты на деньги {1 монета -> 20 денег}")
        print("4. Обменять монеты на винстрик {1 монета -> 5 винстрика}")
        print("5. Что за банк?")
        print("6. Выйти")
        print(f"Запас ваших монеток в банке - {self.bankcoins}")
        act = int(input(">>> "))
        
        if act == 1:
            if self.money >= 25:
                self.money -= 25
                self.bankcoins += 1
                print(f"Вы купили 1 монету. {self.bankcoins}")
                print(f"Ваш баланс - {self.money}")
            else:
                print(f"У вас мало денег для покупки монет.\nНакопите еще {25 - self.money}")
        
        elif act == 2:
            if self.winstreak >= 5:
                self.winstreak -= 5
                self.bankcoins += 1
                print(f"Вы купили 1 монету. {{self.backcoins}}")
                print(f"Ваш винстрик - {self.winstreak}")
            else:
                print(f"У вас мало винстрика для покупки монет! Накопите еще {5 - self.winstreak}")
                
        elif act == 3:
            if self.bankcoins >= 1:
                self.bankcoins -= 1
                self.money += 20
                print(f"Вы обменяли 1 монету на 20 денег. ({self.bankcoins} монет осталось)")
                print(f"Ваш баланс - {self.money}")
            else:
                print("Недостаточно монет.")
                    
        elif act == 4:
            if self.bankcoins >= 1:
                self.bankcoins -= 1
                self.winstreak += 5
                print(f"Вы обменяли 1 монету на 5 винстриков. ({self.bankcoins} монет осталось)")
                print(f"Ваш винстрик - {self.winstreak}")
            else:
                print("Недостаточно монет")
            
        elif act == 5:
            print("\nЭто банк, в котором вы можете обменивать свои ресурсы на монеты. Монеты - накопительная валюта, и она будет лежать в банке бесконечно.\n")
            
        else:
            pass

user = Player()
while True:
    print("Выберите функцию")
    print("1. Коинфлип")
    print("2. Права супер-юзера %s" % user.status)
    print("3. История игр %s" % user.CFlist_status)
    print("4. Сохранить прогресс")
    print("5. Загрузить прогресс")
    print("6. Банк")
    print("7. Баланс игрока")

    act = int(input(">>> "))

    if act == 1:
        user.coinflip()
    elif act == 2:
        user.op()
    elif act == 3:
        user.CFreplays()
    elif act == 4:
        user.savestate()
    elif act == 5:
        user.loadstate()
    elif act == 6:
        user.bank()
    elif act == 7:
        print(f"\nБаланс - {user.money}")
        print(f"Винстрик - {user.winstreak}")
        print(f"Монеты в банке - {user.bankcoins}\n")
    else:
        break
