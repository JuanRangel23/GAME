import tkinter as tk
from tkinter import ttk
import random
import os
from PIL import Image, ImageTk, ImageOps

class Personaje:
    def __init__(self, nombre, vida, ataque):
        self.nombre = nombre
        self.vida = vida
        self.vida_maxima = vida
        self.ataque = ataque

    def atacar(self, otro_personaje):
        daño = random.randint(0, self.ataque)
        otro_personaje.vida = max(otro_personaje.vida - daño, 0)
        return daño

class JuegoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Juego de Combate")
        self.root.geometry("600x700")
        self.root.configure(bg="#2c3e50")

        self.personaje1 = None
        self.personaje2 = None

        self.mostrar_pantalla_inicio()

    def mostrar_pantalla_inicio(self):
        self.limpiar_pantalla()

        try:
            bg_image = Image.open("img/Titulo.png")
            bg_image = bg_image.resize((600, 700))
            self.bg_photo = ImageTk.PhotoImage(bg_image)
            self.lbl_bg = tk.Label(self.root, image=self.bg_photo)
            self.lbl_bg.place(x=0, relwidth=1, relheight=1)
        except Exception as e:
            print(f"⚠️ No se pudo cargar la imagen de fondo: {e}")

        self.lbl_titulo = tk.Label(
            self.root,
            text="¡Bienvenido al Juego de Combate!",
            font=("Arial", 22, "bold"),
            bg="#2c3e50",
            fg="#ecf0f1"
        )
        self.lbl_titulo.pack(pady=40)

        self.boton_jugar = tk.Button(
            self.root,
            text="Jugar",
            font=("Arial", 18, "bold"),
            bg="#27ae60",
            fg="#ecf0f1",
            width=15,
            height=2,
            command=lambda: self.crear_pantalla_seleccion(1)
        )
        self.boton_jugar.pack(pady=200)

    def crear_pantalla_seleccion(self, jugador):
        self.limpiar_pantalla()

        self.jugador_actual = jugador
        self.lbl_titulo = tk.Label(
            self.root,
            text=f"Jugador {jugador}, elige tu personaje",
            font=("Arial", 18, "bold"),
            bg="#2c3e50", fg="#ecf0f1"
        )
        self.lbl_titulo.pack(pady=20)

        self.nombre_entry = tk.Entry(self.root, font=("Arial", 14))
        self.nombre_entry.pack(pady=10)
        self.nombre_entry.insert(0, f"Jugador {jugador}")

        self.botones_frame = tk.Frame(self.root, bg="#2c3e50")
        self.botones_frame.pack(pady=20)

        personajes = [
            ("Guerrero", 120, 25, "img/Guerrero.png"),
            ("Mago", 100, 35, "img/Mago.png"),
            ("Arquero", 110, 30, "img/Arquero.png")
        ]

        self.imagenes = []

        for nombre, vida, ataque, img_path in personajes:
            try:
                if os.path.exists(img_path):
                    imagen_pil = Image.open(img_path)
                    imagen_pil = imagen_pil.resize((100, 100))
                    imagen = ImageTk.PhotoImage(imagen_pil)
                else:
                    print(f"⚠️ Imagen {img_path} no encontrada.")
                    imagen = None
            except Exception as e:
                print(f"No se pudo cargar la imagen {img_path}: {e}")
                imagen = None

            if imagen:
                lbl_imagen = tk.Label(self.botones_frame, image=imagen, bg="#2c3e50")
                lbl_imagen.image = imagen
                lbl_imagen.pack(pady=5)
                self.imagenes.append(imagen)

            btn = tk.Button(
                self.botones_frame,
                text=f"{nombre}\n(Vida: {vida}, Ataque: {ataque})",
                font=("Arial", 12, "bold"),
                bg="#34495e",
                fg="#ecf0f1",
                width=20,
                height=3,
                command=lambda n=nombre, v=vida, a=ataque, i=img_path: self.seleccionar_personaje(n, v, a, i)
            )
            btn.pack(pady=5)

    def seleccionar_personaje(self, nombre, vida, ataque, img_path):
        nombre_completo = f"{self.nombre_entry.get()} el {nombre}"
        personaje = Personaje(nombre_completo, vida, ataque)
        personaje.imagen_path = img_path

        if self.jugador_actual == 1:
            self.personaje1 = personaje
            self.crear_pantalla_seleccion(2)
        else:
            self.personaje2 = personaje
            self.iniciar_combate()

    def iniciar_combate(self):
        self.limpiar_pantalla()

        self.lbl_titulo = tk.Label(
            self.root,
            text="¡Combate en marcha!",
            font=("Arial", 18, "bold"),
            bg="#2c3e50", fg="#ecf0f1"
        )
        self.lbl_titulo.pack(pady=20)

        self.personajes_frame = tk.Frame(self.root, bg="#2c3e50")
        self.personajes_frame.pack(pady=10)

        self.img_p1_label = tk.Label(self.personajes_frame, bg="#2c3e50")
        self.img_p1_label.pack(side=tk.LEFT, padx=20)

        self.img_p2_label = tk.Label(self.personajes_frame, bg="#2c3e50")
        self.img_p2_label.pack(side=tk.LEFT, padx=20)

        self.mostrar_imagen_personaje(self.personaje1, self.img_p1_label, marco_rojo=False)
        self.mostrar_imagen_personaje(self.personaje2, self.img_p2_label, marco_rojo=False)

        self.lbl_p1 = tk.Label(
            self.root,
            text=self.personaje1.nombre,
            font=("Arial", 14, "bold"),
            bg="#2c3e50", fg="#ecf0f1"
        )
        self.lbl_p1.pack()
        self.progress_p1 = ttk.Progressbar(self.root, maximum=self.personaje1.vida_maxima, length=400)
        self.progress_p1.pack(pady=10)
        self.progress_p1["value"] = self.personaje1.vida

        self.lbl_p2 = tk.Label(
            self.root,
            text=self.personaje2.nombre,
            font=("Arial", 14, "bold"),
            bg="#2c3e50", fg="#ecf0f1"
        )
        self.lbl_p2.pack()
        self.progress_p2 = ttk.Progressbar(self.root, maximum=self.personaje2.vida_maxima, length=400)
        self.progress_p2.pack(pady=10)
        self.progress_p2["value"] = self.personaje2.vida

        self.texto_combate = tk.Text(
            self.root, height=10, width=60,
            state="disabled", bg="#ecf0f1", fg="#2c3e50",
            font=("Arial", 12)
        )
        self.texto_combate.pack(pady=20)

        self.botones_control = tk.Frame(self.root, bg="#2c3e50")
        self.botones_control.pack()

        self.boton_atacar = tk.Button(
            self.botones_control, text="¡Atacar!", font=("Arial", 14, "bold"),
            bg="#e74c3c", fg="#ecf0f1", width=12,
            command=self.combate_turno
        )
        self.boton_atacar.pack(side=tk.LEFT, padx=10)

        self.boton_reiniciar = tk.Button(
            self.botones_control, text="🔄 Reiniciar", font=("Arial", 14, "bold"),
            bg="#27ae60", fg="#ecf0f1", width=12,
            command=self.reiniciar_partida
        )
        self.boton_reiniciar.pack(side=tk.LEFT, padx=10)

        self.turno = 0

    def combate_turno(self):
        atacante = self.personaje1 if self.turno % 2 == 0 else self.personaje2
        defensor = self.personaje2 if self.turno % 2 == 0 else self.personaje1

        daño = atacante.atacar(defensor)
        self.mostrar_mensaje(f"{atacante.nombre} ataca a {defensor.nombre} y causa {daño} de daño.")

        self.progress_p1["value"] = self.personaje1.vida
        self.progress_p2["value"] = self.personaje2.vida

        self.mostrar_imagen_personaje(self.personaje1, self.img_p1_label, marco_rojo=False)
        self.mostrar_imagen_personaje(self.personaje2, self.img_p2_label, marco_rojo=False)

        if defensor == self.personaje1:
            self.mostrar_imagen_personaje(defensor, self.img_p1_label, marco_rojo=True)
        else:
            self.mostrar_imagen_personaje(defensor, self.img_p2_label, marco_rojo=True)

        if defensor.vida <= 0:
            self.mostrar_mensaje(f"⚔️ {defensor.nombre} ha sido derrotado.")
            self.mostrar_mensaje(f"🏆 ¡{atacante.nombre} gana el combate!")
            self.boton_atacar.config(state="disabled")

            if atacante == self.personaje1:
                self.lbl_p1.config(text=f"{self.personaje1.nombre} 🏆")
                self.lbl_p2.config(text=f"{self.personaje2.nombre} 💀")
            else:
                self.lbl_p2.config(text=f"{self.personaje2.nombre} 🏆")
                self.lbl_p1.config(text=f"{self.personaje1.nombre} 💀")
        else:
            self.turno += 1

    def mostrar_imagen_personaje(self, personaje, label, marco_rojo=False):
        try:
            if personaje and os.path.exists(personaje.imagen_path):
                imagen_pil = Image.open(personaje.imagen_path)
                if marco_rojo:
                    imagen_pil = ImageOps.expand(imagen_pil, border=5, fill='red')
                imagen_pil = imagen_pil.resize((100, 100))
                imagen = ImageTk.PhotoImage(imagen_pil)
                label.config(image=imagen)
                label.image = imagen
        except Exception as e:
            print(f"No se pudo mostrar la imagen del personaje: {e}")

    def reiniciar_partida(self):
        self.personaje1 = None
        self.personaje2 = None
        self.mostrar_pantalla_inicio()

    def mostrar_mensaje(self, mensaje):
        self.texto_combate.config(state="normal")
        self.texto_combate.insert(tk.END, mensaje + "\n")
        self.texto_combate.config(state="disabled")
        self.texto_combate.see(tk.END)

    def limpiar_pantalla(self):
        for widget in self.root.winfo_children():
            widget.destroy()

def main():
    root = tk.Tk()
    juego = JuegoGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
