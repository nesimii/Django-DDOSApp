import paramiko
import redis as redis
from channels.layers import get_channel_layer

channel_layer = get_channel_layer()
redis = redis.StrictRedis(host="localhost", port=6379, db=0, charset="utf-8", decode_responses=True)


class PcSSHInfo:
    __client = paramiko.SSHClient()

    def __init__(self, ip=None, username=None, password=None, port=22):
        self.ip = ip
        self.__username = username
        self.__password = password
        self.__port = port

    def sshOpen(self):
        if self.__client.get_transport() is None:
            try:
                self.__client.set_missing_host_key_policy(
                    paramiko.AutoAddPolicy())
                self.__client.connect(self.ip, self.__port, self.__username,
                                      self.__password, timeout=10)
                print(self.__username, ": ssh açıldı")
                return True
            except:
                print("ssh bağlantısı kurulamadı: ", self.__username)
                return False

        elif self.__client.get_transport() is not None:
            if self.__client.get_transport().is_active():
                return True

    def sshClose(self):
        if self.__client.get_transport() is not None:
            if self.__client.get_transport().is_active():
                try:
                    self.__client.close()
                    return True
                except:
                    return False
        else:
            return True

    def sshSendCommand(self, command):
        if self.sshOpen():
            try:
                stdin, stdout, stderr = self.__client.exec_command(command)
                while True:
                    line = stdout.readline()
                    if not line:
                        stdin.close()
                        break
                    print(self.__username, " ", self.ip, ": ", line, end="")
                    redis.set(str(self.ip), line)
                    redis.expire(self.ip, 7)
                if self.sshClose():
                    redis.set(str(self.ip), 'ssh bağlantısı kapatıldı')
                else:
                    redis.set(str(self.ip), 'ssh bağlantısı kapatılamadı')
                return None

            except:
                if self.sshClose():
                    redis.set(str(self.ip), 'Komut gönderme hatası - ssh bağlantısı kapatıldı')
                else:
                    redis.set(str(self.ip), 'Komut gönderme hatası - ssh bağlantısı kapatılamadı')
        else:
            redis.set(str(self.ip), 'ssh bağlantısı kurulamadı')
