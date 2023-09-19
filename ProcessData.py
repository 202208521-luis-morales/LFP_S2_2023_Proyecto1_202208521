import datetime
import json
from graphviz import Digraph
import math
import re

class ProcessData:
  def __init__(self, data) -> None:
    self.data = data
    self.errors_data = { "errores": [] }
    self.dot = Digraph(format='pdf', engine='dot')
    self.dot_configs = {
      "text": None,
      "bg-node": None,
      "font-color": None,
      "shape": None
    }
    self.valid_operations = (
      "suma",
      "resta",
      "multiplicacion",
      "division",
      "potencia",
      "raiz",
      "inverso",
      "seno",
      "coseno",
      "tangente",
      "mod"
      )
    self.valid_operations_1value = (
      "inverso",
      "seno",
      "coseno",
      "tangente"
      )

  def get_errors_from_data(self):
    result = self.analize_data()
    
    if result == 0:
      return 1 # Significa que no hay errores
    else:
      with open("errores_" + datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".json", 'w', encoding='utf-8') as archivo_json:
        json.dump(self.errors_data, archivo_json, ensure_ascii=False)
        return 0

  def generate_graphs(self):
    result = self.analize_data()

    if result == 1:
      return 1
    else:
      self.analize_data(for_graphs_option=True)

  def analize_data(self, for_graphs_option: bool = False) -> int:
    if self.data == None:
      print("ERROR: Primero debes de agregar datos")
    else:
      # Voy a suponer que la lista 'configuraciones' solo tiene 1 elemento
      if "configuraciones" in self.data:
        for key, val in self.data["configuraciones"][0]:
          if key == "texto":
            self.dot_configs["text"] = val
          elif key == "fondo":
            self.dot_configs["bg-node"] = val
          elif key == "fuente":
            self.dot_configs["font-color"] = val
          elif key == "forma":
            self.dot_configs["shape"] = val
          else:
            rare_chars = re.sub(r'[a-zA-Z0-9]', '', key)
            
            if rare_chars != "":
              self.errors_data["errores"].append({
                "No": int(len(self.errors_data["errores"]) + 1),
                "lexema": rare_chars,
                "tipo": "léxico",
                "parte": "configuraciones",
                "descripcion": f"Nombre de configuración '{key}' no válido; contiene {rare_chars}"
              })
            else:
              self.errors_data["errores"].append({
                "No": int(len(self.errors_data["errores"]) + 1),
                "lexema": key,
                "tipo": "léxico",
                "parte": "configuraciones",
                "descripcion": f"Nombre de configuración '{key}' no válido"
              })

      if not "operaciones" in self.data:
        self.errors_data["errores"].append({
          "No": int(len(self.errors_data["errores"]) + 1),
          "descripcion": "No existe una etiqueta 'operaciones' en el JSON analizado",
          "tipo": "formato incorrecto"
        })
      elif len(self.data["operaciones"]) == 0:
        self.errors_data["errores"].append({
          "No": int(len(self.errors_data["errores"]) + 1),
          "descripcion": "Debe de existir por lo menos 1 elemento dentro de la lista 'operaciones'",
          "parte": "operaciones",
          "tipo": "formato incorrecto"
        })
      else:
        counter = 1
        for opc in self.data["operaciones"]:
          print("A1")
          self.analize_opc(opc=opc, is_initial_node=True, prev_count=None, curr_count=str(counter), create_nodes=for_graphs_option)
          print("A2")
          counter += 1
    
    
    if len(self.errors_data["errores"]) > 0:
      return 1
    else:
      if for_graphs_option == True:
        self.dot.render(("reporte_" if self.dot_configs["text"] == None else self.dot_configs["text"] + "_") + datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S"), format='png', view=True)
      
      return 0
          

  def analize_opc(self, opc, is_initial_node: bool, prev_count: str | None , curr_count: str, create_nodes: bool):
    curr_opt = None
    curr_val1 = None
    curr_val2 = None
    is_val1_a_list = False

    print("###################")
    print(f"# is_inital_node: {is_initial_node}")
    print(f"# prev_count: {prev_count}")
    print(f"# curr_count: {curr_count}")
    print("###################")

    def generate_nodes(new_val2: int | float, from_list: str = None, from_val: str = None, is_v1_list = False):
      print(f"GENERATE_NODES: curr_count: {curr_count}")
      print(f"curr_opt: {curr_opt}")
      print(f"curr_val1: {curr_val1}")
      print(f"curr_val2: {curr_val2}")
      print(f"new_val2: {new_val2}")
      print(f"prev_count {prev_count}")
      print(f"from_list {from_list}")

      if curr_opt != None and curr_val1 != None:
        print("WWWWW")
        # Método: comprobar si es posible realizar la operación con los valores de 'operacion', 'valor1' y 'valor2'
        if new_val2 != None:
          if curr_opt == "division":
            if new_val2 == 0:
              self.errors_data["errores"].append({
                "No": int(len(self.errors_data["errores"]) + 1),
                "descripcion": "Al usar 'division', valor2 no puede ser 0",
                "tipo": "matemático",
                "parte": "operaciones",
                "NumElemento": curr_count,
                "Elemento": str(opc)
              })

          if curr_opt == "potencia":
            # (-a) ^ (1/b)
            if -1 < new_val2 < 1 and curr_val1 < 0:
              self.errors_data["errores"].append({
                "No": int(len(self.errors_data["errores"]) + 1),
                "descripcion": "Al usar 'potencia', si tienes un valor entre -1 y 1 para valor2, valor1 no puede ser negativo: [-a] ^ [1/b]",
                "tipo": "matemático",
                "parte": "operaciones",
                "NumElemento": curr_count,
                "Elemento": str(opc)
              })
            
            # 0 ^ 0 or 0 ^ (-b)
            if new_val2 <= 0 and curr_val1 == 0:
              self.errors_data["errores"].append({
                "No": int(len(self.errors_data["errores"]) + 1),
                "descripcion": "Al usar 'potencia', si valor1 es 0, valor2 no puede ser ni 0 ni un valor negativo: 0 ^ 0 ó 0 ^ [-b]",
                "tipo": "matemático",
                "parte": "operaciones",
                "NumElemento": curr_count,
                "Elemento": str(opc)
              })
            
          if curr_opt == "raiz":
            # a ^ (1/0)
            if new_val2 == 0:
              self.errors_data["errores"].append({
                "No": int(len(self.errors_data["errores"]) + 1),
                "descripcion": "Al usar 'raiz', valor2 no puede ser 0: a ^ (1/0)",
                "tipo": "matemático",
                "parte": "operaciones",
                "NumElemento": curr_count,
                "Elemento": str(opc)
              })
      
            # (-a) ^ (1/b)
            if (curr_val1 < 0 and (new_val2 < -1 and new_val2 > 1)):
              self.errors_data["errores"].append({
                "No": int(len(self.errors_data["errores"]) + 1),
                "descripcion": "Al usar 'raiz', si tienes un valor menor a -1 y mayor a 1 para valor2, valor1 no puede ser negativo: [-a] ^ [1/b]",
                "tipo": "matemático",
                "parte": "operaciones",
                "NumElemento": curr_count,
                "Elemento": str(opc)
              })
            
            # 0 ^ (-b)
            if new_val2 < 0 and curr_val1 == 0:
              self.errors_data["errores"].append({
                "No": int(len(self.errors_data["errores"]) + 1),
                "descripcion": "Al usar 'raiz', si valor1 es 0, valor2 no puede ser un valor negativo:  0 ^ [-b]",
                "tipo": "matemático",
                "parte": "operaciones",
                "NumElemento": curr_count,
                "Elemento": str(opc)
              })
            
          if curr_opt == "mod":
            if new_val2 == 0:
              self.errors_data["errores"].append({
                "No": int(len(self.errors_data["errores"]) + 1),
                "descripcion": "Al usar 'mod', valor2 no puede ser 0",
                "tipo": "matemático",
                "parte": "operaciones",
                "NumElemento": curr_count,
                "Elemento": str(opc)
              })
      
        else:
          if curr_opt == "inverso":
            if curr_val1 == 0:
              self.errors_data["errores"].append({
                "No": int(len(self.errors_data["errores"]) + 1),
                "descripcion": "Al usar 'inverso', valor2 no puede ser 0",
                "tipo": "matemático",
                "parte": "operaciones",
                "NumElemento": curr_count,
                "Elemento": str(opc)
              })
      
          if curr_opt == "tangente":
            def is_int(valor):
              try:
                  int(valor)
                  return True
              except ValueError:
                  return False
              
            if not is_int((curr_val1 - 90) / 180):
              self.errors_data["errores"].append({
                "No": int(len(self.errors_data["errores"]) + 1),
                "descripcion": "Al usar 'tangente', el ángulo (en grados), no puede ser 180n + 90: (ejemplo: 90, 270, 450...)",
                "tipo": "matemático",
                "parte": "operaciones",
                "NumElemento": curr_count,
                "Elemento": str(opc)
              })
        # FinMétodo

        if len(self.errors_data["errores"]) == 0:
          # Parent
          print(f"XParent: curr_count: {curr_count}, curr_opt: {curr_opt}")
          print(f"str(self.operate(opt=curr_opt, val1=curr_val1, val2=new_val2)): {str(self.operate(opt=curr_opt, val1=curr_val1, val2=new_val2))}")
          self.dot.node(curr_count, style='filled', shape=self.dot_configs["shape"], fillcolor=self.dot_configs["bg-node"], color=self.dot_configs["font-color"] ,label=curr_opt + "\n" + str(self.operate(opt=curr_opt, val1=curr_val1, val2=new_val2)))

          # valor1
          #if from_list:
          if from_list != "valor1" and not is_v1_list:
            print(f"XValor1: curr_count: {curr_count}, curr_val1: {str(curr_val1)}")
            self.dot.node(curr_count + "__v1", style='filled', shape=self.dot_configs["shape"], fillcolor=self.dot_configs["bg-node"], color=self.dot_configs["font-color"], label=str(curr_val1))
          
          # valor2
          if from_list != "valor2" and new_val2 != None:
            print(f"XValor2: curr_count: {curr_count}, curr_val2: {str(curr_val1)}")
            self.dot.node(curr_count + "__v2", style='filled', shape=self.dot_configs["shape"], fillcolor=self.dot_configs["bg-node"], color=self.dot_configs["font-color"], label=str(opc["valor2"]))

          # Relacionar los nodos de valor1 y valor2 con su padre
          if from_list != "valor1" and not is_v1_list:
            print(f"XRelValor1: curr_count: {curr_count}")
            self.dot.edge(curr_count, curr_count + "__v1", "v1")
          if from_list != "valor2" and new_val2 != None:
            print(f"XRelValor2: curr_count: {curr_count}")
            self.dot.edge(curr_count, curr_count + "__v2", "v2")
          
          # Relacionar al padre de los nodos valor1 y valor2 con su propio padre
          if is_initial_node == False:
            print(f"XRelParent: prev_count: {prev_count} curr_count: {curr_count}")
            self.dot.edge(prev_count, curr_count, from_val)

    print("------------------------")
    print("Analizando elemento " + curr_count)
    print(opc)
    print("------------------------")
    
    if not "operacion" in opc:
      self.errors_data["errores"].append({
        "No": int(len(self.errors_data["errores"]) + 1),
        "descripcion": f"No existe un elemento 'operacion'",
        "NumElemento": curr_count,
        "Elemento": str(opc)
      })
    elif not opc["operacion"] in self.valid_operations:
      self.errors_data["errores"].append({
        "No": int(len(self.errors_data["errores"]) + 1),
        "descripcion": f"La 'operacion' '{opc['operacion']}' no es válida",
        "NumElemento": curr_count,
        "Elemento": str(opc)
      })
    else:
      curr_opt = opc["operacion"]

    if not "valor1" in opc:
      self.errors_data["errores"].append({
        "No": int(len(self.errors_data["errores"]) + 1),
        "descripcion": f"No existe un elemento 'valor1'",
        "NumElemento": curr_count,
        "Elemento": str(opc)
      })
    else:
      if isinstance(opc["valor1"], list):
        #counter = 1
        
        #for sub_opc in opc["valor1"]:
        pr_cnt = str(curr_count) + ".v1" # + str(counter)
        # Suponer que si valor1 tiene una lista, tal lista tiene solo un elemento
        result = self.analize_opc(opc["valor1"][0], is_initial_node=False, prev_count=curr_count, curr_count=pr_cnt, create_nodes=create_nodes)
        curr_val1 = float(result)
        is_val1_a_list = True
        #if create_nodes:
        #  print("XD")
        #  generate_nodes(None, "valor1", new_val1=result)
          #self.analize_opc(sub_opc, is_initial_node=False, prev_count=curr_count, curr_count=pr_cnt)

         # counter += 1
      elif isinstance(opc["valor1"], int) or isinstance(opc["valor1"], float):
        curr_val1 = opc["valor1"]
        if curr_opt != None:
          if curr_opt in self.valid_operations_1value:
            if create_nodes:
              print("XC")
              generate_nodes(None, None, "v1")
      else:
        self.errors_data["errores"].append({
          "No": int(len(self.errors_data["errores"]) + 1),
          "descripcion": f"valor1 no es válido. Debe de ser, ya sea un número o una lista de comandos 'operacion'",
          "NumElemento": curr_count,
          "Elemento": str(opc)
      })
        
    if curr_opt != None:
      if not curr_opt in self.valid_operations_1value:
        if not "valor2" in opc:
          self.errors_data["errores"].append({
            "No": int(len(self.errors_data["errores"]) + 1),
            "descripcion": f"No existe un elemento 'valor2'",
            "NumElemento": curr_count,
            "Elemento": str(opc)
          })
          if create_nodes:
            print("XA")
            generate_nodes(None)
          pass
        else:
          if isinstance(opc["valor2"], list):
            #counter = 1

            #for sub_opc in opc["valor2"]:
            # Suponer que cada valor2 que tenga una lista, tal lista tendrá solo un elemento
            pr_cnt = str(curr_count) + ".v2" # + str(counter)

            result = self.analize_opc(opc["valor2"][0], is_initial_node=False, prev_count=curr_count, curr_count=pr_cnt, create_nodes=create_nodes)
            curr_val2 = float(result)
            if create_nodes:
              print("XB")
              generate_nodes(float(result), "valor2")
            #self.analize_opc(sub_opc, is_initial_node=False, prev_count=curr_count, curr_count=pr_cnt)
            
              # counter += 1
          elif isinstance(opc["valor2"], int) or isinstance(opc["valor2"], float):
            if create_nodes:
              print("XF")
              generate_nodes(opc["valor2"], None, "v2", is_val1_a_list)
              
            curr_val2 = opc["valor2"]
          else:
            self.errors_data["errores"].append({
          "No": int(len(self.errors_data["errores"]) + 1),
          "tipo": "léxico",
          "descripcion": f"valor2 no es válido. Debe de ser, ya sea un número o una lista de comandos 'operacion'",
          "NumElemento": curr_count,
          "Elemento": str(opc)
        })
    
    if curr_val1 != None:
      return str(self.operate(opt=curr_opt, val1=curr_val1, val2=curr_val2))

  def operate(self, val1, val2, opt):
    if opt == "suma":
      return val1 + val2
    elif opt == "resta":
      return val1 - val2
    elif opt == "multiplicacion":
      return val1 * val2
    elif opt == "division":
      return val1 / val2
    elif opt == "potencia":
      return val1 ** val2
    elif opt == "raiz":
      return val1 ** (1/val2)
    elif opt == "inverso":
      return (1/val1)
    elif opt == "seno":
      return math.sin(math.radians(val1))
    elif opt == "coseno":
      return math.cos(math.radians(val1))
    elif opt == "tangente":
      return math.tan(math.radians(val1))
    elif opt == "mod":
      return val1 % val2