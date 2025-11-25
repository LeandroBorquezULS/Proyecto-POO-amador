"""
view.py
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

        # --- UI Header ---
        self.frame_top = tk.Frame(root, bg="#E6F2F5")
        self.frame_top.pack(fill="x", pady=10)
        self.lbl_reloj = ttk.Label(self.frame_top, text="00:00", style="Clock.TLabel")
        self.lbl_reloj.pack()
        self.actualizar_reloj()
        tk.Label(self.frame_top, text="Hola Amador, hoy es un gran día.",
                 font=("Verdana", 14), bg="#E6F2F5", fg="#7F8C8D").pack()

        # --- Barra Progreso ---
        self.frame_progreso = tk.Frame(root, bg="#E6F2F5")
        self.frame_progreso.pack(fill="x", padx=20, pady=5)
        self.barra = ttk.Progressbar(self.frame_progreso, orient="horizontal", length=100, mode="determinate")
        self.barra.pack(fill="x")

        # --- Tareas (Scroll) ---
        self.canvas = tk.Canvas(root, bg="#E6F2F5", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#E6F2F5")
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="top", fill="both", expand=True, padx=10)
        self.scrollbar.pack(side="right", fill="y")

        self.renderizar_tareas()

        # --- Footer (Botones) ---
        self.frame_bottom = tk.Frame(root, bg="#2C3E50", height=80)
        self.frame_bottom.pack(fill="x", side="bottom")

        btn_ayuda = tk.Button(self.frame_bottom, text="🆘 NECESITO AYUDA",
                              font=("Arial", 14, "bold"), bg="#C0392B", fg="white",
                              command=self.accion_ayuda_inmediata)
        btn_ayuda.pack(side="left", padx=20, pady=10, fill="x", expand=True)

        btn_admin = tk.Button(self.frame_bottom, text="⚙ Familia",
                              font=("Arial", 10), bg="#34495E", fg="white",
                              command=self.solicitar_acceso_familia)
        btn_admin.pack(side="right", padx=10, pady=10)

    # --- Lógica UI ---
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

            # Texto tarea
            tk.Label(card, text=tarea.get_descripcion_visual(),
                     font=("Arial", 16), bg=bg_color, fg=fg_color, justify="left").pack(side="left", padx=15)

            # Botón Acción (SOLO COMPLETAR, NO BORRAR)
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

    # --- AYUDA CON MANEJO DE SIN CONTACTOS ---
    def accion_ayuda_inmediata(self) -> None:
        def proceso_ayuda():
            estado = self.controller.enviar_alerta_masiva()
            
            # Si el controller dice que no hay nadie...
            if estado == "SIN_CONTACTOS":
                # Usamos invoke para volver al hilo principal de la UI y preguntar
                self.root.after(0, self.pedir_numero_emergencia)
            else:
                messagebox.showinfo("Alerta", "Se han enviado los mensajes de ayuda.")

        # Hilo daemon para no congelar la UI mientras se abren las pestañas
        threading.Thread(target=proceso_ayuda, daemon=True).start()

    def pedir_numero_emergencia(self):
        # Esta función se ejecuta si no hay contactos guardados
        numero = simpledialog.askstring("EMERGENCIA", 
                                        "¡No hay contactos registrados!\n\nIngrese un número ahora para pedir ayuda (ej: 56911223344):")
        if numero:
            # Enviamos solo a ese número
            threading.Thread(target=self.controller.enviar_alerta_individual, args=(numero,), daemon=True).start()
            
            # Opcional: Preguntar si quiere guardarlo
            if messagebox.askyesno("Guardar", "¿Desea guardar este número para el futuro?"):
                self.controller.agregar_contacto("Contacto Emergencia", numero)

    # --- PANEL FAMILIA PROTEGIDO ---
    def solicitar_acceso_familia(self) -> None:
        # AHORA SI PIDE CONTRASEÑA
        pwd = simpledialog.askstring("Acceso Familia", "Ingrese contraseña:", show='*')
        if pwd is None: return
        
        if self.controller.verificar_contrasena(pwd):
            self.abrir_panel_familia()
        else:
            messagebox.showerror("Error", "Contraseña incorrecta")

    def abrir_panel_familia(self) -> None:
        ventana = tk.Toplevel(self.root)
        ventana.title("Panel de Familia")
        ventana.geometry("450x700")

        # 1. CREAR TAREA
        frame_crear = tk.LabelFrame(ventana, text="1. Programar Nueva Tarea", font=("Arial", 10, "bold"))
        frame_crear.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_crear, text="Nombre:").pack(anchor="w")
        entry_nombre = tk.Entry(frame_crear); entry_nombre.pack(fill="x")
        
        frame_row = tk.Frame(frame_crear)
        frame_row.pack(fill="x")
        tk.Label(frame_row, text="Hora (HH:MM):").pack(side="left")
        entry_hora = tk.Entry(frame_row, width=10); entry_hora.pack(side="left", padx=5)

        tk.Label(frame_crear, text="Extra:").pack(anchor="w")
        entry_extra = tk.Entry(frame_crear); entry_extra.pack(fill="x")

        # Radios
        tipo_var = tk.StringVar(value="Medicamento")
        freq_var = tk.StringVar(value="Diaria")
        
        f_radios = tk.Frame(frame_crear); f_radios.pack(anchor="w", pady=5)
        tk.Radiobutton(f_radios, text="Medicamento", variable=tipo_var, value="Medicamento").pack(side="left")
        tk.Radiobutton(f_radios, text="Seguridad", variable=tipo_var, value="Seguridad").pack(side="left")

        f_freq = tk.Frame(frame_crear); f_freq.pack(anchor="w")
        tk.Radiobutton(f_freq, text="Diaria", variable=freq_var, value="Diaria").pack(side="left")
        tk.Radiobutton(f_freq, text="Única", variable=freq_var, value="Única").pack(side="left")

        def guardar():
            if not entry_nombre.get(): return
            if tipo_var.get() == "Medicamento":
                self.controller.agregar_tarea_medicamento(entry_nombre.get(), entry_hora.get(), entry_extra.get(), freq_var.get())
            else:
                self.controller.agregar_tarea_seguridad(entry_nombre.get(), entry_hora.get(), entry_extra.get(), freq_var.get())
            entry_nombre.delete(0,'end'); entry_hora.delete(0,'end'); entry_extra.delete(0,'end')
            refrescar_lista_tareas_admin() # Actualizar lista de abajo
            self.tareas = self.controller.cargar_tareas() # Actualizar memoria UI principal
            self.renderizar_tareas() # Actualizar UI principal
            messagebox.showinfo("OK", "Tarea creada")

        tk.Button(frame_crear, text="Guardar Tarea", bg="#27AE60", fg="white", command=guardar).pack(fill="x", pady=5)

        # 2. CONTACTOS
        frame_contactos = tk.LabelFrame(ventana, text="2. Contactos Emergencia", font=("Arial", 10, "bold"))
        frame_contactos.pack(fill="x", padx=10, pady=5)
        
        lb_contactos = tk.Listbox(frame_contactos, height=4)
        lb_contactos.pack(fill="x")
        
        def ref_contactos():
            lb_contactos.delete(0, 'end')
            for c in self.controller.obtener_contactos():
                lb_contactos.insert('end', f"{c['nombre']} ({c['numero']})")
        ref_contactos()

        f_add_c = tk.Frame(frame_contactos); f_add_c.pack(fill="x")
        e_cnom = tk.Entry(f_add_c, width=15); e_cnom.pack(side="left", fill="x", expand=True)
        e_cnum = tk.Entry(f_add_c, width=15); e_cnum.pack(side="left", fill="x", expand=True)
        
        def add_c():
            if e_cnom.get() and e_cnum.get():
                self.controller.agregar_contacto(e_cnom.get(), e_cnum.get())
                e_cnom.delete(0,'end'); e_cnum.delete(0,'end'); ref_contactos()

        def del_c():
            sel = lb_contactos.curselection()
            if sel: self.controller.eliminar_contacto(sel[0]); ref_contactos()

        tk.Button(frame_contactos, text="Agregar (+)", command=add_c).pack(fill="x")
        tk.Button(frame_contactos, text="Borrar Contacto (-)", command=del_c, bg="#E74C3C", fg="white").pack(fill="x")


        # 3. GESTIONAR TAREAS ACTIVAS (AQUÍ ESTÁ EL BORRAR TAREAS)
        frame_gest_tareas = tk.LabelFrame(ventana, text="3. Eliminar Tareas", font=("Arial", 10, "bold"), fg="#C0392B")
        frame_gest_tareas.pack(fill="both", expand=True, padx=10, pady=5)

        lb_tareas = tk.Listbox(frame_gest_tareas, height=6)
        lb_tareas.pack(fill="both", expand=True)

        def refrescar_lista_tareas_admin():
            lb_tareas.delete(0, 'end')
            mis_tareas = self.controller.cargar_tareas() # Cargar frescas
            for t in mis_tareas:
                lb_tareas.insert('end', f"{t.hora} - {t.nombre} ({t.frecuencia})")

        refrescar_lista_tareas_admin()

        def borrar_tarea_admin():
            sel = lb_tareas.curselection()
            if sel:
                idx = sel[0]
                self.controller.eliminar_tarea(idx)
                refrescar_lista_tareas_admin()
                # Actualizar ventana principal también
                self.tareas = self.controller.cargar_tareas()
                self.renderizar_tareas()
        
        tk.Button(frame_gest_tareas, text="ELIMINAR TAREA SELECCIONADA", bg="#C0392B", fg="white", command=borrar_tarea_admin).pack(fill="x", pady=5)
