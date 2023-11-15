import os
import errno
import platform
import time

def fecha_creacion(ruta_carpeta):
    if platform.system() == 'Windows':
        fecha_creacion = os.path.getctime(ruta_carpeta)
    else:
        fecha_creacion = os.path.getmtime(ruta_carpeta)

    # Formatear la fecha en un formato legible
    fecha_formateada = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(fecha_creacion))

    return fecha_formateada

# calcula la direccion de la carpeta(calcula el peso de la carpeta)

def calcular_directorio(directorio): return sum([sum([os.path.getsize(rutas+"\\"+archivo) for archivo in archivos]) for rutas, _, archivos in os.walk(directorio)])





 

print(calcular_directorio('/Users/Daniel/Desktop/arbolesPractica'))

class Node:

  def __init__(self, value, weight, route,type,createAt):


    self.value = value

    self.weight = weight

    self.tree = []
    
    self.route = route
    
    self.type = type

    self. createAt = createAt
class Folder:
   
   def __init__(self,head) -> None:
      self.head = head
    
   
   def create(self,route,new_archive,type): # new_archive = nombre de la carpeta 
      new_route = f'{route}/{new_archive}'
      folder_mother = self.traverse_until(route,self.head)
      if type == "folder":
         try:
            os.mkdir(f'{route}/{new_archive}')
            weight = calcular_directorio(new_route) # calcular peso de la carpeta que quiero crear
            new_folder = Node(new_archive,weight,new_route,"folder",fecha_creacion(new_route))
            folder_mother.tree.append(new_folder) # agregar en la posicion en donde esta la carpeta que queremos agregar
         except OSError as e:
            if e.errno != errno.EEXIST:
               raise 
      else:
         try:
            with open(new_route, 'w') as archivo:
               archivo.write("Hola py")
               print(f'Se ha creado el archivo "{new_archive}" con éxito.')
               weight = calcular_directorio(new_route) # calcular peso de la carpeta que quiero crear
               new_file = Node(new_archive,weight,new_route,"file", fecha_creacion(new_route))
               folder_mother.tree.append(new_file)
         except Exception as e:
            print(f'Ocurrió un error al intentar crear el archivo: {e}')
   
   
   def remove(self,route,name,type): # route = la ruta de la carpeta a eliminar ---- name = es el nombre de la carpeta a eliminar
      folder_mother = self.traverse_until(route,self.head)
      if type == 'folder':
         try:
            os.rmdir(route)
            for child in folder_mother.tree:
               if child.value == name:
                  folder_mother.tree.remove(child)
                  break
         except OSError as e:
            if e.errno != errno.EEXIST:
               raise
      else:
         try:
            os.remove(route)
            print(f'Se ha eliminado el archivo "{name}" con éxito.')
            for child in folder_mother.tree:
               if child.value == name:
                  folder_mother.tree.remove(child)
                  break
         except Exception as e:
            print(f'Ocurrió un error al intentar eliminar el archivo: {e}')
      
         
   def rename(self,old_route,new_route,name,new_name):
      rename_folder = self.traverse_until(old_route,self.head)
      print(rename_folder.value)
      for child in rename_folder.tree:
         if child.value == name:
            child.value = new_name
            child.route = new_route
            break
      
      try:
        os.rename(old_route,new_route)
      except OSError as e:
         if e.errno != errno.EEXIST:
            raise
      
      
      
   
   def mapear_carpeta(self, nodo,directed):
    
    contenido = os.listdir(directed) # listdir devuelve un arreglo de  todas las carpetas que estan en la carpeta madre
    for i in contenido:

        newroute = f"{directed}/{i}" # direccion de la carpeta que esta dentro de la carpeta madre , i = al nombre de la carpeta

        if os.path.isfile(newroute)==True:  # Crea un nodo para un archivo.txt o cualquiera

            weight = os.path.getsize(newroute)

            nodoHijo = Node(i,weight,newroute,"file",fecha_creacion(newroute))

            nodo.tree.append(nodoHijo)


        else:
            # Crea un nodo para la carpeta

            nodoHijo = Node(i,calcular_directorio(newroute),newroute,"folder",fecha_creacion(newroute))

            nodo.tree.append(nodoHijo)

            self.mapear_carpeta(nodoHijo,newroute)
   
   def search_heavier_folder(self, current: Node):
      max = 0
      nodomayor = 0
   
      for node   in current.tree:
         if node.type == "folder":

            if node.weight >= max:
               max = node.weight
               nodomayor = node
      return nodomayor
   
 
   def search_heavier_file(self,current,max= 0, nodomayor = 0):
      if current.type == 'file':
         if current.weight > max:
            nodomayor = current
            max = current.weight
         
      for i in range(len(current.tree)):
          new_node = current.tree[i]
          nodomayor, max =  self.search_heavier_file(new_node,max,nodomayor)   
      return nodomayor , max

   

   def folder_with_more_archives(self, current,max= 0, nodomayor = 0): 
      if len(current.tree) == 0:
         pass
      if len(current.tree) > max:
         nodomayor = current
         max = len(current.tree)
         
      for i in range(len(current.tree)):
          new_node = current.tree[i]
          nodomayor, max =  self.folder_with_more_archives(new_node,max,nodomayor)   
      return nodomayor , max

    
    
   def traverse_tree(self,node):
       
    if len(self.head.tree) == 0:
        return f"Arbol Vacio"
       
    else:

        for i in range(len(node.tree)): #for i in range(len(node.tree)-1,0,-1): este for recorre de atras hacia delante
           #print(self.head.tree[i].value)
           new_node = node.tree[i]
           print(f'{node.route} --> {new_node.value}')
           #print(f'{node.value} --> {new_node.route}') para imprimir la ruta nivel pro
           self.traverse_tree(new_node)
    
   def traverse_until(self,route,node): # node es igual node cabeza
      if node.route == route:
        
        return node
      else:
         for i in range(len(node.tree)):  
          
          new_node = node.tree[i]
          return self.traverse_until(new_node.route,new_node)
      
   def tiene_solo_vocales(self, cadena):
      vocales = "aeiou"
      for vocal in vocales:
        if vocal not in cadena.lower():
            return False
      return True
   
   def vowel_node (self, node, vowels = 0):
      if node != None:
         verify = self.tiene_solo_vocales(node.value)
         if verify==True:
            print('encontrado')
            vowels = node
            return vowels
         else:
               for i in range(len(node.tree)):  
                  new_node = node.tree[i]
                  vowels =  self.vowel_node(new_node, vowels)
      return vowels








            


          

    


from zipfile import ZipFile
filename = 'grave'
ext = '.zip'
folder = f'{filename}{ext}'
extfolder = f'/Users/Usuario/Desktop/{folder}' # lugar donde se ubica la carpeta en zip
address = f"/Users/Usuario/Desktop/{filename}"# ruta en donde va a qeudar la carpeta extrida

with ZipFile(extfolder, "r") as zip:
    zip.extractall("/Users/Usuario/Desktop") # La ruta donde queremos que quede la carpeta extraida
    #print(zip.printdir())      # Imprime todo la lista de directorios de la carpeta extraida



nodo = Node(filename, calcular_directorio(address),address,"folder", fecha_creacion(address)) # Nodo Madre
folder = Folder(nodo)
folder.mapear_carpeta(nodo,address)



#folder.traverse_tree(folder.head)

'''
add1 = '/Users/Usuario/Desktop/grave'
name= 'aaaa.txt'
folder.create(add1,name,'file')

nodeadd= folder.traverse_until(add1,folder.head)
print(nodeadd.tree[5].createAt)
print(len(nodeadd.tree))

old_route = f"{add1}/{name}"
new_name = "dddddd"
new_route = f"{add1}/{new_name}"
print(old_route)
print(new_route)
folder.rename(old_route,new_route,name,new_name)
x = folder.traverse_until(add1,folder.head)
print(x.tree[3].value)

'''
maximo :Node= folder.search_heavier_folder(folder.head)
print(f"El folder mas pesado es: {maximo.route}")
nodo , max = folder.search_heavier_file(folder.head)
print(max)
print(nodo.createAt)
#print(max.weight)

vowels = folder.vowel_node(folder.head)
print(vowels.value, vowels.weight)