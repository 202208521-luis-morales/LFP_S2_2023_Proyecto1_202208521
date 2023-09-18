import datetime
import json
from graphviz import Digraph
import math

class ProcessData:
  def __init__(self, data) -> None:
    self.data = data
    self.errors_data = {"errores": []}
    self.dot= Digraph(format='pdf', engine='dot')
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
      if not "operaciones" in self.data:
        self.errors_data["errores"].append({
          "No": int(len(self.errors_data["errores"]) + 1),
          "descripcion": "No existe una etiqueta 'operaciones en el JSON analizado'"
        })
      elif len(self.data["operaciones"]) == 0:
        self.errors_data["errores"].append({
          "No": int(len(self.errors_data["errores"]) + 1),
          "descripcion": "Debe de existir por lo menos 1 elemento dentro de la lista 'operaciones'"
        })
      else:
        counter = 1
        for opc in self.data["operaciones"]:
          self.analize_opc(opc=opc, is_initial_node=True, prev_count=None, curr_count=str(counter))

          counter += 1
    
    
    if len(self.errors_data["errores"]) > 0:
      return 1
    else:
      if for_graphs_option == True:
        self.dot.render("reporte_" + datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S"), format='png', view=True)
      
      return 0
          

  def analize_opc(self, opc, is_initial_node: bool, prev_count: str | None , curr_count: str):
    curr_opt = None
    curr_val1 = None

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
        counter = 1
        
        for sub_opc in opc["valor1"]:
          pr_cnt = str(curr_count) + ".v2_" + str(counter)
          self.analize_opc(sub_opc, is_initial_node=False, prev_count=curr_count, curr_count=pr_cnt)

          counter += 1
      elif isinstance(opc["valor1"], int) or isinstance(opc["valor1"], float):
        curr_val1 = opc["valor1"]
      else:
        self.errors_data["errores"].append({
          "No": int(len(self.errors_data["errores"]) + 1),
          "descripcion": f"valor1 no es válido. Debe de ser, ya sea un número o una lista de comandos 'operacion'",
          "NumElemento": curr_count,
          "Elemento": str(opc)
      })

    if not "valor2" in opc:
      self.errors_data["errores"].append({
        "No": int(len(self.errors_data["errores"]) + 1),
        "descripcion": f"No existe un elemento 'valor2'",
        "NumElemento": curr_count,
        "Elemento": str(opc)
      })
    else:
      if isinstance(opc["valor2"], list):
        counter = 1
        
        for sub_opc in opc["valor2"]:
          pr_cnt = str(curr_count) + ".v2_" + str(counter)
          self.analize_opc(sub_opc, is_initial_node=False, prev_count=curr_count, curr_count=pr_cnt)

          counter += 1
      elif isinstance(opc["valor2"], int) or isinstance(opc["valor2"], float):
        if curr_opt != None and curr_val1 != None:
          # Parent
          self.dot.node(curr_count, label=curr_opt + "\n" + self.operate(opt=curr_opt, val1=curr_val1, val2=opc["valor2"]))

          # valor1
          self.dot.node(curr_count + "__v1", shape='circle', label=curr_val1)
          
          # valor2
          self.dot.node(curr_count + "__v2", shape='circle', label=opc["valor2"])

          if is_initial_node == True:
            self.dot.edge(curr_count, curr_count + "__v1")
            self.dot.edge(curr_count, curr_count + "__v2")
          else:
            self.dot.edge(prev_count, curr_count)
      else:
        self.errors_data["errores"].append({
          "No": int(len(self.errors_data["errores"]) + 1),
          "descripcion": f"valor2 no es válido. Debe de ser, ya sea un número o una lista de comandos 'operacion'",
          "NumElemento": curr_count,
          "Elemento": str(opc)
        })

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