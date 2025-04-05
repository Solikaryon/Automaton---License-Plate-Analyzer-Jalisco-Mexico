""" 
Autores:
    Monjaraz Briseño Luis Fernando
    Huerta Gómez Ethan Antonio

Teoría de la Computación
Nombre del docente: Gómez Andrade Abelardo
"""
import tkinter as tk 
from tkinter import messagebox
import numpy as np

# Definimos el alfabeto y los estados
ALPHABET = {
    'J': 0, 'A': 1, 'L': 2, '-': 3,
    '0': 4, '1': 5, '2': 6, '3': 7, '4': 8, '5': 9,
    '6': 10, '7': 11, '8': 12, '9': 13
}
for char in "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ":
    if char not in ALPHABET:
        ALPHABET[char] = len(ALPHABET)

STATES = {
    'q0': 0, 'q1': 1, 'q2': 2, 'q3': 3, 'q4': 4,
    'q5': 5, 'q6': 6, 'q7': 7, 'q8': 8,
    'q9': 9, 'q10': 10, 'q11': 11, 'q12': 12, 'q13': 13
}

class PlateValidator:
    def __init__(self, final_state, transitions):
        self.current_state = STATES['q0']
        self.final_state = final_state
        self.transitions = transitions

    def reset(self):
        self.current_state = STATES['q0']
    
    def process_char(self, char):
        if char in ALPHABET:
            next_state = self.transitions[self.current_state, ALPHABET[char]]
            if next_state != -1:
                self.current_state = next_state
                return True
        return False
    
    def is_accepted(self):
        return self.current_state == self.final_state

def setup_transitions():
    transition_matrix_format1 = -np.ones((14, len(ALPHABET)), dtype=int)
    transition_matrix_format2 = -np.ones((14, len(ALPHABET)), dtype=int)

    # Transiciones iniciales para "JXX-"
    for trans_matrix in [transition_matrix_format1, transition_matrix_format2]:
        trans_matrix[STATES['q0'], ALPHABET['J']] = STATES['q1']
        for char in ALPHABET:
            if char not in {'J', '-', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}:
                trans_matrix[STATES['q1'], ALPHABET[char]] = STATES['q2']
                trans_matrix[STATES['q2'], ALPHABET[char]] = STATES['q3']
        trans_matrix[STATES['q3'], ALPHABET['-']] = STATES['q4']

    # Transiciones para el formato "JXX-00-00" (con guion intermedio)
    for i in range(4, 14):  # dígitos '0' a '9'
        transition_matrix_format1[STATES['q4'], i] = STATES['q9']  # Primer dígito del primer bloque
        transition_matrix_format1[STATES['q9'], i] = STATES['q10']  # Segundo dígito del primer bloque
    transition_matrix_format1[STATES['q10'], ALPHABET['-']] = STATES['q11']  # Guion después del primer bloque de dígitos
    for i in range(4, 14):  # dígitos '0' a '9'
        transition_matrix_format1[STATES['q11'], i] = STATES['q12']  # Primer dígito del segundo bloque
        transition_matrix_format1[STATES['q12'], i] = STATES['q13']  # Segundo dígito del segundo bloque (estado final q13)

    # Transiciones para el formato "JXX-0000" (sin guion intermedio)
    for i in range(4, 14):  # dígitos '0' a '9'
        transition_matrix_format2[STATES['q4'], i] = STATES['q5']   # Primer dígito del bloque de cuatro dígitos
        transition_matrix_format2[STATES['q5'], i] = STATES['q6']  # Segundo dígito
        transition_matrix_format2[STATES['q6'], i] = STATES['q7'] # Tercer dígito
        transition_matrix_format2[STATES['q7'], i] = STATES['q8'] # Cuarto dígito (estado final q8)

    return transition_matrix_format1, transition_matrix_format2

def is_valid_plate(plate):
    # Configura las transiciones para ambos formatos
    transition_matrix_format1, transition_matrix_format2 = setup_transitions()

    # Crea validadores de matrícula para ambos formatos
    validator_format1 = PlateValidator(final_state=STATES['q13'], transitions=transition_matrix_format1)
    validator_format2 = PlateValidator(final_state=STATES['q8'], transitions=transition_matrix_format2)

    last_valid_state_format1 = validator_format1.current_state
    last_valid_state_format2 = validator_format2.current_state

    for index, char in enumerate(plate):
        # Procesa el carácter en ambos validadores
        valid_format1 = validator_format1.process_char(char)
        valid_format2 = validator_format2.process_char(char)

        # Rastrea el último estado válido antes de fallar
        if valid_format1:
            last_valid_state_format1 = validator_format1.current_state
        if valid_format2:
            last_valid_state_format2 = validator_format2.current_state

        # Si ambos caminos fallan, identifica el fallo
        if not valid_format1 and not valid_format2:
            error_message = (
                f"Rechazado en estado q{last_valid_state_format1} (formato 1) "
                f"y estado q{last_valid_state_format2} (formato 2) "
                f"con carácter '{char}'."
            )
            return False, error_message

    # Verifica si alguno de los validadores está en su estado final
    if validator_format1.is_accepted():
        return True, "Aceptado en formato 1."
    elif validator_format2.is_accepted():
        return True, "Aceptado en formato 2."
    else:
        # Si ambos fallan, identifica los estados finales en los que quedaron
        error_message = (
            f"Rechazado: no se alcanzó un estado final. "
            f"Últimos estados: q{validator_format1.current_state} (formato 1), "
            f"q{validator_format2.current_state} (formato 2)."
        )
        return False, error_message


# Interfaz gráfica en Tkinter
class PlateValidatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Validador de Matrículas")
        self.root.geometry("500x300")
        self.root.configure(bg="black")

        # Campo de entrada para la cadena a evaluar
        tk.Label(root, text="Cadena a evaluar", bg="black", fg="white").place(x=30, y=20)
        self.entry_plate = tk.Entry(root, width=20)
        self.entry_plate.place(x=150, y=20)

        # Etiquetas para mostrar el resultado de aceptación/rechazo
        self.label_result = tk.Label(root, text="Cadena: Rechazada/Aceptada", bg="black", fg="white")
        self.label_result.place(x=30, y=60)

        self.label_reason = tk.Label(root, text="Por qué fue rechazada", bg="black", fg="white")
        self.label_reason.place(x=30, y=90)

        # Botones de acción
        self.button_show_table = tk.Button(root, text="Mostrar tabla de transiciones", bg="yellow", command=self.show_table)
        self.button_show_table.place(x=30, y=200, width=150, height=30)

        self.button_reset = tk.Button(root, text="Reiniciar", bg="yellow", command=self.reset)
        self.button_reset.place(x=200, y=200, width=70, height=30)

        self.button_evaluate = tk.Button(root, text="Evaluar", bg="yellow", command=self.evaluate)
        self.button_evaluate.place(x=280, y=200, width=70, height=30)

        self.button_exit = tk.Button(root, text="Salir", bg="yellow", command=root.quit)
        self.button_exit.place(x=360, y=200, width=70, height=30)

    def show_table(self): 
        # Crear una nueva ventana para la tabla de transiciones
        table_window = tk.Toplevel(self.root)
        table_window.title("Tabla de Transiciones")
        table_window.geometry("800x600")
        table_window.configure(bg="white")
        tk.Label(table_window, text="Estado inicio AZUL", bg="blue", fg="white", borderwidth=1, relief="solid", width=20).grid(row=0, column=0, columnspan=3, padx=5, pady=5)
        tk.Label(table_window, text="Estado Final ROJO", bg="red", fg="white", borderwidth=1, relief="solid", width=20).grid(row=0, column=3, columnspan=3, padx=5, pady=5)

        # Encabezados de la tabla
        headers = ['J', 'A...Z', 'A...Z', '-'] + [str(i) for i in range(10)]
        states = ['q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9', 'q10', 'q11', 'q12', 'q13']
        transitions = [
            #  J  A-Z    L    -    0    1    2    3    4    5    6    7    8    9
            ['q1', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', 'q2', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', 'q3', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', 'q4', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', 'q5 q9', 'q5 q9', 'q5 q9', 'q5 q9', 'q5 q9', 'q5 q9', 'q5 q9', 'q5 q9', 'q5 q9', 'q5 q9'],
            ['-', '-', '-', '-', 'q6', 'q6', 'q6', 'q6', 'q6', 'q6', 'q6', 'q6', 'q6', 'q6'],
            ['-', '-', '-', '-', 'q7', 'q7', 'q7', 'q7', 'q7', 'q7', 'q7', 'q7', 'q7', 'q7'],
            ['-', '-', '-', '-', 'q8', 'q8', 'q8', 'q8', 'q8', 'q8', 'q8', 'q8', 'q8', 'q8'],
            ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', 'q10', 'q10', 'q10', 'q10', 'q10', 'q10', 'q10', 'q10', 'q10', 'q10'],
            ['-', '-', '-', 'q11', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', 'q12', 'q12', 'q12', 'q12', 'q12', 'q12', 'q12', 'q12', 'q12', 'q12'],
            ['-', '-', '-', '-', 'q13', 'q13', 'q13', 'q13', 'q13', 'q13', 'q13', 'q13', 'q13', 'q13'],
            ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-']
        ]

        # Colocar encabezados en la primera fila
        tk.Label(table_window, text="Estados", bg="black", fg="white", borderwidth=1, relief="solid", width=10).grid(row=0, column=0)
        for j, header in enumerate(headers):
            tk.Label(table_window, text=header, bg="black", fg="white", borderwidth=1, relief="solid", width=10).grid(row=0, column=j+1)

        # Colocar los estados en la primera columna con colores específicos para algunos
        for i, state in enumerate(states):
            # Configurar color de fondo para los estados específicos
            if state == 'q0':
                bg_color = "blue"
            elif state in ['q8', 'q13']:
                bg_color = "red"
            else:
                bg_color = "black"

            fg_color = "white"  # Color de texto en blanco para contrastar

            # Estado en la primera columna
            tk.Label(table_window, text=state, bg=bg_color, fg=fg_color, borderwidth=1, relief="solid", width=10).grid(row=i+1, column=0)
            
            # Colocar transiciones en el resto de las celdas
            for j, transition in enumerate(transitions[i]):
                # Celdas de transiciones
                tk.Label(table_window, text=transition, borderwidth=1, relief="solid", width=10, height=2).grid(row=i+1, column=j+1)

        # Configurar el redimensionamiento de las celdas al ajustar el tamaño de la ventana
        for i in range(len(states) + 1):
            table_window.grid_rowconfigure(i, weight=1)
            table_window.grid_columnconfigure(i, weight=1)

    def reset(self):
        # Limpia el campo de entrada y las etiquetas de resultados
        self.entry_plate.delete(0, tk.END)
        self.label_result.config(text="Cadena: Rechazada/Aceptada")
        self.label_reason.config(text="Por qué fue rechazada")

    # Modifica la función `evaluate` en la GUI para mostrar el mensaje completo
    def evaluate(self):
        plate = self.entry_plate.get()
        if len(plate) < 7:
            self.label_result.config(text="Cadena: Rechazada")
            self.label_reason.config(text="Error: La cadena es demasiado corta.")
            return

        is_valid, message = is_valid_plate(plate)
        if is_valid:
            self.label_result.config(text="Cadena: Aceptada")
            self.label_reason.config(text=f"Detalle: {message}")
        else:
            self.label_result.config(text="Cadena: Rechazada")
            self.label_reason.config(text=f"Detalle: {message}")

# Configuración de la interfaz principal
if __name__ == "__main__":
    root = tk.Tk()
    app = PlateValidatorGUI(root)
    root.mainloop()
