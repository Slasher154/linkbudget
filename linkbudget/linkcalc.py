__author__ = 'thanatv'

# Main class for link calculation.
from linkbudget.models import *
from LinkCalcResult import LinkCalcResult

class LinkCalc:
    def __init__(self, channel, modem, bandwidth, uplink_station=None,
                 downlink_station=None, gateway=None, rain_model=None, power_optimization=True,
                 power_overused=0, num_carriers_in_transponder=10, force_operating_mode=None):
        """
        Initialize the parameters required for the link budget.
        Required parameters: channel, modem and bandwidth
        Optional parameters: uplink station, downlink station, rain model, power optimization, overused power,
        number of carriers in the transponders
        """
        self.channel = channel
        self.modem = modem
        self.bandwidth = bandwidth
        self.uplink_station = uplink_station
        self.downlink_station = downlink_station
        self.gateway = gateway
        self.rain_model = rain_model
        self.power_optimization = power_optimization
        self.power_overused = power_overused
        self.num_carriers_in_transponder = num_carriers_in_transponder
        self.force_operating_mode = force_operating_mode
        self.result = LinkCalcResult()


    def calculate(self):
        """
        Calculate a link budget and return a result object
        """
        uplink = self.result.uplink
        downlink = self.result.downlink


        # Seek the optimized uplink power. This is the default case unless
        # is_power_optimized is explicitly assigned false.
        # Ex. the IPSTAR return channel normally calculates with full BUC power
        # so no power optimization required.

        # ---- C/N Uplink ----

        # For forward or broadcast channel, check whether the uplink station is specified.
        # If not, use the default gateway of the channel
        # If uplink station is specified, check the following for usage compatibility:
        # 1. Antenna's transmit frequency range and polarization matches the beam
        # 2. Uplink location is in the beam coverage
        # Return error if requirements are not met

        # Compute C/N Uplink (clear sky and rain fade)

        # ---- C/N Downlink ----

        # Compute EIRP downlink of the channel from uplink power flux density and satellite settings

        # For return channel, check whether the downlink station is specified.
        # If not, use the default gateway of the channel
        # If downlink station is specified, check the following for usage compatibility:
        # 1. Antenna's receive frequency range and polarization matches the beam
        # 2. Downlink location is in the beam coverage
        # Return error if requirements are not met

        # Compute C/N Downlink (clear sky, up fade only, down fade only and both fade from default availability)

        # ---- C/I ----

        # Compute the value of C/I from power source if it has default value of C/I3IM or NPR in the database.

        # Compute C/I from satellite if it has default value of transponder's C/I3M or NPR

        # Compute C/I uplink from adjacent satellites

        # Compute C/I downlink from adjacent satellites

        # Compute C/I uplink from adjacent cells

        # Compute C/I downlink from adjacent cells

        # ---- C/N Total ----

        # Compute C/N Total (clear sky, up fade only, down fade only and both fade )

        # ---- Capacity ----
        # Compute link capacity (clear sky, up fade only, down fade only and both fade )
        # in both MHz and Mbps

        # Pick the MCG at both fade and calculate capacity. If the modem has no ACM function, let capacity
        # at clear sky equals to capacity at both fade

        # Else, pick MCG at clear sky and calculate capacity separately for clear sky condition.

        # Seek the maximum total link availability if needed.

        # Record all parameters into the result object

    def seek_optimized_eirp_uplink(self, transponder, gt_at_location, force_operating_mode=None,
                                   required_output_backoff=0):
        """
        Seek an optimized EIRP uplink of the uplink station
        """

        # If the operating mode is not forced by user (which should be a normal case), use the transponder's primary
        # mode
        operating_mode = ""
        if force_operating_mode:
            operating_mode = force_operating_mode
        else:
            operating_mode = transponder.primary_mode