import random
import os
from .Ticket import Ticket
from .tools import yes_or_no


class LottoGame:
    def __init__(self):
        self.player = Ticket('Ваш билет')
        self.computer = Ticket('Билет компьютера')
        self.user_made_a_mistake = False
        self.player_won = False
        self.computer_won = False
        self.barrels = list(range(1, 91))
        random.shuffle(self.barrels)
        self._game_over = False

    def run(self):
        if self._game_over:
            raise Exception('Game over')

        for barrel in self.barrels:
            os.system('cls||clear')
            print(f'Текущий боченок: {barrel}')
            print(self.player)
            print(self.computer)

            if self.user_made_a_mistake or self.player_won or self.computer_won:
                self._game_over = True
                return True

            user_answered_yes = yes_or_no('Вычеркнуть число?')
            self.user_made_a_mistake = user_answered_yes != self.player.has(barrel)

            if self.player.has(barrel):
                self.player.cross_out(barrel)
            if self.computer.has(barrel):
                self.computer.cross_out(barrel)

            self.player_won = self.player.is_finished()
            self.computer_won = self.computer.is_finished()

    def get_the_result_of_game(self):
        if self.user_made_a_mistake:
            return 'Будте внимательнее! Вы ошиблись. Игра окончена.'
        elif self.player_won and self.computer_won:
            return 'Ничья!'
        elif self.player_won:
            return 'Вы победили!'
        elif self.computer_won:
            return 'Компьютер выйграл'
        else:
            return 'Oops! чтото пошло не так. Никто не победил.'
