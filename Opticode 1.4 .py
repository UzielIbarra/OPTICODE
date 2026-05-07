import tkinter as tk
from tkinter import messagebox, filedialog
import json

# ================= BACKEND =================
class Tarea:
    def __init__(self, nombre, tiempo, valor):
        self.nombre = nombre
        self.tiempo = float(tiempo)
        self.valor = float(valor)
        self.rentabilidad = self.valor / self.tiempo if self.tiempo != 0 else 0
        self.estado = "Pendiente"  # Pendiente, Completada, No completada

    def __str__(self):
        return (f"{self.nombre} | Tiempo: {self.tiempo} min | "
                f"Valor: {self.valor} | Valor/min: {self.rentabilidad:.2f}")


# ================= ALGORITMO VORAZ =================

def ordenar_tareas(tareas):
    # O(n log n) - ordena por rentabilidad descendente
    return sorted(tareas, key=lambda x: x.rentabilidad, reverse=True)


def seleccionar_tareas(tareas, tiempo_disponible):
    # O(n) - selección greedy dentro del tiempo límite
    seleccionadas = []
    tiempo_usado = 0
    valor_total = 0
    for tarea in tareas:
        if tiempo_usado + tarea.tiempo <= tiempo_disponible:
            seleccionadas.append(tarea)
            tiempo_usado += tarea.tiempo
            valor_total += tarea.valor
    return seleccionadas, tiempo_usado, valor_total


class Backend:
    def __init__(self):
        self.tareas = []
        self.tiempo_limite = 0

    def agregar_tarea(self, nombre, tiempo, valor):
        tiempo = float(tiempo)
        if self.tiempo_usado() + tiempo > self.tiempo_limite and self.tiempo_limite > 0:
            return False
        self.tareas.append(Tarea(nombre, tiempo, valor))
        return True

    def tiempo_usado(self):
        return sum(t.tiempo for t in self.tareas if t.estado != "No completada")

    def marcar_estado(self, index, estado):
        if 0 <= index < len(self.tareas):
            self.tareas[index].estado = estado

    def obtener_por_estado(self, estado):
        return [t for t in self.tareas if t.estado == estado]

    def estadisticas(self):
        total = len(self.tareas)
        tiempo = sum(t.tiempo for t in self.tareas)
        valor = sum(t.valor for t in self.tareas)
        return total, tiempo, valor

    def ejecutar_voraz(self):
        # Corre el algoritmo sobre todas las tareas con el tiempo limite definido
        tareas_ordenadas = ordenar_tareas(self.tareas)
        seleccionadas, tiempo_usado, valor_total = seleccionar_tareas(
            tareas_ordenadas, self.tiempo_limite
        )
        return tareas_ordenadas, seleccionadas, tiempo_usado, valor_total


backend = Backend()


# ================= FUNCIONES UI =================

def agregar():
    nombre = entry_nombre.get()
    tiempo = entry_tiempo.get()
    valor = entry_valor.get()

    if nombre and tiempo and valor:
        if backend.agregar_tarea(nombre, tiempo, valor):
            actualizar_listas()
            limpiar()
        else:
            messagebox.showwarning("Sin tiempo", "No tienes tiempo disponible para esta tarea")
    else:
        messagebox.showwarning("Error", "Completa todos los campos")


def marcar_completada():
    sel = lista_pendientes.curselection()
    if sel:
        tarea = backend.obtener_por_estado("Pendiente")[sel[0]]
        tarea.estado = "Completada"
        actualizar_listas()


def marcar_no_completada():
    sel = lista_pendientes.curselection()
    if sel:
        tarea = backend.obtener_por_estado("Pendiente")[sel[0]]
        tarea.estado = "No completada"
        actualizar_listas()


def actualizar_listas():
    lista_pendientes.delete(0, tk.END)
    lista_completadas.delete(0, tk.END)
    lista_no.delete(0, tk.END)

    for t in backend.obtener_por_estado("Pendiente"):
        lista_pendientes.insert(tk.END, t.nombre)

    for t in backend.obtener_por_estado("Completada"):
        lista_completadas.insert(tk.END, t.nombre)

    for t in backend.obtener_por_estado("No completada"):
        lista_no.insert(tk.END, t.nombre)

    total, tiempo, valor = backend.estadisticas()
    label_stats.config(
        text=f"Tareas: {total} | Tiempo total: {tiempo} min | Valor total: {valor} pts"
    )


def definir_tiempo():
    try:
        backend.tiempo_limite = float(entry_total.get())
        messagebox.showinfo("OK", f"Tiempo limite definido: {backend.tiempo_limite} min")
    except Exception:
        messagebox.showerror("Error", "Valor invalido")


def cargar_json():
    file = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if file:
        with open(file, "r") as f:
            data = json.load(f)
            for t in data:
                backend.tareas.append(Tarea(t["nombre"], t["tiempo"], t["valor"]))
        actualizar_listas()


def ejecutar_voraz():
    if not backend.tareas:
        messagebox.showwarning("Sin tareas", "Agrega tareas antes de calcular")
        return
    if backend.tiempo_limite == 0:
        messagebox.showwarning("Sin tiempo", "Define el tiempo limite primero")
        return

    tareas_ord, seleccionadas, tiempo_usado, valor_total = backend.ejecutar_voraz()

    # Ventana de resultados
    win = tk.Toplevel(root)
    win.title("Resultado - Algoritmo Voraz")
    win.geometry("600x500")
    win.config(bg="#0f172a")

    tk.Label(win, text="ALGORITMO VORAZ - RESULTADO", font=("Segoe UI", 14, "bold"),
             fg="#22c55e", bg="#0f172a").pack(pady=10)

    texto = tk.Text(win, bg="#1e293b", fg="white", font=("Courier", 10), height=25, width=72)
    texto.pack(padx=10, pady=5)

    texto.insert(tk.END, "TAREAS ORDENADAS POR RENTABILIDAD:\n\n")
    for t in tareas_ord:
        texto.insert(tk.END, f"  {str(t)}\n")

    texto.insert(tk.END, "\nTAREAS SELECCIONADAS (optimas):\n\n")
    for t in seleccionadas:
        texto.insert(tk.END, f"  {str(t)}\n")

    texto.insert(tk.END, f"\n--- RESUMEN ---\n")
    texto.insert(tk.END, f"Tiempo disponible : {backend.tiempo_limite} min\n")
    texto.insert(tk.END, f"Tiempo usado      : {tiempo_usado} min\n")
    texto.insert(tk.END, f"Tiempo restante   : {backend.tiempo_limite - tiempo_usado} min\n")
    texto.insert(tk.END, f"Valor total       : {valor_total} pts\n")
    texto.config(state=tk.DISABLED)


def limpiar():
    entry_nombre.delete(0, tk.END)
    entry_tiempo.delete(0, tk.END)
    entry_valor.delete(0, tk.END)


# ================= UI =================

root = tk.Tk()
root.title("OPTICODE PRO MAX")
root.geometry("1100x700")
root.config(bg="#0f172a")

tk.Label(root, text="OPTICODE PRO MAX", font=("Segoe UI", 24, "bold"),
         fg="#22c55e", bg="#0f172a").pack(pady=10)

# FORM
frame = tk.Frame(root, bg="#1e293b", padx=15, pady=10)
frame.pack(pady=5)

entry_nombre = tk.Entry(frame, width=25)
entry_tiempo = tk.Entry(frame, width=25)
entry_valor  = tk.Entry(frame, width=25)

tk.Label(frame, text="Nombre", bg="#1e293b", fg="white").grid(row=0, column=0, sticky="w")
tk.Label(frame, text="Tiempo (min)", bg="#1e293b", fg="white").grid(row=1, column=0, sticky="w")
tk.Label(frame, text="Valor/Puntaje", bg="#1e293b", fg="white").grid(row=2, column=0, sticky="w")

entry_nombre.grid(row=0, column=1, padx=8, pady=3)
entry_tiempo.grid(row=1, column=1, padx=8, pady=3)
entry_valor.grid(row=2, column=1, padx=8, pady=3)

tk.Button(frame, text="Agregar Tarea", command=agregar,
          bg="#22c55e", fg="white", width=20).grid(row=3, column=0, columnspan=2, pady=8)

# TIEMPO LIMITE
frame_tiempo = tk.Frame(root, bg="#0f172a")
frame_tiempo.pack(pady=5)

tk.Label(frame_tiempo, text="Tiempo disponible (min):", bg="#0f172a", fg="white").grid(row=0, column=0, padx=5)
entry_total = tk.Entry(frame_tiempo, width=15)
entry_total.grid(row=0, column=1, padx=5)
tk.Button(frame_tiempo, text="Definir tiempo", command=definir_tiempo,
          bg="#f59e0b", fg="white").grid(row=0, column=2, padx=5)

# BOTONES ACCION
frame_btns = tk.Frame(root, bg="#0f172a")
frame_btns.pack(pady=5)

tk.Button(frame_btns, text="Cargar JSON", command=cargar_json,
          bg="#3b82f6", fg="white", width=18).grid(row=0, column=0, padx=8)
tk.Button(frame_btns, text="Ejecutar Algoritmo Voraz", command=ejecutar_voraz,
          bg="#8b5cf6", fg="white", width=22).grid(row=0, column=1, padx=8)

# LISTAS
frame_list = tk.Frame(root, bg="#0f172a")
frame_list.pack(pady=15)

lista_pendientes  = tk.Listbox(frame_list, width=30, height=12, bg="#1e293b", fg="white")
lista_completadas = tk.Listbox(frame_list, width=30, height=12, bg="#1e293b", fg="#22c55e")
lista_no          = tk.Listbox(frame_list, width=30, height=12, bg="#1e293b", fg="#ef4444")

tk.Label(frame_list, text="Pendientes",     fg="white",   bg="#0f172a").grid(row=0, column=0)
tk.Label(frame_list, text="Completadas",    fg="#22c55e", bg="#0f172a").grid(row=0, column=1)
tk.Label(frame_list, text="No completadas", fg="#ef4444", bg="#0f172a").grid(row=0, column=2)

lista_pendientes.grid(row=1, column=0, padx=5)
lista_completadas.grid(row=1, column=1, padx=5)
lista_no.grid(row=1, column=2, padx=5)

# BOTONES ESTADO
frame_est = tk.Frame(root, bg="#0f172a")
frame_est.pack(pady=5)
tk.Button(frame_est, text="Completar",    command=marcar_completada,    bg="#22c55e", fg="white", width=18).grid(row=0, column=0, padx=10)
tk.Button(frame_est, text="No completar", command=marcar_no_completada, bg="#ef4444", fg="white", width=18).grid(row=0, column=1, padx=10)

# STATS
label_stats = tk.Label(root, text="Tareas: 0 | Tiempo total: 0 min | Valor total: 0 pts",
                        fg="#94a3b8", bg="#0f172a", font=("Segoe UI", 10))
label_stats.pack(pady=8)

root.mainloop()