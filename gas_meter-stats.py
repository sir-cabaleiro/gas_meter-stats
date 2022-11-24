import paramiko
import datetime
import json

now = datetime.datetime.now()
mes = str(now.month)
dia = int(now.day)
hora = int(now.hour)
minuto = int(now.minute)
ahora = {"dia": dia, "hora": hora, "minuto": minuto}
HOST = ""
USER = "root"
PORT = ""
local = 'C:/Users/adri/Desktop/gas/' + mes + '.json'
remote = ""

def archivo_json():
    with open(local) as archivo:
        data = json.load(archivo)
        temp = data["dias"]
        temp.append(ahora)
        print(data)

    with open(local, 'w') as archivo:
        json.dump(data, archivo)

def conexion():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy( paramiko.AutoAddPolicy() )
    try:
        client.connect(HOST, port=PORT, username=USER, password='')

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
    archivo_json()
    conexion()


    


#   antes de añadir la linea en el json pruedo mirar si el contador ha cambiado respecto a los 5 minutos anteriores

#   consumo = m3 * 11.0519




