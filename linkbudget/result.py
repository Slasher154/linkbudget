__author__ = 'thanatv'

class LinkResult(object):
    def __init__(self):
        self.uplink = UplinkResult()
        self.satellite = SatelliteResult()
        self.downlink = DownlinkResult()
        self.carrier = CarrierResult()
        self.uplink_interferences = UplinkInterferencesResult()
        self.downlink_interferences = DownlinkInterferencesResult()
        self.clear_sky = ClearSkyResult()
        self.rain_up = RainUplinkResult()
        self.rain_down = RainDownlinkResult()
        self.rain_both = RainBothResult()
        self.warning_messages = []
        self.error_messages = []

    def display(self):
        print "-------------"
        print "Uplink"
        print "EIRP: {0} dBW".format(self.uplink.eirp)
        print "G/T {0} dB/K".format(self.uplink.gt)
        print "Path Loss {0} dB".format(self.uplink.path_loss)
        print "Noise BW {0} dB".format(self.uplink.noise_bw)
        print "C/N Uplink {0} dB".format(self.uplink.cn)
        print "-------------"
        print "downlink"
        print "EIRP: {0} dBW".format(self.downlink.eirp)
        print "G/T {0} dB/K".format(self.downlink.gt)
        print "Path Loss {0} dB".format(self.downlink.path_loss)
        print "Noise BW {0} dB".format(self.downlink.noise_bw)
        print "C/N downlink {0} dB".format(self.downlink.cn)
        print "--------------"
        print "C/N Total {0} dB".format(self.cn_total)


class UplinkResult(object):
    def __init__(self):
        self.latitude = 0
        self.longitude = 0
        self.polarization = ""
        self.slant_range = 0
        self.frequency = 0
        self.elevation = 0
        self.antenna_diameter = 0
        self.antenna_efficiency = 0
        self.antenna_gain = 0
        self.hpa_full_power = 0
        self.hpa_output_power_per_carrier = 0
        self.spreading_loss = 0
        self.relative_contour = 0
        self.gt = 0
        self.optimized_eirp = 0
        self.eirp = 0
        self.upc = 0
        self.ifl = 0
        self.hpa_obo = 0
        self.pfd = 0
        self.availability = 0
        self.pointing_loss = 0
        self.xpol_loss = 0
        self.axial_ratio_loss = 0
        self.path_loss = 0
        self.cloud_attenuation = 0
        self.gas_attenuation = 0
        self.scin_attenuation = 0
        self.rain_attenuation = 0
        self.noise_bandwidth = 0


class SatelliteResult(object):
    def __init__(self):
        self.name = ""
        self.orbital_slot = 0
        self.half_station_keeping_box = 0
        self.channel_bandwidth = 0
        self.peak_gt = 0
        self.channel_sfd = 0
        self.channel_input_backoff = 0
        self.channel_output_backoff = 0
        self.carrier_input_backoff = 0
        self.carrier_output_backoff = 0
        self.channel_operating_mode = ""
        self.peak_saturated_eirp = 0
        self.gain_variation = 0


class DownlinkResult(object):
    def __init__(self):
        self.latitude = 0
        self.longitude = 0
        self.polarization = ""
        self.slant_range = 0
        self.frequency = 0
        self.azimuth = 0
        self.elevation = 0
        self.antenna_diameter = 0
        self.antenna_efficiency = 0
        self.antenna_gain = 0
        self.antenna_gt_clear = 0
        self.antenna_gt_rain = 0
        self.eirp_at_peak = 0
        self.eirp_at_location = 0
        self.ifl_loss = 0
        self.lnb_gain = 0
        self.lnb_temp = 0
        self.clearsky_noise_temp = 0
        self.clearsky_gt = 0
        self.rain_noise_temp = 0
        self.rain_gt = 0
        self.availability = 0
        self.pointing_loss = 0
        self.xpol_loss = 0
        self.axial_ratio_loss = 0
        self.path_loss = 0
        self.cloud_attenuation = 0
        self.gas_attenuation = 0
        self.scin_attenuation = 0
        self.rain_attenuation = 0


class CarrierResult(object):
    def __init__(self):
        self.bandwidth = 0


class UplinkInterferencesResult(object):
    def __init__(self):
        self.adjacent_cells = 50
        self.adjacent_satellite = 50
        self.intermodulation = 50


class DownlinkInterferencesResult(object):
    def __init__(self):
        self.adjacent_cells = 50
        self.adjacent_cells = 50
        self.intermodulation = 50


class ClearSkyResult(object):
    def __init__(self):
        self.cn_uplink = 0
        self.cn_downlink = 0
        self.ci_uplink = 0
        self.ci_downlink = 0
        self.cn_total = 0


class RainUplinkResult(object):
    def __init__(self):
        self.cn_uplink = 0
        self.cn_downlink = 0
        self.ci_uplink = 0
        self.ci_downlink = 0
        self.cn_total = 0


class RainDownlinkResult(object):
    def __init__(self):
        self.cn_uplink = 0
        self.cn_downlink = 0
        self.ci_uplink = 0
        self.ci_downlink = 0
        self.cn_total = 0


class RainBothResult(object):
    def __init__(self):
        self.cn_uplink = 0
        self.cn_downlink = 0
        self.ci_uplink = 0
        self.ci_downlink = 0
        self.cn_total = 0
