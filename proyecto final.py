import numpy as np
from sympy import Matrix
from tkinter import Tk, Entry, Button, Text, Frame, Label

import tkinter as tk

class MatrixCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora Multifuncional de Matrices")
        self.root.geometry("1600x1000")  # Ajustamos el ancho a un valor más razonable
        self.root.configure(bg='#a8d5a2')

        # Frame principal para la parte izquierda (entrada y botones)
        calc_frame = Frame(root, bg='#a8d5a2')
        calc_frame.pack(side="left", padx=10, pady=0, anchor='n')

        # Etiqueta de instrucciones
        self.instruction_label = Label(calc_frame, text="Ingrese 4 números separados por comas", bg='#a8d5a2', font=("Arial", 16, "bold"))
        self.instruction_label.pack(pady=10)

        # Campo de entrada de la matriz
        self.matrix_input = Entry(calc_frame, width=30, font=("Arial", 18))
        self.matrix_input.pack(pady=5)

        # Botones de operaciones con mayor separación (pady=15)
        Button(calc_frame, text="Gauss-Jordan", command=self.gauss_jordan, width=30, height=3, font=("Arial", 16, "bold"), bg='blue', fg='white').pack(pady=15)
        Button(calc_frame, text="Regla de Cramer", command=self.cramer, width=30, height=3, font=("Arial", 16, "bold"), bg='blue', fg='white').pack(pady=15)
        Button(calc_frame, text="Multiplicación de Matrices", command=self.multiplicar, width=30, height=3, font=("Arial", 16, "bold"), bg='blue', fg='white').pack(pady=15)
        Button(calc_frame, text="Matriz Inversa", command=self.inversa, width=30, height=3, font=("Arial", 16, "bold"), bg='blue', fg='white').pack(pady=15)

        # Frame para el área de resultados
        result_frame = Frame(root, bg='#a8d5a2')
        result_frame.pack(side="left", padx=10, pady=0, anchor='n')

        # Etiqueta de resultados
        result_label = Label(result_frame, text="Resultado", bg='#a8d5a2', font=("Arial", 18, "bold"), fg='black')
        result_label.pack(pady=10)

        # Área de texto para mostrar resultados
        self.result_text = Text(result_frame, wrap="word", width=40, height=35, font=("Arial", 16), bg='#a8d5a2', relief="flat")
        self.result_text.pack(pady=5, fill="both", expand=True)

        # Nueva sección de texto con alineación a la izquierda para evitar cortes
        description_frame = Frame(root, bg='#a8d5a2')
        description_frame.pack(side="right", padx=20, pady=0, anchor='n')

        # Crear etiquetas para los títulos y párrafos, con justificación a la izquierda y wraplength ajustado
        self.add_description(description_frame, "Gauss-Jordan:", 
                             "El método de Gauss-Jordan se usa para resolver sistemas de \n"
                             "ecuaciones lineales, encontrar la inversa de una matriz,\n"
                             "o comprobar si un sistema es consistente. Además, muestra\n"
                             "la matriz resultante en su forma escalonada, lo que facilita \n"
                             "la resolución de sistemas de ecuaciones lineales.")
        
        self.add_description(description_frame, "Regla de Cramer:", 
                             "La regla de Cramer es un método para resolver sistemas de \n"
                             "ecuaciones lineales con tantas ecuaciones como incógnitas,\n"
                             "usando determinantes. El determinante también es útil para \n"
                             "verificar si una matriz es invertible y debería mostrar el valor \n"
                             "del determinante de la matriz en el área de resultados.")
        
        self.add_description(description_frame, "Multiplicación de matrices:", 
                             "La multiplicación de matrices es fundamental en álgebra lineal \n"
                             "para diversas aplicaciones, como la transformación de \n"
                             "coordenadas, la resolución de ecuaciones lineales y el \n"
                             "modelado en física o ingeniería. Debería mostrar el producto \n"
                             "de la multiplicación de la matriz en el área de resultados.")
        
        self.add_description(description_frame, "Matriz inversa:", 
                             "La matriz inversa es esencial en la resolución de sistemas de \n"
                             "ecuaciones lineales y en muchos problemas de álgebra lineal.\n"
                             "Solo matrices cuadradas y no singulares (aquellas cuyo \n"
                             "determinante no es cero) tienen inversa y debería mostrar la \n"
                             "matriz inversa en el área de resultados o indicar si la matriz \n"
                             "no es invertible.")

    def add_description(self, frame, title, text):
        """Añadir un título y un texto con justificación a la izquierda"""
        # Título centrado
        title_label = tk.Label(frame, text=title, font=("Arial", 14, "bold"), bg='#a8d5a2', anchor="center")
        title_label.pack(padx=10, pady=10)

        # Texto justificado a la izquierda con wraplength ajustado a 600 píxeles
        text_label = tk.Label(frame, text=text, justify="left", wraplength=600, bg='#a8d5a2', font=("Arial", 12), anchor="w")
        text_label.pack(padx=10, pady=0)

    def get_matrix(self):
        try:
            elements = list(map(float, self.matrix_input.get().split(',')))
            n = int(len(elements) ** 0.5)
            return np.array(elements).reshape(n, n)
        except ValueError:
            self.result_text.delete(1.0, "end")
            self.result_text.insert("end", "Error: Asegúrese de que todos los valores sean números y estén separados por comas.")
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
                if abs(el - round(el)) < 1e-9:  # Si la diferencia es muy pequeña, lo redondeamos
                    formatted_row.append(int(round(el)))
                else:
                    formatted_row.append(round(el, 2))  # Redondeamos a 2 decimales si no es entero
            formatted_matrix.append(formatted_row)
        return formatted_matrix

    def gauss_jordan(self):
        matrix = self.get_matrix()
        if matrix is not None:
            try:
                m = Matrix(matrix)
                result = m.rref()[0]

                # Convertir los valores cercanos a enteros y redondear
                result_list = self.format_matrix(result.tolist())

                self.result_text.delete(1.0, "end")
                self.result_text.insert("end", f"Matriz en forma escalonada:\n{result_list}")
            except Exception as e:
                self.result_text.delete(1.0, "end")
                self.result_text.insert("end", f"Error calculando Gauss-Jordan: {e}")

    def cramer(self):
        matrix = self.get_matrix()
        if matrix is not None:
            try:
                m = Matrix(matrix)
                det = m.det()
                self.result_text.delete(1.0, "end")
                self.result_text.insert("end", f"Determinante: {int(det)}")
            except Exception as e:
                self.result_text.delete(1.0, "end")
                self.result_text.insert("end", f"Error calculando Regla de Cramer: {e}")

    def multiplicar(self):
        matrix = self.get_matrix()
        if matrix is not None:
            try:
                result = np.dot(matrix, matrix).astype(int)
                self.result_text.delete(1.0, "end")
                self.result_text.insert("end", f"Multiplicación de matrices:\n{result}")
            except Exception as e:
                self.result_text.delete(1.0, "end")
                self.result_text.insert("end", f"Error multiplicando matrices: {e}")

    def inversa(self):
        matrix = self.get_matrix()
        if matrix is not None:
            try:
                inv_matrix = np.linalg.inv(matrix).astype(float)
                # Convertir los valores cercanos a enteros y redondear
                inv_matrix_list = self.format_matrix(inv_matrix.tolist())

                self.result_text.delete(1.0, "end")
                self.result_text.insert("end", f"Matriz Inversa:\n{inv_matrix_list}")
            except np.linalg.LinAlgError:
                self.result_text.delete(1.0, "end")
                self.result_text.insert("end", "La matriz no es invertible.")
            except Exception as e:
                self.result_text.delete(1.0, "end")
                self.result_text.insert("end", f"Error calculando inversa: {e}")

# Configuración de la ventana principal
root = Tk()
app = MatrixCalculator(root)
root.mainloop()

