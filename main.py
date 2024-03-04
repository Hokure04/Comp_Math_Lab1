import colors as color
from solver import input_from_file, input_from_console

print(color.BOLD + color.RED, 'Решатель Системы Уравнений методом простых итерации!', color.END)

while True:
    try:
        print('\n', 'Доступные функции программы:')
        print(color.GREEN,
              '\t', '1: Считывание линейной системы из файла.')
        print('\t', '2: Ввод линейной системы.')
        param = int(input('Введите число функции = '))

        if param == 1:
            print(color.YELLOW, 'Выбран способ считывание с файла.', color.END)
            print('Файл должен содержать линейную систему вида (Размерность не более n = 20):', '\n',
                  '\t', 'a11 a12 ... a1n | b1', '\n',
                  '\t', 'a21 a22 ... a2n | b2', '\n',
                  '\t', '... ... ... ... | ..', '\n',
                  '\t', 'an1 an2 ... ann | bn')
            input_from_file(input('Введите путь к фалу: ').strip())
        elif param == 2:
            print(color.YELLOW, 'Выбран сбособ ввода вручную.', color.END)
            input_from_console()
        else:
            print(color.BOLD + color.RED, 'Неправильно введено значение! Попробуйте снова.', color.END)
    except:
        print(color.BOLD + color.RED, 'Что-то пошло не так', color.END)
