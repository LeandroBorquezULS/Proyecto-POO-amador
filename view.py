"""
view.py (Modificado)
"""
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime
import threading

from controller import AppController

class InterfazAmador(tk.Frame):
    def __init__(self, root: tk.Tk, controller: AppController):
        super().__init__(root)
        self.root = root
        self.controller = controller
        self.root.title("Asistente Personal - Amador")
        self.root.geometry("600x750")
        self.root.configure(bg="#E6F2F5")

        self.estilo = ttk.Style()
        self.estilo.theme_use('clam')
        self.estilo.configure("Clock.TLabel", font=("Arial", 30, "bold"), background="#E6F2F5", foreground="#34495E")

        self.tareas = self.controller.cargar_tareas()

        # --- UI Setup ---
        self.frame_top = tk.Frame(root, bg="#E6F2F5")
        self.frame_top.pack(fill="x", pady=10)

        self.lbl_reloj = ttk.Label(self.frame_top, text="00:00", style="Clock.TLabel")
        self.lbl_reloj.pack()
        self.actualizar_reloj()

        tk.Label(self.frame_top, text="Hola Amador, hoy es un gran día.",
                 font=("Verdana", 14), bg="#E6F2F5", fg="#7F8C8D").pack()

        self.frame_progreso = tk.Frame(root, bg="#E6F2F5")
        self.frame_progreso.pack(fill="x", padx=20, pady=5)
        self.barra = ttk.Progressbar(self.frame_progreso, orient="horizontal", length=100, mode="determinate")
        self.barra.pack(fill="x")

        self.canvas = tk.Canvas(root, bg="#E6F2F5", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#E6F2F5")

        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="top", fill="both", expand=True, padx=10)
        self.scrollbar.pack(side="right", fill="y")

        self.renderizar_tareas()

        self.frame_bottom = tk.Frame(root, bg="#2C3E50", height=80)
        self.frame_bottom.pack(fill="x", side="bottom")

        # --- BOTÓN AYUDA (MODIFICADO: Sin confirmación) ---
        btn_ayuda = tk.Button(self.frame_bottom, text="🆘 NECESITO AYUDA",
                              font=("Arial", 14, "bold"), bg="#C0392B", fg="white",
                              command=self.accion_ayuda_inmediata)
        btn_ayuda.pack(side="left", padx=20, pady=10, fill="x", expand=True)

        btn_admin = tk.Button(self.frame_bottom, text="⚙ Familia",
                              font=("Arial", 10), bg="#34495E", fg="white",
                              command=self.solicitar_acceso_familia)
        btn_admin.pack(side="right", padx=10, pady=10)

    # ----- UI Helpers -----
    def actualizar_reloj(self) -> None:
        ahora = datetime.now().strftime("%H:%M:%S")
        self.lbl_reloj.config(text=ahora)
        self.root.after(1000, self.actualizar_reloj)

    def renderizar_tareas(self) -> None:
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        completadas = 0
        total = len(self.tareas)

        for idx, tarea in enumerate(self.tareas):
            if tarea.estado == "Completado":
                completadas += 1
                bg_color, fg_color, txt = "#D5F5E3", "#1E8449", "✓ LISTO"
            else:
                bg_color, fg_color, txt = "white", "black", "Pendiente"

            card = tk.Frame(self.scrollable_frame, bg=bg_color, bd=1, relief="solid")
            card.pack(fill="x", pady=8, padx=5, ipady=10)

            tk.Label(card, text=tarea.get_descripcion_visual(),
                     font=("Arial", 16), bg=bg_color, fg=fg_color, justify="left").pack(side="left", padx=15)

            if tarea.estado == "Pendiente":
                tk.Button(card, text="Ya lo hice", bg="#2980B9", fg="white", font=("Arial", 12, "bold"),
                          command=lambda i=idx: self.marcar_completado(i)).pack(side="right", padx=15)
            else:
                tk.Label(card, text=txt, font=("Arial", 12, "bold"), bg=bg_color, fg=fg_color).pack(side="right", padx=15)

        self.barra["value"] = (completadas / total) * 100 if total > 0 else 0

    def marcar_completado(self, indice: int) -> None:
        self.controller.marcar_completado(indice)
        self.tareas = self.controller.cargar_tareas()
        self.renderizar_tareas()

    # ----- LÓGICA AYUDA INMEDIATA (MODIFICADO) -----
    def accion_ayuda_inmediata(self) -> None:
        """Envía alerta a todos los contactos SIN PREGUNTAR NADA."""
        # Se ejecuta en un hilo para no congelar la UI mientras se abren las pestañas
        threading.Thread(target=self.controller.enviar_alerta_masiva, daemon=True).start()
        
        # Feedback visual simple de que algo pasó
        messagebox.showinfo("ALERTA ENVIADA", "Se está enviando el mensaje de ayuda a tus contactos de emergencia.")

    # ----- Administración (Panel Familia) -----
    def solicitar_acceso_familia(self) -> None:
        pwd = simpledialog.askstring("Acceso Familia", "Ingrese contraseña:", show='*')
        if pwd is None: return
        if self.controller.verificar_contrasena(pwd):
            self.abrir_panel_familia()
        else:
            messagebox.showerror("Error", "Contraseña incorrecta")

    def abrir_panel_familia(self) -> None:
        """
        Ventana unificada: Arriba agrega tareas, Abajo gestiona contactos.
        """
        ventana = tk.Toplevel(self.root)
        ventana.title("Panel de Familia")
        ventana.geometry("400x600")

        # --- SECCIÓN 1: AGREGAR TAREAS ---
        frame_tareas = tk.LabelFrame(ventana, text="1. Programar Nueva Tarea", font=("Arial", 10, "bold"), padx=10, pady=10)
        frame_tareas.pack(fill="x", padx=10, pady=10)

        tk.Label(frame_tareas, text="Nombre:").pack(anchor="w")
        entry_nombre = tk.Entry(frame_tareas); entry_nombre.pack(fill="x")

        tk.Label(frame_tareas, text="Hora (HH:MM):").pack(anchor="w")
        entry_hora = tk.Entry(frame_tareas); entry_hora.pack(fill="x")

        tk.Label(frame_tareas, text="Extra (Dosis/Ubicación):").pack(anchor="w")
        entry_extra = tk.Entry(frame_tareas); entry_extra.pack(fill="x")

        tipo_var = tk.StringVar(value="Medicamento")
        frame_radios = tk.Frame(frame_tareas); frame_radios.pack(anchor="w", pady=5)
        tk.Radiobutton(frame_radios, text="Medicamento", variable=tipo_var, value="Medicamento").pack(side="left")
        tk.Radiobutton(frame_radios, text="Seguridad", variable=tipo_var, value="Seguridad").pack(side="left", padx=10)

        def guardar_tarea():
            if not entry_nombre.get(): return
            if tipo_var.get() == "Medicamento":
                self.controller.agregar_tarea_medicamento(entry_nombre.get(), entry_hora.get(), entry_extra.get())
            else:
                self.controller.agregar_tarea_seguridad(entry_nombre.get(), entry_hora.get(), entry_extra.get())
            entry_nombre.delete(0, 'end'); entry_hora.delete(0, 'end'); entry_extra.delete(0, 'end')
            self.tareas = self.controller.cargar_tareas() # Refrescar
            self.renderizar_tareas()
            messagebox.showinfo("Guardado", "Tarea agregada correctamente.")

        tk.Button(frame_tareas, text="Guardar Tarea", bg="#27AE60", fg="white", command=guardar_tarea).pack(fill="x", pady=5)

        # --- SECCIÓN 2: CONTACTOS EMERGENCIA ---
        frame_contactos = tk.LabelFrame(ventana, text="2. Contactos de Emergencia (Alerta)", font=("Arial", 10, "bold"), padx=10, pady=10)
        frame_contactos.pack(fill="both", expand=True, padx=10, pady=10)

        # Lista de contactos actuales
        listbox = tk.Listbox(frame_contactos, height=5)
        listbox.pack(fill="x", pady=5)

        def refrescar_lista():
            listbox.delete(0, 'end')
            contactos = self.controller.obtener_contactos()
            for c in contactos:
                listbox.insert('end', f"{c['nombre']} - {c['numero']}")

        refrescar_lista() # Carga inicial

        # Formulario contacto
        tk.Label(frame_contactos, text="Nuevo Contacto (Nombre):").pack(anchor="w")
        entry_c_nombre = tk.Entry(frame_contactos); entry_c_nombre.pack(fill="x")
        
        tk.Label(frame_contactos, text="Número (ej: 56912345678):").pack(anchor="w")
        entry_c_numero = tk.Entry(frame_contactos); entry_c_numero.pack(fill="x")

        def agregar_contacto():
            nom = entry_c_nombre.get().strip()
            num = entry_c_numero.get().strip()
            if nom and num:
                self.controller.agregar_contacto(nom, num)
                entry_c_nombre.delete(0, 'end'); entry_c_numero.delete(0, 'end')
                refrescar_lista()
            else:
                messagebox.showwarning("Error", "Faltan datos del contacto")

        def borrar_contacto():
            seleccion = listbox.curselection()
            if seleccion:
                idx = seleccion[0]
                self.controller.eliminar_contacto(idx)
                refrescar_lista()

        btn_box = tk.Frame(frame_contactos)
        btn_box.pack(fill="x", pady=5)
        tk.Button(btn_box, text="Agregar Contacto", bg="#2980B9", fg="white", command=agregar_contacto).pack(side="left", expand=True, fill="x")
        tk.Button(btn_box, text="Borrar Seleccionado", bg="#C0392B", fg="white", command=borrar_contacto).pack(side="right", expand=True, fill="x")
