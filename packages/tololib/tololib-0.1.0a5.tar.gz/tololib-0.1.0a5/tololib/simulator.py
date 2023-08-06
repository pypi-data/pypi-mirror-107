
import logging
from threading import Thread
from time import sleep

from .const import AromaTherapy, Calefaction, LampMode
from .server import ToloServer


logger = logging.getLogger(__name__)


class Simulator(Thread):
    def __init__(self, server: ToloServer) -> None:
        super().__init__(daemon=True)
        self._server = server

    def run(self) -> None:
        logger.debug('simulator started')

        # assign shortcut variables
        status = self._server.status
        settings = self._server.settings

        # define reasonable default values
        status.calefaction = Calefaction.INACTIVE
        status.flow_in = False
        status.flow_out = True
        status.current_humidity = 25
        status.tank_temperature = 15

        settings.target_temperature = 45
        settings.target_humidity = 95
        settings.power_timer = 30
        settings.salt_bath_timer = None
        settings.aroma_therapy = AromaTherapy.B
        settings.sweep_timer = 0
        settings.lamp_mode = LampMode.MANUAL
        settings.fan_timer = 10

        # the loop
        while True:
            if status.power_on:
                status.flow_out = False
                if status.water_level < 3:
                    status.flow_in = True
                    status.water_level += 1
                else:
                    status.flow_in = False

                if status.tank_temperature < 100:
                    status.calefaction = Calefaction.HEAT
                    status.tank_temperature += 5
                else:
                    status.calefaction = Calefaction.KEEP

            else:
                status.flow_in = False
                status.calefaction = Calefaction.INACTIVE
                if status.water_level > 0:
                    status.flow_out = True
                    status.water_level -= 1

            sleep(1)
