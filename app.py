#Desarrollado por:Ana Maria Rodriguez Alfonso
#Curso: Programacion (213023_44)-UNAD

#---ESTA LIBRERIA SE ENCARGA DE GUARDAR EL ARCHIVO DE TEXTO---
import logging

# configuracion para que cree el archivo "sistema_gestion.log"
logging.basicConfig(
    filename=r"c:\Users\anita\OneDrive\Escritorio\UNAD\TERCER SEMESTRE UNAD\PROGRAMACION\sistema_gestion.log",
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
 
#---1 Creacion de plantilla del cliente--- 
class Cliente:
    def __init__(self,id_cliente,nombre,correo):
        #seguridad:validamos si el correo esta bien (@)
        if"@" not in correo:
            logging.error(f"Intento fallido de registro de cliente: Correo '{correo}' no válido.")
            #excepcion
            raise ValueError("¡Error de datos! El correo electronico debe incluir un @. ")
        
        #Si el correo esta bien , el programa continua y guarda los datos:
        self.id_cliente= id_cliente
        self.nombre= nombre
        self.correo= correo

#--- 2 plantilla general de servicios---
from abc import ABC, abstractmethod

class Servicio (ABC):
    def __init__(self,codigo,nombre,costo_base):
        #validacion de seguridad : el costo  no puede ser cero ni negativo
        if costo_base <=0:
            logging.error(f"Intento de crear servicio '{nombre}' con costo inválido: {costo_base}")
            raise ValueError("¡Error! El costo base del servicio debe ser mayor a cero.") 
        
        self.codigo= codigo
        self.nombre= nombre
        self.costo_base= costo_base

    @abstractmethod 
    def calcular_costo(self,cantidad):
        pass

# clases hijas
class ReservaSala(Servicio):
    def calcular_costo(self, horas):
        # Las salas se cobran por horas
        return self.costo_base * horas

class AlquilerEquipo(Servicio):
    def calcular_costo(self, dias):
        # Los equipos se cobran por dias y se les suma el 19% de IVA obligatoriamente
        costo_sin_iva = self.costo_base * dias
        return costo_sin_iva * 1.19  
    
class AsesoriaEspecializada(Servicio):
    def calcular_costo(self, sesiones):
        return self.costo_base * sesiones
    
#---3 bloque de reservas---
class Reserva:
    def __init__(self, id_reserva, cliente, servicio, duracion):
        # Validación: la duración (horas o dias) debe ser mayor a cero
        if duracion <= 0:
            logging.error(f"Intento de reserva {id_reserva} con duración invalida: {duracion}")
            raise ValueError("¡Error! La duracion de la reserva debe ser mayor a cero.")
            
        self.id_reserva = id_reserva
        self.cliente = cliente      # Aqui guardamos el objeto Cliente completo
        self.servicio = servicio    # Aqui guardamos el objeto Servicio completo
        self.duracion = duracion
        self.estado = "Pendiente"   # Toda reserva nace en estado 'Pendiente'

    def confirmar_reserva(self):
        # Si ya esta confirmada, lanzamos un error para evitar duplicados
        if self.estado == "Confirmada":
            logging.error(f"Intento fallido: La reserva {self.id_reserva} ya estaba confirmada.")
            raise ValueError(f"¡Operación invalida! La reserva {self.id_reserva} ya se encuentra confirmada.")
            
        self.estado = "Confirmada"

#---4 interaz grafica---
import tkinter as tk
from tkinter import messagebox

class InterfazApp:
    def __init__(self, ventana_principal):
        self.ventana = ventana_principal
        self.ventana.title("Software FJ - Control de gestion")
        self.ventana.geometry("650x380")

        self.clientes_registrados = []
        self.reserva_actual = None 

        # --- CONTENEDOR COLUMNA IZQUIERDA ---
        columna_izquierda = tk.Frame(ventana_principal)
        columna_izquierda.pack(side="left", fill="both", expand=True, padx=20, pady=10)

        # --- SECCIÓN 1: CLIENTES (Va a la izquierda) ---
        tk.Label(columna_izquierda, text="REGISTRO DE CLIENTES", font=("Arial", 11, "bold")).pack(pady=5)

        tk.Label(columna_izquierda, text="ID Cliente:").pack()
        self.entrada_id = tk.Entry(columna_izquierda)
        self.entrada_id.pack(pady=2)

        tk.Label(columna_izquierda, text="Nombre completo:").pack()
        self.entrada_nombre = tk.Entry(columna_izquierda)
        self.entrada_nombre.pack(pady=2)

        tk.Label(columna_izquierda, text="Correo Electrónico:").pack()
        self.entrada_correo = tk.Entry(columna_izquierda)
        self.entrada_correo.pack(pady=2)

        tk.Button(columna_izquierda, text="Guardar Cliente", bg="#4CAF50", fg="white", command=self.procesar_cliente).pack(pady=10)


        # --- CONTENEDOR COLUMNA DERECHA ---
        columna_derecha = tk.Frame(ventana_principal)
        columna_derecha.pack(side="right", fill="both", expand=True, padx=20, pady=10)

        # --- SECCIÓN 2: SERVICIOS (Va a la derecha arriba) ---
        tk.Label(columna_derecha, text="REGISTRO DE SERVICIOS", font=("Arial", 11, "bold")).pack(pady=5)
        
        tk.Label(columna_derecha, text="Código Servicio:").pack()
        self.entrada_cod_serv = tk.Entry(columna_derecha)
        self.entrada_cod_serv.pack(pady=2)

        tk.Label(columna_derecha, text="Costo Base ($):").pack()
        self.entrada_costo = tk.Entry(columna_derecha)
        self.entrada_costo.pack(pady=2)

        tk.Button(columna_derecha, text="Guardar Servicio", bg="#2196F3", fg="white", command=self.procesar_servicio).pack(pady=5)

        # --- SECCIÓN 3: RESERVAS (Va a la derecha abajo) ---
        tk.Label(columna_derecha, text="GESTION DE RESERVAS", font=("Arial", 11, "bold")).pack(pady=5)
        
        tk.Label(columna_derecha, text="ID Reserva:").pack()
        self.entrada_id_reserva = tk.Entry(columna_derecha)
        self.entrada_id_reserva.pack(pady=2)
        
        tk.Label(columna_derecha, text="Duracion (Horas/Dias):").pack()
        self.entrada_duracion = tk.Entry(columna_derecha)
        self.entrada_duracion.pack(pady=2)

        tk.Button(columna_derecha, text="1. Crear Reserva", bg="#FF9800", fg="white", command=self.procesar_reserva).pack(pady=3)
        tk.Button(columna_derecha, text="2. Confirmar Reserva", bg="#9C27B0", fg="white", command=self.procesar_confirmacion).pack(pady=3)

    def procesar_cliente(self):
        try:
            id_txt = self.entrada_id.get()
            nombre_txt = self.entrada_nombre.get()
            correo_txt = self.entrada_correo.get()

            nuevo_cliente = Cliente(id_txt, nombre_txt, correo_txt)

            self.clientes_registrados.append(nuevo_cliente)

            messagebox.showinfo("Éxito", f"¡Cliente registrado!\nNombre: {nuevo_cliente.nombre}")
                                
            self.entrada_id.delete(0, tk.END)
            self.entrada_nombre.delete(0, tk.END)
            self.entrada_correo.delete(0, tk.END)

        except ValueError as error_detectado:
            messagebox.showerror("Error de Validación", str(error_detectado))

    def procesar_servicio(self):
        try:
            cod_txt = self.entrada_cod_serv.get()
            costo_num = int(self.entrada_costo.get())

            nuevo_servicio = ReservaSala(cod_txt, "Sala de Juntas", costo_num)
            
            messagebox.showinfo("Éxito", f"¡Servicio guardado!\nCosto Base: ${nuevo_servicio.costo_base}")
            
            self.entrada_cod_serv.delete(0, tk.END)
            self.entrada_costo.delete(0, tk.END)

        except ValueError as error_detectado:
            messagebox.showerror("Error de Costo", "¡Error! El costo debe ser un número mayor a cero.")

    def procesar_reserva(self):
        try:
            id_res = self.entrada_id_reserva.get()
            duracion_num = int(self.entrada_duracion.get())

            cliente_temp = Cliente("T01", "Usuario Prueba", "prueba@unad.edu.co")
            servicio_temp = ReservaSala("S_TEMP", "Sala General", 40000)

            self.reserva_actual = Reserva(id_res, cliente_temp, servicio_temp, duracion_num)
            messagebox.showinfo("Éxito", f"¡Reserva {self.reserva_actual.id_reserva} creada!\nEstado: {self.reserva_actual.estado}")
            
        except ValueError as error_detectado:
            messagebox.showerror("Error de Duración", str(error_detectado))

    def procesar_confirmacion(self):
        if self.reserva_actual is None:
            messagebox.showwarning("Atención", "Primero debes crear una reserva válida utilizando el botón naranja.")
            return

        try:
            self.reserva_actual.confirmar_reserva()
            messagebox.showinfo("Éxito", f"Reserva {self.reserva_actual.id_reserva} cambiada a: {self.reserva_actual.estado}")
            
            self.entrada_id_reserva.delete(0, tk.END)
            self.entrada_duracion.delete(0, tk.END)
            
        except ValueError as error_detectado:
            messagebox.showerror("Error de Operación", str(error_detectado))        

if __name__ == "__main__":
    raiz = tk.Tk()
    mi_aplicacion = InterfazApp(raiz)
    raiz.mainloop()        