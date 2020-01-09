import random
from copy import deepcopy


class Ticket:
    def __init__(self, name):
        self.name = name
        # Создаем пустой билет
        self.matrix = []
        for _ in range(3):
            self.matrix.append([0 for column in range(9)])

        shuffled_matrix = deepcopy(self.matrix)

        # Заполняем билет числами 99 на месте будущих номеров. Пустые поля остаются со значением ''.
        NONEMPTY_MARKER = 99

        def get_candidatures(column):
            return [row for row in range(3) if self.matrix[row].count(NONEMPTY_MARKER) < 5]

        for column in range(9):
            candidature_rows = get_candidatures(column)
            random_row = random.choice(candidature_rows)
            self.matrix[random_row][column] = NONEMPTY_MARKER
            if column < 6:
                candidature_rows.remove(random_row)
                random_row = random.choice(candidature_rows)
                self.matrix[random_row][column] = NONEMPTY_MARKER

        # меняем порядок колонок (тебуется Python 3.8)
        random.shuffle(new_order := list(range(9)))

        for i, column in enumerate(new_order):
            for row in range(3):
                shuffled_matrix[row][column] = self.matrix[row][i]

        self.matrix = shuffled_matrix

        # Заполняем матрицу числами
        used_numbers = set([NONEMPTY_MARKER])

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

        for row in self.matrix:
            print(row)


class LottoGame:
    def __init__(self):
        self.player = Ticket('Ваша карточка')
        self.computer = Ticket('Карточка компьютера')
        self.barrels = list(range(1, 91))
        random.shuffle(self.barrels)
        # self.barrels.pop()

    def run(self):
        for barrel in self.barrels:
            pass


def main():
    lotto = LottoGame()
    lotto.run()



if __name__ == '__main__':
    main()
