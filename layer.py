from yowsup.layers.interface                           import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_messages.protocolentities  import TextMessageProtocolEntity
from yowsup.layers.protocol_presence.protocolentities  import AvailablePresenceProtocolEntity
from yowsup.layers.protocol_chatstate.protocolentities import OutgoingChatstateProtocolEntity   #is writing, writing pause
from yowsup.common.tools                               import Jid                               #is writing, writing pause
from yowsup.layers import YowLayerEvent
from yowsup.layers.network                     import YowNetworkLayer

import time

import logging
import os
import sys


import RPi.GPIO as GPIO

# Seleccionar la numeracion de los pines

GPIO.setmode(GPIO.BOARD)

# Desactivar advertencias

GPIO.setwarnings(False)

# Selecionar los pines de salida

GPIO.setup(7, GPIO.OUT)

GPIO.setup(11, GPIO.OUT)

GPIO.setup(13, GPIO.OUT)

GPIO.setup(15, GPIO.OUT)

# Seleccionar los pines como entrada

GPIO.setup(12, GPIO.IN)

GPIO.setup(16, GPIO.IN)

GPIO.setup(18, GPIO.IN)

GPIO.setup(22, GPIO.IN)

# Inicializar los pines como apagados

GPIO.output(7, False)

GPIO.output(11, False)

GPIO.output(13, False)

GPIO.output(15, False)

logger = logging.getLogger('Sistema Domotico WSP')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('debug.log')
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

#--------------- TIPOS DE MENSAJES -----------------
#logger.debug('mensaje debug')               #Mensaje de debug
#logger.info('mensaje info')                 #Mensaje de informacion
#logger.warning('mensaje warning')           #Mensaje de warning
#logger.error('mensaje error')               #Mensaje de error
#logger.critical('mensaje critical')         #Mensaje de critico


def restart_program():
    """Restarts the current program.
    Note: this function does not return. Any cleanup action (like
    saving data) must be done before calling this function."""
    python = sys.executable
    os.execl(python, python, * sys.argv)


logger.debug('--------------------------------------------------')
logger.debug('-----------------INICIANDO EL SISTEMA-------------')

class EchoLayer(YowInterfaceLayer):

    @ProtocolEntityCallback("message")
    def onMessage(self, messageProtocolEntity):

        logger.debug('@ProtocolEntityCallback("message")')
        if messageProtocolEntity.getType() == 'text':
            time.sleep(0.5)
            logger.debug('if messageProtocolEntity.getType() == text')
            self.onTextMessage(messageProtocolEntity)
            logger.debug('self.onTextMessage(messageProtocolEntity)')
            time.sleep(0.5)
            self.toLower(messageProtocolEntity.ack())  # Set received (double v)
            logger.debug(' self.toLower(messageProtocolEntity.ack())')
            time.sleep(0.5)
            self.toLower(AvailablePresenceProtocolEntity())  # Set online
            logger.debug('self.toLower(AvailablePresenceProtocolEntity())')
            time.sleep(0.5)
            self.toLower(messageProtocolEntity.ack(True))  # Set read (double v blue)
            logger.debug('self.toLower(messageProtocolEntity.ack(True))')
            time.sleep(0.5)
            self.toLower(OutgoingChatstateProtocolEntity(OutgoingChatstateProtocolEntity.STATE_TYPING, Jid.normalize(
                messageProtocolEntity.getFrom(False))))  # Set is writing
            logger.debug('self.toLower(OutgoingChatstateProtocolEntity(OutgoingChatstateProtocolEntity.STATE_TYPING, Jid.normalize(messageProtocolEntity.getFrom(False))))')
            time.sleep(1)
            self.toLower(OutgoingChatstateProtocolEntity(OutgoingChatstateProtocolEntity.STATE_PAUSED, Jid.normalize(
                messageProtocolEntity.getFrom(False))))  # Set no is writing

            self.enviarMessage(messageProtocolEntity, "Bienvenido al Sistema UV-Clean")
            self.enviarMessage(messageProtocolEntity, "==============================")


            self.enviarMessage(messageProtocolEntity,
                                   "Por favor escriba el numero de opcion que desee consultar:\r\n1- Iniciar Desinfeccion.\n2- Parar Desinfeccion.\n3- Ver Estado.")
            if messageProtocolEntity.getBody().lower() == '1':
                self.enviarMessage(messageProtocolEntity, "Opcion Enviada => " + messageProtocolEntity.getBody())
                self.enviarMessage(messageProtocolEntity, "==> INICIANDO DESINFECION  <==")

                GPIO.output(13, True) #azul

            elif messageProtocolEntity.getBody().lower() == '2':
                self.enviarMessage(messageProtocolEntity, "Opcion Enviada => " + messageProtocolEntity.getBody())
                self.enviarMessage(messageProtocolEntity, "==> PARAR DESINFECION <==")
                GPIO.output(13, False) #azul

            else:
                self.enviarMessage(messageProtocolEntity, "Opcion Invalida!")

        self.toLower(messageProtocolEntity.ack())
        self.toLower(messageProtocolEntity.ack(True))

    @ProtocolEntityCallback("event")
    def onEvent(self, entity):
        if entity.getName() == YowNetworkLayer.EVENT_STATE_DISCONNECTED:
            logger.debug("Disconnected: %s" % entity.getArg("reason"))
            self.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT))
            logger.debug("Disconnected: REINICIO AUTOMATICO")
            restart_program()


    @ProtocolEntityCallback("receipt")

    def onReceipt(self, entity):
        self.toLower(entity.ack())

    def onTextMessage(self,messageProtocolEntity):
        # just print info
        print("Opcion recibida :  %s del Numero %s" % (messageProtocolEntity.getBody(), messageProtocolEntity.getFrom(False)))

    def enviarMessage(self, messageProtocolEntity, message):

        outMessage = TextMessageProtocolEntity(
            message,
            to=messageProtocolEntity.getFrom()
        )
        logger.info(outMessage)

        self.toLower(outMessage)

    def onMediaMessage(self, messageProtocolEntity):
        # just print info
        if messageProtocolEntity.media_type == "image":
            print("Echoing image %s to %s" % (messageProtocolEntity.url, messageProtocolEntity.getFrom(False)))

        elif messageProtocolEntity.media_type == "location":
            print("Echoing location (%s, %s) to %s" % (messageProtocolEntity.getLatitude(), messageProtocolEntity.getLongitude(), messageProtocolEntity.getFrom(False)))

        elif messageProtocolEntity.media_type == "contact":
            print("Echoing contact (%s, %s) to %s" % (messageProtocolEntity.getName(), messageProtocolEntity.getCardData(), messageProtocolEntity.getFrom(False)))

