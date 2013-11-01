from django.db import models

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
    ('Broadcast', 'Broadcast')
        ('Spot', 'Spot'),
    ('Shape', 'Shape'),
    ('Augment', 'Augment')
)


# Satellite
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

    def __str__(self):
        return self.name


class FrequencyBand(models.Model):
    """
    Represents a frequency band with start and stop range in GHz
    """
    name = models.CharField(max_length=10, help_text="Ex. C, Ku, Ka, S, X")
    start = models.FloatField(help_text="Start frequency of this band in GHz")
    stop = models.FloatField(help_text="Stop frequency of this band in GHz")

    def __str__(self):
        return "{0}-Band ({1}-{2} GHz)".format(self.name, str(self.start), str(self.stop))


class UplinkBeam(models.Model):
    """
    Represents an uplink beam
    """
    satellite = models.ForeignKey(Satellite)
    name = models.CharField(max_length=10)
    peak_gt = models.FloatField("Peak G/T")
    polarization = models.CharField(max_length=10, choices=POLARIZATION_CHOICES)
    sfd_max_atten = models.FloatField("SFD at Max Atten.", help_text="SFD at max attenuation in the form of -(X+G/T). "
                                                                     "Ex. If SFD = -(88+G/T), input '88' here.")
    type = models.CharField(max_length=20, choices=BEAM_TYPE_CHOICES)

    def __str__(self):
        return "{0}: {1}".format(self.satellite.name, self.name)


class UplinkDefinedContour(models.Model):
    """
    Represents a defined contour for uplink beams
    """
    beam = models.ForeignKey(UplinkBeam)
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
    satellite = models.ForeignKey(Satellite)
    name = models.CharField(max_length=10)
    peak_sat_eirp = models.FloatField("Peak saturated EIRP")


class DownlinkDefinedContour(models.Model):
    """
    Represents a defined contour for downlink beams
    """
    beam = models.ForeignKey(DownlinkBeam)
    CONTOUR_CHOICES = (
        ('50%', '50%'),
        ('EOC', 'EOC'),
        ('EOC-2', 'EOC-2'),
    )
    type = models.CharField(max_length=30, choices=CONTOUR_CHOICES)
    value = models.FloatField()


class Transponder(models.Model):
    """
    Represents a satellite transponder with high power amplifier
    """
    satellite = models.ForeignKey(Satellite)
    name = models.CharField(max_length=30)
    hpa_name = models.CharField(max_length=30, help_text="For non-Thaicom satellites, input the transponder name")
    HPA_TYPE_CHOICES = (
        ('TWTA', 'TWTA'),
        ('SSPA', 'SSPA')
    )
    hpa_type = models.CharField(max_length=10, choices=HPA_TYPE_CHOICES)
    linearizer = models.BooleanField()
    dynamic_range = models.FloatField()


class Channel(models.Model):
    """
    Represents a communication channel from satellite receive antenna to satellite transmit antenna.
    Mainly consists of uplink beam, transponder and downlink beam.
    """
    name = models.CharField(max_length=30)
    uplink_beam = models.ForeignKey(UplinkBeam)
    downlink_beam = models.ForeignKey(DownlinkBeam)
    transponder = models.ForeignKey(Transponder)
    bandwidth = models.FloatField()
    center_frequency = models.FloatField(help_text="Unit is in GHz")
    CHANNEL_TYPE_CHOICES = (
        ('Forward', 'Forward'),
        ('Return', 'Return'),
        ('Broadcast', 'Broadcast')
    )
    type = models.CharField(max_length=30, choices=CHANNEL_TYPE_CHOICES)


class Antenna(models.Model):
    """
    Represents an antenna
    """
    name = models.CharField(max_length=50)
    vendor = models.CharField(max_length=50)
    diameter = models.FloatField()
    minimum_elevation = models.FloatField(help_text="The minimum value possible is 0 degrees")
    maximum_elevation = models.FloatField(help_text="The maximum value possible is 90 degrees")
    ANTENNA_TYPE_CHOICE = (
        ('Parabolic', 'Parabolic'),
        ('Phased Array', 'Phased Array'),
    )
    type = models.CharField(max_length=30, choices=ANTENNA_TYPE_CHOICE)
    gains = models.ManyToManyField(AntennaGain, verbose_name="Gain", help_text="Antenna gain at each frequency")
    gts = models.ManyToManyField(AntennaGT, verbose_name="G/T", help_text="Antenna G/T at each frequency and elevation"
                                                                          " angle")
    transmit_bands = models.ManyToManyField(TransmitBand, help_text="Transmit frequency and polarization of this"
                                                                    "antenna")
    receive_bands = models.ManyToManyField(ReceiveBand, help_text="Receive frequency and polarization of this antenna")


class AntennaGain(models.Model):
    """
    Represents an antenna gain at each frequency
    """
    frequency = models.FloatField(help_text="Frequency which antenna gain is measured (GHz)")
    value = models.FloatField(help_text="Gain value in dB")


class AntennaGT(models.Model):
    """
    Represents an antenna G/T at each frequency and elevation angle
    """
    frequency = models.FloatField(help_text="Frequency which antenna G/T is measured (GHz)")
    elevation_angle = models.FloatField(help_text="Elevation angle which antenna G/T is measured (degrees)")
    value = models.FloatField(help_text="G/T value in dB/K")


class TransmitBand(models.Model):
    """
    Represents a transmit band and polarization for an antenna
    """
    start_frequency = models.FloatField(help_text="Start frequency of the transmit range")
    stop_frequency = models.FloatField(help_text="Stop frequency of the transmit range")
    polarization = models.CharField(max_length=10, choices=ANTENNA_POLARIZATION_CHOICES)


class ReceiveBand(models.Model):
    """
    Represents a receive band and polarization for an antenna
    """
    start_frequency = models.FloatField(help_text="Start frequency of the receive range")
    stop_frequency = models.FloatField(help_text="Stop frequency of the receive range")
    polarization = models.CharField(max_length=10, choices=ANTENNA_POLARIZATION_CHOICES)


class Hpa(models.Model):
    """
    Represents a high power amplifier for the earth station. Also represents user terminal 's BUC.
    """
    name = models.CharField(max_length=50)
    output_power = models.FloatField(help_text="Saturated output power in Watts")
    output_backoff = models.CharField(help_text="Default output backoff (dB)")
    c_im3 = models.FloatField("C/3IM", help_text="C/3IM at output backoff. Leave it blank for BUC", default=50)
    npr = models.FloatField("NPR", help_text="NPR at output backoff. Leave it blank for BUC", default=50)
    upc = models.FloatField("UPC", help_text="Default UPC for this amplifier")
    ifl = models.FloatField("IFL", help_text="Loss between amplifier output and antenna feed")


class Location(models.Model):
    name = models.CharField(max_length=50)
    latitude = models.FloatField(help_text="Latitude is between -90 to 90 degrees")
    longitude = models.FloatField(help_text="Longitude is between -180 to 180 degrees")
    notes = models.CharField(max_length=1000, help_text="Additional notes for this location", blank=True)


class Station(models.Model):
    """
    Represents a user terminal. Consists of antenna, power amplifier, and location
    """
    antenna = models.ForeignKey(Antenna, verbose_name="Antenna", help_text="Antenna of this station")
    hpa = models.ForeignKey(Hpa, verbose_name="Power Amplifier", help_text="Power amplifier of this station")
    location = models.ForeignKey(Location)


