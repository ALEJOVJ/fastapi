ALEJANDRO FUENTES CASTILLO 
FICHA : 3407186

principalmente tuve varios errores con la clonacion del repo , resulta que lo tenia duplicado con otros archivos inecesarios entonces lo que hice fue aplicar estos comando para eliminar la carpeta duplicada 

entonces borre todo desde cero y empece a clonar de nuevo todo desde git bash

aplique el comando "dir" para saber que no haya quedado ninguna de fastapi

aplique despues el git clone con la url del repositorio

entre en la carpeta con el comando

cd fastapi

y para entrar desde la terminal de git bash a visual code aplique el comando

code .

despues al momento de iniciar el servidor me decia que tenia rutas antiguas que ya no existen a lo que me toco eliminar el entorno virtual y volverlo a crear para que quede con las rutas nuevas y pueda iniciar el servidor 

utilice los siguentes comandos

eliminar:
rm -Recurse -Force my_env

crear de nuevo:
python -m venv my_env

e instale el paquete de librerias:
pip install "fastapi[standard]"

y luego prendi el servidor:
fastapi dev main.py

cree modelos facturas.py y transacciones.py

cree sus clases facturabase, facturacrear, facturaeditar como asi tambien en transacciones 

aparecieron errores de importaciones pero era por mayusculas en los nombres de las clases definidas

se resolvieron los errores y se acomodo el codigo 

se crearon los enrutadores de clientes, facturas y transacciones 

aparecieron errores de nombres estaba poniendo APIrouter cuando era APIRouter era confusion de mayusculas

se agrego listas_app

se creo la base de datos funcional y se edito el enrutador clientes creando variables nuevas
para que se generen en la base de datos 


se agrega __pycache_/
my_venv/
venv/



