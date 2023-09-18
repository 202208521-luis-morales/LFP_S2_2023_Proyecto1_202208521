from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from ProcessData import ProcessData
import json

root = Tk()

root.title("Proyecto 1 - 202208521")
frm = ttk.Frame(root, padding=10)
frm.grid()

ttk.Label(frm, text="Menú").grid(column=0, row=0)

options = ("Abrir", "Guardar", "Guardar Como...", "Salir")

selected_option = StringVar()
selected_option.set("Abrir")

ttk.Label(frm, text=" ", padding=3).grid(column=1, row=0)
textarea = Text(frm)
textarea.grid(column=2, row=0, rowspan=8)

route_current_json_file = StringVar()
route_current_json_file.set("")

def on_option_selected(sel_option):
  if sel_option == "Abrir":
    json_file = filedialog.askopenfilename(filetypes=[("Archivos JSON", "*.json")])

    if json_file:
        try:
            with open(json_file, 'r') as archivo:
                contenido = archivo.read()
                json.loads(contenido)
                route_current_json_file.set(json_file)
                textarea.delete("1.0", END)
                textarea.insert('1.0', contenido)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print("Error", "No se pudo cargar el archivo JSON: {}".format(str(e)))

  elif sel_option == "Guardar":
    json_file = route_current_json_file.get()
    
    if json_file:
        try:
            contenido = textarea.get('1.0', END)
            
            with open(json_file, 'w') as archivo:
                archivo.write(contenido)
                
            print("Éxito", "Los cambios se han guardado exitosamente.")
        except Exception as e:
            print("Error", "No se pudo guardar el archivo JSON: {}".format(str(e)))

  elif sel_option == "Guardar Como...":
    try:
        contenido = textarea.get('1.0', END)
        
        archivo_json = filedialog.asksaveasfilename(filetypes=[("Archivos JSON", "*.json")])
        
        if archivo_json:
            with open(archivo_json, 'w') as archivo:
                archivo.write(contenido)
            
            print("Éxito", "El archivo JSON se ha guardado exitosamente.")
    except Exception as e:
        print("Error", "No se pudo guardar el archivo JSON: {}".format(str(e)))
  elif sel_option == "Salir":
    root.destroy()

dropdown_options = OptionMenu(frm, selected_option, *options, command=on_option_selected).grid(column=0, row=1)

# ttk.Button(frm, text="Quit", command=root.destroy).grid(column=0, row=1)

def analize():
  contenido = textarea.get("1.0", END)

  try:
    datos_json = json.loads(contenido)
    
    print(datos_json)
    result = ProcessData(data=datos_json).analize_data()

    if result == 1:
       messagebox.showwarning("Información analizada", "Información analizada con éxito \nSe encontraron algunos errores en este código \nPuedes checar en el botón 'Errores'")
    else:
       messagebox.showinfo("Información analizada", "Información analizada con éxito \nNo se encontró ningún error en este código")
    
  except json.JSONDecodeError as e:
    print("Error al convertir a JSON:", str(e))
    messagebox.showerror("Error", f"Error al convertir a JSON: {str(e)}")

def errors():
  contenido = textarea.get("1.0", END)

  try:
    datos_json = json.loads(contenido)
    
    print(datos_json)
    result = ProcessData(data=datos_json).get_errors_from_data()

    if result == 1:
       messagebox.showerror("Mostrar Errores", "Error: La información enviada no contiene errores.")
    else:
      messagebox.showinfo("Mostrar Errores", "Archivo generado con éxito. \nVerifique el JSON generado en la raíz del proyecto")
    
  except json.JSONDecodeError as e:
    print("Error al convertir a JSON:", str(e))
    messagebox.showerror("Error", f"Error al convertir a JSON: {str(e)}")

def report():
  contenido = textarea.get("1.0", END)

  try:
    datos_json = json.loads(contenido)
    
    print(datos_json)
    result = ProcessData(data=datos_json).generate_graphs()

    if result == 1:
       messagebox.showerror("Generar Reporte", "Error: La información enviada contiene errores.")
    else:
      messagebox.showinfo("Generar Reporte", "Gráficas generadas con éxito. \nVerifique la imagen PNG generada en la raíz del proyecto")
    
  except json.JSONDecodeError as e:
    print("Error al convertir a JSON:", str(e))
    messagebox.showerror("Error", f"Error al convertir a JSON: {str(e)}")

ttk.Label(frm, text=" ", padding=3).grid(column=0, row=2)
ttk.Label(frm, text="Opciones", padding=3).grid(column=0, row=3)
ttk.Button(frm, text="Analizar", command=analize).grid(column=0, row=4)
ttk.Button(frm, text="Errores", command=errors).grid(column=0, row=6)
ttk.Button(frm, text="Reporte", command=report).grid(column=0, row=7)

root.mainloop()