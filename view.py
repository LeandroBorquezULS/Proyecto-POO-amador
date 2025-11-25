"""
view.py

Interfaz gráfica (Tkinter). Implementa solo UI: botones, cuadros de diálogo y
renderizado de las tareas. Depende del controlador para la lógica.
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime
import threading

from controller import AppController
from models import Medicamento, Seguridad


class InterfazAmador(tk.Frame):
    """
    Clase de la vista principal. Requiere una instancia de AppController.
    """

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

        # Cargar tareas desde controlador
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

        btn_ayuda = tk.Button(self.frame_bottom, text="🆘 NECESITO AYUDA",
                              font=("Arial", 14, "bold"), bg="#C0392B", fg="white",
                              command=self.iniciar_proceso_ayuda)
        btn_ayuda.pack(side="left", padx=20, pady=10, fill="x", expand=True)

        btn_admin = tk.Button(self.frame_bottom, text="⚙ Familia",
                              font=("Arial", 10), bg="#34495E", fg="white",
                              command=self.solicitar_acceso_familia)
        btn_admin.pack(side="right", padx=10, pady=10)

    # ----- UI Helpers -----
    def actualizar_reloj(self) -> None:
        """Actualiza el reloj en la UI cada segundo."""
        ahora = datetime.now().strftime("%H:%M:%S")
        self.lbl_reloj.config(text=ahora)
        self.root.after(1000, self.actualizar_reloj)

    def renderizar_tareas(self) -> None:
        """Dibuja las tarjetas de tareas en la UI."""
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
        """Callback para marcar tarea como completada vía controlador."""
        self.controller.marcar_completado(indice)
        messagebox.showinfo("Excelente", f"¡Muy bien!\nHas completado: {self.tareas[indice].nombre}")
        # refrescar lista desde controlador (para consistencia)
        self.tareas = self.controller.cargar_tareas()
        self.renderizar_tareas()

    def iniciar_proceso_ayuda(self) -> None:
        """Inicia el flujo de envío de alerta a la familia."""
        respuesta = messagebox.askyesno("EMERGENCIA", "¿Enviar alerta automática a la familia?")
        if not respuesta:
            return

        # Preguntar número y mensaje (podrían venir de configuración; pedimos al usuario)
        numero = simpledialog.askstring("Número de contacto", "Ingrese número objetivo en formato internacional (ej: 569XXXXXXXX):")
        if not numero:
            messagebox.showwarning("Cancelado", "No se envió la alerta: número vacío.")
            return
        mensaje = simpledialog.askstring("Mensaje", "Texto del mensaje (predeterminado disponible):",
                                         initialvalue="¡AYUDA! Necesito asistencia urgente en casa.")
        if not mensaje:
            mensaje = "¡AYUDA! Necesito asistencia urgente en casa."

        # Ejecutar envío (controller maneja directamente utils)
        threading.Thread(target=self.controller.enviar_alerta_familia, args=(numero, mensaje), daemon=True).start()
        messagebox.showinfo("Alerta", "Se inició el proceso de envío. Verifica WhatsApp Web.")

    # ----- Administración (agregar tareas) -----
    def solicitar_acceso_familia(self) -> None:
        """
        Solicita contraseña para entrar al modo familia. Si es válida, abre ventana para agregar.
        """
        pwd = simpledialog.askstring("Acceso Familia", "Ingrese contraseña:", show='*')
        if pwd is None:
            return
        if self.controller.verificar_contrasena(pwd):
            self.abrir_ventana_agregar()
        else:
            messagebox.showerror("Error", "Contraseña incorrecta")

    def abrir_ventana_agregar(self) -> None:
        """Ventana modal para agregar una nueva tarea."""
        ventana_add = tk.Toplevel(self.root)
        ventana_add.title("Agregar Tarea")
        ventana_add.geometry("320x300")

        tk.Label(ventana_add, text="Nombre:").pack(pady=(10, 0))
        entry_nombre = tk.Entry(ventana_add); entry_nombre.pack(fill="x", padx=10)

        tk.Label(ventana_add, text="Hora:").pack(pady=(8, 0))
        entry_hora = tk.Entry(ventana_add); entry_hora.pack(fill="x", padx=10)

        tk.Label(ventana_add, text="Extra (dosis/ubicación):").pack(pady=(8, 0))
        entry_extra = tk.Entry(ventana_add); entry_extra.pack(fill="x", padx=10)

        tipo_var = tk.StringVar(value="Medicamento")
        tk.Radiobutton(ventana_add, text="Medicamento", variable=tipo_var, value="Medicamento").pack(anchor="w", padx=10, pady=4)
        tk.Radiobutton(ventana_add, text="Seguridad", variable=tipo_var, value="Seguridad").pack(anchor="w", padx=10)

        def guardar():
            nombre = entry_nombre.get().strip()
            hora = entry_hora.get().strip()
            extra = entry_extra.get().strip()

            if not nombre:
                messagebox.showwarning("Datos incompletos", "El nombre no puede estar vacío.")
                return

            if tipo_var.get() == "Medicamento":
                self.controller.agregar_tarea_medicamento(nombre, hora, extra)
            else:
                self.controller.agregar_tarea_seguridad(nombre, hora, extra)

            # Recargar y renderizar
            self.tareas = self.controller.cargar_tareas()
            self.renderizar_tareas()
            ventana_add.destroy()

        tk.Button(ventana_add, text="Guardar", command=guardar).pack(pady=12)
