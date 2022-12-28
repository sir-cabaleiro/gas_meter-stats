from picamera import PiCamera
import RPi.GPIO as GPIO
import pytesseract as tess
from PIL import Image
import paramiko
import datetime
import json
import time


def captura_contador() :
    pin = 7
    camera = PiCamera()
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)
    camera.capture('file directory.jpg')
    GPIO.output(pin, GPIO.LOW)



def leer_contador() :
    global contador

    tess.pytesseract.tesseract_cmd = r'tesseract-dir\tesseract.exe'
    my_image = Image.open('file directory.jpg')
    
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

    local = 'file directory' + mes + '.json'
    remote = "file directory" + mes + ".json"

    with open(local) as archivo:
        data = json.load(archivo)
        temp = data["dias"]
        temp.append(ahora)
        print(data)

    with open(local, 'w') as archivo:
        json.dump(data, archivo)

def conexion():
    HOST = "host"
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
        captura_contador()
        time.sleep(60)
        leer_contador()
        comprobacion()
    except:
        print("Lectura no tomada")
        exit()

    archivo_json()
    conexion()




