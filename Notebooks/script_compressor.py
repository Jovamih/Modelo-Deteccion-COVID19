import os 
from PIL import Image
import subprocess
import pandas as pd

def reduction_image(source,dest):
  #reducir el tamaño y guardarlo
  img=Image.open(source)
  new_size=(int(img.size[0]*0.5),int(img.size[1]*0.5))
  img=img.resize(new_size,Image.ANTIALIAS)
  img.save(dest,quality=95)
  print(">BEFORE:",os.stat(source).st_size/(1024*1024),"MB | AFTER:",os.stat(dest).st_size/(1024*1024),end="")
        
def compress_image_pngquant(source):
    new_name=source.rstrip(".png")+"-fs8.png"
    if not os.path.exists(new_name):
        subprocess.run([r"C:\Experimental\ProjectsGithub\Modelo-Prediccion-Covid-Radiografias\Notebooks\pngquant\pngquant.exe",source]) #comprimo la imagen
        os.remove(source) ##elimino la imagen anterior
        
        os.rename(new_name ,source)
        print("> OPTIMIZE",os.stat(source).st_size/1024.0," KB")

def script_compresion_por_criterio(source, dest, tabla_condicional,delete_origin=True):
    """
    SCRIPT QUE DISMINUYE EL PESO DE LOS ARCHIVOS EN FUNCION DE UNA TABLA DE CONDICIONES
    """
    for (root,dirs,files) in os.walk(source):
        for file_name in files:
            print(file_name,end=" ")
            if file_name.endswith(".jpg") or file_name.endswith(".jpeg") or file_name.endswith(".png"): #si el archivo es una imagen
            #verifico si se encuentra en la tabla condicional
                mask_found=tabla_condicional["File"]==file_name
                if mask_found.any(): #si existe al menos una coincidencia
                    row_found=tabla_condicional[mask_found]
                    row_found=row_found.values[0]
                    if row_found[1]=="PA" and row_found[2]==False:
                        reduction_image(os.path.join(root,file_name),os.path.join(dest,file_name))
                        compress_image_pngquant(os.path.join(dest,file_name))
                    else:
                        print(" |EXCLUIDO")
                else:
                    print(" | NO PROCESADO - NO EXISTE EN EL REGISTRO")
            else:
                print(" |OMITIDO - NO IMAGEN")
        #todo archivo que se procesa al final se elimina
            if delete_origin:
                os.remove(os.path.join(root,file_name)) 
                print("> (OK)")


if __name__=="__main__":
    import sys 

    if len(sys.argv)==3:       
        tabla_condicional=pd.read_csv(r"C:\Experimental\ProjectsGithub\Modelo-Prediccion-Covid-Radiografias\Notebooks\tabla_filtros.csv")
        print("Optimizando arbol de Imagenes")
        script_compresion_por_criterio(sys.argv[1],sys.argv[2],tabla_condicional)
    else:
        print("Ingrese 3 parametros")
        print(sys.argv)
        sys.exit(0)