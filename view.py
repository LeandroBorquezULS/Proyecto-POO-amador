"""
view.py
"""
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime
import threading

from controller import AppController

# --- PALETA DE ALTO CONTRASTE (OPTIMIZADA PARA PROYECTORES) ---
COLORES = {
    "fondo_sidebar": "#2C3E50",   # Azul Oscuro (Casi negro)
    "texto_sidebar": "#FFFFFF",   # Blanco Puro
    "fondo_main":    "#FFFFFF",   # Blanco Puro (Mejor brillo)
    "texto_main":    "#000000",   # Negro Puro (Máxima legibilidad)
    "btn_accion":    "#0056b3",   # Azul fuerte
    "btn_alerta":    "#D92525",   # Rojo Intenso
    "btn_verde":     "#007E33",   # Verde Tráfico
    "btn_negro":     "#000000",   # Botones neutros
    "tarea_bg":      "#F0F0F0",   # Gris claro separador
    "tarea_done":    "#D4EFDF",   # Verde pálido
}

FUENTES = {
    "reloj": ("Arial", 48, "bold"),
    "fecha": ("Arial", 16, "bold"),
    "titulo": ("Arial", 24, "bold"),
    "subtitulo": ("Arial", 14, "bold"),
    "tarea_txt": ("Arial", 14),
    "tarea_hora": ("Arial", 14, "bold"),
    "btn_txt": ("Arial", 11, "bold"),
}

class InterfazAmador(tk.Frame):
    def __init__(self, root: tk.Tk, controller: AppController):
        super().__init__(root)
        self.root = root
        self.controller = controller
        
        # 1. Configuración Ventana (Formato Desktop Landscape)
        self.root.title("Asistente Personal - Amador")
        self.root.geometry("1100x700") 
        self.root.configure(bg=COLORES["fondo_main"])

        # Estilos TTK
        self.estilo = ttk.Style()
        self.estilo.theme_use('alt') 
        self.estilo.configure("HighContrast.Horizontal.TProgressbar", 
                              troughcolor="#CCCCCC", 
                              background=COLORES["btn_verde"], 
                              thickness=30)

        self.tareas = self.controller.cargar_tareas()

        # --- LAYOUT PRINCIPAL (2 COLUMNAS) ---
        # Sidebar Izquierda
        self.sidebar = tk.Frame(root, bg=COLORES["fondo_sidebar"], width=400)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Área Principal Derecha
        self.main_area = tk.Frame(root, bg=COLORES["fondo_main"])
        self.main_area.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        # ====================
        # CONTENIDO SIDEBAR
        # ====================
        
        # Reloj
        self.lbl_reloj = tk.Label(self.sidebar, text="00:00", font=FUENTES["reloj"], 
                                  bg=COLORES["fondo_sidebar"], fg=COLORES["texto_sidebar"])
        self.lbl_reloj.pack(pady=(30, 5))
        
        # Fecha
        self.lbl_fecha = tk.Label(self.sidebar, text="---", font=FUENTES["fecha"],
                                  bg=COLORES["fondo_sidebar"], fg="#BDC3C7")
        self.lbl_fecha.pack(pady=(0, 10)) # Reduje un poco el padding inferior aquí

        # --- NUEVO SALUDO ---
        self.lbl_saludo = tk.Label(self.sidebar, text="Hola", font=("Arial", 16, "italic"),
                                   bg=COLORES["fondo_sidebar"], fg="#F4D03F") # Color dorado/amarillo suave para resaltar
        self.lbl_saludo.pack(pady=(0, 30))
        # --------------------
        self.actualizar_reloj()

        # Barra Progreso
        tk.Label(self.sidebar, text="PROGRESO DIARIO", font=FUENTES["subtitulo"],
                 bg=COLORES["fondo_sidebar"], fg="white").pack(anchor="w", padx=20)
        
        self.barra = ttk.Progressbar(self.sidebar, orient="horizontal", length=100, 
                                     mode="determinate", style="HighContrast.Horizontal.TProgressbar")
        self.barra.pack(fill="x", padx=20, pady=10)
        
        self.lbl_porcentaje = tk.Label(self.sidebar, text="0%", font=("Arial", 20, "bold"),
                                       bg=COLORES["fondo_sidebar"], fg="white")
        self.lbl_porcentaje.pack()

        # Espaciador
        tk.Frame(self.sidebar, bg=COLORES["fondo_sidebar"]).pack(fill="both", expand=True)

        # Botón Configuración (Familia)
        btn_admin = tk.Button(self.sidebar, text="FAMILIA",
                              font=FUENTES["btn_txt"], bg="#5D6D7E", fg="white",
                              relief="raised", bd=3, pady=10,
                              command=self.solicitar_acceso_familia)
        btn_admin.pack(fill="x", padx=15, pady=10)

        # Botón Pánico
        btn_ayuda = tk.Button(self.sidebar, text="🆘  PEDIR AYUDA",
                              font=("Arial", 16, "bold"), bg=COLORES["btn_alerta"], fg="white",
                              relief="raised", bd=5, cursor="hand2",
                              command=self.accion_ayuda_inmediata)
        btn_ayuda.pack(fill="x", padx=20, pady=(0, 30), ipady=15)


        # ====================
        # CONTENIDO PRINCIPAL
        # ====================

        # Header
        header_frame = tk.Frame(self.main_area, bg=COLORES["fondo_main"])
        header_frame.pack(fill="x", pady=(0, 15))
        
        tk.Label(header_frame, text="LISTA DE TAREAS", font=FUENTES["titulo"], 
                 bg=COLORES["fondo_main"], fg=COLORES["texto_main"]).pack(side="left")
        
        # Lista Scrollable
        self.canvas = tk.Canvas(self.main_area, bg=COLORES["fondo_main"], highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.main_area, orient="vertical", command=self.canvas.yview)
        
        self.scrollable_frame = tk.Frame(self.canvas, bg=COLORES["fondo_main"])
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", width=650)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.renderizar_tareas()


    # --- Lógica UI Principal ---
    def actualizar_reloj(self) -> None:
        now = datetime.now()
        
        # Actualizar hora y fecha
        self.lbl_reloj.config(text=now.strftime("%H:%M"))
        self.lbl_fecha.config(text=now.strftime("%d-%m-%Y"))
        
        # --- LÓGICA DEL SALUDO ---
        hora = int(now.strftime("%H"))
        if 6 <= hora < 12:
            texto_saludo = "¡Buen día, Amador!"
        elif 12 <= hora < 20:
            texto_saludo = "¡Buenas tardes, Amador!"
        else:
            texto_saludo = "¡Buenas noches, Amador!"
            
        self.lbl_saludo.config(text=texto_saludo)
        # -------------------------

        self.root.after(1000, self.actualizar_reloj)

    def renderizar_tareas(self) -> None:
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        completadas = 0
        total = len(self.tareas)

        # Cabecera de tabla
        if total > 0:
            h_row = tk.Frame(self.scrollable_frame, bg="black", height=35)
            h_row.pack(fill="x", pady=(0,5))
            tk.Label(h_row, text="HORA", fg="white", bg="black", font=("Arial",11,"bold"), width=8).pack(side="left", padx=5)
            tk.Label(h_row, text="ACTIVIDAD", fg="white", bg="black", font=("Arial",11,"bold")).pack(side="left", padx=10)

        for idx, tarea in enumerate(self.tareas):

            # Colores según estado
            if tarea.estado == "Completado":
                completadas += 1
                bg_c = COLORES["tarea_done"]
                fg_c = "#005000"
                estado_txt = "✅ HECHO"
            else:
                bg_c = COLORES["tarea_bg"]
                fg_c = "black"
                estado_txt = ""

            # Fila de tarea
            row = tk.Frame(self.scrollable_frame, bg=bg_c, bd=1, relief="solid")
            row.pack(fill="x", pady=4, ipady=10)

            # Columna izquierda: Hora
            tk.Label(row, text=tarea.hora, font=FUENTES["tarea_hora"],
                    bg=bg_c, fg="black", width=8).pack(side="left", padx=5)

            # Separador
            tk.Frame(row, bg="black", width=2).pack(side="left", fill="y", padx=5)

            # --- Construcción del texto de tarea ---
            icono = "💊" if "edicamento" in tarea.nombre.lower() or "pastilla" in tarea.nombre.lower() else "📝"
            texto = f"{icono} {tarea.nombre}"

            detalle = getattr(tarea, 'detalle_extra', getattr(tarea, 'detalles',
                        getattr(tarea, 'descripcion', '')))
            if detalle:
                texto += f"\n({detalle})"

            # Frame del texto + botón
            frame_texto = tk.Frame(row, bg=bg_c)
            frame_texto.pack(side="left", padx=15)

            # Texto
            tk.Label(frame_texto, text=texto, font=("Arial", 16),
                    bg=bg_c, fg=fg_c, justify="left").pack(anchor="w")

            # Botón hablar
            tk.Button(
                frame_texto,
                text="▶️",
                font=("Arial", 14, "bold"),
                bg="#F1C40F",
                command=lambda t=tarea: self.controller.hablar_tarea(t)
            ).pack(anchor="w", pady=3)

            # Botón marcar o estado
            if tarea.estado == "Pendiente":
                tk.Button(
                    row, text="MARCAR LISTO",
                    bg=COLORES["btn_accion"], fg="white",
                    font=FUENTES["btn_txt"], relief="raised", bd=3,
                    command=lambda i=idx: self.marcar_completado(i)
                ).pack(side="right", padx=15)
            else:
                tk.Label(row, text=estado_txt, font=("Arial", 12, "bold"),
                        bg=bg_c, fg=fg_c).pack(side="right", padx=20)

        # Actualización de barra de progreso
        porcentaje = (completadas / total * 100) if total > 0 else 0
        self.barra["value"] = porcentaje
        self.lbl_porcentaje.config(text=f"{int(porcentaje)}%")
        self.lbl_porcentaje.config(fg=COLORES["btn_verde"] if porcentaje == 100 else "white")

    def marcar_completado(self, indice: int) -> None:
        self.controller.marcar_completado(indice)
        self.tareas = self.controller.cargar_tareas()
        self.renderizar_tareas()

    # --- AYUDA / EMERGENCIA ---
    def accion_ayuda_inmediata(self) -> None:
        def proceso_ayuda():
            estado = self.controller.enviar_alerta_masiva()
            if estado == "SIN_CONTACTOS":
                self.root.after(0, self.pedir_numero_emergencia)
            else:
                messagebox.showinfo("ALERTA", "Se han enviado los mensajes de ayuda.")

        threading.Thread(target=proceso_ayuda, daemon=True).start()

    def pedir_numero_emergencia(self):
        numero = simpledialog.askstring("EMERGENCIA", 
                                        "¡NO HAY CONTACTOS!\nIngrese un número para pedir ayuda:")
        if numero:
            threading.Thread(target=self.controller.enviar_alerta_individual, args=(numero,), daemon=True).start()
            if messagebox.askyesno("GUARDAR", "¿Guardar este número para el futuro?"):
                self.controller.agregar_contacto("Contacto Emergencia", numero)

    # --- PANEL FAMILIA (ADMINISTRACIÓN) ---
    def solicitar_acceso_familia(self) -> None:
        pwd = simpledialog.askstring("ADMINISTRADOR", "Ingrese contraseña:", show='*')
        if not pwd: return
        
        if self.controller.verificar_contrasena(pwd):
            self.abrir_panel_familia()
        else:
            messagebox.showerror("ERROR", "Contraseña incorrecta")

    def abrir_panel_familia(self) -> None:
        ventana = tk.Toplevel(self.root)
        ventana.title("PANEL DE CONTROL - FAMILIA")
        ventana.geometry("650x800")
        ventana.configure(bg="#E0E0E0") 

        # Scroll para el panel admin (por si es muy pequeña la pantalla)
        main_frame = tk.Frame(ventana, bg="#E0E0E0")
        main_frame.pack(fill="both", expand=True)
        
        canvas = tk.Canvas(main_frame, bg="#E0E0E0")
        scroll = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        frame_contenido = tk.Frame(canvas, bg="#E0E0E0")
        
        frame_contenido.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0,0), window=frame_contenido, anchor="nw", width=620)
        canvas.configure(yscrollcommand=scroll.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        # Estilo cajas
        def crear_caja(titulo, color_texto):
            f = tk.LabelFrame(frame_contenido, text=titulo, font=("Arial", 12, "bold"), 
                              bg="white", fg=color_texto, bd=2, relief="groove")
            f.pack(fill="x", padx=15, pady=10, ipady=5)
            return f

        # 1. CREAR TAREA
        f_crear = crear_caja("1. PROGRAMAR NUEVA TAREA", "black")

        tk.Label(f_crear, text="Nombre:", bg="white", font=("Arial", 10)).pack(anchor="w", padx=10)
        e_nom = tk.Entry(f_crear, font=("Arial", 11), bg="#F9F9F9"); e_nom.pack(fill="x", padx=10)

        f_fila = tk.Frame(f_crear, bg="white"); f_fila.pack(fill="x", padx=10, pady=5)
        tk.Label(f_fila, text="Hora (HH:MM):", bg="white").pack(side="left")
        e_hora = tk.Entry(f_fila, width=10, font=("Arial", 11)); e_hora.pack(side="left", padx=5)

        tk.Label(f_crear, text="Detalle extra:", bg="white", font=("Arial", 10)).pack(anchor="w", padx=10)
        e_extra = tk.Entry(f_crear, font=("Arial", 11), bg="#F9F9F9"); e_extra.pack(fill="x", padx=10)

        # Radios
        tipo_var = tk.StringVar(value="Medicamento")
        freq_var = tk.StringVar(value="Diaria")
        
        f_rad = tk.Frame(f_crear, bg="white"); f_rad.pack(fill="x", padx=10, pady=10)
        tk.Label(f_rad, text="Tipo:", font=("Arial",10,"bold"), bg="white").grid(row=0, column=0)
        tk.Radiobutton(f_rad, text="Medicamento", variable=tipo_var, value="Medicamento", bg="white").grid(row=0, column=1)
        tk.Radiobutton(f_rad, text="Seguridad", variable=tipo_var, value="Seguridad", bg="white").grid(row=0, column=2)

        tk.Label(f_rad, text="Frec:", font=("Arial",10,"bold"), bg="white").grid(row=1, column=0)
        tk.Radiobutton(f_rad, text="Diaria", variable=freq_var, value="Diaria", bg="white").grid(row=1, column=1)
        tk.Radiobutton(f_rad, text="Única", variable=freq_var, value="Única", bg="white").grid(row=1, column=2)

        def guardar_tarea():
            if not e_nom.get(): return
            if tipo_var.get() == "Medicamento":
                self.controller.agregar_tarea_medicamento(e_nom.get(), e_hora.get(), e_extra.get(), freq_var.get())
            else:
                self.controller.agregar_tarea_seguridad(e_nom.get(), e_hora.get(), e_extra.get(), freq_var.get())
            
            e_nom.delete(0,'end'); e_hora.delete(0,'end'); e_extra.delete(0,'end')
            refrescar_listas()
            self.tareas = self.controller.cargar_tareas()
            self.renderizar_tareas()
            messagebox.showinfo("OK", "Tarea guardada", parent=ventana)

        tk.Button(f_crear, text="GUARDAR TAREA", bg=COLORES["btn_verde"], fg="white", font=FUENTES["btn_txt"], 
                  command=guardar_tarea).pack(fill="x", padx=10, pady=5)

        # 2. CONTACTOS (Funcionalidad restaurada completa)
        f_cont = crear_caja("2. CONTACTOS EMERGENCIA", COLORES["btn_accion"])
        
        lb_cont = tk.Listbox(f_cont, height=4, font=("Arial", 11))
        lb_cont.pack(fill="x", padx=10)

        def ref_contactos():
            lb_cont.delete(0, 'end')
            for c in self.controller.obtener_contactos():
                lb_cont.insert('end', f"{c['nombre']} ({c['numero']})")
        ref_contactos()

        f_add = tk.Frame(f_cont, bg="white"); f_add.pack(fill="x", padx=10, pady=5)
        e_cnom = tk.Entry(f_add, width=15); e_cnom.pack(side="left", fill="x", expand=True)
        tk.Label(f_add, text="#", bg="white").pack(side="left")
        e_cnum = tk.Entry(f_add, width=15); e_cnum.pack(side="left", fill="x", expand=True)
        
        def add_c():
            if e_cnom.get() and e_cnum.get():
                self.controller.agregar_contacto(e_cnom.get(), e_cnum.get())
                e_cnom.delete(0,'end'); e_cnum.delete(0,'end')
                ref_contactos()

        def del_c():
            sel = lb_cont.curselection()
            if sel:
                self.controller.eliminar_contacto(sel[0])
                ref_contactos()

        tk.Button(f_cont, text="AGREGAR CONTACTO (+)", bg=COLORES["btn_accion"], fg="white", font=("Arial", 9, "bold"), command=add_c).pack(fill="x", padx=10, pady=2)
        tk.Button(f_cont, text="BORRAR SELECCIONADO (-)", bg=COLORES["btn_alerta"], fg="white", font=("Arial", 9, "bold"), command=del_c).pack(fill="x", padx=10, pady=2)

        # 3. ELIMINAR TAREAS
        f_borrar = crear_caja("3. GESTIONAR TAREAS", COLORES["btn_alerta"])
        lb_tareas = tk.Listbox(f_borrar, height=5, font=("Arial", 11))
        lb_tareas.pack(fill="x", padx=10)

        def refrescar_listas():
            lb_tareas.delete(0, 'end')
            for t in self.controller.cargar_tareas():
                lb_tareas.insert('end', f"{t.hora} - {t.nombre} ({t.frecuencia})")
        
        refrescar_listas()

        def borrar_tarea_sel():
            sel = lb_tareas.curselection()
            if sel:
                if messagebox.askyesno("Confirmar", "¿Borrar tarea?"):
                    self.controller.eliminar_tarea(sel[0])
                    refrescar_listas()
                    self.tareas = self.controller.cargar_tareas()
                    self.renderizar_tareas()

        tk.Button(f_borrar, text="ELIMINAR TAREA SELECCIONADA", bg=COLORES["btn_alerta"], fg="white", font=FUENTES["btn_txt"], 
                  command=borrar_tarea_sel).pack(fill="x", padx=10, pady=5)

        # 4. SEGURIDAD (Funcionalidad restaurada)
        f_seg = crear_caja("4. SEGURIDAD", "#8E44AD")

        def cambiar_pass():
            n = simpledialog.askstring("Clave", "Nueva contraseña (min 6):", show='*', parent=ventana)
            if not n: return
            if len(n) < 6:
                messagebox.showwarning("Error", "Muy corta.", parent=ventana); return
            c = simpledialog.askstring("Clave", "Repetir contraseña:", show='*', parent=ventana)
            if n == c:
                self.controller.establecer_contrasena(n)
                messagebox.showinfo("OK", "Contraseña actualizada", parent=ventana)
            else:
                messagebox.showerror("Error", "No coinciden", parent=ventana)

        tk.Button(f_seg, text="CAMBIAR CONTRASEÑA ADMIN", bg="#8E44AD", fg="white", font=FUENTES["btn_txt"], 
                  command=cambiar_pass).pack(fill="x", padx=10, pady=5)