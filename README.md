# ***Amador Assistant: Asistencia personal para adultos mayores***

En este proyecto se abordó el **caso N°4 de Mi memoria me falla**. Este problema centrado en **Amador**, un adulto mayor de 74 años que vive solo y comenzó a tener problemas de memoria. Amador es una persona que valora su independencia, pero olvida ciertas tareas muy importantes como por ejemplo tomar sus medicamentos...


La forma que se encontró una solución a este problema, es desarrollar una aplicación de escritorio (PC) en python de asistente personal llamada "Amador Assitant" que le pueda ayudar en su vida cotidiana y ayudarle a gestionar su vida de forma mucho más facil. Esto bajo el modelo de MVC (Modelo-Vista-Controlador)


# Características Principales
-🚨 El Botón de Pánico que consiste en mandar un mensaje automatizado de alerta por WhatsApp a los contactos que se registraron previamente, sin necesidad de escribir.

-🔒 El Panel Familiar Seguro que es un área protegida con una contraseña para que la familia configure las tareas y contactos, esto para evitar que Amador borre información por error.

-♿ Una Interfaz accesible con botones de gran tamaño, alto contraste, tipogtafías legibles (Arial 16).

-⏰ Gestión de Tareas y seguridad que hay recordatorios claros para medicamentos y seguridad (gas/puertas).

---

# Entre las tecnologías usadas están:
- Uso de TTS (Text to Speech) que ocupa la biblioteca de **pyttsx3** para recordatorios audibles.
  
- Python 3.12+
  
- GUI con Tkinter
  
- Se ocupan archivos JSON para las estructuras complejas por ejemplo los contactos y CSV para la agilidad de lectura
  
- Hashlib (SHA-256) para la encriptación de claves
  
- PyAutoGUI y Webbrowser que se ocuparon para el navegador y control de perifericos

---

# Librerias que se ocuparon:
- pyttsx3
  
- pyautogui

---

### Pasos de Instalación

1.  Clona el repositorio:
    ```bash
    git clone [https://github.com/tu_usuario/Proyecto-POO-amador.git](https://github.com/tu_usuario/Proyecto-POO-amador.git)
    cd Proyecto-POO-amador
    ```
2.  Instala las bibliotecas de Python requeridas:
    ```bash
    pip install -r requirements.txt
    ```
3.  Ejecuta la aplicación:
    ```bash
    python main.py 
    # (Asegúrate de que 'main.py' es el archivo principal)
    ```

## 🏗️ Estructura del Proyecto

El proyecto cumple estrictamente con los principios de la Programación Orientada a Objetos:
- Herencia: Se implementó una clase madre TareaBase de la cual heredan Medicamento (añade dosis) y Seguridad (añade ubicación). Esto facilita la escalabilidad del código.
- Polimorfismo: El método get_descripcion_visual() actúa de forma distinta según si el objeto es un medicamento (muestra icono de píldora) o seguridad (muestra candado).
- Encapsulamiento: El manejo de la base de datos y la autenticación se realiza a través de métodos específicos en el controlador, ocultando la complejidad al usuario final.
