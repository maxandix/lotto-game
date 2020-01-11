import random
from copy import deepcopy
import logging
import os

logger = logging.getLogger(__name__)


class Ticket:
    def __init__(self, name):
        self.name = name
        self.sum_crossed_out = 0
        # Создаем пустой билет
        self.matrix = []
        for row in range(3):
            self.matrix.append([0 for column in range(9)])

        shuffled_matrix = deepcopy(self.matrix)

        # Заполняем билет числами 99 на месте будущих номеров. Пустые поля остаются со значением ''.
        NONEMPTY_MARKER = 99

        def get_candidatures(column):
            return [row for row in range(3) if self.matrix[row].count(NONEMPTY_MARKER) < 5]

        for column in range(9):
            try:
                candidature_rows = get_candidatures(column)
                random_row = random.choice(candidature_rows)
                self.matrix[random_row][column] = NONEMPTY_MARKER
                if column < 6:
                    candidature_rows.remove(random_row)
                    random_row = random.choice(candidature_rows)
                    self.matrix[random_row][column] = NONEMPTY_MARKER
            except IndexError as ex:
                logger.exception(f'Возник IndexError. Так как candidature_rows пуст. matrix = {self.matrix}',
                                 exc_info=False)

        # меняем порядок колонок (тебуется Python 3.8)
        random.shuffle(new_order := list(range(9)))

        for i, column in enumerate(new_order):
            for row in range(3):
                shuffled_matrix[row][column] = self.matrix[row][i]

        self.matrix = shuffled_matrix

        # Заполняем матрицу числами
        used_numbers = {NONEMPTY_MARKER}

        def get_number(column):
            random_args = (0, 9)
            if column == 0:
                random_args = (1, 9)
            elif column == 8:
                random_args = (0, 10)

            new_number = NONEMPTY_MARKER
            while new_number in used_numbers:
                new_number = column * 10 + random.randint(*random_args)

            used_numbers.add(new_number)

            return new_number

        for column in range(9):
            for row in range(3):
                if self.matrix[row][column] == NONEMPTY_MARKER:
                    self.matrix[row][column] = get_number(column)

    def has(self, num) -> bool:
        '''
        Возвращает True, если в билете есть число num, иначе возвращает False.
        :param num:
        :return: bool
        '''
        for row in self.matrix:
            if row.count(num):
                return True
        return False

    def cross_out(self, num):
        '''
        Вычёркивает значение num из билета и возвращает его (вычеркнутый элемент заменяется на -1). Если такого значения нет, поднимает Exception.
        :param num:
        :return:
        '''
        for row in range(0, 3):
            for column in range(0, 9):
                if self.matrix[row][column] == num:
                    self.matrix[row][column] = -1
                    self.sum_crossed_out += 1
                    return num
        raise Exception(f'Число {num} не найдено')

    def is_finished(self) -> bool:
        '''
        Проверяет все ли числа вычеркнуты из билета
        :return: bool
        '''
        for row in self.matrix:
            for cell in row:
                if cell > 0:
                    return False
        return True

    def __str__(self):
        all_str = [(' ' + self.name + ' ').center(27, '-')]

        for row in self.matrix:
            str_row = []
            for cell in row:
                if not cell:
                    str_row.append('   ')
                elif cell == -1:
                    str_row.append('  -')
                else:
                    str_row.append('{:>3}'.format(cell))

            all_str.append(''.join(str_row))

        all_str.append('-' * 27)
        return '\n'.join(all_str)


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


def yes_or_no(question) -> bool:
    while "the answer is invalid":
        reply = str(input(question + ' (y/n): ')).lower().strip()
        if reply[:1] == 'y':
            return True
        if reply[:1] == 'n':
            return False


def main():
    lotto = LottoGame()
    if lotto.run():
        print(lotto.get_the_result_of_game())
    else:
        print('Oops!')


if __name__ == '__main__':
    main()
