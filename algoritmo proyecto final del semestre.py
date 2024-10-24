import numpy as np
from sympy import Matrix
from tkinter import Tk, Entry, Button, Text, Frame, Label
import tkinter as tk

class MatrixCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora Multifuncional de Matrices")
        self.root.geometry("1200x800")
        self.root.configure(bg='#98FF98')

        # Marco principal para la parte izquierda (entrada y botones)
        calc_frame = Frame(root, bg='#98FF98')
        calc_frame.pack(side="left", padx=10, pady=0, anchor='n')

        # Etiqueta de instrucciones
        self.instruction_label = Label(calc_frame, text="Ingrese una matriz (use comas para separar los elementos y ; para separar las filas)", bg='#98FF98', font=("Arial", 16, "bold"))
        self.instruction_label.pack(pady=10)

        # Campo de entrada de la matriz
        self.matrix_input = Entry(calc_frame, width=30, font=("Arial", 18))
        self.matrix_input.pack(pady=5)

        # Botones de operación
        Button(calc_frame, text="Gauss-Jordan", command=self.gauss_jordan, width=30, height=3, font=("Arial", 16, "bold"), bg='blue', fg='white').pack(pady=15)
        Button(calc_frame, text="Regla de Cramer", command=self.cramer, width=30, height=3, font=("Arial", 16, "bold"), bg='blue', fg='white').pack(pady=15)
        Button(calc_frame, text="Multiplicación de Matrices", command=self.multiplicar, width=30, height=3, font=("Arial", 16, "bold"), bg='blue', fg='white').pack(pady=15)
        Button(calc_frame, text="Matriz Inversa", command=self.inversa, width=30, height=3, font=("Arial", 16, "bold"), bg='blue', fg='white').pack(pady=15)

        # Marco para el área de resultados
        result_frame = Frame(root, bg='#98FF98')
        result_frame.pack(side="left", padx=10, pady=0, anchor='n')

        # Etiqueta de resultados
        result_label = Label(result_frame, text="Resultado", bg='#98FF98', font=("Arial", 18, "bold"), fg='black')
        result_label.pack(pady=10)

        # Área de texto para mostrar resultados
        self.result_text = Text(result_frame, wrap="word", width=40, height=20, font=("Courier", 20, "bold"), bg='#f0f0f0', fg='black', relief="flat")
        self.result_text.pack(pady=5, fill="both", expand=True)

    def get_matrix(self):
        try:
            # Obtener la matriz de la entrada del usuario
            rows = self.matrix_input.get().split(';')
            matrix = [list(map(float, row.split(','))) for row in rows]
            if len(matrix) > 5 or any(len(row) > 5 for row in matrix):
                raise ValueError("Se permiten matrices de hasta 5x5.")
            return np.array(matrix)
        except ValueError as e:
            self.result_text.delete(1.0, "end")
            self.result_text.insert("end", f"Error: {e}")
            return None
        except Exception as e:
            self.result_text.delete(1.0, "end")
            self.result_text.insert("end", f"Error en los datos de entrada: {e}")
            return None

    def format_matrix(self, matrix):
        """Convierte los valores flotantes cercanos a enteros en enteros para eliminar los .0000"""
        formatted_matrix = []
        for row in matrix:
            formatted_row = []
            for el in row:
                if abs(el - round(el)) < 1e-9:
                    formatted_row.append(int(round(el)))
                else:
                    formatted_row.append(round(el, 2))
            formatted_matrix.append(formatted_row)
        return formatted_matrix

    def gauss_jordan(self):
        matrix = self.get_matrix()
        if matrix is not None:
            try:
                self.result_text.delete(1.0, "end")
                self.result_text.insert("end", f"Paso 1: Matriz original:\n{self.format_matrix(matrix.tolist())}\n\n")
                
                m = Matrix(matrix)
                result, pivot_indices = m.rref()  # Calcular la matriz reducida por filas y los pivotes
                
                self.result_text.insert("end", "Paso 2: Aplicamos operaciones elementales para reducir la matriz:\n")
                for idx, pivot in enumerate(pivot_indices):
                    self.result_text.insert("end", f"Operación {idx + 1}: Se hace pivot en la columna {pivot + 1}\n")
                
                self.result_text.insert("end", f"Resultado final (forma escalonada):\n{self.format_matrix(result.tolist())}\n")
            except Exception as e:
                self.result_text.delete(1.0, "end")
                self.result_text.insert("end", f"Error al calcular Gauss-Jordan: {e}")

    def cramer(self):
        matrix = self.get_matrix()
        if matrix is not None:
            try:
                self.result_text.delete(1.0, "end")
                
                # Verificamos que sea un sistema cuadrado
                if matrix.shape[0] != matrix.shape[1] - 1:
                    self.result_text.insert("end", "La matriz no tiene la forma adecuada para aplicar la regla de Cramer (debe ser una matriz cuadrada aumentada).\n")
                    return
                
                m = Matrix(matrix[:, :-1])  # Coeficientes (sin términos independientes)
                det = m.det()  # Determinante de la matriz de coeficientes
                self.result_text.insert("end", f"Paso 1: Calculamos el determinante de la matriz de coeficientes:\nDeterminante = {det}\n\n")

                if det == 0:
                    self.result_text.insert("end", "El sistema no tiene solución única porque el determinante es 0.\n")
                else:
                    b = Matrix(matrix[:, -1])  # Términos independientes
                    solution = []
                    for i in range(m.shape[1]):
                        mi = m.copy()
                        mi[:, i] = b  # Reemplazamos la columna i por los términos independientes
                        det_mi = mi.det()  # Determinante de la nueva matriz
                        self.result_text.insert("end", f"Paso 2.{i+1}: Reemplazamos la columna {i+1} por los términos independientes y calculamos el nuevo determinante:\nDeterminante = {det_mi}\n\n")
                        solution.append(det_mi / det)
                    
                    self.result_text.insert("end", f"Solución final del sistema:\n{solution}\n")
            except Exception as e:
                self.result_text.delete(1.0, "end")
                self.result_text.insert("end", f"Error al calcular la regla de Cramer: {e}")

    def multiplicar(self):
        matrix = self.get_matrix()
        if matrix is not None:
            try:
                self.result_text.delete(1.0, "end")
                self.result_text.insert("end", "Paso 1: Seleccionamos las dos matrices a multiplicar (en este caso la matriz consigo misma):\n\n")
                self.result_text.insert("end", f"{self.format_matrix(matrix.tolist())}\n\n")
                
                self.result_text.insert("end", "Paso 2: Aplicamos la fórmula de multiplicación de matrices: A(i,j) = sumatoria de los productos de los elementos de la fila i de la primera matriz con los de la columna j de la segunda matriz.\n\n")

                rows, cols = matrix.shape
                result = np.zeros((rows, cols))
                for i in range(rows):
                    for j in range(cols):
                        row_values = matrix[i, :]
                        col_values = matrix[:, j]
                        element_result = np.dot(row_values, col_values)
                        self.result_text.insert("end", f"Elemento ({i+1},{j+1}): Producto de la fila {i+1} y la columna {j+1}: {row_values.tolist()} * {col_values.tolist()} = {element_result}\n")
                        result[i, j] = element_result
                
                formatted_result = self.format_matrix(result)
                self.result_text.insert("end", f"\nResultado de la multiplicación:\n{formatted_result}\n")
            except Exception as e:
                self.result_text.delete(1.0, "end")
                self.result_text.insert("end", f"Error al multiplicar matrices: {e}")

    def inversa(self):
        matrix = self.get_matrix()
        if matrix is not None:
            try:
                self.result_text.delete(1.0, "end")
                self.result_text.insert("end", "Paso 1: Calculamos el determinante de la matriz:\n")
                
                m = Matrix(matrix)
                det = m.det()
                self.result_text.insert("end", f"Determinante = {det}\n\n")

                if det == 0:
                    self.result_text.insert("end", "La matriz no tiene inversa porque el determinante es 0.\n")
                else:
                    self.result_text.insert("end", "Paso 2: Aplicamos la fórmula para calcular la inversa:\n")
                    inv_matrix = m.inv()
                    self.result_text.insert("end", f"Inversa de la matriz:\n{self.format_matrix(inv_matrix.tolist())}\n")
            except Exception as e:
                self.result_text.delete(1.0, "end")
                self.result_text.insert("end", f"Error al calcular la inversa: {e}")

# Inicializar la interfaz gráfica
if __name__ == "__main__":
    root = Tk()
    calculator = MatrixCalculator(root)
    root.mainloop()
