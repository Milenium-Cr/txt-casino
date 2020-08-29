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

        # для сохранения/загрузки прогресса
        self.state = {}

        # супер-юзер
        self.gm = 0
        self.status = ""

        # переменные для "монеточки"
        self.coin = 0
        self.buyHelp = None
        self.CFgames = []
        self.CFlist_status = ""

    def coinflip(self):
        # coin = 0
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
                    print("Видимо, вы очень смелый человек, раз решили потратить сразу все деньги..")
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
            print("Неактивирован. Сыграйте 1 игру в CF.")
        else:
            self.CFlist_status = "[Активно!]"
            count = 0
            for j in self.CFgames:
                count += 1
                print(f"{count}. {j}")

    def savestate(self):
        self.states = {"money": self.money, "winstreak": self.winstreak}
        f = open(statesfile, 'wb')
        pickle.dump(self.states, f)
        f.close()
        print("Прогресс сохранен!\n")

    def loadstate(self):
        f = open(statesfile, 'rb')
        loadeddata = pickle.load(f)
        f.close()
        self.money = loadeddata["money"]
        self.winstreak = loadeddata["winstreak"]
        print("Прогресс загружен!\n")


user = Player()
while True:
    print("Выберите функцию")
    print("1. Коинфлип")
    print("2. Права супер-юзера %s" % user.status)
    print("3. История игр %s" % user.CFlist_status)
    print("4. Сохранить прогресс")
    print("5. Загрузить прогресс")
    print("6. Баланс игрока")

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
        print(f"Баланс - {user.money}")
    else:
        break
