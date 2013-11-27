# Create your views here.
from django.shortcuts import render
from django.contrib import messages
from linkbudget.linkcalc import Link, LinkCalcError
from linkbudget.result import LinkResult
from linkbudget.models import *
from django.http import HttpResponse


def index(request):
    """
    Link budget input page
    """
    return render(request, "linkbudget/index.html")


def result(request):
    """
    Link budget result page
    """
    my_string = []
    my_channel = Channel.objects.filter(name="1G").first()
    my_channel2 = Channel.objects.filter(name="207-FWD").first()
    my_link = Link(my_channel2, None, 57.375, gateway=True, operating_obo=-4)
    try:
        link_result = my_link.calculate()
    except LinkCalcError, e:
        my_string.append(e.message)
    else:
        my_string.append("Lat: {0} Degrees".format(str(link_result.uplink.latitude)))
        my_string.append("Lon: {0} Degrees".format(str(link_result.uplink.longitude)))
        my_string.append("Pol: {0} ".format(link_result.uplink.polarization))
        my_string.append("Range: {0} km".format(str(link_result.uplink.slant_range)))
        my_string.append("Frequency: {0} GHz".format(str(link_result.uplink.frequency)))
        my_string.append("Elevation: {0} degrees".format(str(link_result.uplink.elevation)))
        my_string.append("AntennaDiameter {0} m".format(str(link_result.uplink.antenna_diameter)))
        my_string.append("AntennaEfficiency {0} %".format(str(link_result.uplink.antenna_efficiency*100)))
        my_string.append("AntennaGain {0} m".format(str(link_result.uplink.antenna_gain)))
        my_string.append("HPA {0} Watts".format(str(link_result.uplink.hpa_full_power)))
        my_string.append("HPAop.perCarrier {0} Watts".format(str(link_result.uplink.hpa_output_power_per_carrier)))
        my_string.append("SpreadingLoss {0} dB".format(str(link_result.uplink.spreading_loss)))
        my_string.append("Contour {0} dB".format(str(link_result.uplink.relative_contour)))
        my_string.append("G/T {0} dB/K".format(str(link_result.uplink.gt)))
        my_string.append("OptimizedEIRP {0} dBW".format(str(link_result.uplink.optimized_eirp)))
        my_string.append("EIRP {0} dBW".format(str(link_result.uplink.eirp)))
        my_string.append("UPC {0} dB".format(str(link_result.uplink.upc)))
        my_string.append("IFL {0} dB".format(str(link_result.uplink.ifl)))
        my_string.append("OBO {0} dB".format(str(link_result.uplink.hpa_obo)))
        my_string.append("PFD {0} dBW/m^2".format(str(link_result.uplink.pfd)))
        my_string.append("LinkAvailability {0} %".format(str(link_result.uplink.availability)))
        my_string.append("PointingLoss {0} dB".format(str(link_result.uplink.pointing_loss)))
        my_string.append("XPolLoss {0} dB".format(str(link_result.uplink.xpol_loss)))
        my_string.append("AxialRatioLoss {0} dB".format(str(link_result.uplink.axial_ratio_loss)))
        my_string.append("PathLoss {0} dB".format(str(link_result.uplink.axial_ratio_loss)))
        my_string.append("PathLoss {0} dB".format(str(link_result.uplink.path_loss)))
        my_string.append("Cloud {0} dB".format(str(link_result.uplink.cloud_attenuation)))
        my_string.append("Gas {0} dB".format(str(link_result.uplink.gas_attenuation)))
        my_string.append("Scin {0} dB".format(str(link_result.uplink.scin_attenuation)))
        my_string.append("Rain {0} dB".format(str(link_result.uplink.rain_attenuation)))
        my_string.append("NoiseBW {0} dB".format(str(link_result.uplink.noise_bandwidth)))
        my_string.append("C/NUplinkClear {0} dB".format(str(link_result.clear_sky.cn_uplink)))
        my_string.append("C/NUplinkRain {0} dB".format(str(link_result.rain_both.cn_uplink)))
        my_string.append("EIRP Downlink at peak {0} dB".format(str(link_result.downlink.eirp_at_peak)))

    return render(request, "linkbudget/result.html", {"mystring": my_string})