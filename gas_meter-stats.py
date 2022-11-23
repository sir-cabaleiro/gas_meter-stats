import paramiko
import time
from datetime import datetime

HOST = "185.254.204.239"
USER = "root"
local = "gas.json"
remote = ""

if __name__ == '__main__':
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy( paramiko.AutoAddPolicy() )
    try: 
        client.connect(HOST, username=USER, password='')

        stdin, stdout, stderr = client.exec_command('ls')
        time.sleep(1)
        result = stdout.read().decode()
        print(result)

        sftp = client.open_sftp()

        try: 
            sftp.put(local,remote)
            print("subido :)")
        except:
            print("cmamut :(")

        client.close()

    
    except:
        print('no se conectó :(')


    



#   consumo = Xm3 * 11.0519

# JSON '{"mes":"11", "dia":24, "hora":17, "minuto":"11",}'