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
 
# Exepciones personalizadas
class ErrorSistemaFJ(Exception):
    """Clase base para todas las excepciones del Software FJ"""
    pass

class ErrorDatosInvalidos(ErrorSistemaFJ):
    """cuando los datos de entrada no cumplen los requisitos"""
    pass

class ErrorOperacionInvalida(ErrorSistemaFJ):
    """cuando se intenta realizar una acción no permitida"""
    pass

#---1 Creacion de plantilla del cliente---  
class Cliente:
    def __init__(self, id_cliente, nombre, correo):
        # seguridad: validamos si el correo está bien (@)
        if "@" not in correo:
            logging.error(f"Intento fallido de registro de cliente: Correo '{correo}' no válido.")
            raise ErrorDatosInvalidos("¡Error de datos! El correo electrónico debe incluir un @. ")
        
        # Si el correo está bien, el programa continúa y guarda los datos:
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.correo = correo

#--- 2 plantilla general de servicios---
from abc import ABC, abstractmethod

class Servicio(ABC):
    def __init__(self, codigo, nombre, costo_base):
        # Validación de seguridad no costos en cero o negativos
        if costo_base <= 0:
            logging.error(f"Intento de crear servicio '{nombre}' con costo inválido: {costo_base}")
            raise ErrorDatosInvalidos("¡Error! El costo base del servicio debe ser mayor a cero.") 
        
        self.codigo = codigo
        self.nombre = nombre
        self.costo_base = costo_base

    @abstractmethod 
    def calcular_costo(self, cantidad, descuento=0.0):
        pass

    @abstractmethod
    def obtener_descripcion(self):
        pass

# Clases hijas 
class ReservaSala(Servicio):
    def calcular_costo(self, horas, descuento=0.0):
        # horas por el costo base menos el descuento 
        costo_total = (self.costo_base * horas) * (1 - descuento)
        return costo_total

    def obtener_descripcion(self):
        return f"Reserva de Sala de Juntas o Espacios Físicos (Código: {self.codigo})"

class AlquilerEquipo(Servicio):
    def calcular_costo(self, dias, descuento=0.0):
        # Los equipos cobran días, aplican descuento opcional y suman el 19% de IVA
        costo_con_descuento = (self.costo_base * dias) * (1 - descuento)
        return costo_con_descuento * 1.19  
    
    def obtener_descripcion(self):
        return f"Alquiler de Equipos Tecnológicos y Cómputo (Código: {self.codigo})"
    
class AsesoriaEspecializada(Servicio):
    def calcular_costo(self, sesiones, descuento=0.0):
        #multiplica costo base por el numero de sesiones agendadas
        costo_total = (self.costo_base * sesiones) * (1 - descuento)
        return costo_total

    def obtener_descripcion(self):
        return f"Asesoría Técnica Especializada en Sistemas (Código: {self.codigo})"
    
#---3 bloque de reservas---
class Reserva:
    def __init__(self, id_reserva, cliente, servicio, duracion):
        # Validación la duracion no puede ser cero ni negativa
        if duracion <= 0:
            logging.error(f"Intento de reserva {id_reserva} con duración inválida: {duracion}")
            raise ErrorDatosInvalidos("¡Error! La duración de la reserva debe ser mayor a cero.")
            
        self.id_reserva = id_reserva
        self.cliente = cliente      #  guardamos el objeto Cliente completo
        self.servicio = servicio    # guardamos el objeto Servicio completo
        self.duracion = duracion
        self.estado = "Pendiente"   # Toda reserva nace en estado 'Pendiente'

    def confirmar_reserva(self):
        # Validaciones no se confirma algo ya confirmado o que este cancelado 
        if self.estado == "Confirmada":
            logging.error(f"Intento fallido: La reserva {self.id_reserva} ya estaba confirmada.")
            raise ErrorOperacionInvalida(f"¡Operación inválida! La reserva {self.id_reserva} ya se encuentra confirmada.")
        if self.estado == "Cancelada":
            raise ErrorOperacionInvalida("No se puede confirmar una reserva que ya fue Cancelada.")
            
        self.estado = "Confirmada"

    def cancelar_reserva(self):
        #permite cancelar la reserva 
        if self.estado == "Cancelada":
            raise ErrorOperacionInvalida(f"La reserva {self.id_reserva} ya se encuentra cancelada.")
            
        self.estado = "Cancelada"

#---4 interaz grafica---
import tkinter as tk
from tkinter import messagebox

class InterfazApp:
    def __init__(self, ventana_principal):
        self.ventana = ventana_principal
        self.ventana.title("Software FJ - Control de gestion")
        self.ventana.geometry("650x450")

        self.clientes_registrados = []
        self.reserva_actual = None 

        # --- CONTENEDOR COLUMNA IZQUIERDA ---
        columna_izquierda = tk.Frame(ventana_principal)
        columna_izquierda.pack(side="left", fill="both", expand=True, padx=20, pady=10)

        # --- SECCIÓN 1: CLIENTES 
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

        # --- SECCIÓN 2: SERVICIOS 
        tk.Label(columna_derecha, text="REGISTRO DE SERVICIOS", font=("Arial", 11, "bold")).pack(pady=5)
        
        tk.Label(columna_derecha, text="Código Servicio:").pack()
        self.entrada_cod_serv = tk.Entry(columna_derecha)
        self.entrada_cod_serv.pack(pady=2)

        tk.Label(columna_derecha, text="Costo Base ($):").pack()
        self.entrada_costo = tk.Entry(columna_derecha)
        self.entrada_costo.pack(pady=2)

        tk.Button(columna_derecha, text="Guardar Servicio", bg="#2196F3", fg="white", command=self.procesar_servicio).pack(pady=5)

        # --- SECCIÓN 3: RESERVAS 
        tk.Label(columna_derecha, text="GESTION DE RESERVAS", font=("Arial", 11, "bold")).pack(pady=5)
        
        tk.Label(columna_derecha, text="ID Reserva:").pack()
        self.entrada_id_reserva = tk.Entry(columna_derecha)
        self.entrada_id_reserva.pack(pady=2)
        
        tk.Label(columna_derecha, text="Duracion (Horas/Dias):").pack()
        self.entrada_duracion = tk.Entry(columna_derecha)
        self.entrada_duracion.pack(pady=2)


        tk.Button(columna_derecha, text="1. Crear Reserva", bg="#FF9800", fg="white", command=self.procesar_reserva).pack(pady=3)
        tk.Button(columna_derecha, text="2. Confirmar Reserva", bg="#9C27B0", fg="white", command=self.procesar_confirmacion).pack(pady=3)
        tk.Button(columna_derecha, text="3. Ejecutar Simulación (10 Op)", bg="#E91E63", fg="white", command=self.ejecutar_simulacion_guia).pack(pady=10)

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

        except ErrorDatosInvalidos as error_detectado:
            messagebox.showerror("Error de Validación", str(error_detectado))

    def procesar_servicio(self):
        try:
            cod_txt = self.entrada_cod_serv.get()
            costo_num = int(self.entrada_costo.get())

            #servicio de prueba 
            nuevo_servicio = ReservaSala(cod_txt, "Sala de Juntas", costo_num)
            messagebox.showinfo("Éxito", f"¡Servicio guardado!\nCosto Base: ${nuevo_servicio.costo_base}")
            
            self.entrada_cod_serv.delete(0, tk.END)
            self.entrada_costo.delete(0, tk.END)

        except ValueError:
            messagebox.showerror("Error de Costo", "¡Error! El costo debe ser un número válido.")
        except ErrorDatosInvalidos as error_detectado:
            messagebox.showerror("Error de Validación", str(error_detectado))

    def procesar_reserva(self):
        try:
            id_res = self.entrada_id_reserva.get()
            duracion_num = int(self.entrada_duracion.get())

            #Datos simulados 
            cliente_temp = Cliente("T01", "Usuario Prueba", "prueba@unad.edu.co")
            servicio_temp = ReservaSala("S_TEMP", "Sala General", 40000)

            self.reserva_actual = Reserva(id_res, cliente_temp, servicio_temp, duracion_num)
            messagebox.showinfo("Éxito", f"¡Reserva {self.reserva_actual.id_reserva} creada!\nEstado: {self.reserva_actual.estado}")
            
        except ValueError:
            messagebox.showerror("Error de Duración", "¡Error! La duración debe ser un número válido.")
        except ErrorDatosInvalidos as error_detectado:
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
            
        except ErrorOperacionInvalida as error_detectado:
            messagebox.showerror("Error de Operación", str(error_detectado))


# Simulacion automatica 
    def ejecutar_simulacion_guia(self):
        """Simula automáticamente las 10 operaciones """
        reporte = "--- INICIO DE SIMULACIÓN (10 OPERACIONES) ---\n\n"
        logging.info("Iniciando simulación automática de 10 operaciones.")
        
        # Objetos base para las pruebas cruzadas
        c_valido = Cliente("C01", "Ana Maria", "ana@unad.edu.co")
        s_valido = ReservaSala("S01", "Sala A", 50000)

        # Matriz de operaciones completas (Válidas e Inválidas)
        operaciones = [
            ("1. Registro Cliente Válido", lambda: Cliente("C10", "Pedro", "pedro@mail.com")),
            ("2. Registro Cliente Inválido (Sin @)", lambda: Cliente("C11", "Luis", "luis.com")),
            ("3. Creación Servicio Válido", lambda: AlquilerEquipo("E01", "Portátil", 30000)),
            ("4. Creación Servicio Inválido (Costo <= 0)", lambda: ReservaSala("S02", "Sala VIP", -500)),
            ("5. Reserva Válida", lambda: Reserva("R10", c_valido, s_valido, 4)),
            ("6. Reserva Inválida (Duración 0)", lambda: Reserva("R11", c_valido, s_valido, 0)),
            ("7. Flujo Completo Confirmación", lambda: Reserva("R12", c_valido, s_valido, 2).confirmar_reserva()),
            ("8. Error Operación (Confirmar Duplicado)", lambda: self._simular_duplicado(c_valido, s_valido)),
            ("9. Cancelación de Reserva Válida", lambda: Reserva("R14", c_valido, s_valido, 3).cancelar_reserva()),
            ("10. Encadenamiento de Excepciones Avanzado", lambda: self._simular_encadenamiento())
        ]

        for nombre, operacion in operaciones:
            # Estructura avanzada de control try-except-else-finally
            try:
                operacion()
            except ErrorSistemaFJ as e:
                reporte += f"❌ {nombre}: Fallo esperado capturado -> {e}\n"
            except Exception as e:
                reporte += f"❌ {nombre}: Error genérico -> {e}\n"
            else:
                reporte += f"✅ {nombre}: Ejecutada con éxito absoluto.\n"
            finally:
                logging.info(f"Operación evaluada en simulación: {nombre}")

        messagebox.showinfo("Resultados", "Simulación de 10 operaciones completada. Revisa la terminal y el archivo .log.")
        print(reporte)

    def _simular_duplicado(self, c, s):
        #forzamos a intentar confirmar una reserva confirmada
        res = Reserva("R13", c, s, 2)
        res.confirmar_reserva()
        res.confirmar_reserva()  # Fuerza el error de duplicado

    def _simular_encadenamiento(self):
        try:
            resultado = 10 / 0  # Fuerza error nativo
        except ZeroDivisionError as error_origen:
            logging.error("Encadenamiento de excepciones ejecutado en simulación.")
            # Uso estricto del raise 
            raise ErrorOperacionInvalida("Cálculo inconsistente detectado en el sistema") from error_origen        

if __name__ == "__main__":
    raiz = tk.Tk()
    mi_aplicacion = InterfazApp(raiz)
    raiz.mainloop()        