import math


class Calculator:
    def __init__(self):
        self.__bin_operators = ['^', '*', '/', '+', '-']
        self.__un_operators = ['~', 'cos', 'sin']
        self.__operators = self.__bin_operators + self.__un_operators

    def calc(self, expression_in: str):
        if not expression_in:
            return -1

        if expression_in.count('(') != expression_in.count(')'):
            raise Exception('[ERROR] Неверная формула')

        expression_rpn = self.__convert_to_rpn(expression_in)
        result = self.__compute(expression_rpn)

        return result, expression_rpn

    def __compute(self, expression_rpn: str):
        expr = expression_rpn.split()
        stack = []
        for elem in expr:
            try:
                operand = float(elem)
                stack.append(operand)
                continue
            except ValueError:
                if not (elem in self.__operators):
                    raise Exception('[ERROR] Неверная формула')

            try:
                operand_2 = stack.pop()
            except Exception:
                raise Exception('[ERROR] Неверная формула')

            match elem:
                case "~":
                    stack.append(operand_2 * (-1))
                    continue
                case "sin":
                    stack.append(math.sin(operand_2))
                    continue
                case "cos":
                    stack.append(math.cos(operand_2))
                    continue

            try:
                operand_1 = stack.pop()
            except Exception:
                raise Exception('[ERROR] Неверная формула')

            match elem:
                case "^":
                    stack.append(operand_1 ** operand_2)
                case "+":
                    stack.append(operand_1 + operand_2)
                case "-":
                    stack.append(operand_1 - operand_2)
                case "*":
                    stack.append(operand_1 * operand_2)
                case "/":
                    try:
                        stack.append(operand_1 / operand_2)
                    except ZeroDivisionError:
                        raise ZeroDivisionError('[ERROR] Попытка деления на нуль')

        if len(stack) != 1:
            raise Exception('[ERROR] Неверная формула')

        return stack[0]

    def __get_operator_priority(self, operator: str):
        match operator:
            case 'cos':
                return 6
            case 'sin':
                return 6
            case '~':
                return 5
            case '^':
                return 4
            case '*':
                return 3
            case '/':
                return 3
            case '+':
                return 2
            case '-':
                return 2
            case '(':
                return 1

    def __convert_to_rpn(self, expression_in: str):
        expression_rpn = ""
        operator_stack = []

        i = 0
        while i < len(expression_in):
            elem = expression_in[i]

            if elem.isdigit() or elem == '.' or elem == ' ':
                expression_rpn += elem
                i += 1
                continue

            if elem == '(':
                expression_rpn += ' '
                operator_stack.append(elem)
                i += 1
                continue

            if elem == ')':
                try:
                    while len(operator_stack) > 0 and operator_stack[-1] != '(':
                        expression_rpn += ' '
                        expression_rpn += operator_stack.pop()
                    expression_rpn += ' '
                    operator_stack.pop()
                    i += 1
                    continue
                except Exception:
                    raise Exception('[ERROR] Неверная формула')

            if elem == '-' and (i == 0 or i >= 1 and expression_in[i - 1] == '('):
                elem = '~'

            try:
                if (elem == 's'
                        and
                        expression_in[i + 1] == 'i'
                        and
                        expression_in[i + 2] == 'n'
                        and
                        expression_in[i + 3] == '('):
                    elem = 'sin'
                    i += 2

                if (elem == 'c'
                        and
                        expression_in[i + 1] == 'o'
                        and
                        expression_in[i + 2] == 's'
                        and
                        expression_in[i + 3] == '('):
                    elem = 'cos'
                    i += 2
            except IndexError:
                raise Exception('[ERROR] Неверная формула')

            if elem in self.__operators:
                if len(operator_stack) > 0 and elem == '^' and operator_stack[-1] == '^':
                    pass
                else:
                    while (len(operator_stack) > 0
                           and
                           self.__get_operator_priority(operator_stack[-1]) >= self.__get_operator_priority(elem)):
                        expression_rpn += ' '
                        expression_rpn += operator_stack.pop()

                expression_rpn += ' '
                operator_stack.append(elem)
                i += 1
            else:
                raise Exception('[ERROR] Неверная формула')

        for i in range(len(operator_stack) - 1, -1, -1):
            expression_rpn += ' '
            expression_rpn += operator_stack[i]

        flag = False
        normalized_expression_rpn = ""

        for elem in expression_rpn:
            if elem == ' ':
                if flag:
                    flag = False
                    normalized_expression_rpn += elem
            else:
                flag = True
                normalized_expression_rpn += elem

        return normalized_expression_rpn


if __name__ == "__main__":
    my_calc = Calculator()
    while True:
        expression_in = input("Введите выражение в инфиксной нотации: ")
        result, expression_rpn = my_calc.calc(expression_in)
        print(f"Выражение в обратной польской нотации: {expression_rpn}")
        print(f"Результат вычислений: {result}")
        print()
        print("####################################################")
        print()
