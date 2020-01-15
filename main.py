from lotto_game import LottoGame


def main():
    lotto = LottoGame()
    if lotto.run():
        print(lotto.get_the_result_of_game())
    else:
        print('Oops!')


if __name__ == '__main__':
    main()
