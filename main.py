import pickle
from random import randint


class Player:
    def __init__(self):
        self.money = 25
        self.winstreak = 0
        self.bet = 0
        self.rate = 0
        self.gm = 0

        # переменные для игр
        self.coin = 0

    def coinflip(self):
        coin = 0
        print("Коинфлип (или же монеточка) - все зависит от вашей удачи.")
        print("Поставьте ставку, и если вы победите, вы получите в 2 раза больше.")
        print("Если проиграете, вы потеряете ту сумму, которую вложили.")
        while True:
            print("\nВаша ставка? {%s}" % self.money)
            self.rate = int(input(">>> "))
            if self.rate > self.money:
                print("У вас мало денег для такой ставки!")
            else:
                self.bet = int(input("\nОрел или решка? (1/2)\n>>> "))
                self.coin = randint(1, 2)
                if self.coin == self.bet:
                    self.money += self.rate * 2
                    print(f"Вы победили! Ваш приз - {self.rate * 2}.\nВаш баланс - {self.money}.\n")
                else:
                    self.money -= self.rate
                    print("К сожалению, вы проиграли.")
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

            coin = 0
            self.bet = 0
            self.rate = 0


user = Player()
user.coinflip()
