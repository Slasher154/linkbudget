from math import pi, log10, sin, cos, sqrt, atan, tan
from django.db import models
from django.core.validators import MinValueValidator
from linkcalc import LinkCalcError
from linkcalc import SPEED_OF_LIGHT
from scipy.interpolate import interp1d

# Create your models here.

POLARIZATION_CHOICES = (
    ('H', 'H'),
    ('V', 'V'),
    ('LHCP', 'LHCP'),
    ('RHCP', 'RHCP'),
)

ANTENNA_POLARIZATION_CHOICES = (
    ('H Only', 'H'),
    ('V Only', 'V'),
    ('H & V', 'Linear'),
    ('LHCP Only', 'LHCP'),
    ('RHCP Only', 'RHCP'),
    ('LHCP & RHCP', 'Circular')
)

BEAM_TYPE_CHOICES = (
    ('Broadcast', 'Broadcast'),
    ('Spot', 'Spot'),
    ('Shape', 'Shape'),
    ('Augment', 'Augment')
)

# TODO: Write comments and validators for the models


class FrequencyBand(models.Model):
    """
    Represents a frequency band with start and stop range in GHz
    """
    name = models.CharField(max_length=10, help_text="Ex. C, Ku, Ka, S, X")
    start = models.FloatField(help_text="Start frequency of this band in GHz")
    stop = models.FloatField(help_text="Stop frequency of this band in GHz")

    class Meta:
        ordering = ["start"]

    @staticmethod
    def get_frequency_band(frequency):
        """
        Returns frequency band object which given frequency is in
        """
        return FrequencyBand.objects.filter(start__lt=frequency, stop__gt=frequency)[0]

    def __str__(self):
        return "{0}-Band ({1}-{2} GHz)".format(self.name, str(self.start), str(self.stop))


class Satellite(models.Model):
    """
    Represents a satellite object
    """
    name = models.CharField(max_length=50)
    orbital_slot = models.FloatField(help_text="Orbital slot is between -180 to 180.")
    half_station_keeping_box = models.FloatField(help_text="Unit is in degrees")
    launch_date = models.DateField()
    SERVICE_TYPE_CHOICE = (
        ('Conventional', 'Conventional'),
        ('Broadband', 'Broadband'),
        ('Both', 'Hybrid'),
    )
    service_type = models.CharField(max_length=30, choices=SERVICE_TYPE_CHOICE)
    frequency_bands = models.ManyToManyField(FrequencyBand)

    def elevation_angle(self, lat, lon):
        """
        Returns elevation angle from given lat, lon to this satellite
        """
        # Function to find parameters for satellite-earth geometry
        # Based on methods derived by GEOM Spreadsheet
        # Paiboon P. 30 November 1999
        
        # INPUT
        # es_lat = latitude of earth station in degree (positive in North)
        # es_lon = longitude of earth station in degree (positive in East)
        # sat_lon = longitude of satellite in degree (positive in East)
        
        # Constants
        degrees_to_radians = pi / 180
        radians_to_degrees = 180 / pi
        equatorial_earth_radius = 6378144  # Equatorial Earth Radius in meters; changed from 6378159.9
        geo_altitude_radius = 42164500  # Radius at Geosynchronous Altitude; changed from 42166454
        earth_oblateness = 1 / 298.257  # Earth Oblateness
        
        # Calculates basic parameters
        dif_lon = lon - self.orbital_slot
        x_1 = equatorial_earth_radius * cos(lat * degrees_to_radians) / sqrt(1 - (2 - earth_oblateness) * earth_oblateness * sin(lat * degrees_to_radians) ** 2)
        x_2 = geo_altitude_radius * cos(dif_lon * degrees_to_radians)
        y_2 = geo_altitude_radius * sin(dif_lon * degrees_to_radians)
        z_1 = (1 - earth_oblateness) ** 2 * equatorial_earth_radius * sin(lat * degrees_to_radians) / sqrt(1 - (2 - earth_oblateness) * earth_oblateness * sin(lat * degrees_to_radians) ** 2)
        slant_range = sqrt((x_2 - x_1) ** 2 + y_2 ** 2 + z_1 ** 2) / 1000
        
        # Calculates elevation angle
        re_prime = sqrt(x_1 ** 2 + z_1 ** 2)
        cos_el = (re_prime ** 2 + (slant_range * 1000) ** 2 - geo_altitude_radius ** 2) / (2 * re_prime * slant_range * 1000)
        elevation = (atan(-cos_el / sqrt(-cos_el * cos_el + 1)) + 2 * atan(1)) * radians_to_degrees
        if elevation > 90:
            return elevation - 90
        else:
            return elevation

    def azimuth_angle(self, lat, lon):
        """
        Returns azimuth angle from given lat, lon to this satellite
        """
        # Function to find parameters for satellite-earth geometry
        # Based on methods derived by GEOM Spreadsheet
        # Paiboon P. 30 November 1999

        # INPUT
        # es_lat = latitude of earth station in degree (positive in North)
        # es_lon = longitude of earth station in degree (positive in East)
        # sat_lon = longitude of satellite in degree (positive in East)

        # Constants
        degrees_to_radians = pi / 180
        radians_to_degrees = 180 / pi

        # Calculates longitude difference
        dif_lon = lon - self.orbital_slot

        # Calculates azimuth angle
        if dif_lon == 0:
            if lat <= 0:
                return 0
            else:
                return 180
        elif lat == 0:
            if dif_lon < 0:
                return 90
            else:
                return 270
        else:
            cosctr_ang = cos(dif_lon * degrees_to_radians) * cos(lat * degrees_to_radians)
            acos_ctr = atan(-cosctr_ang / sqrt(-cosctr_ang * cosctr_ang + 1)) + 2 * atan(1)
            cos_ga = -tan(lat * degrees_to_radians) / tan(acos_ctr)
            ga = (atan(-cos_ga / sqrt(-cos_ga * cos_ga + 1)) + 2 * atan(1)) * radians_to_degrees
            if dif_lon < 0:
                return ga
            else:
                return 360 - ga

    def __str__(self):
        return self.name


class UplinkBeam(models.Model):
    """
    Represents an uplink beam
    """
    satellite = models.ForeignKey(Satellite, null=True)
    name = models.CharField(max_length=20)
    peak_gt = models.FloatField("Peak G/T")
    polarization = models.CharField(max_length=10, choices=POLARIZATION_CHOICES, null=True)
    type = models.CharField(max_length=20, choices=BEAM_TYPE_CHOICES, blank=True)

    def get_contour(self, lat, lon):
        """
        Returns relative contour from given lat, lon
        """
        # TODO: Write this function
        return 0

    def __str__(self):
        return "{0}: {1}".format(self.satellite.name, self.name)


class UplinkDefinedContour(models.Model):
    """
    Represents a defined contour for uplink beams
    """
    beam = models.ForeignKey(UplinkBeam, null=True)
    CONTOUR_CHOICES = (
        ('50%', '50%'),
        ('EOC', 'EOC'),
        ('EOC-2', 'EOC-2'),
    )
    type = models.CharField(max_length=30, choices=CONTOUR_CHOICES)
    value = models.FloatField()

    def __str__(self):
        return "Beam: {0} / {1}".format(self.beam.name, self.type)


class DownlinkBeam(models.Model):
    """
    Represents a downlink beam
    """
    satellite = models.ForeignKey(Satellite, null=True)
    name = models.CharField(max_length=20)
    peak_sat_eirp = models.FloatField("Peak saturated EIRP")
    polarization = models.CharField(max_length=10, choices=POLARIZATION_CHOICES, null=True)
    type = models.CharField(max_length=20, choices=BEAM_TYPE_CHOICES, blank=True)


    def get_contour(self, lat, lon):
        """
        Returns relative contour from given lat, lon
        """
        # TODO: Write this function
        return 0

    def __str__(self):
        return "{0}: {1}".format(self.satellite.name, self.name)


class DownlinkDefinedContour(models.Model):
    """
    Represents a defined contour for downlink beams
    """
    beam = models.ForeignKey(DownlinkBeam, null=True)
    CONTOUR_CHOICES = (
        ('50%', '50%'),
        ('EOC', 'EOC'),
        ('EOC-2', 'EOC-2'),
    )
    type = models.CharField(max_length=30, choices=CONTOUR_CHOICES)
    value = models.FloatField()

    def __str__(self):
        return "Beam: {0} / {1}".format(self.beam.name, self.type)


class Transponder(models.Model):
    """
    Represents a satellite transponder with high power amplifier
    """
    satellite = models.ForeignKey(Satellite, null=True)
    name = models.CharField(max_length=30)
    hpa_name = models.CharField(max_length=30, help_text="For non-Thaicom satellites, input the transponder name")
    HPA_TYPE_CHOICES = (
        ('TWTA', 'TWTA'),
        ('SSPA', 'SSPA')
    )
    hpa_type = models.CharField(max_length=10, choices=HPA_TYPE_CHOICES)
    linearizer = models.BooleanField()
    dynamic_range = models.FloatField()
    design_alc_deepin = models.FloatField("Designed ALC deep-in (dB)", help_text="Designed deep-in level at full-load "
                                                                                 "for this transponder (positive "
                                                                                 "value). Input 0 if transponder has "
                                                                                 "only FGM mode", default=0)

    MODE_CHOICE = (
        ('ALC', 'ALC'),
        ('FGM', 'FGM'),
    )
    primary_mode = models.CharField(max_length=10, choices=MODE_CHOICE, default="None")
    secondary_mode = models.CharField(max_length=10, choices=MODE_CHOICE, null=True)

    def __str__(self):
        return "{0}: {1}".format(self.satellite.name, self.name)


    def ibo_at_specific_obo(self, requested_obo):
        """
        Returns input backoff of the transponder at specific output backoff
        """

        # Raises error if the transponder has no FGM mode
        if not "FGM" in (self.primary_mode.upper(), self.secondary_mode.upper()):
            raise LinkCalcError("Transponder {0} has no FGM mode".format(self.name))

        # Raises error if requested OBO is more than zero
        elif requested_obo > 0:
            raise LinkCalcError(
                "Expected output backoff of transponder {0} should be negative value.".format(self.name))

        # Raises error if this transponder has no ibo/obo pair in the database
        elif not self.transpondercharacteristic_set.exists():
            raise LinkCalcError("There is no transponder characteristics data for transponder {0}".format(self.name))

        tp_chars_queryset = self.transpondercharacteristic_set.all()

        minimum_obo_ibo_pair = tp_chars_queryset.all()[0]
        maximum_obo_ibo_pair = tp_chars_queryset.all().reverse()[0]

        # If requested OBO is higher than maximum (least negative) in the database, returns an error.
        # (Not allow to uplink to get that OBO level)
        if requested_obo > maximum_obo_ibo_pair.output_backoff:
            raise LinkCalcError("Expected output backoff of {0} dB is higher than transponder {1} "
                                "characteristics at {2} dB".format(str(requested_obo), self.name,
                                                                   str(maximum_obo_ibo_pair.output_backoff)))

        # If requested OBO is lower (more negative) than the lowest in the database, assume the transfer curve is linear
        # for all OBO lower than that.
        if requested_obo < minimum_obo_ibo_pair.output_backoff:
            return minimum_obo_ibo_pair.input_backoff - (minimum_obo_ibo_pair.output_backoff - requested_obo)

        # If requested OBO is within IBO and OBO pairs in the database, interpolate to get the IBO
        list1, list2 = [], []
        for tp_char in tp_chars_queryset:
            list1.append(tp_char.output_backoff)
            list2.append(tp_char.input_backoff)
        interpolated_function = interp1d(list1, list2)
        return interpolated_function(requested_obo)

    def validate_transponder_mode(self, mode):
        return str(mode).lower() in (self.primary_mode.lower(), self.secondary_mode.lower())


class AlcFullLoadBackoff(models.Model):
    """
    Represents a default ALC mode full-load output backoff of the transponder
    """
    transponder = models.ForeignKey(Transponder, null=True)
    operating_output_backoff = models.FloatField(help_text="Operating output backoff at full-load for this transponder")
    contract_output_backoff = models.FloatField(help_text="Contractual output backoff at full-load for this "
                                                          "transponder")

    def __str__(self):
        return "{0}: ALC Full-load output backoff".format(self.transponder)


class TransponderCharacteristic(models.Model):
    """
    Represents a transponder characteristics i.e. relation of IBO, OBO, C/3IM and NPR
    """
    transponder = models.ForeignKey(Transponder, null=True)
    input_backoff = models.FloatField(help_text="Input 0 for IPSTAR transponder at first phase")
    output_backoff = models.FloatField()
    c_3im = models.FloatField("C/3IM (dB)")
    npr = models.FloatField("NPR (dB)")

    class Meta:
        ordering = ['output_backoff']

    def __str__(self):
        return "{0} - IBO {1} dB / OBO {2} dB".format(self.transponder, str(self.input_backoff),
                                                      str(self.output_backoff))


class Channel(models.Model):
    """
    Represents a communication channel from satellite receive antenna to satellite transmit antenna.
    Mainly consists of uplink beam, transponder and downlink beam.
    """
    name = models.CharField(max_length=30)
    uplink_beam = models.ForeignKey(UplinkBeam, null=True)
    downlink_beam = models.ForeignKey(DownlinkBeam, null=True)
    transponder = models.ForeignKey(Transponder, null=True)
    bandwidth = models.FloatField()
    uplink_center_frequency = models.FloatField(help_text="Uplink center frequency in GHz.")
    downlink_center_frequency = models.FloatField(help_text="Downlink center frequency in GHz")
    sfd_max_atten_alc = models.FloatField("SFD at Max Atten ALC.",
                                          help_text="SFD at max channel per transponder in "
                                                    "the form of -(X+G/T). Ex. If SFD = -(88+G/T),"
                                                    "input '88' here",
                                          default=0, validators=[MinValueValidator(0)])
    sfd_max_atten_fgm = models.FloatField("SFD at Max Atten FGM.",
                                          help_text="SFD at max channel per transponder in "
                                                    "the form of -(X+G/T). Ex. If SFD = -(88+G/T),"
                                                    "input '88' here",
                                          default=0, validators=[MinValueValidator(0)])
    CHANNEL_TYPE_CHOICES = (
        ('Forward', 'Forward'),
        ('Return', 'Return'),
        ('Broadcast', 'Broadcast')
    )
    type = models.CharField(max_length=30, choices=CHANNEL_TYPE_CHOICES)
    
    def seek_optimized_pfd_uplink(self, carrier_bandwidth, uplink_gt):
        """
        Seek an optimized PFD uplink of the uplink station
        """
        # In FGM mode, maximum allowable EIRP is equal to an amount that drives the amplifier to get required OBO
        # Default OBO = 0 dB
        if self.operating_mode == "FGM":
            backoff_per_carrier = 10 * log10(self.bandwidth / carrier_bandwidth)
            return self.sfd_channel_at_uplink_location(uplink_gt) + self.operating_ibo - backoff_per_carrier
        # In ALC mode, maximum allowable is equal to an amount that drives the amplifier at desired deepin
        elif self.operating_mode == "ALC":
            return self.sfd_channel_at_uplink_location(uplink_gt) - self.transponder.dynamic_range + self.transponder.\
                design_alc_deepin
        else:
            raise LinkCalcError("No valid operating mode specified for channel {0}".format(self.name))

    def sfd_channel_at_uplink_location(self, uplink_gt):
        """
        Returns SFD per channel at uplink location
        """
        if self.operating_mode == "FGM":
            return -(self.sfd_max_atten_fgm + uplink_gt)-(self.transponder.dynamic_range-self.attenuation)
        elif self.operating_mode == "ALC":
            return -(self.sfd_max_atten_alc + uplink_gt)
        else:
            raise LinkCalcError("No valid operating mode specified for channel {0}".format(self.name))

    def obo_per_carrier(self, uplink_pfd, uplink_gt, carrier_bandwidth):
        """
        Returns output backoff per carrier from given PFD
        """
        if self.operating_mode == "FGM":
            # OBO is sought from linear graph
            ibo_per_carrier = uplink_pfd - self.sfd_channel_at_uplink_location(uplink_gt)
            return ibo_per_carrier - self.operating_ibo + self.operating_obo
        elif self.operating_mode == "ALC":
            # Check if given PFD reaches deep-in or not
            min_sfd = self.sfd_channel_at_uplink_location(uplink_gt) - self.transponder.dynamic_range
            deepin = uplink_pfd - min_sfd  # Not reach deepin dynamic range
            if deepin < 0:
                return self.operating_obo - 10 * log10(self.bandwidth / carrier_bandwidth) + deepin
            else:
                return self.operating_obo - 10 * log10(self.bandwidth / carrier_bandwidth)
        else:
            raise LinkCalcError("No valid operating mode specified for channel {0}".format(self.name))


    def eirp_downlink_at_peak_per_carrier(self, uplink_pfd, uplink_gt, carrier_bandwidth):
        return self.downlink_beam.peak_sat_eirp + self.obo_per_carrier(uplink_pfd, uplink_gt, carrier_bandwidth)

    def default_gateway(self):
        """
        Returns default gateway for this channel
        """
        hpa = self.hpa_set.first()
        if hpa:
            return hpa.gateway
        else:
            return None

    # ------------------ Properties ---------------------       

    @property
    def attenuation(self):
        return self._attenuation

    @attenuation.setter
    def attenuation(self, value):
        self._attenuation = value

    def __str__(self):
        return "{0} | {1} | {2}".format(self.uplink_beam.satellite, self.uplink_beam.name, self.transponder.name)

    @property
    def operating_mode(self):
        return self._operating_mode

    @operating_mode.setter
    def operating_mode(self, value):
        self._operating_mode = value

    @property
    def operating_obo(self):
        return self._operating_obo

    @operating_obo.setter
    def operating_obo(self, value):
        self._operating_obo = value

    @property
    def operating_ibo(self):
        if self.operating_mode == "FGM":
            return self.transponder.ibo_at_specific_obo(self.operating_obo)
        elif self.operating_mode == "ALC":
            return "N/A"
        else:
            raise LinkCalcError("No valid operating mode specified for channel {0}".format(self.name))


    @property
    def is_forward(self):
        return self.type in ('Forward', 'Broadcast')

    @property
    def is_return(self):
        """
        Return true if the chanel is a link from remote site to hub
        """
        return self.type == 'Return'

class AntennaVendor(models.Model):
    """
    Represents an antenna Antenna
    """
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Antenna(models.Model):
    """
    Represents an antenna
    """
    name = models.CharField(max_length=50)
    vendor = models.ForeignKey(AntennaVendor, null=True)
    diameter = models.FloatField()
    minimum_elevation = models.FloatField(help_text="The minimum value possible is 0 degrees")
    maximum_elevation = models.FloatField(help_text="The maximum value possible is 90 degrees")
    ANTENNA_TYPE_CHOICE = (
        ('Parabolic', 'Parabolic'),
        ('Phased Array', 'Phased Array'),
    )
    type = models.CharField(max_length=30, choices=ANTENNA_TYPE_CHOICE)
    has_tracking = models.BooleanField(help_text="True if this antenna has satellite tracking function.", default=False)

    def gain(self, frequency):
        """
        Returns antenna gain at given frequency in GHz
        """
        return 10 * log10(self.efficiency(frequency) * (pi * self.diameter * frequency * 10 ** 9 / SPEED_OF_LIGHT) ** 2)

    def efficiency(self, frequency):
        """
        Returns antenna efficiency at given frequency in GHz
        """
        band = FrequencyBand.get_frequency_band(frequency)
        if band:
            # Seek if there is antenna gain data at this band (from the spec sheet)
            gain_at_frequency = self.antennagain_set.filter(frequency__gt=band.start, frequency__lt=band.stop)

            # If the gain data exists, loop all the gain values to find closest frequency
            # This step is to differentiate between Tx and Rx frequency
            if gain_at_frequency:
                gain_difference = 100
                for g in gain_at_frequency:
                    if abs(g.frequency - frequency) < gain_difference:
                        gain = g
                return 10 ** (gain.value/10) * (SPEED_OF_LIGHT / (pi * gain.frequency * 10 ** 9 * self.diameter)) ** 2
            else:
                return 0.6
        else:
            raise LinkCalcError("Invalid frequency range.")

    def gt(self, frequency, elevation_angle, noise_temp=100):
        """
        Returns antenna G/T at given frequency(GHz) and elevation angle
        """
        # G/T in the database is used by default if stored
        # TODO: Modify to seek from frequency also
        gt = self.antennagt_set.filter(elevation_angle__gt=elevation_angle).order_by('elevation_angle').first()
        if gt:
            return gt
        # If no G/T in the database, use antenna gain and noise temp
        else:
            # TODO: Add accurate functions to noise temp
            # Default noise temp is 100 K
            return self.gain(frequency) - 10 * log10(noise_temp)

    def __str__(self):
        return "{0} {1}".format(self.vendor, self.name)


class AntennaGain(models.Model):
    """
    Represents an antenna gain at each frequency
    """
    antenna = models.ForeignKey(Antenna, null=True)
    frequency = models.FloatField(help_text="Frequency which antenna gain is measured (GHz)")
    value = models.FloatField(help_text="Gain value in dB")

    def __str__(self):
        return "{0} dBi at {1} GHz".format(str(self.value), str(self.frequency))


class AntennaGT(models.Model):
    """
    Represents an antenna G/T at each frequency and elevation angle
    """
    antenna = models.ForeignKey(Antenna, null=True)
    frequency = models.FloatField(help_text="Frequency which antenna G/T is measured (GHz)")
    elevation_angle = models.FloatField(help_text="Elevation angle which antenna G/T is measured (degrees)")
    value = models.FloatField(help_text="G/T value in dB/K")

    class Meta:
        verbose_name = "Antenna G/T"

    def __str__(self):
        return "{0} dB/K at {1} GHz at {2} degrees elevation".format(str(self.value), str(self.frequency),
                                                                     str(self.elevation_angle))


class AntennaNoiseTemperature(models.Model):
    """
    Represents an antenna noise temperature at each elevation angle
    """
    antenna = models.ForeignKey(Antenna, null=True)
    elevation_angle = models.FloatField(help_text="Elevation angle which noise temperature is measured (degrees)")
    value = models.FloatField(help_text="Noise temperature value in Kelvin")

    class Meta:
        verbose_name = "Antenna Noise Temperature"


    def __str__(self):
        return "{0} degrees at {1} degrees elevation".format(str(self.value), str(self.elevation_angle))


class TransmitBand(models.Model):
    """
    Represents a transmit band and polarization for an antenna
    """
    antenna = models.ForeignKey(Antenna, null=True)
    start_frequency = models.FloatField(help_text="Start frequency of the transmit range")
    stop_frequency = models.FloatField(help_text="Stop frequency of the transmit range")
    polarization = models.CharField(max_length=10, choices=ANTENNA_POLARIZATION_CHOICES)

    def __str__(self):
        return "{0}-{1} GHz POL: {2}".format(str(self.start_frequency), str(self.stop_frequency), self.polarization)


class ReceiveBand(models.Model):
    """
    Represents a receive band and polarization for an antenna
    """
    antenna = models.ForeignKey(Antenna, null=True)
    start_frequency = models.FloatField(help_text="Start frequency of the receive range")
    stop_frequency = models.FloatField(help_text="Stop frequency of the receive range")
    polarization = models.CharField(max_length=10, choices=ANTENNA_POLARIZATION_CHOICES)

    def __str__(self):
        return "{0}-{1} GHz POL: {2}".format(str(self.start_frequency), str(self.stop_frequency), self.polarization)


class Location(models.Model):
    name = models.CharField(max_length=50)
    latitude = models.FloatField(help_text="Latitude is between -90 to 90 degrees")
    longitude = models.FloatField(help_text="Longitude is between -180 to 180 degrees")
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    notes = models.CharField(max_length=1000, help_text="Additional notes for this location", blank=True)

    def __str__(self):
        return "{0}, {1}".format(self.name, self.country)


class Gateway(models.Model):
    name = models.CharField(max_length=50)
    PURPOSE_CHOICE = (
        ('Main', 'Main'),
        ('Diversity', 'Diversity'),
    )
    purpose = models.CharField(max_length=20, choices=PURPOSE_CHOICE)
    antenna = models.ForeignKey(Antenna, null=True)
    location = models.ForeignKey(Location, null=True)
    diversity_gateway = models.ForeignKey('self', help_text="Select the diversity gateway if any", blank=True,
                                          null=True)

    def get_hpa_for_channel(self, channel):
        """
        Returns hpa for the given channel
        """
        return self.hpa_set.filter(channels=channel).first()

    def uplink_eirp_for_channel(self, channel, frequency):
        """
        Returns uplink eirp for the given channel
        """
        hpa = self.get_hpa_for_channel(channel)
        if hpa:
            return Hpa(hpa).power_at_antenna_feed() + self.antenna.gain(frequency)
        raise LinkCalcError("Cannot find uplink EIRP of channel {0} of gateway {1}".format(channel.name, self.namee))

    def convert_to_station(self, channel):
        """
        Returns a station object used to uplink into given channel from the gateway object
        """
        hpa = self.get_hpa_for_channel(channel)
        if not hpa:
            return None
        station = Station()
        station.antenna = self.antenna
        station.hpa = hpa
        station.location = self.location
        station.name = self.name
        return station

    def __str__(self):
        return "{0}-{1} : {2}".format(self.name, self.purpose, self.location)


class Hpa(models.Model):
    """
    Represents a high power amplifier for the earth station. Also represents user terminal 's BUC.
    """
    name = models.CharField(max_length=50)
    TYPE_CHOICES = (
        ('BUC', 'BUC'),
        ('HPA', 'HPA'),
    )
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    output_power = models.FloatField(help_text="Saturated output power in Watts")
    output_backoff = models.FloatField(help_text="Default output backoff (dB)")
    c_im3 = models.FloatField("C/3IM", help_text="C/3IM at output backoff. Leave it blank for BUC", default=50)
    npr = models.FloatField("NPR", help_text="NPR at output backoff. Leave it blank for BUC", default=50)
    upc = models.FloatField("UPC", help_text="Default UPC for this amplifier. Positive value")
    ifl = models.FloatField("IFL", help_text="Loss between amplifier output and antenna feed. Negative Value.")
    channels = models.ManyToManyField(Channel, help_text="Satellite channel associated with this HPA (for HPA in"
                                                         "gateway only)", null=True, blank=True)
    gateway = models.ForeignKey(Gateway, help_text="Leave it blank if this HPA is not in the gateway", null=True,
                                blank=True)

    def power_at_antenna_feed(self, ifl=None, obo=None, upc=None):
        """
        Returns output power at antenna feed
        """
        if not ifl:
            ifl = self.ifl
        if not obo:
            obo = self.output_backoff
        if not upc:
            upc = self.upc
        if ifl > 0:
            raise LinkCalcError("IFL of HPA {0} ({1} dB) should be less than zero.".format(self.name, str(ifl)))
        if obo > 0:
            raise LinkCalcError("OBO of HPA {0} ({1} dB) should be less than zero".format(self.name, str(obo)))
        if upc < 0:
            raise LinkCalcError("UPC of HPA {0} ({1} dB) should be more than zero.".format(self.name, str(upc)))
        return 10 ** ((self.output_power + obo + ifl - upc) / 10)


    def __str__(self):
        return "{0} - {1} W".format(self.name, str(int(self.output_power)))


class Station(models.Model):
    """
    Represents a user terminal. Consists of antenna, power amplifier, and location
    """
    name = models.CharField(max_length=50)
    antenna = models.ForeignKey(Antenna, verbose_name="Antenna", help_text="Antenna of this station", null=True)
    hpa = models.ForeignKey(Hpa, verbose_name="Power Amplifier", help_text="Power amplifier of this station", null=True)
    location = models.ForeignKey(Location)

    def __str__(self):
        return self.name

    def uplink_eirp(self, frequency):
        """
        Returns uplink EIRP of this station
        """
        return self.hpa.power_at_antenna_feed() + self.antenna.gain(frequency)


class ModemVendor(models.Model):
    """
    Represents a modem vendor
    """
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Modem(models.Model):
    """
    Represents a satellite modem
    """
    model = models.CharField(max_length=70, help_text="Input the modem without its vendor. Ex. Gilat Skyedge II-C"
                                                      "just put 'Skyedge II-C' here")
    vendor = models.ForeignKey(ModemVendor, null=True)

    def __str__(self):
        return "{0} {1}".format(self.vendor, self.model)


class ModemApplication(models.Model):
    """
    Represents a communication protocol in the modem (DVB-S2, SCPC, TDMA, Outbound/Inbound)
    """
    name = models.CharField(max_length=50)
    modem = models.ForeignKey(Modem, null=True)
    PATH_CHOICES = (
        ('Forward/Outbound', 'Forward'),
        ('Return/Inbound', 'Return'),
        ('Any (hubless system)', 'Both'),
    )
    path = models.CharField(max_length=20, choices=PATH_CHOICES)
    minimum_symbol_rate = models.FloatField(help_text="Minimum symbol rate in Msps")
    maximum_symbol_rate = models.FloatField(help_text="Maximum symbol rate in Msps")
    rolloff_factor = models.FloatField(help_text="Roll-off factor from modem's specification")
    rolloff_factor_from_test = models.FloatField("Roll-off factor from real performance.")
    link_margin = models.FloatField(help_text="Default link margin for this application in dB")

    def get_best_mcg(self, cn_total, link_margin=None):
        """
        Returns best mcg from given C/N total and link margin
        """
        # If link margin is not given, use the application's default link margin (this is common case)
        if not link_margin:
            link_margin = self.link_margin

        # Check if this application is set to use value from real operation test
        if self.use_value_from_test:
            return self.mcg_set.filter(cn_threshold_from_test__lte=cn_total-link_margin).order_by('efficiency_from_test').last()
        else:
            return self.mcg_set.filter(cn_threshold__lte=cn_total-link_margin).order_by('efficiency').last()

    @property
    def use_value_from_test(self):
        try:
            self._use_value_from_test
        except AttributeError:
            self._use_value_from_test = False
        return self._use_value_from_test

    # Set this attribute to True will seek
    @use_value_from_test.setter
    def use_value_from_test(self, value):
        self._use_value_from_test = value

    @property
    def rolloff_factor_for_calculation(self):
        if self.use_value_from_test:
            return self.rolloff_factor_from_test
        return self.rolloff_factor

    def __str__(self):
        return "{0}: {1}".format(self.modem, self.name)


class AvailableSymbolRate(models.Model):
    """
    Represents an available symbol rates for an application
    """
    application = models.ForeignKey(ModemApplication, null=True)
    value = models.FloatField("Symbol Rate (Msps)")

    def __str__(self):
        return "{0} Msps".format(str(self.value))


class MCG(models.Model):
    """
    Represents a modulation and coding scheme of the application
    """
    name = models.CharField(max_length=30)
    application = models.ForeignKey(ModemApplication, null=True)
    fec = models.FloatField("Forward Error Correction (FEC)")
    modulation = models.CharField(max_length=20, help_text="QPSK, 8PSK, 16QAM, etc.")
    efficiency = models.FloatField(help_text="Mod Bit Efficiency (MBE) from modem's specification")
    efficiency_from_test = models.FloatField(help_text="Efficiency from the real test. Put the same value as the"
                                                       " modem's specification if no test provided")
    cn_threshold = models.FloatField("C/N Threshold", help_text="C/N Required for this MCG")
    cn_threshold_from_test = models.FloatField(help_text="C/N required for this MCG from the real test. Put the same"
                                                         "value as the modem's specification if no test provided")

    @property
    def efficiency_for_calculation(self):
        if self.application.use_value_from_test:
            return self.efficiency_from_test
        return self.efficiency

    def __str__(self):
        return "{0} - {1}".format(self.application, self.name)




class ModemOperationMode(models.Model):
    """
    Represents a modem operation mode or network topology which modem can provides.
    Ex. Hub-Remote operation will have outbound application as its forward and inbound application as its return
    """
    name = models.CharField(max_length=50)
    modem = models.ForeignKey(Modem)
    forward_application = models.ForeignKey(ModemApplication, related_name='+')
    return_application = models.ForeignKey(ModemApplication, related_name='+', null=True, blank=True) # 1-Way link can let this blank
    default = models.BooleanField(help_text="True if this operation mode is default for the modem.")

    def __str__(self):
        return "{0} - {1}".format(self.modem, self.name)