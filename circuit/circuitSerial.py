from serial.tools.list_ports import comports, grep
from time import *
import serial

class circuitSerial:
    
    def validaPort(self, puerto, serie, modelo, command, baudios, timeout):
        try:
            ser = self.connectSerial(puerto, baudios, timeout )
            if ser is not None and ser:
                for _ in range(5):
                    self.writeSerial(ser, command)
                    data = ( self.readSerial( ser, 11 ) ).decode()
                    
                    if data == "" or data == 'False' or data == False: continue
                    if data.find(serie) == -1 and data.find(modelo) == -1: continue

                    print( "RESPUESTA DEL PUERTO {} : {}".format( ser.port, data ) )

                    return ser

                self.disconnectSerial(ser)
            return False
        except Exception as e:
            print(e)
            return False        

    def connectSerial(self, puerto, baudios, timeout):
        try:
            return serial.Serial(puerto, baudios, timeout=timeout)
        except Exception as e:
            print(e)
            return False

    def writeSerial(self, ser, command):
        #self.resetBufferInp(ser)
        if self.statusSerial(ser):
            ser.write(command.encode())
        return True

    def readSerial(self, ser, numByte=1):
        try:
            #if self.statusSerial(ser):
            data = ser.readline()
            #data = ser.read(numByte)

            #self.resetBufferOup(ser)
            #print(data)
            return data
        except Exception as e:
            return False
    
    def readSerialImp(self, ser):
        try:
            rep = 0
            ser.flushInput()
            message = list()
            while len(message) <= 5:
                data = ser.read(1)
                if data != b'': message.append(ord(data))
                if rep == 5 and data == b'': break
                rep += 1

            return message
        except Exception as e:
            return False

    def disconnectSerial(self, ser):
        if self.statusSerial(ser):
            ser.close()
            #if ser.port in self._dispActive:
            #self._dispActive.remove(ser.port)

    def resetBufferInp(self, ser):
        if self.statusSerial(ser):
            ser.flushInput()

    def resetBufferOup(self, ser):
        if self.statusSerial(ser):
            ser.flushOutput()
    
    def statusSerial(self, ser):
        if ser is not None: return ser.is_open
        return False
    
    def delCircuitActive(self, ser):
        self._dispActive.remove(ser.port)

    def scannerSerial(self, modelo, serie, baudios, timeout, command, pattern):
        for comport in grep( pattern ):
            print( "VALIDANDO PUERTO {}".format( comport.device ) )
            ser = self.validaPort( comport.device, serie, modelo, command, baudios, timeout )
            if ser: return ser