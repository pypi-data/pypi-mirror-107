Overview
========

A system for automated device discovery and commmunication,
using UDP (for discovery) and MQTT (via mosquito and
Paho-mqtt) for communication.

It is a work in progress.

Installation
============

The Device Net doesn't install on its own, but is part of a Module or 
Controller as a client library, to manage networking and communications.

When used on a Module, that project needs to add these entries to their
`requirements.txt`:

* paho-mqtt
* pi-device-net

When used on a Controller, that project needs to add these to its 
`requirements.txt`:

* paho-mqtt
* pi-device-net>=0.1.20
* mosquito

In addition, on the Controller system, you need to install and launch the
Mosquito service during device setup:

    sudo apt-get update
    sudo apt-get install mosquitto
 
Development
===========
