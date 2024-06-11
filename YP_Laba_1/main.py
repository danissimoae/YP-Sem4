from algorithm import Calculator

if __name__ == "__main__":
    calculator = Calculator()

    while True:
        expression_in = input("Введите выражение в инфиксной нотации: ")
        result, expression_rpn = calculator.calc(expression_in)

        print(f"Выражение в обратной польской нотации: {expression_rpn}")
        print(f"Результат вычислений: {result}")
        print()
        print("-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-")
        print()
