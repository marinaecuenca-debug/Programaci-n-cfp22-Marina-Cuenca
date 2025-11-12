import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
import random
import os

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="ecommerce_db"
)
cursor = db.cursor(dictionary=True)


class Usuario:
    def __init__(self, nombre, contraseña, admin=False):
        self.nombre = nombre
        self.contraseña = contraseña
        self.admin = admin


        

class EcommerceApp:
    def __init__(self):
        self.usuarios = [Usuario("admin", "admin123", True)]
        self.productos = []
        self.carritos = {} 
        self.intentos_login = 3
        self.usuario_actual = None

        self.ventana_principal = tk.Tk()
        self.ventana_principal.title("Ecommerce - Menú Principal")
        self.ventana_principal.geometry("400x400")
        self.ventana_principal.withdraw()
        
        try:
            icono = tk.PhotoImage(file="icono-ecommerce.png")
            self.ventana_principal.iconphoto(True, icono)
        except:
            pass  

        self.ventana_login = tk.Toplevel()
        self.ventana_login.title("Login")

        self.cuadro_login()

    def cuadro_login(self):
        self.login = tk.Frame(self.ventana_login)
        self.login.grid(row=0, column=0, padx=20, pady=20)

        tk.Label(self.login, text="Nombre:").grid(row=0, column=0, sticky="e", pady=5)
        self.nombre = tk.StringVar()
        self.entry_nombre = tk.Entry(self.login, textvariable=self.nombre)
        self.entry_nombre.grid(row=0, column=1, pady=5)

        tk.Label(self.login, text="Contraseña:").grid(row=1, column=0, sticky="e", pady=5)
        self.contraseña = tk.StringVar()
        self.entry_contraseña = tk.Entry(self.login, show="*", textvariable=self.contraseña)
        self.entry_contraseña.grid(row=1, column=1, pady=5)

        tk.Button(self.login, text="Ingresar", command=self.ingresar, background="green", fg="white").grid(row=2, column=0, pady=10)
        tk.Button(self.login, text="Registrarse", command=self.registrar, background="blue", fg="white").grid(row=2, column=1, pady=10)

    def ingresar(self):
        nombre = self.nombre.get()
        contraseña = self.contraseña.get()
        for usuario in self.usuarios:
            if usuario.nombre == nombre and usuario.contraseña == contraseña:
                self.usuario_actual = usuario
                self.ventana_principal.deiconify()
                self.mostrar_menu()
                self.ventana_login.destroy()
                return
        
        self.intentos_login -= 1
        if self.intentos_login > 0:
            self.mensaje_login(f"⚠️ Usuario o contraseña incorrectos. Te quedan {self.intentos_login} intentos")
        else:
            self.mensaje_login("❌ Te quedaste sin intentos. Esta ventana se autodestruirá en 3...2...1...💣")
            self.ventana_login.after(3000, self.cerrar_aplicacion)

    def registrar(self):
        nombre = self.nombre.get()
        contraseña = self.contraseña.get()
        if not (nombre and contraseña):
            self.mensaje_login("⚠️ Completa ambos campos")
            return
            
        for usuario in self.usuarios:
            if usuario.nombre.lower() == nombre.lower():
                self.mensaje_login("⚠️ Este usuario ya existe")
                return

        nuevo_usuario = Usuario(nombre, contraseña)
        self.usuarios.append(nuevo_usuario)
        
        if hasattr(self, 'nombre') and hasattr(self, 'contraseña'):
            self.nombre.set("")
            self.contraseña.set("")
        self.mensaje_login("✅ Usuario registrado. Podes iniciar sesión")

    def mensaje_login(self, texto):
        for elemento in self.login.grid_slaves():#me trae los elementos en el grid y despues busco con el if el que quiero eliminar
            if self.obtener_elemento(elemento) == 3:
                elemento.destroy()
        
        tk.Label(self.login, text=texto).grid(row=3, column=0, columnspan=2, pady=5)

    def mostrar_menu(self):
        
        if hasattr(self, 'menu'):
            self.menu.destroy()
        self.menu = tk.Frame(self.ventana_principal)
        self.menu.pack(padx=20, pady=20)

        titulo = "✍️ Panel de Administración" if self.usuario_actual.admin else "🛒 Menú de Compras"
        tk.Label(self.menu, text=titulo, font=("Arial", 14)).pack(pady=10)
        tk.Label(self.menu, 
                text=f"Bienvenida: {self.usuario_actual.nombre}!",
                font=("Arial", 10, "italic")).pack(pady=5)

        opciones_admin = [
            ("Agregar productos", self.formulario_producto, "#1976D2", "white"),
            ("Visualizar productos", self.visualizar_productos, "#0288D1", "white"),
            ("Eliminar producto", self.eliminar_producto, "#D32F2F", "white"),
            ("Cerrar sesión", self.cerrar_sesion, "gray", "white"),
            ("Salir", self.salir, "black", "white")
        ]

        opciones_usuario = [
            ("Comprar", self.comprar, "#388E3C", "white"),
            ("Ver mi carrito", self.ver_carrito, "#FBC02D", "black"),
            ("Cerrar sesión", self.cerrar_sesion, "gray", "white"),
            ("Salir", self.salir, "black", "white")
        ]

        opciones = opciones_admin if self.usuario_actual.admin else opciones_usuario

        for texto, comando, bg, fg in opciones:
            tk.Button(self.menu, text=texto, width=30, command=comando, background=bg, fg=fg, font=("Arial", 11, "bold")).pack(pady=5)

    def ocultar_menu(self):
        if hasattr(self, 'menu'): #verifica si el objeto self tiene un atributo llamado menu, y si existe se oculta el widget menu de la interfaz. 
            self.menu.pack_forget()#elimina el menu de la vista, lo oculta, no lo destruye, se puede volver a mostrarse con .pack()

    def formulario_producto(self):
        self.ocultar_menu()
        self.ventana_formulario = tk.Frame(self.ventana_principal)
        self.ventana_formulario.pack(padx=20, pady=20)

        tk.Label(self.ventana_formulario, text="Agregar Producto", font=("Arial", 14)).grid(row=0, column=0, columnspan=2, pady=10)

        tk.Label(self.ventana_formulario, text="Nombre:").grid(row=1, column=0, sticky="e")
        self.ing_prod = tk.Entry(self.ventana_formulario)
        self.ing_prod.grid(row=1, column=1)

        tk.Label(self.ventana_formulario, text="Categoría:").grid(row=2, column=0, sticky="e")
        self.ing_categoria = tk.Entry(self.ventana_formulario)
        self.ing_categoria.grid(row=2, column=1)

        tk.Label(self.ventana_formulario, text="Stock:").grid(row=3, column=0, sticky="e")
        self.ing_stock = tk.Entry(self.ventana_formulario)
        self.ing_stock.grid(row=3, column=1)

        tk.Label(self.ventana_formulario, text="Precio:").grid(row=4, column=0, sticky="e")
        self.ing_precio = tk.Entry(self.ventana_formulario)
        self.ing_precio.grid(row=4, column=1)

        tk.Button(self.ventana_formulario, text="Guardar", command=self.guardar_producto, background="green", fg="white").grid(row=5, column=0, pady=10, padx=5)
        tk.Button(self.ventana_formulario, text="Volver", command=self.volver_menu, background="gray", fg="white").grid(row=5, column=1, pady=10, padx=5)
        
        self.mensaje_formulario = tk.Label(self.ventana_formulario, text="", fg="green")
        self.mensaje_formulario.grid(row=6, column=0, columnspan=2)

    def guardar_producto(self):
        nombre = self.ing_prod.get().strip()
        categoria = self.ing_categoria.get().strip()
        stock = self.ing_stock.get().strip()
        precio = self.ing_precio.get().strip()
        
        if not (nombre and categoria and stock and precio):
            self.mensaje_formulario.config(text="⚠️ Completa todos los campos", fg="red")
            return

        if not self.es_numero_entero(stock):
            self.mensaje_formulario.config(text="⚠️ Stock debe ser un número entero", fg="red")
            return
        
        stock_int = int(stock)
        if stock_int < 0:
            self.mensaje_formulario.config(text="⚠️ El stock no puede ser negativo", fg="red")
            return

        if not self.es_numero_decimal(precio):
            self.mensaje_formulario.config(text="⚠️ Precio debe ser un número", fg="red")
            return
        
        precio_f = float(precio)
        if precio_f <= 0:
            self.mensaje_formulario.config(text="⚠️ El precio debe ser mayor a 0", fg="red")
            return

        self.productos.append({
            "nombre": nombre,
            "categoria": categoria,
            "stock": stock_int,
            "precio": precio_f
        })
        print(f"Producto agregado: {nombre}, Categoria: {categoria}, Stock: {stock_int}, Precio: {precio_f}")

        
        self.ing_prod.delete(0, tk.END)# Limpia los campos despues de guardar el producto
        self.ing_categoria.delete(0, tk.END)
        self.ing_stock.delete(0, tk.END)
        self.ing_precio.delete(0, tk.END)
        self.mensaje_formulario.config(text="✅ Producto agregado con éxito!", fg="green")

    def obtener_elemento(self, elemento):
        return elemento.grid_info()["row"]

        

    def volver_menu(self):
        self.ventana_formulario.pack_forget()
        self.mostrar_menu()

    def visualizar_productos(self):
        self.ocultar_menu()
        vent_mostrar_prod = tk.Frame(self.ventana_principal)
        vent_mostrar_prod.pack(padx=20, pady=20, fill='both', expand=True)
        
        tk.Label(vent_mostrar_prod, text="Lista de productos", font=("Arial", 14)).pack(pady=10)
        
        
        frame_lista = tk.Frame(vent_mostrar_prod, relief="sunken", bd=2)# estilo del borde
        frame_lista.pack(fill='both', expand=True, pady=10)
        
       
        scrollbar = tk.Scrollbar(frame_lista)#scrollbar
        scrollbar.pack(side="right", fill="y")
        
        
        listbox = tk.Listbox(frame_lista, yscrollcommand=scrollbar.set, height=12, font=("Courier", 10))
        listbox.pack(side="left", fill="both", expand=True)#listbox
        
        scrollbar.config(command=listbox.yview)
        
        
        if not self.productos:
            listbox.insert(tk.END, "No hay productos registrados")
        else:
            for p in self.productos:
                listbox.insert(tk.END, "="*50)
                listbox.insert(tk.END, f"  Producto: {p['nombre']}")
                listbox.insert(tk.END, f"  Categoría: {p['categoria']}")
                listbox.insert(tk.END, f"  Stock: {p['stock']}")
                listbox.insert(tk.END, f"  Precio: ${p['precio']}")
                listbox.insert(tk.END, "="*50)
                listbox.insert(tk.END, "")
        
        def volve_de_vista():
            vent_mostrar_prod.pack_forget()
            self.mostrar_menu()

        tk.Button(vent_mostrar_prod, text="Volver", command=volve_de_vista, bg="gray", fg="white", font=("Arial", 11)).pack(pady=10)

    def modificar_producto(self):
        print("Modificar producto")

    def buscar_producto(self):
        print("Buscar producto")

    def eliminar_producto(self):
        if not self.usuario_actual.admin:
            return
            
        self.ocultar_menu()
        vent_borrar_prod = tk.Frame(self.ventana_principal)
        vent_borrar_prod.pack(padx=20, pady=20)

        tk.Label(vent_borrar_prod, text="Eliminar Productos", font=("Arial", 14)).pack(pady=10)

        if not self.productos:
            tk.Label(vent_borrar_prod, text="No hay productos para eliminar").pack(pady=10)
        else:
            for i, p in enumerate(self.productos):
                contenedor_producto = tk.Frame(vent_borrar_prod)
                contenedor_producto.pack(fill='x', pady=5)
                
                tk.Label(contenedor_producto, 
                        text=f"{p['nombre']} - ${p['precio']} (Stock: {p['stock']})").pack(side='left')
                
                def eliminar_prod(indice=i):
                    self.confirmar_eliminacion(vent_borrar_prod, indice)

                tk.Button(contenedor_producto, text="❌ Eliminar",
                         command=eliminar_prod,
                         background="red", fg="white").pack(side='right')

        def volver_desde_eliminar():
            vent_borrar_prod.destroy()
            self.mostrar_menu()

        tk.Button(vent_borrar_prod, text="Volver",
                 command=volver_desde_eliminar,
                 background="gray", fg="white").pack(pady=10)

    def confirmar_eliminacion(self, vent_borrar_prod, indice):
        producto = self.productos[indice]
        if self.preguntar_si_o_no("Confirmar eliminación", 
                                f"¿Estás segura de eliminar {producto['nombre']}?"):
            del self.productos[indice]
            vent_borrar_prod.destroy()
            self.mostrar_menu()

    def ver_carrito(self):
        self.ocultar_menu()
        ventana_carrito = tk.Frame(self.ventana_principal)
        ventana_carrito.pack(padx=20, pady=20)

        tk.Label(ventana_carrito, text="🛒 Tu Carrito", font=("Arial", 14)).pack(pady=10)
        carrito_usuario = self.carritos.get(self.usuario_actual.nombre, [])

        if not carrito_usuario:
            tk.Label(ventana_carrito, text="El carrito está vacío").pack(pady=10)
        else:
            
            agregado = {}
            for item in carrito_usuario:
                nombre = item['nombre']
                if nombre not in agregado:
                    agregado[nombre] = {'cantidad': 0, 'precio': item['precio']}
                agregado[nombre]['cantidad'] += item['cantidad']

            total = 0
            for nombre, info in agregado.items():
                contenedor_item = tk.Frame(ventana_carrito)
                contenedor_item.pack(fill='x', pady=5)
                subtotal = info['precio'] * info['cantidad']
                total += subtotal
                tk.Label(contenedor_item, text=f"{nombre} - Cantidad: {info['cantidad']} - Subtotal: ${subtotal:.2f}").pack()

            tk.Label(ventana_carrito, text=f"Total a pagar: ${total:.2f}", font=("Arial", 12, "bold")).pack(pady=10)

            def finalizar_btn():
                self.finalizar_compra(ventana_carrito)

            tk.Button(ventana_carrito, text="Finalizar Compra ✅", command=finalizar_btn, background="#388E3C", fg="white", font=("Arial", 11, "bold")).pack(pady=5)
            

        def volver_carrito():
            ventana_carrito.destroy()
            self.mostrar_menu()

        tk.Button(ventana_carrito, text="Volver",
                 command=volver_carrito,
                 background="gray", fg="white").pack(pady=5)

    def agregar_al_carrito(self, ventana_comprar):
        alguno_agregado = False
        errores = []

        if self.usuario_actual.nombre not in self.carritos:
            self.carritos[self.usuario_actual.nombre] = []

        for producto in self.productos:
            if 'cantidad_var' in producto:
                texto_cantidad = producto['cantidad_var'].get().strip()
                if texto_cantidad:
                    try:
                        cantidad = int(texto_cantidad)
                    except ValueError:
                        errores.append(f"⚠️ Cantidad inválida para {producto['nombre']}")
                        continue

                    if cantidad <= 0:
                        errores.append(f"⚠️ La cantidad debe ser mayor a 0 para {producto['nombre']}")
                        continue

                    if cantidad > producto['stock']:
                        errores.append(f"⚠️ Stock insuficiente para {producto['nombre']}. Disponible: {producto['stock']}")
                        continue

                    
                    self.carritos[self.usuario_actual.nombre].append({
                        'nombre': producto['nombre'],
                        'cantidad': cantidad,
                        'precio': producto['precio']
                    })
                    producto['stock'] -= cantidad
                    alguno_agregado = True
        
        if alguno_agregado:
            ventana_comprar.destroy()
            self.mostrar_menu()
        else:
            self.limpiar_mensajes(ventana_comprar)
            self.mostrar_mensajes(ventana_comprar, errores)



    def finalizar_compra(self, ventana_carrito):
        carrito_usuario = self.carritos.get(self.usuario_actual.nombre, [])
        if not carrito_usuario:
            return

        total = sum(item['precio'] * item['cantidad'] for item in carrito_usuario)

        if self.preguntar_si_o_no("Confirmar compra", f"¿Finalizar la compra?\nTotal a pagar: ${total:.2f}"):
            fecha_factura = datetime.now().strftime('%d/%m/%Y')#paso la fecha a cadena de texto
            identificador_factura = 'F' + str(random.randint(1000000, 9999999))

            
            factura_contenido = f"""========================================
                    FACTURA
========================================
Ecommerce TuMercado S.A.
Calle Falsa N30 CP 21020
B32312312
Fecha: {fecha_factura}

Número Factura: {identificador_factura}

----------------------------------------
Datos del Cliente:
Nombre: {self.usuario_actual.nombre}
Ciudad: Buenos Aires

----------------------------------------
Detalles de la Compra:
"""

            for item in carrito_usuario:
                subtotal = item['precio'] * item['cantidad']
                factura_contenido += f"- {item['nombre']} x{item['cantidad']} = ${subtotal:.2f}\n"

            factura_contenido += "\n----------------------------------------\n"
            factura_contenido += f"TOTAL: ${total:.2f}\n\n"
            factura_contenido += "¡Gracias por su compra!\n========================================"

            
            ruta_carpeta = r"C:\Users\u544811\Downloads\Programacion\Ecommerce"
            self.crear_carpeta_si_no_existe(ruta_carpeta, exist_ok=True)
            nombre_archivo = f"Factura_{self.usuario_actual.nombre}_{identificador_factura}.txt"
            ruta_completa = os.path.join(ruta_carpeta, nombre_archivo)
            
            with open(ruta_completa, 'w', encoding='utf-8') as archivo:
                archivo.write(factura_contenido)

            
            self.abrir_archivo(ruta_completa)

            
            self.carritos[self.usuario_actual.nombre] = []
            self.mostrar_mensaje_informativo("Compra exitosa", f"Gracias por tu compra!\nFactura guardada en:\n{ruta_completa}")
            ventana_carrito.destroy()
            self.mostrar_menu()

    def comprar(self):
        self.ocultar_menu()
        ventana_comprar = tk.Frame(self.ventana_principal)
        ventana_comprar.pack(padx=20, pady=20)

        tk.Label(ventana_comprar, text="Realizar Compra", font=("Arial", 14)).pack(pady=10)

        contenedor_lista_productos = tk.Frame(ventana_comprar)
        contenedor_lista_productos.pack(pady=10)

        tk.Label(contenedor_lista_productos, text="Productos disponibles:").pack()

        for i, p in enumerate(self.productos):
            if p['stock'] > 0: 
                contenedor_producto = tk.Frame(contenedor_lista_productos)
                contenedor_producto.pack(fill='x', pady=5)
                
                tk.Label(contenedor_producto, text=f"{p['nombre']} - ${p['precio']} (Stock: {p['stock']})").pack(side='left')
                
                
                cantidad_var = tk.StringVar()
                cantidad_spinbox = tk.Spinbox(contenedor_producto, from_=0, to=p['stock'], width=5, textvariable=cantidad_var)
                cantidad_spinbox.pack(side='right')

                
                subtotal_label = tk.Label(contenedor_producto, text="Subtotal: $0.00", font=("Arial", 10, "bold"), fg="#2E8B57")
                subtotal_label.pack(side='right', padx=8)

                
                p['cantidad_var'] = cantidad_var
                p['subtotal_label'] = subtotal_label

                #para actualizar subtotal automticamente
                def actualizar_subtotal(name=None, index=None, mode=None, producto=p):
                    try:
                        cantidad_texto = producto['cantidad_var'].get().strip()
                        if cantidad_texto and cantidad_texto.isdigit():
                            cantidad = int(cantidad_texto)
                            if cantidad > 0:
                                subtotal = cantidad * producto['precio']
                                producto['subtotal_label'].config(text=f"Subtotal: ${subtotal:.2f}")
                            else:
                                producto['subtotal_label'].config(text="Subtotal: $0.00")
                        else:
                            producto['subtotal_label'].config(text="Subtotal: $0.00")
                    except:
                        producto['subtotal_label'].config(text="Subtotal: $0.00")

                
                cantidad_var.trace('w', actualizar_subtotal)#trace mira si hay cambios y lo actualiza

        
        def boton_agregar_carrito():
            self.agregar_al_carrito(ventana_comprar)

        tk.Button(ventana_comprar, text="Agregar al Carrito 🛒",
         command=boton_agregar_carrito,
         background="#FBC02D", fg="black", font=("Arial", 11, "bold")).pack(pady=10)
        
        
        def regresar_desde_compra():
            ventana_comprar.destroy()
            self.mostrar_menu()

        tk.Button(ventana_comprar, text="Volver",
                 command=regresar_desde_compra,
                 background="gray", fg="white").pack()



    def salir(self):
        self.ventana_principal.destroy()

    def cerrar_aplicacion(self):
        if self.tiene_atributo(self, 'ventana_principal'):
            self.ventana_principal.destroy()
        if self.tiene_atributo(self, 'ventana_login'):
            self.ventana_login.destroy()

    def cerrar_sesion(self):
        self.usuario_actual = None
        self.ventana_principal.withdraw()
        
        self.ventana_login = tk.Toplevel()
        self.ventana_login.title("Login")
        self.intentos_login = 3

        self.cuadro_login()

    
    def preguntar_si_o_no(self, titulo, mensaje):
        return messagebox.askyesno(titulo, mensaje)
    
    def mostrar_mensaje_informativo(self, titulo, mensaje):
        return messagebox.showinfo(titulo, mensaje)
    
    def crear_carpeta_si_no_existe(self, ruta, exist_ok=True):
        return os.makedirs(ruta, exist_ok=exist_ok)#crea la carpeta si no existe
    
    def abrir_archivo(self, ruta):
        return os.startfile(ruta)
    
    def tiene_atributo(self, objeto, nombre_atributo):
        return hasattr(objeto, nombre_atributo)
    
    def es_tipo_etiqueta(self, elemento, tipo_esperado):
        return isinstance(elemento, tipo_esperado)
    
    def es_numero_entero(self, texto):
        if texto.isdigit():
            return True
        if texto.startswith('-') and texto[1:].isdigit():
            return True
        return False
    
    def es_numero_decimal(self, texto):
        try:
            float(texto)
            return True
        except ValueError:
            return False
    
    def limpiar_mensajes(self, ventana):
        for elemento in ventana.winfo_children():
            if isinstance(elemento, tk.Label) and elemento.cget("fg") == "red":
                elemento.destroy()
    
    def mostrar_mensajes(self, ventana, errores):
        if errores:
            mensaje = ""
            for error in errores:
                mensaje = mensaje + error + "\n"
            mensaje = mensaje.strip() 
        else:
            mensaje = "⚠️ Ingresa al menos una cantidad"
        
        tk.Label(ventana, text=mensaje, fg="red").pack()


app = EcommerceApp()
app.ventana_principal.mainloop()

