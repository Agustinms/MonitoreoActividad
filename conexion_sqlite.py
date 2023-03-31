from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3





###Interfaz###

root  = Tk()
root.title("Monitoreo de actividad")
root.geometry("464x360")
root.resizable(False,False)

###Base de datos###

id = StringVar()
fecha = StringVar()
actividad = StringVar()
tiempo = StringVar()
detalle = StringVar()


def conexion_base():
    mi_conexion = sqlite3.connect("db.db")
    mi_cursor = mi_conexion.cursor()

    try:
        mi_cursor.execute('''
        CREATE TABLE actividad(
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        FECHA DATE NOT NULL,
        ACTIVIDAD VARCHAR(50) NOT NULL,
        TIEMPO FLOAT NOT NULL,
        DETALLE VARCHAR(50) NOT NULL
        )''')
        print("Base creada correctamente")
    except :
        print("Conexión realizada correctamente")


def eliminarBBDD():
    mi_conexion = sqlite3.connect("db.db")
    mi_cursor = mi_conexion.cursor()
    if messagebox.askyesno(message="Los datos se perderán permanentemente. ¿Desea continuar?"):
        mi_cursor.execute("DROP TABLE actividad")

def salirAplicacion():
    if messagebox.askyesno("Salir", "¿Salir de la aplicación?"):
        root.quit()
    
    limpiarCampos()
    mostrar()

def limpiarCampos():
    id.set("")
    fecha.set("")
    actividad.set("")
    tiempo.set("")
    detalle.set("")



def crear():
    mi_conexion = sqlite3.connect("db.db")
    mi_cursor = mi_conexion.cursor()

    try:
        datos = fecha.get(), actividad.get(), tiempo.get(), detalle.get()
        mi_cursor.execute("INSERT INTO actividad VALUES(NULL,?,?,?,?)", (datos))
        mi_conexion.commit()
    except:
        messagebox.showwarning("ADVERTENCIA", "Error al crear el registro. Verificar conexión con la base")
    limpiarCampos()
    mostrar()

def mostrar():
    mi_conexion = sqlite3.connect("db.db")
    mi_cursor = mi_conexion.cursor()
    registros = tree.get_children()
    for elemento in registros:
        tree.delete(elemento)
    try:
        mi_cursor.execute("SELECT * FROM actividad")
        for row in mi_cursor:
            tree.insert("", 0, text=row[0], values=(row[1], row[2], row[3], row[4]))
    except:
        pass 
###TABLA###

style=ttk.Style()
style.theme_use('clam')

tree = ttk.Treeview(height=10, columns=('#0', '#1', '#2', '#3'))

tree.column('#0',anchor=CENTER, stretch=NO, width=50)
tree.heading('#0', text="ID")
tree.column('#1',anchor=CENTER, stretch=NO, width=100)
tree.heading('#1', text="Fecha")
tree.column('#2',anchor=CENTER, stretch=NO, width=100)
tree.heading('#2', text="Actividad")
tree.column('#3',anchor=CENTER, stretch=NO, width=100)
tree.heading('#3', text="Tiempo(H)")
tree.column('#4',anchor=CENTER, stretch=NO, width=100)
tree.heading('#4', text="Detalle")

tree.place(x=5, y=127)

def seleccionarUsandoClick(event):
    item=tree.identify('item', event.x, event.y)
    id.set(tree.item(item,"text"))
    fecha.set(tree.item(item,"values")[0])
    actividad.set(tree.item(item,"values")[1])
    tiempo.set(tree.item(item,"values")[2])
    detalle.set(tree.item(item,"values")[3])

tree.bind("<Double-1>", seleccionarUsandoClick)



def actualizar():
    mi_conexion = sqlite3.connect("db.db")
    mi_cursor = mi_conexion.cursor()

    try:
        datos = fecha.get(), actividad.get(), tiempo.get(), detalle.get()
        mi_cursor.execute("UPDATE actividad SET FECHA=?, ACTIVIDAD=?,TIEMPO=?,DETALLE=? WHERE ID="+id.get(), (datos))
        mi_conexion.commit()
    except:
        messagebox.showwarning("ADVERTENCIA", "Error al actualizar el registro.")
    limpiarCampos()
    mostrar()


def borrar():
    mi_conexion = sqlite3.connect("db.db")
    mi_cursor = mi_conexion.cursor()

    try:
        if messagebox.askyesno(message="¿Eliminar registro?", title="ADVERTENCIA"):
            mi_cursor.execute("DELETE FROM actividad WHERE ID="+id.get())
            mi_conexion.commit()
    except:
         messagebox.showwarning("ADVERTENCIA", "Error al borrar el registro.")
         print(id.get())
    limpiarCampos()
    mostrar()



###Interfaz###

menubar = Menu(root)
menubasedat = Menu(menubar, tearoff=0)
menubasedat.add_command(label="Crear/Conectar Base de Datos", command=conexion_base)
menubasedat.add_command(label="Eliminar Base de Datos", command=eliminarBBDD)
menubasedat.add_command(label="Limpiar campos", command=limpiarCampos)
menubasedat.add_separator()
menubasedat.add_command(label="Salir", command=salirAplicacion)

menubar.add_cascade(label="Inicio", menu=menubasedat)

e1 = Entry(root, textvariable=id)


l2 = Label(root, text="Fecha")
l2.place(x=50, y=10)
e2 = Entry(root, textvariable=fecha, width=50)
e2.place(x=100, y=10)

l3 = Label(root, text="Actividad")
l3.place(x=220, y=10)
e3 = Entry(root, textvariable=actividad, width=25)
e3.place(x=275, y=10)

l4 = Label(root, text="Tiempo")
l4.place(x=50, y=50)
e4 = Entry(root, textvariable=tiempo, width=20)
e4.place(x=100, y=50)

l5 = Label(root, text="Detalle")
l5.place(x=220, y=50)
e5 = Entry(root, textvariable=detalle, width=25)
e5.place(x=275, y=50)

root.config(menu=menubar)

b1 = Button(root, text="Crear Registro",bg="green", fg="white", command=crear)
b1.place(x=10, y=90)
b2 = Button(root, text="Modificar Registro", bg="blue", fg="white", command=actualizar)
b2.place(x=110, y=90)
b3 = Button(root, text="Mostrar Lista", command=mostrar)
b3.place(x=235, y=90)
b4 = Button(root, text="Eliminar Registro", bg="red", fg="white", command=borrar)
b4.place(x=350, y=90)

#conexion_base()
root.mainloop()