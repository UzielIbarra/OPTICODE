# Opticode 1.2
import tkinter as tk

class Tarea:
    def __init__(self, nombre, tiempo, valor):
        self.nombre = nombre
        self.tiempo = tiempo
        self.valor = valor
        self.rentabilidad = valor / tiempo if tiempo != 0 else 0

    def __str__(self):
        return f"{self.nombre} | Tiempo: {self.tiempo} min | Valor: {self.valor} | Valor/min: {self.rentabilidad:.2f}"


def ordenar_tareas(tareas):
    return sorted(tareas, key=lambda x: x.rentabilidad, reverse=True)


def seleccionar_tareas(tareas, tiempo_disponible):
    seleccionadas = []
    tiempo_usado = 0
    valor_total = 0
    for tarea in tareas:
        if tiempo_usado + tarea.tiempo <= tiempo_disponible:
            seleccionadas.append(tarea)
            tiempo_usado += tarea.tiempo
            valor_total += tarea.valor
    return seleccionadas, tiempo_usado, valor_total


class OpticodeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("OPTICODE")
        self.root.geometry("600x500")
        self.tareas = []
        
        # Titulo
        titulo = tk.Label(root, text="OPTICODE - Organizador de Tareas", font=("Arial", 14, "bold"))
        titulo.pack(pady=10)
        
        # Entrada de nombre
        tk.Label(root, text="Nombre tarea:").pack()
        self.entrada_nombre = tk.Entry(root, width=30)
        self.entrada_nombre.pack(pady=5)
        
        # Entrada de tiempo
        tk.Label(root, text="Tiempo (min):").pack()
        self.entrada_tiempo = tk.Entry(root, width=30)
        self.entrada_tiempo.pack(pady=5)
        
        # Entrada de valor
        tk.Label(root, text="Valor/Puntaje:").pack()
        self.entrada_valor = tk.Entry(root, width=30)
        self.entrada_valor.pack(pady=5)
        
        # Boton agregar tarea
        tk.Button(root, text="Agregar Tarea", command=self.agregar_tarea).pack(pady=10)
        
        # Entrada tiempo disponible
        tk.Label(root, text="Tiempo disponible (min):").pack()
        self.entrada_tiempo_disponible = tk.Entry(root, width=30)
        self.entrada_tiempo_disponible.pack(pady=5)
        
        # Boton calcular
        tk.Button(root, text="Calcular", command=self.calcular).pack(pady=10)
        
        # Area de texto para resultados
        tk.Label(root, text="Resultados:").pack()
        self.texto_resultados = tk.Text(root, height=15, width=70)
        self.texto_resultados.pack(pady=10)
        
    def agregar_tarea(self):
        nombre = self.entrada_nombre.get()
        tiempo = float(self.entrada_tiempo.get())
        valor = float(self.entrada_valor.get())
        
        self.tareas.append(Tarea(nombre, tiempo, valor))
        
        self.entrada_nombre.delete(0, tk.END)
        self.entrada_tiempo.delete(0, tk.END)
        self.entrada_valor.delete(0, tk.END)
        
        self.texto_resultados.delete(1.0, tk.END)
        self.texto_resultados.insert(tk.END, f"Tarea '{nombre}' agregada!\n")
    
    def calcular(self):
        tiempo_disponible = float(self.entrada_tiempo_disponible.get())
        
        self.texto_resultados.delete(1.0, tk.END)
        
        tareas_ordenadas = ordenar_tareas(self.tareas)
        seleccionadas, tiempo_usado, valor_total = seleccionar_tareas(tareas_ordenadas, tiempo_disponible)
        
        self.texto_resultados.insert(tk.END, "TAREAS ORDENADAS:\n\n")
        for t in tareas_ordenadas:
            self.texto_resultados.insert(tk.END, str(t) + "\n")
        
        self.texto_resultados.insert(tk.END, "\nTAREAS SELECCIONADAS:\n\n")
        for t in seleccionadas:
            self.texto_resultados.insert(tk.END, str(t) + "\n")
        
        self.texto_resultados.insert(tk.END, f"\n--- RESUMEN ---\n")
        self.texto_resultados.insert(tk.END, f"Tiempo disponible: {tiempo_disponible} min\n")
        self.texto_resultados.insert(tk.END, f"Tiempo usado: {tiempo_usado} min\n")
        self.texto_resultados.insert(tk.END, f"Tiempo restante: {tiempo_disponible - tiempo_usado} min\n")
        self.texto_resultados.insert(tk.END, f"Valor total: {valor_total} pts\n")


if __name__ == "__main__":
    root = tk.Tk()
    app = OpticodeApp(root)
    root.mainloop()