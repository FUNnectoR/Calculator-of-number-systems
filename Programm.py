import tkinter as tk
from tkinter import messagebox

def is_valid_number(number: str, base: int) -> bool:
    valid_digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"[:base]
    return all(char in valid_digits for char in number.upper() if char != '.')

def convert_number(number: str, from_base: int, to_base: int = 10) -> str:
    is_negative = number.startswith('-')
    if is_negative:
        number = number[1:]

    if '.' in number:
        whole, frac = number.split('.')
        whole_decimal = int(whole, from_base)
        frac_decimal = sum(int(digit, from_base) * (from_base ** -i) for i, digit in enumerate(frac, 1))
        decimal_number = whole_decimal + frac_decimal
    else:
        decimal_number = int(number, from_base)

    if is_negative:
        decimal_number = -decimal_number

    if to_base == 10:
        return str(decimal_number)

    digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    whole_number = abs(int(decimal_number))
    result = ""

    if whole_number == 0:
        result = '0'
    else:
        while whole_number > 0:
            result = digits[whole_number % to_base] + result
            whole_number //= to_base

    frac_part = abs(decimal_number) - abs(int(decimal_number))
    if frac_part > 0:
        result += '.'
        for _ in range(5):
            frac_part *= to_base
            result += digits[int(frac_part)]
            frac_part -= int(frac_part)

    if is_negative:
        result = '-' + result

    return result or '0'

def perform_operation(num1: str, num2: str, operation: str, base: int) -> str:
    if not is_valid_number(num1, base) or not is_valid_number(num2, base):
        return "Ошибка: одно или оба числа некорректны для выбранной системы счисления."

    decimal_num1 = float(convert_number(num1, base, 10))
    decimal_num2 = float(convert_number(num2, base, 10))

    if operation == '+':
        result = decimal_num1 + decimal_num2
    elif operation == '-':
        result = decimal_num1 - decimal_num2
    elif operation == '*':
        result = decimal_num1 * decimal_num2
    elif operation == '/':
        if decimal_num2 == 0:
            return "Ошибка: деление на ноль"
        result = decimal_num1 / decimal_num2
    elif operation == '**':
        result = decimal_num1 ** decimal_num2
    elif operation == '%':
        result = decimal_num1 % decimal_num2
    elif operation == '&':
        result = int(decimal_num1) & int(decimal_num2)
    elif operation == '|':
        result = int(decimal_num1) | int(decimal_num2)
    elif operation == '^':
        result = int(decimal_num1) ^ int(decimal_num2)
    else:
        return "Неверная операция"

    return convert_number(f"{result:.5f}", 10, base)

def on_convert():
    number = entry_number.get()
    from_base = int(entry_from_base.get())
    to_base = int(entry_to_base.get())
    
    if not is_valid_number(number, from_base):
        messagebox.showerror("Ошибка", "Число некорректно для выбранной системы счисления.")
        return
    
    result = convert_number(number, from_base, to_base)
    label_result.config(text=f"Результат: {result}")

def on_arithmetic():
    number1 = entry_number1.get()
    number2 = entry_number2.get()
    operation = entry_operation.get()
    base = int(entry_base.get())
    
    result = perform_operation(number1, number2, operation, base)
    label_result.config(text=f"Результат: {result}")

def create_conversion_window():
    window = tk.Toplevel(root)
    window.title("Перевод чисел")
    
    global entry_number, entry_from_base, entry_to_base, label_result
    entry_number = tk.Entry(window)
    entry_from_base = tk.Entry(window)
    entry_to_base = tk.Entry(window)
    
    tk.Label(window, text="Число для перевода:").pack()
    entry_number.pack()
    tk.Label(window, text="Из системы счисления (2-36):").pack()
    entry_from_base.pack()
    tk.Label(window, text="В систему счисления (2-36):").pack()
    entry_to_base.pack()
    
    button_convert = tk.Button(window, text="Перевести", command=on_convert)
    button_convert.pack()
    
    label_result = tk.Label(window, text="Результат:")
    label_result.pack()

def create_arithmetic_window():
    window = tk.Toplevel(root)
    window.title("Арифметические операции")
    
    global entry_number1, entry_number2, entry_operation, entry_base, label_result
    entry_number1 = tk.Entry(window)
    entry_number2 = tk.Entry(window)
    entry_operation = tk.Entry(window)
    entry_base = tk.Entry(window)
    
    tk.Label(window, text="Первое число:").pack()
    entry_number1.pack()
    tk.Label(window, text="Второе число:").pack()
    entry_number2.pack()
    tk.Label(window, text="Операция (+, -, *, /, **, %, |, ^):").pack()
    entry_operation.pack()
    tk.Label(window, text="Система счисления (2-36):").pack()
    entry_base.pack()
    
    button_calculate = tk.Button(window, text="Вычислить", command=on_arithmetic)
    button_calculate.pack()
    
    label_result = tk.Label(window, text="Результат:")
    label_result.pack()

def create_menu():
    menubar = tk.Menu(root)
    
    conversion_menu = tk.Menu(menubar, tearoff=0)
    conversion_menu.add_command(label="Просто перевод чисел", command=create_conversion_window)
    
    arithmetic_menu = tk.Menu(menubar, tearoff=0)
    arithmetic_menu.add_command(label="Арифметические операции", command=create_arithmetic_window)
    
    menubar.add_cascade(label="Перевод", menu=conversion_menu)
    menubar.add_cascade(label="Арифметика", menu=arithmetic_menu)
    menubar.add_command(label="Выход", command=root.quit)
    
    root.config(menu=menubar)

root = tk.Tk()
root.title("Конвертер чисел и арифметика")

create_menu()

root.mainloop()