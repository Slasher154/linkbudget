__author__ = 'thanatv'

# Main class for link calculation.
from linkbudget.models import *
from linkbudget.result import LinkResult
from scipy.interpolate import interp1d
from math import log10, pi


# Link budget constants
BOLTZMANN_CONSTANT = -228.6  # dBJ/K
SPEED_OF_LIGHT = 300000000  # m/s
EQUATORIAL_EARTH_RADIUS = 6378.14  # km
EARTH_FLATTENING_FACTOR = 0.003352813
GEOSYNCHRONOUS_ALTITUDE = 35786  # km


class LinkCalcError(Exception):
    pass


class Link:
    def __init__(self, channel, modem, bandwidth, uplink_station=None,
                 downlink_station=None, gateway=None, rain_model=None, power_optimization=True,
                 power_overused=0, num_carriers_in_transponder=10, force_operating_mode=None, force_contour=None,
                 operating_obo=0):
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
        self.force_contour = force_contour
        self.operating_obo = operating_obo
        self.result = LinkResult()

    def calculate(self):
        """
        Calculate a link budget and return a result object
        """
        uplink = self.result.uplink
        downlink = self.result.downlink
        satellite = self.result.satellite
        carrier = self.result.carrier
        uplink_interferences = self.result.uplink_interferences
        downlink_interferences = self.result.downlink_interferences

        # Runs validation
        try:
            self.validate()
        except LinkCalcError, e:
            raise LinkCalcError("Validation error. {0}".format(e.message))

        # Seek the optimized uplink power. This is the default case unless
        # is_power_optimized is explicitly assigned false.
        # Ex. the IPSTAR return channel normally calculates with full BUC power
        # so no power optimization required.
        uplink_gt = self.channel.uplink_beam.peak_gt  # Beam peak
        uplink_frequency = self.channel.uplink_center_frequency

        # If the operating mode is not forced by user (which should be a normal case), use the transponder's primary
        # mode
        if self.forced_operating_mode:
            operating_mode = self.forced_operating_mode
        else:
            operating_mode = self.channel.transponder.primary_mode

        # ---- C/N Uplink ----


        # Set uplink parameters

        # For forward or broadcast channel, check whether the uplink station or gateway is specified
        if self.uplink_station and isinstance(self.uplink_station, Station):
            uplink_station = Station(self.uplink_station)

        # Use default gateway if specified
        elif self.gateway and isinstance(self.gateway, Gateway) and self.channel.is_forward():
            uplink_station = Gateway(self.gateway).convert_to_station(self.channel)

        else:
            raise LinkCalcError("No uplink station provided.")

        station_eirp = uplink_station.uplink_eirp(uplink_frequency)

        # Find optimized PFD if power optimization is true
        if self.power_optimization:
            optimized_pfd = self.seek_optimized_pfd_uplink(self.channel, self.bandwidth, uplink_gt,
                                                           operating_mode, self.operating_obo)
            # TODO: Write a function for exact slant range
            spreading_loss = self.spreading_loss(GEOSYNCHRONOUS_ALTITUDE)
            optimized_eirp = optimized_pfd + spreading_loss

            # Uplink EIRP will be limited at optimized EIRP if station has higher power
            # Else, the station is underused power
            if station_eirp > optimized_eirp:
                uplink_eirp = optimized_eirp
            else:  # underused power
                uplink_eirp = station_eirp

        else:
            uplink_eirp = station_eirp

        # Calculates power at HPA output per carrier from uplink eirp
        # hpa_output_power_per_carrier = uplink_eirp - uplink_station.antenna.g - uplink.ifl + uplink.upc

        # Finds uplink relative contour of the station
        contour = self.channel.uplink_beam.get_contour(uplink_station.location.latitude, uplink_station.location.longitude)

        # Calculates path losses
        path_loss = self.path_loss(GEOSYNCHRONOUS_ALTITUDE, uplink_frequency)

        # Calculates noise bandwidth
        noise_bandwidth = self.noise_bandwidth(self.bandwidth)

        # Compute C/N Uplink (clear sky and rain fade)
        cn_clear = uplink_eirp + uplink_gt + contour - path_loss - noise_bandwidth - BOLTZMANN_CONSTANT

        # Record uplink station parameters
        uplink.latitude = uplink_station.location.latitude
        uplink.longitude = uplink_station.location.longitude
        uplink.polarization = self.channel.uplink_beam.polarization
        uplink.slant_range = GEOSYNCHRONOUS_ALTITUDE
        uplink.frequency = uplink_frequency
        uplink.elevation = self.channel.uplink_beam.satellite.elevation_angle(uplink_station.location.latitude, uplink_station.location.longitude)
        uplink.ifl = uplink_station.hpa.ifl
        uplink.hpa_obo = uplink_station.hpa.output_backoff
        uplink.upc = uplink_station.hpa.upc
        uplink.antenna_diameter = uplink_station.antenna.diameter
        uplink.antenna_gain = uplink_station.antenna.gain(uplink.frequency)
        uplink.antenna_efficiency = uplink_station.antenna.efficiency(uplink.frequency)
        uplink.latitude = uplink_station.location.latitude
        uplink.longitude = uplink_station.location.longitude

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

        return self.result

    def validate(self):
        """
        Validates the input parameters
        """
        if self.num_carriers_in_transponder < 0:
            raise LinkCalcError("Number of carriers in the transponder {0} cannot be less than zero.".format(
                self.channel.transponder.name))
        if self.power_overused < 0:
            raise LinkCalcError("Power overused cannot be less than zero.")
        if self.bandwidth > self.channel.bandwidth:
            raise LinkCalcError(
                "Input bandwidth ({0} MHz) is bigger than the channel bandwidth ({1}) MHz.".format(str(self.bandwidth),
                                                                                                   str(
                                                                                                       self.channel.bandwidth)))
        if self.bandwidth < 0:
            raise LinkCalcError("Input bandwidth ({0} MHz) cannot be less than zero.".format(str(self.bandwidth)))
        if self.force_operating_mode:
            self.channel.transponder.validate_transponder_mode(self.force_operating_mode)

    def seek_optimized_pfd_uplink(self, channel, carrier_bandwidth, gt_at_location, operating_mode,
                                  operating_obo=0, fca_step=0):
        """
        Seek an optimized PFD uplink of the uplink station
        """

        # In FGM mode, maximum allowable EIRP is equal to an amount that drives the amplifier to get required OBO
        # Default OBO = 0 dB
        if operating_mode is "FGM":
        # TODO Add calculation for different FCA steps
            operating_ibo = channel.transponder.ibo_at_specific_obo(operating_obo)
            backoff_per_carrier = 10 * log10(channel.bandwidth / carrier_bandwidth)
            sfd_channel_at_location = -(
                channel.sfd_max_atten_fgm + gt_at_location)  # Channel SFD in the form of -(X+G/T)
            return sfd_channel_at_location + operating_ibo - backoff_per_carrier

    def spreading_loss(self, slant_range):
        """
        Computes spreading loss from slant range (km) and frequency (GHz)
        """
        return 10 * log10(4 * pi * (slant_range * 10 ** 3) ** 2)

    def gain_1m(self, frequency):
        """
        Computes effective aperture of 1m antenna
        """
        return 10 * log10(4 * pi * (1 / self.wavelength(frequency)))

    def path_loss(self, slant_range, frequency):
        """
        Computes path loss of this link
        """
        return self.spreading_loss(slant_range) + self.gain_1m(frequency)

    def noise_bandwidth(self, bandwidth):
        """
        Returns noise bandwidth from given bandwidth in MHz
        """
        return 10 * log10(bandwidth * 10 ** 6)

    def carrier_over_noise(self):
        pass

    @staticmethod
    def wavelength(frequency):
        return SPEED_OF_LIGHT / (frequency * 10 ** 9)


