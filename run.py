from yowsup.stacks import YowStackBuilder
from layer import EchoLayer
from yowsup.layers import YowLayerEvent
from yowsup.layers.network import YowNetworkLayer
from yowsup.env import YowsupEnv
from yowsup.layers.axolotl.props import PROP_IDENTITY_AUTOTRUST


stackBuilder = YowStackBuilder()

stack = stackBuilder\
    .pushDefaultLayers()\
    .push(EchoLayer)\
    .build()

stack.setProfile("56921788592") # phone
YowsupEnv.setEnv("android")
stack.setProp(PROP_IDENTITY_AUTOTRUST, True)
stack.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT))
stack.loop()
