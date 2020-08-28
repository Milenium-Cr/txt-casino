from random import randint


class Player:
    def __init__(self):
        self.money = 25
        self.winstreak = 0
        self.bet = 0
        self.rate = 0
        self.gm = 0

        # переменные для "монеточки"
        self.coin = 0
        self.buyHelp = None

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
                    # +1 к винстрику
                    if self.winstreak <= 0:
                        self.winstreak = 1
                    elif self.winstreak >= 1:
                        self.winstreak += 1
                    
                    print(f"Вы победили! Ваш приз - {self.rate * 2}.\nВаш баланс - {self.money}.\n")
                    print(f"Ваш винстрик - {self.winstreak}")
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
                    else:
                        self.buyHelp = False
                            
                    if self.buyHelp == False:
                        self.money -= self.rate
                        print(f"Ваш баланс - {self.money} (-{self.rate})")
                    # обнуление/-1 к винстрику
                        if self.winstreak < 0:
                            self.winstreak -= 1
                        
                        elif self.winstreak > 0:
                            self.winstreak = 0
                        print(f"Ваш винстрик - {self.winstreak}")
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
