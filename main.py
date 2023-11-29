import tkinter as tk
from tkinter import ttk

historique = []

import re

def shunting_yard(expression):
    output_queue = []
    operator_stack = []

    operators = {'+': 1, '-': 1, 'x': 2, '/': 2, '%': 2}

    expression = re.sub(r'([-+x/*%()])', r' \1 ', expression)
    tokens = expression.split()

    for i, token in enumerate(tokens):
        if token.isdigit() or (token == '-' and (i == 0 or (i > 0 and tokens[i-1] in operators))):
            # Gérer les nombres (positifs et négatifs)
            output_queue.append(token)
        elif token in operators:
            while operator_stack and operators.get(operator_stack[-1], 0) >= operators.get(token, 0):
                output_queue.append(operator_stack.pop())
            operator_stack.append(token)
        elif token == '(':
            operator_stack.append(token)
        elif token == ')':
            while operator_stack and operator_stack[-1] != '(':
                output_queue.append(operator_stack.pop())
            operator_stack.pop()

    while operator_stack:
        output_queue.append(operator_stack.pop())

    return output_queue


def calculate_rpn(rpn_queue):
    stack = []

    for token in rpn_queue:
        if token.replace('.', '', 1).isdigit() or (token[0] == '-' and token[1:].replace('.', '', 1).isdigit()):
            stack.append(int(float(token)))
        elif token in ('+', '-', 'x', '/', '%'):
            if len(stack) < 2:
                raise ValueError("Pas assez d'opérandes pour l'opérateur '{}'".format(token))
            num2 = stack.pop()
            num1 = stack.pop()
            if token == '+':
                stack.append(num1 + num2)
            elif token == '-':
                stack.append(num1 - num2)
            elif token == 'x':
                stack.append(num1 * num2)
            elif token == '/':
                if num2 == 0:
                    raise ZeroDivisionError("Division par zéro")
                stack.append(num1 / num2)
            elif token == '%':
                stack.append(num1 % num2)

    if len(stack) != 1:
        raise ValueError("L'expression est invalide")

    return stack[0]

def calcule(expression, entry_var, historique_listbox):
    try:
        rpn_queue = shunting_yard(expression)
        result = calculate_rpn(rpn_queue)
        historique.append(f"{expression} = {result}")
        entry_var.set(result)
        historique_listbox.insert(tk.END, f"{expression} = {result}")
    except (ZeroDivisionError, ValueError) as e:
        entry_var.set(f"Erreur : {e}")
    except Exception as e:
        entry_var.set(f"Une erreur est survenue : {e}")

def effacer_historique(historique_listbox):
    historique.clear()
    historique_listbox.delete(0, tk.END)

# Fonction principale de l'interface graphique
def create_gui():
    root = tk.Tk()
    root.title("Calculatrice 9000")

    entry_var = tk.StringVar()
    entry = ttk.Entry(root, textvariable=entry_var, font=('Arial', 14), justify='right', state='readonly')
    entry.grid(row=0, column=0, columnspan=4, sticky='nsew')

    button_texts = [
        '7', '8', '9', '/',
        '4', '5', '6', 'x',
        '1', '2', '3', '-',
        '0', '.', '=', '+'
    ]

    row_val = 1
    col_val = 0

    for text in button_texts:
        ttk.Button(root, text=text, command=lambda t=text: on_button_click(t, entry_var, historique_listbox)).grid(row=row_val, column=col_val, sticky='nsew', padx=2, pady=2)
        col_val += 1
        if col_val > 3:
            col_val = 0
            row_val += 1

    ttk.Button(root, text='Effacer', command=lambda: entry_var.set('')).grid(row=row_val, column=col_val, sticky='nsew', padx=2, pady=2)

    historique_label = ttk.Label(root, text="Historique:")
    historique_label.grid(row=row_val + 1, column=0, columnspan=4, pady=(10, 0))

    historique_listbox = tk.Listbox(root, selectbackground="yellow", selectmode=tk.SINGLE, height=5, font=('Arial', 10))
    historique_listbox.grid(row=row_val + 2, column=0, columnspan=4, sticky='nsew', padx=2, pady=2)

    effacer_button = ttk.Button(root, text='Effacer Historique', command=lambda: effacer_historique(historique_listbox))
    effacer_button.grid(row=row_val + 3, column=0, columnspan=4, sticky='nsew', padx=2, pady=10)

    for i in range(4):
        root.grid_columnconfigure(i, weight=1)
        root.grid_rowconfigure(i, weight=1)

    root.grid_rowconfigure(row_val, weight=1)

    return root, entry_var, historique_listbox

# Fonction appelée lorsqu'un bouton est cliqué
def on_button_click(button_text, entry_var, historique_listbox):
    current_text = entry_var.get()

    if button_text == '=':
        calcule(current_text, entry_var, historique_listbox)
    else:
        entry_var.set(current_text + button_text)

# Point d'entrée principal
if __name__ == "__main__":
    root, entry_var, historique_listbox = create_gui()
    root.mainloop()






