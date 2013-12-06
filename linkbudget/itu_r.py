from math import sqrt, pi, sin, cos, exp, log, log10, atan

__author__ = 'thanatv'


class Attenuation(object):
    """
    Defines an atmospheric attenuation based on ITU-R
    """

    def __init__(self, frequency, elevation, antenna_diameter, polarization,
                 link_availability, lat, lon, antenna_efficiency=0.5, atmospheric_pressure=1, surface_temp=27,
                 humidity=99, r100=None):
        self.frequency = frequency
        self.elevation = elevation
        self.antenna_diameter = antenna_diameter
        self.polarization = polarization
        self.link_availability = link_availability
        self.latitude = lat
        self.longitude = lon
        self.antenna_efficiency = antenna_efficiency
        self.atmospheric_pressure = atmospheric_pressure
        self.surface_temp = surface_temp
        self.humidity = humidity
        self.r100 = r100

    @property
    def cloud(self):
        """
        Returns cloud attenuation
        """
        # Calculate attenuation due to cloud for any frequency up to 1000GHz.
        # Assumption is used for temperature of 0 degree C (273K) as recommended in ITU-R P.840-3 (1999)
        # The calculation is based on the worst case normalized total columnar content of cloud liquid water exceeded
        # for 1% of the year which is estimated to 2Kg/m**2

        # TODO: Correct function for New Zealand

        l1pct = 2
        theta = 300 / 273.0
        fp = 20.09 - 142 * (theta - 1) + 294 * (theta - 1) ** 2
        fs = 590 - 1500 * (theta - 1)
        ep0 = 77.6 + 103.3 * (theta - 1)
        ep1 = 5.48
        ep2 = 3.51
        ep_p = ((ep0 - ep1) / (1 + (self.frequency / fp) ** 2)) + ((ep1 - ep2) / (1 + (self.frequency / fs) ** 2)) + ep2
        ep_pp = (self.frequency * (ep0 - ep1) / (fp * (1 + (self.frequency / fp) ** 2))) + (self.frequency * (ep1 - ep2) / (fs * (1 + (self.frequency / fs) ** 2)))
        nue = (2 + ep_p) / ep_pp
        kl = 0.819 * self.frequency / (ep_pp * (1 + nue ** 2))
        
        # This is valid for elevation angle from 5 degree to 90 degree
        return l1pct * kl / (sin(self.elevation * pi / 180))

    @property
    def gas(self):
        """
        Returns gas attenuation
        """
        # This function estimates the attenuation due to atmospheric gases per ITU rec. 676
        # Application is valid for frequency 54GHz and lower
        # Modified according to ITU-R P.676-3 , March 16, 1999
        # 
        # Freq= Frequency in GHz
        # Temp_surf = surface temperature in degrees C
        # Relative Humidity at site (%)
        # Ele = Elevation angle in degrees
        # Station height, Hs of 0Km (sea level) is assumed for conservative estimate

        # TODO: Correct function for New Zealand

        # Saturated Partial pressure of water vapor
        freq = self.frequency
        surface_temp = self.surface_temp
        humidity = self.humidity
        ele = self.elevation
        ps = 206.43 * exp(0.0354 * ((9.0 * surface_temp / 5) + 32))
        rho = (humidity / 100.0) * ps / (0.461 * (surface_temp + 273))
        
        # Specific attenuation for dry air for altitude up to 5Km
        hpa = 1013.0  # dry air pressure in hPa at sea level
        r_t = 288 / (273.0 + surface_temp)
        r_p = hpa / 1013
        nue_1 = 6.7665 * (r_p ** -0.505) * (r_t ** 0.5106) * exp(1.5663 * (1 - r_t)) - 1
        nue_2 = 27.8843 * (r_p ** -0.4908) * (r_t ** -0.8491) * exp(0.5496 * (1 - r_t)) - 1
        a_fact = log(nue_2 / nue_1) / log(3.5)
        b_fact = (4 ** a_fact) / nue_1
        # TODO: Find real sources of a_factor and b_factor (In the link budget, they come out of nowhere)
        gamma_op54 = 2.128 * (r_p ** 1.4954) * (r_t ** -1.6032) * exp(-2.528 * (1 - r_t))
        gamma_o = ((7.34 * (r_p ** 2) * (r_t ** 2) / (freq ** 2 + 0.36 * (r_p ** 2) * (r_t ** 2))) + (0.3429 * b_fact * gamma_op54 / ((54 - freq) ** a_fact + b_fact))) * (freq ** 2) * 10 ** -3
        
        # Specific attenuation for water vapour
        sw1 = 0.9544 * r_p * (r_t ** 0.69) + 0.0061 * rho
        sw2 = 0.95 * r_p * (r_t ** 0.64) + 0.0067 * rho
        sw3 = 0.9561 * r_p * (r_t ** 0.67) + 0.0059 * rho
        sw4 = 0.9543 * r_p * (r_t ** 0.68) + 0.0061 * rho
        sw5 = 0.955 * r_p * (r_t ** 0.68) + 0.006 * rho
        g22 = 1 + (freq - 22.235) ** 2 / (freq + 22.235) ** 2
        g557 = 1 + (freq - 557) ** 2 / (freq + 557) ** 2
        g752 = 1 + (freq - 752) ** 2 / (freq + 752) ** 2
        tm1 = 3.84 * sw1 * g22 * exp(2.23 * (1 - r_t)) / ((freq - 22.235) ** 2 + 9.42 * sw1 ** 2)
        tm2 = 10.48 * sw2 * exp(0.7 * (1 - r_t)) / ((freq - 183.31) ** 2 + 9.48 * sw2 ** 2)
        tm3 = 0.78 * sw3 * exp(6.4385 * (1 - r_t)) / ((freq - 321.226) ** 2 + 6.29 * sw3 ** 2)
        tm4 = 3.76 * sw4 * exp(1.6 * (1 - r_t)) / ((freq - 325.153) ** 2 + 9.22 * sw4 ** 2)
        tm5 = 26.36 * sw5 * exp(1.09 * (1 - r_t)) / (freq - 380) ** 2
        tm6 = 17.87 * sw5 * exp(1.46 * (1 - r_t)) / (freq - 448) ** 2
        tm7 = 883.7 * sw5 * g557 * exp(0.17 * (1 - r_t)) / (freq - 557) ** 2
        tm8 = 302.6 * sw5 * g752 * exp(0.41 * (1 - r_t)) / (freq - 752) ** 2
        sum_tm = tm1 + tm2 + tm3 + tm4 + tm5 + tm6 + tm7 + tm8
        
        gamma_w = (0.0313 * r_p * (r_t ** 2) + 0.00176 * rho * (r_t ** 8.5) + (r_t ** 2.5) * sum_tm) * (freq ** 2) * rho * 10 ** -4
        
        # Station height = Sea level is assumed
        hs = 0
        
        # Dry air equivalent height for freq from 1GHz to 56.7GHz
        ho = 5.386 - 0.0332734 * freq + 0.00187185 * freq ** 2 - 3.52087 * (10 ** -5) * freq ** 3 + 83.26 / (((freq - 60) ** 2) + 1.2)
        
        # Water vapor equivalent height
        hw = 1.65 * (1 + (1.61 / (((freq - 22.23) ** 2) + 2.91)) + (3.33 / (((freq - 183.3) ** 2) + 4.58)) + (1.9 / (((freq - 325.1) ** 2) + 3.34)))

        if ele > 10:
            return (gamma_o * ho + gamma_w * hw) / sin(ele * pi / 180)
        else:
            sin_ele = sin(ele * pi / 180)
            gho = 0.661 * sin_ele + 0.339 * sqrt((sin_ele ** 2) + 5.5 * (ho / 8500))
            ghw = 0.661 * sin_ele + 0.339 * sqrt((sin_ele ** 2) + 5.5 * (hw / 8500))
            return (gamma_o * ho / gho) + (gamma_w * hw / ghw)

    @property
    def scin(self):
        """
        Returns scin attenuation
        """
        # Calculate attenuation due to scintillation effect based on ITU-R P.618-6 for elevation angle > 4deg
        # Input
        # temp=average surface ambient temperature in degree C
        # humidity=average surface relative humidity in %
        # freq=carrier frequency in GHz (>4GHz and <20GHz)
        # Ele=Elevation angle
        # diam=diameter of antenna in m
        # eff=antenna efficiency in fraction (typical =0.5 to be conservative)
        # press=atmospheric pressure at the site, 1atm = 1,013.25hPa
        # avail=availability in %
        
        temp = self.surface_temp
        humidity = self.humidity
        freq = self.frequency
        ele = self.elevation
        diam = self.antenna_diameter
        eff = self.antenna_efficiency
        press = self.atmospheric_pressure
        avail = self.link_availability
        
        # Step-1: Calculate saturation water vapour pressure (Es)
        a = 6.1121
        b = 17.502
        c = 240.97
        es = a * exp(b * temp / (temp + c))
        
        # Step-2: Calculates radio refractivity, Nwet
        eh = humidity * es / 100.0
        nwet = 77.6 * ((press * 1013.25) + (4810.0 * eh / (273.0 + temp))) / (273 + temp)
        
        # Step-3: Calculate standard deviation of signal amplitude, sigma_ref
        sigma_ref = (3.6 * 10 ** -3) + (nwet * 10 ** -4)
        
        # Step-4: Calculate effective path length
        # hL=height of turbulent layer = 1000m
        hl = 1000
        sin_ele = sin(ele * pi / 180)
        length = 2 * hl / (sqrt(sin_ele ** 2 + (2.35 * 10 ** -4)) + sin_ele)
        
        # Step-5: estimate effective antenna diameter
        deff = sqrt(eff) * diam
        
        # Step-6: Calculate antenna averaging factor.
        x_val = 1.22 * (freq / length) * deff ** 2
        gx = sqrt((3.86 * (x_val ** 2 + 1) ** (11.0 / 12)) * sin((11.0 / 6) * atan(1 / x_val)) - (7.08 * x_val ** (5.0 / 6)))
        
        # Step-7: Calculate standard deviation
        sigma = sigma_ref * freq ** (7 / 12.0) * gx / (sin_ele ** 1.2)
        
        # Step-8: Calculate time percentage factor for the value of unavailability
        unavail = 100 - avail
        a_p = -0.061 * (log10(unavail) ** 3) + 0.072 * (log10(unavail) ** 2) - 1.71 * log10(unavail) + 3
        
        # Step-9: Calculation scintillation fade depth
        return a_p * sigma

    @property
    def rain(self):
        """
        Calculates rain attenuation from predicted attenuation exceeded for 0.01% of an average year
        """
        # Calculate the estimated attenuation to be exceeded for other percentages of an average year
        # in the range of .001% to 5%  is approximated by
        unavailability = 100 - self.link_availability
        stat_lat = self.latitude
        ele_rad = self.elevation * pi / 180

        if unavailability >= 1 or abs(stat_lat) >= 36:
            beta = 0
        elif unavailability < 1 and abs(stat_lat) < 36 and self.elevation >= 25:
            beta = -0.005 * (abs(stat_lat) - 36)
        else:
            beta = -0.005 * (abs(stat_lat) - 36) + 1.8 - 4.25 * sin(ele_rad)

        return self.rain_atten_001 * (unavailability / 0.01) ** -(0.655 + 0.033 * log(unavailability) - 0.045 * log(self.rain_atten_001) - beta * (1 - unavailability) * sin(ele_rad))

    @property
    def rain_atten_001(self):
        """
        Calculates the predicted attenuation exceeded 0.01% of an average year
        """
        #  ITU rain attenuation model
        #  based on Rec. ITU-R 618-6, 1999
        #  Modification to allow for all elevation angles, frequencies between 1 and 55GHz,
        #  probabilities between 0.001% and 5% of an average year
        # 
        # Inputs
        # variable:format:Infor: range
        # R_one_hundreth: Rainfall rate in mm/hr as obtain from digital map table in ITU-R P.837-2
        # polarization: String : wave:"V","H","C"
        # stat_height: Number  : Station  height above mean sea level in km: 0 to ~ N
        # stat_lat:Number: absolute value of Latitude of earth station in deg: (0 - 81.3 degrees)
        # stat_lon: Longitude of earth station in East longtitude
        # freq : Number : Frequency in GHz: Range is 1 GHz to 55 GHz
        # el_angle: Number: Earth Station antenna elevation angle in deg.  (0 - 90)
        # availability: Number:Desired link availability: i.e., 99.5,  (min. value is 95., max 99.999)
        
        # Output/Return value is the attenuation in dB.
        
        # Inputs range check
        # Check availability (smallest allowed value will be 95., Max will be 99.999)

        # Set up format of basic parameters used several times
        #  equivalent elevation angle in radians - Excel functions operate in radians
        
        freq = self.frequency
        stat_lat = self.latitude
        stat_lon = self.longitude
        ele_rad = self.elevation * pi / 180
        stat_height = 0

        # TODO: Write the function to find R_100
        # Rainfall rate in mm/hr as obtain from digital map table in ITU-R P.837-2
        if not self.r100:
            r_100 = 80
        else:
            r_100 = self.r100

        # unavailability, (100 percent - given availability)
        unavailability = 100 - self.link_availability
        
        # __________________________________________________________
        # First Step of algorithm is to calculate the Isotherm height for the rain : km
        # i.e., height at which rain is at 0 deg C
        # 
        # Step-1:
        if stat_lat > 23:  # Northern Hemisphere
        # if (stat_lon < 60) Or (stat_lon > 200) Then # for North America and Europe
        # if (stat_lat >= 35) And (stat_lat <= 70) Then # As modified by ITU-R P.839-2
        # rain_height = 3.2 - 0.075 * (stat_lat - 35)
            rain_height = 5 - 0.075 * (stat_lat - 23)
        elif 0 < stat_lat <= 23:  # Northern Hemisphere
            rain_height = 5
        elif -21 < stat_lat <= 0:  # Southern Hemisphere
            rain_height = 5
        elif -71 < stat_lat <= 21:  # Southern Hemisphere
            rain_height = 5 + 0.1 * (stat_lat + 21)
        else:
            rain_height = 0

        # Next determine the slant path length to isotherm, this is the Ls in the ITU Rec
        #  Note the value of 8500 is the earth radius in km
        # Step-2:
        
        if self.elevation >= 5:
            slant_path = (rain_height - stat_height) / sin(ele_rad)
        else:
            #  very low elevation angles
            slant_path = 2 * (rain_height - stat_height) / (sqrt(sin(ele_rad) ** 2 + 2 * (rain_height - stat_height) / 8500) + sin(ele_rad))
                
        # Determine horizontal projection to ground of slant path length.  (this is the LG in the ITU REC)
        # Step-3:
        horizontal_slant_path = slant_path * cos(ele_rad)
        
        #  Now determine the Rain Point intensity (mm/hr)for an exceed of 0.01: R_one_hundreth
        #  select value for selected rain region
        #  only one of the .01  rates are  used (based on the rain region)
        #  Values taken from ITU-R, Rec 837-1, 1994
        # Step-4:
        # R_one_hundreth is obtained from ITU-R P.837 as is passed to this function
        # Use routine RR_001 to get this value
         
        #  Now find the k and alpha factor per ITU-R  Rec.838
        # Step-5:  ITU-R P.838 dated 15 March 1999 stated that the matrix is good up to 55GHz
        # array of frequencies 1 to 400 GHz, used to specify an index value for k and alpha
        freq_array = [1, 2, 4, 6, 7, 8, 10, 12, 15, 20, 25, 30, 35, 40, 45, 50, 60, 70, 80, 90, 100, 120, 150, 200,
                      300, 400]
            
        # the following are arrays of specific values for kh, kv, alphah, and alphav.
        # they are used for interpolating when calculating actual values k_H, k_V,
        # alpha_H, and alpha_V.
        kh = [0.0000387, 0.000154, 0.00065, 0.00175, 0.00301, 0.00454, 0.0101, 0.0188, 0.0367, 0.0751, 0.124, 0.187,
              0.263, 0.35, 0.442, 0.536, 0.707, 0.851, 0.975, 1.06, 1.12, 1.18, 1.31, 1.45, 1.36, 1.32]
                        
        kv = [0.0000352, 0.000138, 0.000591, 0.00155, 0.00265, 0.00395, 0.00887, 0.0168, 0.0335, 0.0691, 0.113, 0.167,
              0.233, 0.31, 0.393, 0.479, 0.642, 0.784, 0.906, 0.999, 1.06, 1.13, 1.27, 1.42, 1.35, 1.31]
            
        alphah = [0.912, 0.963, 1.121, 1.308, 1.332, 1.327, 1.276, 1.217, 1.154, 1.099, 1.061, 1.021, 0.979, 0.939,
                  0.903, 0.873, 0.826, 0.793, 0.769, 0.753, 0.743, 0.731, 0.71, 0.689, 0.688, 0.683]
            
        alphav =[0.88, 0.923, 1.075, 1.265, 1.312, 1.31, 1.264, 1.2, 1.128, 1.065, 1.03, 1, 0.963, 0.929, 0.897, 0.868,
                 0.824]

        #  find index for frequency within the frequency array
        freq1, freq2 = self.excel_match(freq_array, freq)
            
        #  interpolate to find the values for k_H and K_V .: Log (K_x)vs LOG(freq)
        x1 = log10(freq_array[freq1])
        x2 = log10(freq_array[freq2])
        x3 = log10(freq)
        y1 = log10(kh[freq1])
        y2 = log10(kh[freq2])
         
        k_H = 10 ** (y1 - (x3 - x1) * (y1 - y2) / (x2 - x1))
         
             
        y1 = log10(kv[freq1])
        y2 = log10(kv[freq2])
            
        k_v = 10 ** (y1 - (x3 - x1) * (y1 - y2) / (x2 - x1))
        
        # Interpolate to find the valued for alpha_H and alpha_V : Alpha_x vs log (freq)
        y1 = alphah[freq1]
        y2 = alphah[freq2]
            
        alpha_H = y1 - (x3 - x1) * (y1 - y2) / (x2 - x1)
        
        y1 = alphav[freq1]
        y2 = alphav[freq2]
            
        alpha_v = y1 - (x3 - x1) * (y1 - y2) / (x2 - x1)
        
        tau = self.tau
                
        # calculate the factor k
        k = (k_H + k_v + (k_H - k_v) * cos(2 * tau) * (cos(ele_rad) ** 2)) / 2
           
         
        # calculate the factor alpha
        alpha = (k_H * alpha_H + k_v * alpha_v + (k_H * alpha_H - k_v * alpha_v) * cos(2 * tau) * (cos(ele_rad) ** 2)) / (2 * k)
        
             
        # specific attenuation from frequency-dependent coefficients (dB/km)
        gamma_r = k * r_100 ** alpha

        # Step-6:
        # Calculate the horizontal reduction factor,r0.01, for 0.01% of the time
        red_factor = 1 / (1 + 0.78 * sqrt(horizontal_slant_path * gamma_r / freq) - 0.38 * (1 - exp(-2 * horizontal_slant_path)))
            
        # Step-7:
        # Calculate the vertical adjustment factor,V_001,fro 0.01% of the time
        gamma_n = atan((rain_height - stat_height) / (horizontal_slant_path * red_factor)) * (180 / pi)
        if gamma_n > self.elevation:
            l_r = horizontal_slant_path * red_factor / cos(ele_rad)
        else:
            l_r = (rain_height - stat_height) / sin(ele_rad)
            
        if abs(stat_lat) < 36:
            Qhi = 36 - abs(stat_lat)
        else:
            Qhi = 0
            
        v_001 = 1 / (1 + sqrt(sin(ele_rad)) * ((31 * (1 - exp(-self.elevation / (1 + Qhi))) * sqrt(l_r * gamma_r) / freq ** 2) - 0.45))
        #  V_001 = 1 / (1 + sqrt(sin(ele_rad)) * ((31 * (1 - exp(-1 * (El_angle / (1 + Qhi)))) * sqrt(L_R * gamma_R) / (freq ** 2)) - 0.45))
        
        # Step-8:
        # Calculate the effective path length, L_E
        eff_path_length = l_r * v_001
        
        # Step-9:
        # Calculate the predicted attenuation exceeded for .01% of an average year
        return gamma_r * eff_path_length

    @property
    def total_clear_sky(self):
        """
        Return total attenuation during clear sky
        """
        if self.elevation > 10:
            return self.gas + self.cloud
        else:
            return self.gas + sqrt(self.cloud ** 2 + self.scin ** 2)
    
    @property
    def total_rain(self):
        """
        Return total attenuation during rain
        """
        return self.gas + sqrt((self.rain + self.cloud) ** 2 + self.scin ** 2)

    @property
    def tau(self):
        from linkcalc import LinkCalcError
        if self.polarization.upper() == "H":
            return 0
        elif self.polarization.upper() == "V":
            return pi / 2
        elif self.polarization.upper() in ("LHCP", "RHCP"):
            return pi / 4
        else:
            raise LinkCalcError("Polarizaion is invalid.")

    def excel_match(self, list, value):
        """
        Returns 2 indices of the given sorted list which have the number sandwiches the given value
        """
        for k, m in enumerate(list):
            if m > value:
                idx, idx2 = k-1, k
                break
        return idx, idx2

