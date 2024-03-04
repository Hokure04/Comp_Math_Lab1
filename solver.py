import colors as color

# функция для чтения матрицы из файла
def input_from_file(path):
    try:
        e = float(input('Введите точность уравнения: '))
        n = 0
        a = []
        with open(path, 'r', encoding='utf-8') as file:
            for line in file:
                if (line != '\n') and (line != ' ') and (line != ' \n'):
                    n += 1
        if n > 20:
            print(color.BOLD + color.RED, 'В файле больше 20 уравнений! Уменьшите и попробуйте снова.', color.END)
            return
        file.close()
        with open(path, 'r', encoding='utf-8') as file:
            for row in file:
                line = list(row.split())
                if (line[-2] != '|') or (len(line) - 2 != n):
                    print(color.BOLD + color.RED, 'Файл имеет ошибку формата! Исправте и попробуйте снова.', color.END)
                    return
                a.append(list(line))
        file.close()
        calculator = Calculator(n, optimize(a, n), e)
        calculator.calculate()
        del calculator
    except FileNotFoundError:
        print(color.BOLD + color.RED, 'Файл не был найден по пути: ', color.END, path)

# функция для ввода матрицы с консоли
def input_from_console():
    try:
        e = float(input('Введите точность уравнения: '))
        n = int(input('Введите кол-во уравнений не более 20: '))
        if (n <= 20) or (n > 1):
            a = []
            print('Введите коэффициенты уравнения в формает:')
            print(color.YELLOW, '\t', 'ai1 ai2 ... aij | bi', color.END)
            for i in range(n):
                while True:
                    line = list((input(str(i + 1) + ': ').split()))
                    if (int(len(line)) - 2 != n) or (line[-2] != '|'):
                        print(color.BOLD + color.RED, 'Кол-во строк не равно кол-ву столбцов. Или неправильный формат.',
                              color.END)
                        print('Попробуйте снова')
                    else:
                        a.append(line)
                        break
            calculator = Calculator(n, optimize(a, n), e)
            calculator.calculate()
            del calculator
        else:
            print(color.BOLD + color.RED, 'Неправильный ввод!', color.END)
            return
    except ValueError:
        print(color.BOLD + color.RED, 'Неправильный ввод! ', color.END)


# функция, которая делает нашу матрицу дробными числами из строк
def optimize(arr, n):
    i = 0
    while i < n:
        j = 0
        while j < n:
            arr[i][j] = float(arr[i][j])
            j += 1
        arr[i][j + 1] = float(arr[i][j + 1])
        i += 1
    return arr

# Класс выполняющий вычислени метода простой итерации
class Calculator:
    n = 0                   # Количество уравнений и неизвестных
    system = []             # Система уравнений
    e = 0                   # Точность
    res_vector = []         # Вектор неизветных
    inaccuracy_vector = 0   # Вектор погрешностей
    iteration_counter = 0   # Счётчик итерации

    def __init__(self, n, system, e):
        self.n = n
        self.system = system
        self.e = e

    def calculate(self):
        try:
            print('\n', color.YELLOW, 'Наша система:', color.END)
            self.__print_system()
            print('\n')

            boolean = self.__check_diagonal()
            if boolean:
                print('СЛАУ успешно отсортирована')
                print('\n')
                print('\n', color.YELLOW, 'Отсортированная матрица:', color.END)
                self.__print_system()

                self.__expression_of_elements()

                self.__print_matrix_c()
                self.__print_matrix_d()

                success_bool = self.__norm_check()

                if success_bool:
                    self.__approximation()
            else:
                print('Не получилось отсортировать СЛАУ, значит условие преобладания не выполнено')


        except ZeroDivisionError:
            return
        except ArithmeticError:
            return



    # Вывод системы на экран
    def __print_system(self):
        i = 0
        while i < self.n:
            j = 0
            while j < self.n:
                print(self.system[i][j], 'x[' + str(j) + '] ', end='')
                j += 1
            print(self.system[i][-2], self.system[i][-1])
            i += 1

    # Вывод матрицы C
    def __print_matrix_c(self):
        print('\n', color.YELLOW, 'Матрица С:', color.END)
        i = 0
        while i < self.n:
            j = 0
            while j < self.n:
                print(self.system[i][j], 'x[' + str(j) + '] ', end='')
                j += 1
            print()
            i += 1

    # Вывод начального приблежения
    def __print_matrix_d(self):
        print('\n', color.YELLOW, 'Матрица D:', color.END)
        i = 0
        while i < self.n:
            print(self.system[i][-1])
            i += 1



    # Проверка условия преобладания диагональных элементов
    def __check_diagonal(self):
        i = 0
        arr = []
        important_elem = 0
        while i < self.n:
            j = 0
            while j < self.n:
                if i == j:
                    important_elem = self.system[i][j]
                    j += 1
                    continue
                else:
                    arr.append(self.system[i][j])
                    j += 1
            iterator = 0
            row_sum = 0
            while iterator < len(arr):
                row_sum += abs(arr[iterator])
                iterator += 1
            if abs(important_elem) < row_sum:
                print('Условие преобладания не выполнено '+ str(abs(important_elem)) + ' < '+str(row_sum))
                self.__sort_diag_arr()
                bool = False
            else:
                print('Условие преобладния выполнено '+str(abs(important_elem))+' > ' + str(row_sum))
                bool = True
            arr.clear()
            i += 1
        return bool

    # Сортировка уравнений СЛАУ
    def __sort_diag_arr(self):
        for i in range(self.n):
            ind, self.system[i:] = zip(*sorted(enumerate(self.system[i:]),
                                     key=lambda x: -abs(x[1][i])))

        self.__print_system()
        return self.system

    # Выражение неизвестных элементов
    def __expression_of_elements(self):
        i = 0
        expression_elem = 0
        while i < self.n:
            j = 0
            while j < self.n:
                if i == j:
                    expression_elem = self.system[i][j]
                    j += 1
                else:
                    j += 1
            k = 0
            while k < self.n:
                self.system[i][k] = -self.system[i][k]/expression_elem
                k += 1
            self.system[i][-1] = self.system[i][-1]/expression_elem
            i += 1
        iterator = 0
        while iterator < self.n:
            j = 0
            while j < self.n:
                if iterator == j:
                    self.system[iterator][j] = 0
                    j += 1
                else:
                    continue
                iterator += 1

    # Проверка условия сходимости
    def __norm_check(self):
        i = 0
        array = []
        while i < self.n:
            sum = 0
            j = 0
            while j < self.n:
                sum += abs(self.system[i][j])
                j += 1
            round(sum, 1)
            array.append(sum)
            i += 1
        c = max(array)
        #print(c)
        if c < 1:
            print('\n')
            print('Условие сходимости выполнено')
            return True
        else:
            print('\n')
            print('Условие сходимости не выполнено')
            return False

    # получение первого приближения
    def __approximation(self):
        i = 0
        while i < self.n:
            j = 0
            unknowns_vector = 0
            while j < self.n:
                k = 0
                while k < self.n:
                    unknowns_vector += self.system[i][j]*self.system[k][-1]
                    k += 1
                    j += 1
                unknowns_vector += self.system[i][-1]
                unknowns_vector = round(unknowns_vector, 5)
                self.res_vector.append(unknowns_vector)
            i += 1
        print('\n')
        print(color.YELLOW, 'Вектора неизвестных и их погрешности:', color.END)
        print('Вектор неизвестных: ' + str(self.res_vector))
        self.__compute_inaccuracy_vector()


    # Нахождение приближённого значения с учётом погрешности
    def __compute_inaccuracy_vector(self):
        if self.iteration_counter == 0:
            i = 0
            array = []
            while i < self.n:
                array.append(round(abs(self.res_vector[i] - self.system[i][-1]), 5))
                i += 1
            self.inaccuracy_vector = max(array)
            self.iteration_counter += 1

            print('Вектор погрешностей: '+str(self.inaccuracy_vector))
        while self.inaccuracy_vector > self.e:
            i = 0
            array = []
            array.extend(self.res_vector)
            max_array = []
            self.res_vector.clear()
            while i < self.n:
                j = 0
                unknowns_vector = 0
                while j < self.n:
                        k = 0
                        while k < self.n:
                            unknowns_vector += self.system[i][j] * array[k]
                            k += 1
                            j += 1
                        unknowns_vector += self.system[i][-1]
                        unknowns_vector = round(unknowns_vector, 5)
                        self.res_vector.append(unknowns_vector)
                max_array.append(round(abs(self.res_vector[i] - array[i]), 5))
                i += 1
            print('Вектор неизвестных: '+ str(self.res_vector))
            # print(self.res_vector)
            self.inaccuracy_vector = max(max_array)
            self.iteration_counter += 1
            print('Вектор погрешностей: '+str(self.inaccuracy_vector))
        print('Общее количество итерации: '+str(self.iteration_counter))

