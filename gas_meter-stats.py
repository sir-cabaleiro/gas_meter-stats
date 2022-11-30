#from picamera import PiCamera
import pytesseract as tess
from PIL import Image
import paramiko
import datetime
import json


#camera = PiCamera()

def leer_contador() :
    global contador

    tess.pytesseract.tesseract_cmd = r'<<ruta tesseract>>'
    my_image = Image.open(r'<<ruta imagen>>')
    
    contador = tess.image_to_string(my_image, lang='eng', config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789')
    contador = contador[:-1]
    print("Lectura del contador: " + contador)

def comprobacion() :
    global contador

    print(len(contador))

    if len(contador) == 6 :
        print("Lectura correcta")

    else :
        print("Lectura no tomada")
        exit()

def resultado() :
    global ahora
    global mes

    now = datetime.datetime.now()
    mes = str(now.month)
    dia = int(now.day)
    hora = int(now.hour)
    minuto = int(now.minute)
    ahora = {"dia": dia, "hora": hora, "minuto": minuto, "contador": contador}
    print(ahora)

def archivo_json():
    global mes
    global local
    global remote

    local = '<<ruta local>>/' + mes + '.json'
    remote = "<<ruta remota>>/" + mes + ".json"

    with open(local) as archivo:
        data = json.load(archivo)
        temp = data["dias"]
        temp.append(ahora)
        print(data)

    with open(local, 'w') as archivo:
        json.dump(data, archivo)

def conexion():
    HOST = "ip host"
    USER = "user"
    PORT = "port"

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy( paramiko.AutoAddPolicy() )
    try:
        client.connect(HOST, port=PORT, username=USER, password='pass')

        sftp = client.open_sftp()

        try:
            sftp.put(local,remote)
            print("subido :)")
        except:
            print("cmamut, no subido :(")

        client.close()

    except:
        print('no se conectó :(')



if __name__ == '__main__':
    try:
        leer_contador()
        comprobacion()
    except:
        print("Lectura no tomada")
        exit()
    
    resultado()
    archivo_json()
    conexion()


    


#   antes de añadir la linea en el json pruedo mirar si el contador ha cambiado respecto a los 5 minutos anteriores

#   consumo = m3 * 11.0519




