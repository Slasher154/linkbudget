# Create your views here.
from django.shortcuts import render
from django.contrib import messages
from linkbudget.linkcalc import Link, LinkCalcError
from linkbudget.linkcalc2 import Link2
from linkbudget.result import LinkResult
from linkbudget.models import *
from django.http import HttpResponse
import time


def index(request):
    """
    Link budget input page
    """
    return render(request, "linkbudget/index.html")


def result(request):
    """
    Link budget result page
    """
    start_time = time.time()
    uplink = []
    downlink = []
    satellite = []
    clear_sky = []
    rain_up = []
    rain_down = []
    rain_both = []
    my_channel = Channel.objects.filter(name="1G").first()
    my_channel2 = Channel.objects.filter(name="207-FWD").first()
    my_channel3 = Channel.objects.filter(name="207-RTN").first()
    my_station = Station.objects.filter(name="mystation").first()
    my_station2 = Station.objects.filter(name="mystation-cband").first()
    my_app = ModemOperationMode.objects.filter(name="Hub-Remote").first()
    old_link = False
    my_link = Link(my_channel, my_app, 36, gateway=True, downlink_station=my_station2, operating_obo=-4)
    my_link2 = Link(my_channel2, my_app, 57.375, gateway=True, downlink_station=my_station, operating_obo=-4, num_carriers_in_transponder=2)
    my_link3 = Link(my_channel3, my_app, 2.5, gateway=True, uplink_station=my_station, operating_obo=-9.5)
    #my_link4 = Link2(my_channel3, my_app, 2.5, gateway=True, uplink_station=my_station, operating_obo=-9.5)
    link_result = None
    try:
        #link_result = my_link.calculate()
        #link_result = my_link2.calculate()
        #link_result = my_link3.calculate()
        for i in range(0, 500):
            if old_link:
                my_link4 = Link(my_channel3, my_app, 2.5, gateway=True, uplink_station=my_station, operating_obo=-9.5)
                link_result = my_link4.calculate()
            else:
                my_link4 = Link2(my_channel3, my_app, 2.5, gateway=True, uplink_station=my_station, operating_obo=-9.5)
                my_link4.calculate()
    except LinkCalcError, e:
        uplink.append(e.message)
    else:
        if not old_link:
            #---------------------------UPLINK-----------------------------------------
            uplink.append("Lat: {0} Degrees".format(str(my_link4.uplink.latitude)))
            uplink.append("Lon: {0} Degrees".format(str(my_link4.uplink.longitude)))
            uplink.append("Pol: {0} ".format(my_link4.uplink.polarization))
            uplink.append("Range: {0} km".format(str(my_link4.uplink.slant_range)))
            uplink.append("Frequency: {0} GHz".format(str(my_link4.uplink.frequency)))
            uplink.append("Elevation: {0} degrees".format(str(my_link4.uplink.elevation)))
            uplink.append("AntennaDiameter {0} m".format(str(my_link4.uplink.antenna_diameter)))
            uplink.append("AntennaEfficiency {0} %".format(str(my_link4.uplink.antenna_efficiency*100)))
            uplink.append("AntennaGain {0} m".format(str(my_link4.uplink.antenna_gain)))
            uplink.append("HPA {0} Watts".format(str(my_link4.uplink.hpa_full_power)))
            uplink.append("HPAop.perCarrier {0} Watts".format(str(my_link4.uplink.hpa_output_power_per_carrier)))
            uplink.append("SpreadingLoss {0} dB".format(str(my_link4.uplink.spreading_loss)))
            uplink.append("Contour {0} dB".format(str(my_link4.uplink.relative_contour)))
            uplink.append("G/T {0} dB/K".format(str(my_link4.uplink.gt)))
            uplink.append("OptimizedEIRP {0} dBW".format(str(my_link4.uplink.optimized_eirp)))
            uplink.append("EIRP {0} dBW".format(str(my_link4.uplink.eirp)))
            uplink.append("UPC {0} dB".format(str(my_link4.uplink.upc)))
            uplink.append("IFL {0} dB".format(str(my_link4.uplink.ifl)))
            uplink.append("OBO {0} dB".format(str(my_link4.uplink.hpa_obo)))
            uplink.append("PFD {0} dBW/m^2".format(str(my_link4.uplink.pfd)))
            uplink.append("LinkAvailability {0} %".format(str(my_link4.uplink.availability)))
            uplink.append("PointingLoss {0} dB".format(str(my_link4.uplink.pointing_loss)))
            uplink.append("XPolLoss {0} dB".format(str(my_link4.uplink.xpol_loss)))
            uplink.append("AxialRatioLoss {0} dB".format(str(my_link4.uplink.axial_ratio_loss)))
            uplink.append("PathLoss {0} dB".format(str(my_link4.uplink.axial_ratio_loss)))
            uplink.append("PathLoss {0} dB".format(str(my_link4.uplink.path_loss)))
            uplink.append("Cloud {0} dB".format(str(my_link4.uplink.cloud_atten)))
            uplink.append("Gas {0} dB".format(str(my_link4.uplink.gas_atten)))
            uplink.append("Scin {0} dB".format(str(my_link4.uplink.scin_atten)))
            uplink.append("Rain {0} dB".format(str(my_link4.uplink.rain_atten)))
            uplink.append("NoiseBW {0} dB".format(str(my_link4.uplink.noise_bandwidth)))
            uplink.append("C/NUplinkClear {0} dB".format(str(my_link4.uplink.carrier_over_noise_clear_sky)))
            uplink.append("C/NUplinkRain {0} dB".format(str(my_link4.uplink.carrier_over_noise_rain)))

            #---------------------------SATELLITE-----------------------------------------
            satellite.append("Name: {0}".format(my_link4.satellite.name))
            satellite.append("Channel: {0}".format(my_link4.satellite.channel_name))
            satellite.append("Orbital Slot {0} degrees".format(str(my_link4.satellite.orbital_slot)))
            satellite.append("SKB {0} degrees".format(str(my_link4.satellite.half_station_keeping_box)))
            satellite.append("Channel Bandwidth {0} MHz".format(str(my_link4.satellite.channel_bandwidth)))
            satellite.append("Peak G/T {0} dB/K".format(format(str(my_link4.satellite.peak_gt))))
            satellite.append("SFD {0} dBW/m^2".format(str(my_link4.satellite.channel_sfd)))
            satellite.append("IBO {0} dB".format(str(my_link4.satellite.channel_input_backoff)))
            satellite.append("OBO {0} dB".format(str(my_link4.satellite.channel_output_backoff)))
            satellite.append("Carrier OBO {0} dB".format(str(my_link4.satellite.carrier_output_backoff)))
            satellite.append("Deepin {0} dB".format(str(my_link4.satellite.deepin_per_carrier)))
            satellite.append("Operating Mode: {0}".format(my_link4.satellite.channel_operating_mode))
            satellite.append("Peak Saturated EIRP {0} dBW".format(str(my_link4.satellite.peak_saturated_eirp)))
            satellite.append("Gain variation {0} dB".format(str(my_link4.satellite.gain_variation)))

            #---------------------------DOWNLINK-----------------------------------------
            downlink.append("Lat: {0} Degrees".format(str(my_link4.downlink.latitude)))
            downlink.append("Lon: {0} Degrees".format(str(my_link4.downlink.longitude)))
            downlink.append("Pol: {0} ".format(my_link4.downlink.polarization))
            downlink.append("Range: {0} km".format(str(my_link4.downlink.slant_range)))
            downlink.append("Frequency: {0} GHz".format(str(my_link4.downlink.frequency)))
            downlink.append("Elevation: {0} degrees".format(str(my_link4.downlink.elevation)))
            downlink.append("AntennaDiameter {0} m".format(str(my_link4.downlink.antenna_diameter)))
            downlink.append("AntennaEfficiency {0} %".format(str(my_link4.downlink.antenna_efficiency*100)))
            downlink.append("AntennaGain {0} m".format(str(my_link4.downlink.antenna_gain)))
            downlink.append("G/TClearSky {0} dB/K".format(str(my_link4.downlink.antenna_gt_clear)))
            downlink.append("EIRPatLocation {0} dBW".format(str(my_link4.downlink.eirp_at_location)))
            downlink.append("LinkAvailability {0} %".format(str(my_link4.downlink.single_site_availability)))
            downlink.append("PointingLoss {0} dB".format(str(my_link4.downlink.pointing_loss)))
            downlink.append("XPolLoss {0} dB".format(str(my_link4.downlink.xpol_loss)))
            downlink.append("AxialRatioLoss {0} dB".format(str(my_link4.downlink.axial_ratio_loss)))
            downlink.append("PathLoss {0} dB".format(str(my_link4.downlink.axial_ratio_loss)))
            downlink.append("PathLoss {0} dB".format(str(my_link4.downlink.path_loss)))
            downlink.append("Cloud {0} dB".format(str(my_link4.downlink.cloud_atten)))
            downlink.append("Gas {0} dB".format(str(my_link4.downlink.gas_atten)))
            downlink.append("Scin {0} dB".format(str(my_link4.downlink.scin_atten)))
            downlink.append("Rain {0} dB".format(str(my_link4.downlink.rain_atten)))
            downlink.append("NoiseBW {0} dB".format(str(my_link4.downlink.noise_bandwidth)))
            downlink.append("C/NdownlinkClear {0} dB".format(str(my_link4.downlink.carrier_over_noise_clear_sky)))
            downlink.append("C/NdownlinkRain {0} dB".format(str(my_link4.downlink.carrier_over_noise_rain)))
            downlink.append("C/NTotalClear {0} dB".format(str(my_link4.carrier_over_noise_total_clear_sky)))
            downlink.append("C/NTotalRain {0} dB".format(str(my_link4.carrier_over_noise_total_rain_both)))

        else:
            #---------------------------UPLINK-----------------------------------------
            uplink.append("Lat: {0} Degrees".format(str(link_result.uplink.latitude)))
            uplink.append("Lon: {0} Degrees".format(str(link_result.uplink.longitude)))
            uplink.append("Pol: {0} ".format(link_result.uplink.polarization))
            uplink.append("Range: {0} km".format(str(link_result.uplink.slant_range)))
            uplink.append("Frequency: {0} GHz".format(str(link_result.uplink.frequency)))
            uplink.append("Elevation: {0} degrees".format(str(link_result.uplink.elevation)))
            uplink.append("AntennaDiameter {0} m".format(str(link_result.uplink.antenna_diameter)))
            uplink.append("AntennaEfficiency {0} %".format(str(link_result.uplink.antenna_efficiency*100)))
            uplink.append("AntennaGain {0} m".format(str(link_result.uplink.antenna_gain)))
            uplink.append("HPA {0} Watts".format(str(link_result.uplink.hpa_full_power)))
            uplink.append("HPAop.perCarrier {0} Watts".format(str(link_result.uplink.hpa_output_power_per_carrier)))
            uplink.append("SpreadingLoss {0} dB".format(str(link_result.uplink.spreading_loss)))
            uplink.append("Contour {0} dB".format(str(link_result.uplink.relative_contour)))
            uplink.append("G/T {0} dB/K".format(str(link_result.uplink.gt)))
            uplink.append("OptimizedEIRP {0} dBW".format(str(link_result.uplink.optimized_eirp)))
            uplink.append("EIRP {0} dBW".format(str(link_result.uplink.eirp)))
            uplink.append("UPC {0} dB".format(str(link_result.uplink.upc)))
            uplink.append("IFL {0} dB".format(str(link_result.uplink.ifl)))
            uplink.append("OBO {0} dB".format(str(link_result.uplink.hpa_obo)))
            uplink.append("PFD {0} dBW/m^2".format(str(link_result.uplink.pfd)))
            uplink.append("LinkAvailability {0} %".format(str(link_result.uplink.availability)))
            uplink.append("PointingLoss {0} dB".format(str(link_result.uplink.pointing_loss)))
            uplink.append("XPolLoss {0} dB".format(str(link_result.uplink.xpol_loss)))
            uplink.append("AxialRatioLoss {0} dB".format(str(link_result.uplink.axial_ratio_loss)))
            uplink.append("PathLoss {0} dB".format(str(link_result.uplink.axial_ratio_loss)))
            uplink.append("PathLoss {0} dB".format(str(link_result.uplink.path_loss)))
            uplink.append("Cloud {0} dB".format(str(link_result.uplink.cloud_attenuation)))
            uplink.append("Gas {0} dB".format(str(link_result.uplink.gas_attenuation)))
            uplink.append("Scin {0} dB".format(str(link_result.uplink.scin_attenuation)))
            uplink.append("Rain {0} dB".format(str(link_result.uplink.rain_attenuation)))
            uplink.append("NoiseBW {0} dB".format(str(link_result.uplink.noise_bandwidth)))
            uplink.append("C/NUplinkClear {0} dB".format(str(link_result.clear_sky.cn_uplink)))
            uplink.append("C/NUplinkRain {0} dB".format(str(link_result.rain_both.cn_uplink)))
            uplink.append("EIRP Downlink at peak {0} dB".format(str(link_result.downlink.eirp_at_peak)))

            #---------------------------SATELLITE-----------------------------------------
            satellite.append("Name: {0}".format(link_result.satellite.name))
            satellite.append("Channel: {0}".format(link_result.satellite.channel))
            satellite.append("Orbital Slot {0} degrees".format(str(link_result.satellite.orbital_slot)))
            satellite.append("SKB {0} degrees".format(str(link_result.satellite.half_station_keeping_box)))
            satellite.append("Channel Bandwidth {0} MHz".format(str(link_result.satellite.channel_bandwidth)))
            satellite.append("Peak G/T {0} dB/K".format(format(str(link_result.satellite.peak_gt))))
            satellite.append("SFD {0} dBW/m^2".format(str(link_result.satellite.channel_sfd)))
            satellite.append("IBO {0} dB".format(str(link_result.satellite.channel_input_backoff)))
            satellite.append("OBO {0} dB".format(str(link_result.satellite.channel_output_backoff)))
            satellite.append("Carrier OBO {0} dB".format(str(link_result.satellite.carrier_output_backoff)))
            satellite.append("Deepin {0} dB".format(str(link_result.satellite.deepin_per_carrier)))
            satellite.append("Operating Mode: {0}".format(link_result.satellite.channel_operating_mode))
            satellite.append("Peak Saturated EIRP {0} dBW".format(str(link_result.satellite.peak_saturated_eirp)))
            satellite.append("Gain variation {0} dB".format(str(link_result.satellite.gain_variation)))

            #---------------------------DOWNLINK-----------------------------------------
            downlink.append("Lat: {0} Degrees".format(str(link_result.downlink.latitude)))
            downlink.append("Lon: {0} Degrees".format(str(link_result.downlink.longitude)))
            downlink.append("Pol: {0} ".format(link_result.downlink.polarization))
            downlink.append("Range: {0} km".format(str(link_result.downlink.slant_range)))
            downlink.append("Frequency: {0} GHz".format(str(link_result.downlink.frequency)))
            downlink.append("Elevation: {0} degrees".format(str(link_result.downlink.elevation)))
            downlink.append("AntennaDiameter {0} m".format(str(link_result.downlink.antenna_diameter)))
            downlink.append("AntennaEfficiency {0} %".format(str(link_result.downlink.antenna_efficiency*100)))
            downlink.append("AntennaGain {0} m".format(str(link_result.downlink.antenna_gain)))
            downlink.append("G/TClearSky {0} dB/K".format(str(link_result.downlink.antenna_gt_clear)))
            downlink.append("EIRPatLocation {0} dBW".format(str(link_result.downlink.eirp_at_location)))
            downlink.append("LinkAvailability {0} %".format(str(link_result.downlink.availability)))
            downlink.append("PointingLoss {0} dB".format(str(link_result.downlink.pointing_loss)))
            downlink.append("XPolLoss {0} dB".format(str(link_result.downlink.xpol_loss)))
            downlink.append("AxialRatioLoss {0} dB".format(str(link_result.downlink.axial_ratio_loss)))
            downlink.append("PathLoss {0} dB".format(str(link_result.downlink.axial_ratio_loss)))
            downlink.append("PathLoss {0} dB".format(str(link_result.downlink.path_loss)))
            downlink.append("Cloud {0} dB".format(str(link_result.downlink.cloud_attenuation)))
            downlink.append("Gas {0} dB".format(str(link_result.downlink.gas_attenuation)))
            downlink.append("Scin {0} dB".format(str(link_result.downlink.scin_attenuation)))
            downlink.append("Rain {0} dB".format(str(link_result.downlink.rain_attenuation)))
            downlink.append("NoiseBW {0} dB".format(str(link_result.downlink.noise_bandwidth)))
            downlink.append("C/NdownlinkClear {0} dB".format(str(link_result.clear_sky.cn_downlink)))
            downlink.append("C/NdownlinkRain {0} dB".format(str(link_result.rain_both.cn_downlink)))
            downlink.append("C/NTotalClear {0} dB".format(str(link_result.clear_sky.cn_total)))
            downlink.append("C/NTotalRain {0} dB".format(str(link_result.rain_both.cn_total)))

            #------------------------CLEAR SKY------------------------------------------------
            clear_sky.append("C/N Uplink {0} dB".format(str(link_result.clear_sky.cn_uplink)))
            clear_sky.append("C/N Downlink {0} dB".format(str(link_result.clear_sky.cn_downlink)))
            clear_sky.append("C/I Uplink {0} dB".format(str(link_result.clear_sky.ci_uplink)))
            clear_sky.append("C/I Downlink {0} dB".format(str(link_result.clear_sky.ci_downlink)))
            clear_sky.append("C/N Total {0} dB".format(str(link_result.clear_sky.cn_total)))
            clear_sky.append("MCG: {0}".format(link_result.clear_sky.mcg.name))
            clear_sky.append(("Capacity {0} Mbps".format(str(link_result.clear_sky.capacity))))

            #--Rain up--
            rain_up.append("C/N Uplink {0} dB".format(str(link_result.rain_up.cn_uplink)))
            rain_up.append("C/N Downlink {0} dB".format(str(link_result.rain_up.cn_downlink)))
            rain_up.append("C/I Uplink {0} dB".format(str(link_result.rain_up.ci_uplink)))
            rain_up.append("C/I Downlink {0} dB".format(str(link_result.rain_up.ci_downlink)))
            rain_up.append("C/N Total {0} dB".format(str(link_result.rain_up.cn_total)))
            rain_up.append("MCG: {0}".format(link_result.rain_up.mcg.name))
            rain_up.append(("Capacity {0} Mbps".format(str(link_result.rain_up.capacity))))

            #--Rain down--
            rain_down.append("C/N Uplink {0} dB".format(str(link_result.rain_down.cn_uplink)))
            rain_down.append("C/N Downlink {0} dB".format(str(link_result.rain_down.cn_downlink)))
            rain_down.append("C/I Uplink {0} dB".format(str(link_result.rain_down.ci_uplink)))
            rain_down.append("C/I Downlink {0} dB".format(str(link_result.rain_down.ci_downlink)))
            rain_down.append("C/N Total {0} dB".format(str(link_result.rain_down.cn_total)))
            rain_down.append("MCG: {0}".format(link_result.rain_down.mcg.name))
            rain_down.append("Capacity {0} Mbps".format(str(link_result.rain_down.capacity)))

            #--Rain both--
            rain_both.append("C/N Uplink {0} dB".format(str(link_result.rain_both.cn_uplink)))
            rain_both.append("C/N Downlink {0} dB".format(str(link_result.rain_both.cn_downlink)))
            rain_both.append("C/I Uplink {0} dB".format(str(link_result.rain_both.ci_uplink)))
            rain_both.append("C/I Downlink {0} dB".format(str(link_result.rain_both.ci_downlink)))
            rain_both.append("C/N Total {0} dB".format(str(link_result.rain_both.cn_total)))
            rain_both.append("MCG: {0}".format(link_result.rain_both.mcg.name))
            rain_both.append("Capacity {0} Mbps".format(str(link_result.rain_both.capacity)))
        elapsed_time = time.time() - start_time
    return render(request, "linkbudget/result.html", {"uplink": uplink,
                                                      "downlink": downlink,
                                                      "satellite": satellite,
                                                      "clear_sky": clear_sky,
                                                      "rain_up": rain_up,
                                                      "rain_down": rain_down,
                                                      "rain_both": rain_both,
                                                      "time": elapsed_time})