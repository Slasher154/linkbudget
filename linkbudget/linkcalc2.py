__author__ = 'thanatv'

# Main class for link calculation.
from math import log10, pi
from utilities import wavelength, cn_operation
from linkbudget.itu_r import Attenuation

# Link budget constants
BOLTZMANN_CONSTANT = -228.6  # dBJ/K
SPEED_OF_LIGHT = 300000000  # m/s
EQUATORIAL_EARTH_RADIUS = 6378.14  # km
EARTH_FLATTENING_FACTOR = 0.003352813
GEOSYNCHRONOUS_ALTITUDE = 35786  # km


class LinkCalcError(Exception):
    pass


class Link2:
    def __init__(self, channel, modem_operation_mode, bandwidth, uplink_station=None,
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
        self.modem_operation_mode = modem_operation_mode
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
        self.uplink = Uplink(self)
        self.downlink = Downlink(self)
        self.satellite = Satellite(self)
        self._carrier_over_noise_total_clear_sky = None
        self._carrier_over_noise_total_rain_up = None
        self._carrier_over_noise_total_rain_down = None
        self._carrier_over_noise_total_rain_both = None

    def calculate(self):
        self.uplink.relative_contour = 0
        self.downlink.relative_contour = 0
        self.set_uplink_station()
        self.set_downlink_station()
        self.optimize_power()

    @property
    def carrier_over_noise_total_clear_sky(self):
        if self._carrier_over_noise_total_clear_sky is None:
            self._carrier_over_noise_total_clear_sky = cn_operation(self.uplink.carrier_over_noise_clear_sky, self.uplink.carrier_over_interferences_total, self.downlink.carrier_over_noise_clear_sky, self.downlink.carrier_over_interferences_total)
        return self._carrier_over_noise_total_clear_sky

    @property
    def carrier_over_noise_total_rain_up(self):
        if self._carrier_over_noise_total_rain_up is None:
            self._carrier_over_noise_total_rain_up = cn_operation(self.uplink.carrier_over_noise_rain, self.uplink.carrier_over_interferences_total, self.downlink.carrier_over_noise_clear_sky, self.downlink.carrier_over_interferences_total)
        return self._carrier_over_noise_total_rain_up

    @property
    def carrier_over_noise_total_rain_down(self):
        if self._carrier_over_noise_total_rain_down is None:
            self._carrier_over_noise_total_rain_down = cn_operation(self.uplink.carrier_over_noise_rain, self.uplink.carrier_over_interferences_total, self.downlink.carrier_over_noise_rain, self.downlink.carrier_over_interferences_total)
        return self._carrier_over_noise_total_rain_down

    @property
    def carrier_over_noise_total_rain_both(self):
        if self._carrier_over_noise_total_rain_both is None:
            self._carrier_over_noise_total_rain_both = cn_operation(self.uplink.carrier_over_noise_rain, self.uplink.carrier_over_interferences_total, self.downlink.carrier_over_noise_rain, self.downlink.carrier_over_interferences_total)
        return self._carrier_over_noise_total_rain_both

    def set_uplink_station(self):
        # For forward or broadcast channel, check whether the uplink station or gateway is specified
        # Import the models here to prevent circular import (two module imports class from each other)
        # http://stackoverflow.com/questions/10212929/import-error-on-django-models-py
        from linkbudget.models import Station
        if isinstance(self.uplink_station, Station):
            self.uplink.station = self.uplink_station

        # Use default gateway if gateway is true
        elif self.gateway and self.channel.is_forward:
            uplink_gateway = self.channel.default_gateway
            self.uplink.station = uplink_gateway.convert_to_station(self.channel)
            if not self.uplink.station:
                raise LinkCalcError("There is no default gateway for channel {0}".format(self.channel.name))
        else:
            raise LinkCalcError("No uplink station provided.")

    def set_downlink_station(self):
        from linkbudget.models import Station
        # Check if downlink station is given
        if isinstance(self.downlink_station, Station):
            self.downlink.station = self.downlink_station

        # Use default gateway if gateway is true
        elif self.gateway and self.channel.is_return:
            downlink_gateway = self.channel.default_gateway
            self.downlink.station = downlink_gateway.convert_to_station(self.channel)
            if not self.downlink.station:
                raise LinkCalcError("There is no default gateway for channel {0}".format(self.channel.name))
        else:
            raise LinkCalcError("No downlink station provided.")

    def optimize_power(self):
        # Find optimized EIRP if power optimization is true
        if self.power_optimization:
            self.uplink.optimized_pfd = self.channel.seek_optimized_pfd_uplink(self.bandwidth, self.uplink.gt)


class Uplink:
    def __init__(self, link):
        self.link = link
        self._station = None
        self._lat = None
        self._lon = None
        self._pol = None
        self._slant_range = None
        self._freq = None
        self._elevation = None
        self._ifl = None
        self._hpa_obo = None
        self._upc = None
        self._ant_diam = None
        self._ant_eff = None
        self._ant_gain = None
        self._hpa_full_power = None
        self._hpa_output_power_per_carrier = None
        self._spreading_loss = None
        self._relative_contour = None
        self._peak_gt = None
        self._gt = None
        self._optimized_pfd = None
        self._optimized_eirp = None
        self._eirp = None
        self._pfd = None
        self._single_site_availability = None
        self._availability = None
        self._pointing_loss = None
        self._xpol_loss = None
        self._axial_ratio_loss = None
        self._gain1m = None
        self._path_loss = None
        self._atten = None
        self._cloud_atten = None
        self._gas_atten = None
        self._scin_atten = None
        self._rain_atten = None
        self._noise_bw = None
        self._carrier_over_noise_clear_sky = None
        self._carrier_over_noise_rain = None
        self._carrier_over_interferences_adjacent_cells = None
        self._carrier_over_interferences_adjacent_satellites = None
        self._carrier_over_interferences_intermodulation = None
        self._carrier_over_interferences_total = None

    @property
    def station(self):
        return self._station

    @station.setter
    def station(self, value):
        self._station = value

    @property
    def relative_contour(self):
        if self._relative_contour is None:
            self._relative_contour = self.link.channel.uplink_beam.get_contour(self.latitude, self.longitude)
        return self._relative_contour
    
    @relative_contour.setter
    def relative_contour(self, value):
        self._relative_contour = value

    @property
    def single_site_availability(self):
        if self._single_site_availability is None:
            self._single_site_availability = 99.5
        return self._single_site_availability

    @single_site_availability.setter
    def single_site_availability(self, value):
        self._single_site_availability = value

    @property
    def optimized_pfd(self):
        return self._optimized_pfd

    @optimized_pfd.setter
    def optimized_pfd(self, value):
        self._optimized_pfd = value
    
    @property
    def latitude(self):
        if self._lat is None:
            self._lat = self.station.location.latitude
        return self._lat

    @property
    def longitude(self):
        if self._lon is None:
            self._lon = self.station.location.longitude
        return self._lon

    @property
    def polarization(self):
        if self._pol is None:
            self._pol = self.link.channel.uplink_beam.polarization
        return self._pol

    @property
    def slant_range(self):
        #TODO is None: Fixed this
        if self._slant_range is None:
            self._slant_range = GEOSYNCHRONOUS_ALTITUDE
        return self._slant_range

    @property
    def frequency(self):
        if self._freq is None:
            self._freq = self.link.channel.uplink_center_frequency
        return self._freq

    @property
    def elevation(self):
        if self._elevation is None:
            self._elevation = self.link.channel.uplink_beam.satellite.elevation_angle(self.latitude, self.longitude)
        return self._elevation

    @property
    def ifl(self):
        if self._ifl is None:
            self._ifl = self.station.hpa.ifl
        return self._ifl

    @property
    def hpa_obo(self):
        if self._hpa_obo is None:
            self._hpa_obo = self.station.hpa.output_backoff
        return self._hpa_obo

    @property
    def upc(self):
        if self._upc is None:
            self._upc = self.station.hpa.upc
        return self._upc

    @property
    def antenna_diameter(self):
        if self._ant_diam is None:
            self._ant_diam = self.station.antenna.diameter
        return self._ant_diam

    @property
    def antenna_efficiency(self):
        if self._ant_eff is None:
            self._ant_eff = self.station.antenna.efficiency(self.frequency)
        return self._ant_eff

    @property
    def antenna_gain(self):
        if self._ant_gain is None:
            self._ant_gain = self.station.antenna.gain(self.frequency)
        return self._ant_gain

    @property
    def hpa_full_power(self):
        if self._hpa_full_power is None:
            self._hpa_full_power = self.station.hpa.output_power
        return self._hpa_full_power

    @property
    def hpa_output_power_per_carrier(self):
        if self._hpa_output_power_per_carrier is None:
            self._hpa_output_power_per_carrier = self.eirp - self.antenna_gain - self.ifl + self.upc
        return self._hpa_output_power_per_carrier

    @property
    def peak_gt(self):
        if self._peak_gt is None:
            self._peak_gt = self.link.channel.uplink_beam.peak_gt
        return self._peak_gt

    @property
    def gt(self):
        if self._gt is None:
            self._gt = self.peak_gt + self.relative_contour
        return self._gt

    @property
    def optimized_eirp(self):
        if self._optimized_eirp is None:
            if self.optimized_pfd is not None:
                self._optimized_eirp = self.optimized_pfd + self.spreading_loss + self.link.power_overused
        return self._optimized_eirp

    @property
    def eirp(self):
        if self._eirp is None:
            station_eirp = self.station.uplink_eirp(self.frequency)
            if self._optimized_eirp is None:  # No EIRP optimization
                self._eirp = station_eirp
            elif self._optimized_eirp > station_eirp:
                self._eirp = station_eirp
            else:
                self._eirp = self.optimized_eirp
        return self._eirp

    @property
    def pfd(self):
        if self._pfd is None:
            self._pfd = self.eirp - self.spreading_loss
        return self._pfd

    @property
    def spreading_loss(self):
        if self._spreading_loss is None:
            self._spreading_loss = 10 * log10(4 * pi * (self.slant_range * 10 ** 3) ** 2)
        return self._spreading_loss

    @property
    def pointing_loss(self):
        # TODO: Write this function
        if self._pointing_loss is None:
            self._pointing_loss = 0.6
        return self._pointing_loss

    @property
    def xpol_loss(self):
        if self._xpol_loss is None:
            self._xpol_loss = 0
        return self._xpol_loss

    @property
    def axial_ratio_loss(self):
        if self._axial_ratio_loss is None:
            self._axial_ratio_loss = 0
        return self._axial_ratio_loss

    @property
    def gain1m(self):
        if self._gain1m is None:
            self._gain1m = 10 * log10(4 * pi * (1 / wavelength(self.frequency) ** 2))
        return self._gain1m

    @property
    def path_loss(self):
        if self._path_loss is None:
            self._path_loss = self.spreading_loss + self.gain1m
        return self._path_loss

    @property
    def availability(self):
        pass

    @property
    def atten(self):
        if self._atten is None:
            self._atten = Attenuation(self.frequency, self.elevation, self.antenna_diameter, self.polarization, self.single_site_availability, self.latitude, self.longitude, self.antenna_efficiency)
        return self._atten

    @property
    def cloud_atten(self):
        if self._cloud_atten is None:
            self._cloud_atten = self.atten.cloud
        return self._cloud_atten

    @property
    def scin_atten(self):
        if self._scin_atten is None:
            self._scin_atten = self.atten.scin
        return self._scin_atten

    @property
    def gas_atten(self):
        if self._gas_atten is None:
            self._gas_atten = self.atten.gas
        return self._gas_atten

    @property
    def rain_atten(self):
        if self._rain_atten is None:
            self._rain_atten = self.atten.rain
        return self._rain_atten

    @property
    def noise_bandwidth(self):
        if self._noise_bw is None:
            self._noise_bw = 10 * log10(self.link.bandwidth * 10 ** 6)
        return self._noise_bw

    @property
    def carrier_over_noise_clear_sky(self):
        if self._carrier_over_noise_clear_sky is None:
            self._carrier_over_noise_clear_sky = self.eirp + self.gt - self.path_loss - self.noise_bandwidth - BOLTZMANN_CONSTANT - self.atten.total_clear_sky
        return self._carrier_over_noise_clear_sky

    @property
    def carrier_over_noise_rain(self):
        if self._carrier_over_noise_rain is None:
            self._carrier_over_noise_rain = self.eirp + self.gt - self.path_loss - self.noise_bandwidth - BOLTZMANN_CONSTANT - self.atten.total_rain
        return self._carrier_over_noise_rain

    @property
    def carrier_over_interferences_adjacent_cells(self):
        if self._carrier_over_interferences_adjacent_cells is None:
            self._carrier_over_interferences_adjacent_cells = 50
        return self._carrier_over_interferences_adjacent_cells

    @property
    def carrier_over_interferences_adjacent_satellites(self):
        if self._carrier_over_interferences_adjacent_satellites is None:
            self._carrier_over_interferences_adjacent_satellites = 50
        return self._carrier_over_interferences_adjacent_satellites

    @property
    def carrier_over_interferences_intermodulation(self):
        if self._carrier_over_interferences_intermodulation is None:
            self._carrier_over_interferences_intermodulation = 50
        return self._carrier_over_interferences_intermodulation

    @property
    def carrier_over_interferences_total(self):
        if self._carrier_over_interferences_total is None:
            self._carrier_over_interferences_total = cn_operation(self.carrier_over_interferences_adjacent_cells, self.carrier_over_interferences_adjacent_satellites, self.carrier_over_interferences_intermodulation)
        return self._carrier_over_interferences_total


class Satellite:
    def __init__(self, link):
        self.link = link
        self._name = None
        self._channel_name = None
        self._orbital_slot = None
        self._half_station_keeping_box = None
        self._channel_bandwidth = None
        self._peak_gt = None
        self._channel_sfd = None
        self._channel_input_backoff = None
        self._channel_output_backoff = None
        self._channel_operating_mode = None
        self._carrier_output_backoff = None
        self._deepin_per_carrier = None
        self._peak_saturated_eirp = None
        self._gain_variation = None
        self._peak_eirp_per_carrier = None

    @property
    def name(self):
        if self._name is None:
            self._name = self.link.channel.uplink_beam.satellite.name
        return self._name

    @property
    def channel_name(self):
        if self._channel_name is None:
            self._channel_name = self.link.channel.name
        return self._channel_name

    @property
    def orbital_slot(self):
        if self._orbital_slot is None:
            self._orbital_slot = self.link.channel.uplink_beam.satellite.orbital_slot
        return self._orbital_slot

    @property
    def half_station_keeping_box(self):
        if self._half_station_keeping_box is None:
            self._half_station_keeping_box = self.link.channel.uplink_beam.satellite.half_station_keeping_box
        return self._half_station_keeping_box

    @property
    def channel_bandwidth(self):
        if self._channel_bandwidth is None:
            self._channel_bandwidth = self.link.channel.bandwidth
        return self._channel_bandwidth

    @property
    def peak_gt(self):
        if self._peak_gt is None:
            self._peak_gt = self.link.channel.uplink_beam.peak_gt
        return self._peak_gt

    @property
    def channel_sfd(self):
        if self._channel_sfd is None:
            self._channel_sfd = self.link.channel.sfd_channel_at_uplink_location(self.link.uplink.gt)
        return self._channel_sfd

    @property
    def channel_input_backoff(self):
        if self._channel_input_backoff is None:
            self._channel_input_backoff = self.link.channel.operating_ibo
        return self._channel_input_backoff

    @property
    def channel_output_backoff(self):
        if self._channel_output_backoff is None:
            self._channel_output_backoff = self.link.channel.operating_obo
        return self._channel_output_backoff

    @property
    def channel_operating_mode(self):
        if self._channel_operating_mode is None:
            self._channel_operating_mode = self.link.channel.operating_mode
        return self._channel_operating_mode

    @property
    def carrier_output_backoff(self):
        if self._carrier_output_backoff is None:
            self._carrier_output_backoff = self.link.channel.obo_per_carrier(self.link.uplink.pfd, self.link.uplink.gt, self.link.bandwidth)
        return self._carrier_output_backoff

    @property
    def deepin_per_carrier(self):
        if self._deepin_per_carrier is None:
            self._deepin_per_carrier = self.link.channel.deepin_per_carrier(self.link.uplink.pfd, self.link.uplink.gt, self.link.bandwidth)
        return self._deepin_per_carrier

    @property
    def peak_saturated_eirp(self):
        if self._peak_saturated_eirp is None:
            self._peak_saturated_eirp = self.link.channel.downlink_beam.peak_sat_eirp
        return self._peak_saturated_eirp

    @property
    def gain_variation(self):
        if self._gain_variation is None:
            self._gain_variation = 0
        return self._gain_variation

    @property
    def peak_eirp_per_carrier(self):
        if self._peak_eirp_per_carrier is None:
            self._peak_eirp_per_carrier = self.peak_saturated_eirp + self.carrier_output_backoff
        return self._peak_eirp_per_carrier


class Downlink:
    def __init__(self, link):
        self.link = link
        self._station = None
        self._lat = None
        self._lon = None
        self._pol = None
        self._slant_range = None
        self._freq = None
        self._elevation = None
        self._ant_diam = None
        self._ant_gain = None
        self._ant_eff = None
        self._ant_gain = None
        self._ant_gt_clear = None
        self._ant_gt_rain = None
        self._relative_contour = None
        self._eirp_at_location = None
        self._single_site_availability = None
        self._pointing_loss = None
        self._xpol_loss = None
        self._axial_ratio_loss = None
        self._spreading_loss = None
        self._gain1m = None
        self._path_loss = None
        self._atten = None
        self._cloud_atten = None
        self._gas_atten = None
        self._scin_atten = None
        self._rain_atten = None
        self._noise_bw = None
        self._carrier_over_noise_clear_sky = None
        self._carrier_over_noise_rain = None
        self._carrier_over_interferences_adjacent_cells = None
        self._carrier_over_interferences_adjacent_satellites = None
        self._carrier_over_interferences_intermodulation = None
        self._carrier_over_interferences_total = None

    @property
    def station(self):
        return self._station

    @station.setter
    def station(self, value):
        self._station = value

    @property
    def relative_contour(self):
        if self._relative_contour is None:
            self._relative_contour = self.link.channel.downlink_beam.get_contour(self.latitude, self.longitude)
        return self._relative_contour

    @relative_contour.setter
    def relative_contour(self, value):
        self._relative_contour = value

    @property
    def latitude(self):
        if self._lat is None:
            self._lat = self.station.location.latitude
        return self._lat

    @property
    def longitude(self):
        if self._lon is None:
            self._lon = self.station.location.longitude
        return self._lon

    @property
    def polarization(self):
        if self._pol is None:
            self._pol = self.link.channel.downlink_beam.polarization
        return self._pol

    @property
    def slant_range(self):
        if self._slant_range is None:
            self._slant_range = GEOSYNCHRONOUS_ALTITUDE
        return self._slant_range

    @property
    def frequency(self):
        if self._freq is None:
            self._freq = self.link.channel.downlink_center_frequency
        return self._freq

    @property
    def elevation(self):
        if self._elevation is None:
            self._elevation = self.link.channel.downlink_beam.satellite.elevation_angle(self.latitude, self.longitude)
        return self._elevation

    @property
    def antenna_diameter(self):
        if self._ant_diam is None:
            self._ant_diam = self.station.antenna.diameter
        return self._ant_diam

    @property
    def antenna_efficiency(self):
        if self._ant_eff is None:
            self._ant_eff = self.station.antenna.efficiency(self.frequency)
        return self._ant_eff

    @property
    def antenna_gain(self):
        if self._ant_gain is None:
            self._ant_gain = self.station.antenna.gain(self.frequency)
        return self._ant_gain

    @property
    def antenna_gt_clear(self):
        if self._ant_gt_clear is None:
            self._ant_gt_clear = self.station.antenna.gt(self.frequency, self.elevation)
        return self._ant_gt_clear

    @property
    def antenna_gt_rain(self):
        if self._ant_gt_rain is None:
            #TODO : Modify this
            noise_temp_at_rain = 220
            self._ant_gt_rain = self.station.antenna.gt(self.frequency, self.elevation, noise_temp_at_rain)
        return self._ant_gt_rain

    @property
    def eirp_at_location(self):
        if self._eirp_at_location is None:
            self._eirp_at_location = self.link.satellite.peak_eirp_per_carrier + self.relative_contour
        return self._eirp_at_location

    @property
    def single_site_availability(self):
        if self._single_site_availability is None:
            self._single_site_availability = 99.5
        return self._single_site_availability

    @property
    def pointing_loss(self):
        if self._pointing_loss is None:
            #TODO: Write this function
            self._pointing_loss = 0.6
        return self._pointing_loss

    @property
    def xpol_loss(self):
        if self._xpol_loss is None:
            self._xpol_loss = 0
        return self._xpol_loss

    @property
    def axial_ratio_loss(self):
        if self._axial_ratio_loss is None:
            self._axial_ratio_loss = 0
        return self._axial_ratio_loss

    @property
    def gain1m(self):
        if self._gain1m is None:
            self._gain1m = 10 * log10(4 * pi * (1 / wavelength(self.frequency) ** 2))
        return self._gain1m

    @property
    def spreading_loss(self):
        if self._spreading_loss is None:
            self._spreading_loss = 10 * log10(4 * pi * (self.slant_range * 10 ** 3) ** 2)
        return self._spreading_loss

    @property
    def path_loss(self):
        if self._path_loss is None:
            self._path_loss = self.spreading_loss + self.gain1m
        return self._path_loss

    @property
    def atten(self):
        if self._atten is None:
            self._atten = Attenuation(self.frequency, self.elevation, self.antenna_diameter, self.polarization, self.single_site_availability, self.latitude, self.longitude, self.antenna_efficiency)
        return self._atten

    @property
    def cloud_atten(self):
        if self._cloud_atten is None:
            self._cloud_atten = self.atten.cloud
        return self._cloud_atten

    @property
    def gas_atten(self):
        if self._gas_atten is None:
            self._gas_atten = self.atten.gas
        return self._gas_atten

    @property
    def scin_atten(self):
        if self._scin_atten is None:
            self._scin_atten = self.atten.scin
        return self._scin_atten

    @property
    def rain_atten(self):
        if self._rain_atten is None:
            self._rain_atten = self.atten.rain
        return self._rain_atten

    @property
    def noise_bandwidth(self):
        if self._noise_bw is None:
            self._noise_bw = 10 * log10(self.link.bandwidth * 10 ** 6)
        return self._noise_bw

    @property
    def carrier_over_noise_clear_sky(self):
        if self._carrier_over_noise_clear_sky is None:
            self._carrier_over_noise_clear_sky = self.eirp_at_location + self.antenna_gt_clear - self.path_loss - self.noise_bandwidth - BOLTZMANN_CONSTANT - self.atten.total_clear_sky
        return self._carrier_over_noise_clear_sky

    @property
    def carrier_over_noise_rain(self):
        if self._carrier_over_noise_rain is None:
            self._carrier_over_noise_rain = self.eirp_at_location + self.antenna_gt_rain - self.path_loss - self.noise_bandwidth - BOLTZMANN_CONSTANT - self.atten.total_rain
        return self._carrier_over_noise_rain

    @property
    def carrier_over_interferences_adjacent_cells(self):
        if self._carrier_over_interferences_adjacent_cells is None:
            self._carrier_over_interferences_adjacent_cells = 50
        return self._carrier_over_interferences_adjacent_cells

    @property
    def carrier_over_interferences_adjacent_satellites(self):
        if self._carrier_over_interferences_adjacent_satellites is None:
            self._carrier_over_interferences_adjacent_satellites = 50
        return self._carrier_over_interferences_adjacent_satellites

    @property
    def carrier_over_interferences_intermodulation(self):
        if self._carrier_over_interferences_intermodulation is None:
            self._carrier_over_interferences_intermodulation = 50
        return self._carrier_over_interferences_intermodulation

    @property
    def carrier_over_interferences_total(self):
        if self._carrier_over_interferences_total is None:
            self._carrier_over_interferences_total = cn_operation(self.carrier_over_interferences_adjacent_cells, self.carrier_over_interferences_adjacent_satellites, self.carrier_over_interferences_intermodulation)
        return self._carrier_over_interferences_total


class Carrier:
    def __init__(self, link, condition, cn_total, link_margin=None):
        self.link = link
        self.condition = condition
        self.cn_total = cn_total
        self.link_margin = link_margin
        if link_margin is None:
            self.link_margin = 0.01
        self._application = None
        self._modulation = None
        self._capacity_per_carrier = None

    @property
    def application(self):
        if self._application is None:
            # Find modem application based on modem operation mode and type of channel (FWD/RTN)
            if self.link.channel.is_forward:
                self._application = self.link.modem_operation_mode.forward_application
            elif self.link.channel.is_return:
                self._application = self.link.modem_operation_mode.return_application
            else:
                raise LinkCalcError("Cannot identify channel type")
        return self._application

    @property
    def modulation(self):
        if self._modulation is None:
            self._modulation = self.application.get_best_mcg(self.cn_total, self.link_margin)
        return self._modulation

    @property
    def capacity_per_carrier(self):
        if self._capacity_per_carrier is None:
            self._capacity_per_carrier = (self.link.bandwidth / self.application.rolloff_factor_for_calculation) * self.modulation.efficiency_for_calculation
        return self._capacity_per_carrier




