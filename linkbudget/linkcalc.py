__author__ = 'thanatv'

# Main class for link calculation.
from linkbudget.result import LinkResult
from math import log10, pi
from linkbudget.itu_r import Attenuation


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
                 operating_obo=0, fgm_attenuation=0):
        """
        Initialize the parameters required for the link budget.
        Required parameters: channel, modem and bandwidth
        Optional parameters: uplink station, downlink station, rain model, power optimization, overused power,
        number of carriers in the transponders
        """
        self.channel = channel
        self.channel.attenuation = fgm_attenuation
        self.channel.operating_obo = operating_obo
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

        :return: LinkResult
        """
        uplink = self.result.uplink
        downlink = self.result.downlink
        satellite = self.result.satellite
        carrier = self.result.carrier
        uplink_interferences = self.result.uplink_interferences
        downlink_interferences = self.result.downlink_interferences
        clear_sky = self.result.clear_sky
        rain_up = self.result.rain_up
        rain_down = self.result.rain_down
        rain_both = self.result.rain_both

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
        uplink_availability = 0.995
        downlink_frequency = self.channel.downlink_center_frequency
        downlink_availability = 0.995

        # If the operating mode is not forced by user (which should be a normal case), use the transponder's primary
        # mode
        if self.force_operating_mode:
            self.channel.operating_mode = self.force_operating_mode
        else:
            self.channel.operating_mode = self.channel.transponder.primary_mode

        # ---- C/N Uplink ----

        # Set uplink parameters

        # For forward or broadcast channel, check whether the uplink station or gateway is specified
        # Import the models here to prevent circular import (two module imports class from each other)
        # http://stackoverflow.com/questions/10212929/import-error-on-django-models-py
        from linkbudget.models import Station
        if isinstance(self.uplink_station, Station):
            uplink_station = self.uplink_station

        # Use default gateway if gateway is true
        elif self.gateway and self.channel.is_forward:
            uplink_gateway = self.channel.default_gateway()
            uplink_station = uplink_gateway.convert_to_station(self.channel)
            if not uplink_station:
                raise LinkCalcError("There is no default gateway for channel {0}".format(self.channel.name))
        else:
            raise LinkCalcError("No uplink station provided.")

        station_eirp = uplink_station.uplink_eirp(uplink_frequency)

        # Find optimized PFD if power optimization is true
        if self.power_optimization:
            optimized_pfd = self.channel.seek_optimized_pfd_uplink(self.bandwidth, uplink_gt)
            # TODO: Write a function for exact slant range
            # If power overused is specified, EIRP required will increase based on that overused power
            spreading_loss = self.spreading_loss(GEOSYNCHRONOUS_ALTITUDE)
            optimized_eirp = optimized_pfd + spreading_loss + self.power_overused

            # Uplink EIRP will be limited at optimized EIRP if station has higher power
            # Else, the station is underused power
            if station_eirp > optimized_eirp:
                uplink_eirp = optimized_eirp
            else:  # underused power or overused but less than given value
                uplink_eirp = station_eirp

        else:
            uplink_eirp = station_eirp

        # Calculates PFD
        uplink_pfd = uplink_eirp - self.spreading_loss(GEOSYNCHRONOUS_ALTITUDE)

        # Declare local variables for uplink station lat/lon
        uplink_lat = uplink_station.location.latitude
        uplink_lon = uplink_station.location.longitude

        # Finds uplink relative contour of the station
        uplink_contour = self.channel.uplink_beam.get_contour(uplink_lat, uplink_lon)

        # Calculates path losses
        uplink_path_loss = self.path_loss(GEOSYNCHRONOUS_ALTITUDE, uplink_frequency)

        # Calculates noise bandwidth
        uplink_noise_bandwidth = self.noise_bandwidth(self.bandwidth)

        # Calculates atmospheric attenuation
        uplink_atten = Attenuation(uplink_frequency, self.channel.uplink_beam.satellite.elevation_angle(uplink_lat,
                                                                                                        uplink_lon),
                                   uplink_station.antenna.diameter, uplink_availability, uplink_lat, uplink_lon)

        # Compute C/N Uplink (clear sky and rain fade)
        cn_uplink_without_atten = uplink_eirp + uplink_gt + uplink_contour - uplink_path_loss - uplink_noise_bandwidth \
            - BOLTZMANN_CONSTANT
        cn_uplink_clear = cn_uplink_without_atten - uplink_atten.total_clear_sky()
        cn_uplink_rain = cn_uplink_without_atten - uplink_atten.total_rain()

        # ---- C/N Downlink ----

        # Compute EIRP downlink of the channel from uplink power flux density and satellite settings
        downlink_eirp_at_peak = self.channel.eirp_downlink_at_peak_per_carrier(uplink_pfd, uplink_gt, self.bandwidth)

        # For return channel, check whether the downlink station is specified.
        # If not, use the default gateway of the channel
        # If downlink station is specified, check the following for usage compatibility:
        # 1. Antenna's receive frequency range and polarization matches the beam
        # 2. Downlink location is in the beam coverage
        # Return error if requirements are not met

        # Compute C/N Downlink (clear sky, up fade only, down fade only and both fade from default availability)

        # Check if downlink station is given
        if isinstance(self.downlink_station, Station):
            downlink_station = self.downlink_station

        # Use default gateway if gateway is true
        elif self.gateway and self.channel.is_return:
            downlink_gateway = self.channel.default_gateway()
            downlink_station = downlink_gateway.convert_to_station(self.channel)
            if not downlink_station:
                raise LinkCalcError("There is no default gateway for channel {0}".format(self.channel.name))
        else:
            raise LinkCalcError("No downlink station provided.")

        # Declare local variables for uplink station lat/lon
        downlink_lat = downlink_station.location.latitude
        downlink_lon = downlink_station.location.longitude

        # Finds downlink relative contour of the station
        downlink_contour = self.channel.downlink_beam.get_contour(downlink_lat, downlink_lon)

        # Finds noise temp at rain
        # TODO: Modify this
        noise_temp_at_rain = 220

        # Calculates downlink G/T at clear sky and rain fade
        downlink_gt_clear_sky = downlink_station.antenna.gt(downlink_frequency, self.channel.uplink_beam.satellite.elevation_angle(downlink_lat, downlink_lon))
        downlink_gt_rain = downlink_station.antenna.gt(downlink_frequency, self.channel.uplink_beam.satellite.elevation_angle(downlink_lat, downlink_lon), noise_temp=noise_temp_at_rain)

        # Calculates path losses
        downlink_path_loss = self.path_loss(GEOSYNCHRONOUS_ALTITUDE, downlink_frequency)

        # Calculates noise bandwidth
        downlink_noise_bandwidth = self.noise_bandwidth(self.bandwidth)

        # Calculates atmospheric attenuation
        downlink_atten = Attenuation(downlink_frequency, self.channel.downlink_beam.satellite.elevation_angle
            (downlink_lat, downlink_lon), downlink_station.antenna.diameter, downlink_availability, downlink_lat, downlink_lon)

        # Compute C/N downlink (clear sky and rain fade)
        cn_downlink_without_atten_clear = downlink_eirp_at_peak + downlink_gt_clear_sky + downlink_contour - downlink_path_loss - downlink_noise_bandwidth \
            - BOLTZMANN_CONSTANT
        cn_downlink_without_atten_rain = downlink_eirp_at_peak + downlink_gt_rain + downlink_contour - downlink_path_loss - downlink_noise_bandwidth \
            - BOLTZMANN_CONSTANT
        cn_downlink_clear = cn_downlink_without_atten_clear - downlink_atten.total_clear_sky()
        cn_downlink_rain = cn_downlink_without_atten_rain - downlink_atten.total_rain()

        # Record uplink budget parameters
        uplink.latitude = uplink_station.location.latitude
        uplink.longitude = uplink_station.location.longitude
        uplink.polarization = self.channel.uplink_beam.polarization
        uplink.slant_range = GEOSYNCHRONOUS_ALTITUDE
        uplink.frequency = uplink_frequency
        uplink.elevation = self.channel.uplink_beam.satellite.elevation_angle(uplink_station.location.latitude,
                                                                              uplink_station.location.longitude)
        uplink.ifl = uplink_station.hpa.ifl
        uplink.hpa_obo = uplink_station.hpa.output_backoff
        uplink.upc = uplink_station.hpa.upc
        uplink.antenna_diameter = uplink_station.antenna.diameter
        uplink.antenna_efficiency = uplink_station.antenna.efficiency(uplink_frequency)
        uplink.antenna_gain = uplink_station.antenna.gain(uplink.frequency)
        uplink.hpa_full_power = uplink_station.hpa.output_power
        uplink.hpa_output_power_per_carrier = uplink_eirp - uplink_station.antenna.gain(
            uplink_frequency) - uplink_station.hpa.ifl + uplink_station.hpa.upc
        uplink.spreading_loss = self.spreading_loss(GEOSYNCHRONOUS_ALTITUDE)
        uplink.relative_contour = uplink_contour
        uplink.gt = uplink_gt
        if self.power_optimization:
            uplink.optimized_eirp = optimized_eirp
        uplink.eirp = uplink_eirp
        uplink.pfd = uplink_pfd
        uplink.availability = 0
        uplink.pointing_loss = self.pointing_loss()
        uplink.xpol_loss = self.xpol_loss()
        uplink.axial_ratio_loss = self.axial_ratio_loss()
        uplink.path_loss = uplink_path_loss
        uplink.cloud_attenuation = uplink_atten.cloud()
        uplink.gas_attenuation = uplink_atten.gas()
        uplink.scin_attenuation = uplink_atten.scin()
        uplink.rain_attenuation = uplink_atten.rain()
        uplink.noise_bandwidth = uplink_noise_bandwidth

        # Record satellite parameters
        sat = self.channel.uplink_beam.satellite
        satellite.name = sat.name
        satellite.orbital_slot = sat.orbital_slot
        satellite.half_station_keeping_box = sat.half_station_keeping_box
        satellite.channel_bandwidth = self.channel.bandwidth
        satellite.peak_gt = self.channel.uplink_beam.peak_gt
        satellite.channel_sfd = self.channel.sfd_channel_at_uplink_location(uplink_gt)
        satellite.channel_input_backoff = self.channel.operating_ibo
        satellite.channel_output_backoff = self.channel.operating_obo
        satellite.channel_operating_mode = self.channel.operating_mode
        satellite.carrier_output_backoff = self.channel.obo_per_carrier(uplink_pfd, uplink_gt, self.bandwidth)
        satellite.peak_saturated_eirp = self.channel.downlink_beam.peak_sat_eirp
        satellite.gain_variation = 0

        # Record downlink budget parameters
        downlink.latitude = downlink_station.location.latitude
        downlink.longitude = downlink_station.location.longitude
        downlink.polarization = self.channel.downlink_beam.polarization
        downlink.slant_range = GEOSYNCHRONOUS_ALTITUDE
        downlink.frequency = downlink_frequency
        downlink.elevation = self.channel.downlink_beam.satellite.elevation_angle(downlink_station.location.latitude,
                                                                              downlink_station.location.longitude)
        downlink.antenna_diameter = downlink_station.antenna.diameter
        downlink.antenna_efficiency = downlink_station.antenna.efficiency(downlink_frequency)
        downlink.antenna_gain = downlink_station.antenna.gain(downlink.frequency)
        downlink.antenna_gt_clear = downlink_gt_clear_sky
        downlink.antenna_gt_rain = downlink_gt_rain
        downlink.relative_contour = downlink_contour
        downlink.eirp_at_location = downlink_eirp_at_peak + downlink_contour
        downlink.availability = downlink_availability
        downlink.pointing_loss = self.pointing_loss()
        downlink.xpol_loss = self.xpol_loss()
        downlink.axial_ratio_loss = self.axial_ratio_loss()
        downlink.path_loss = downlink_path_loss
        downlink.cloud_attenuation = downlink_atten.cloud()
        downlink.gas_attenuation = downlink_atten.gas()
        downlink.scin_attenuation = downlink_atten.scin()
        downlink.rain_attenuation = downlink_atten.rain()
        downlink.noise_bandwidth = downlink_noise_bandwidth

        # Record to C/N results
        clear_sky.cn_uplink = cn_uplink_clear
        clear_sky.cn_downlink = cn_downlink_clear
        clear_sky.cn_total = self.carrier_over_noise_total(cn_uplink_clear, cn_downlink_clear)
        rain_down.cn_downlink = cn_downlink_rain
        rain_down.cn_uplink = cn_uplink_clear
        rain_down.cn_total = self.carrier_over_noise_total(cn_uplink_clear, cn_downlink_rain)
        rain_up.cn_uplink = cn_uplink_rain
        rain_up.cn_downlink = cn_downlink_clear
        rain_up.cn_total = self.carrier_over_noise_total(cn_uplink_rain, cn_downlink_clear)
        rain_both.cn_uplink = cn_uplink_rain
        rain_both.cn_downlink = cn_downlink_rain
        rain_both.cn_total = self.carrier_over_noise_total(cn_uplink_rain, cn_downlink_rain)



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

    def spreading_loss(self, slant_range):
        """
        Computes spreading loss from slant range (km)
        """
        return 10 * log10(4 * pi * (slant_range * 10 ** 3) ** 2)

    def gain_1m(self, frequency):
        """
        Computes gain of 1 sq.meter (dBi/m^2)
        """
        return 10 * log10(4 * pi * (1 / self.wavelength(frequency) ** 2))

    def path_loss(self, slant_range, frequency):
        """
        Computes path loss of this link
        """
        return self.spreading_loss(slant_range) + self.gain_1m(frequency)

    def pointing_loss(self):
        # TODO: Write this function
        return 0.6

    def xpol_loss(self):
        return 0.1

    def axial_ratio_loss(self):
        return 0

    def noise_bandwidth(self, bandwidth):
        """
        Returns noise bandwidth from given bandwidth in MHz
        """
        return 10 * log10(bandwidth * 10 ** 6)

    def carrier_over_noise(self):
        pass

    def carrier_over_noise_total(self, cn_uplink, cn_downlink, ci_uplink=50, ci_downlink=50):
        """
        Returns C/N total from C/N uplink, C/N downlink, C/I uplink and C/N downlink
        """
        return self.cn_operation(cn_uplink, cn_downlink, ci_uplink, ci_downlink)



    @staticmethod
    def wavelength(frequency):
        return SPEED_OF_LIGHT / (frequency * 10 ** 9)


    @staticmethod
    def cn_operation(*args):
        result = 0
        for cn in args:
            result += 1 / (10 ** (cn / 10))
        return -10 * log10(result)