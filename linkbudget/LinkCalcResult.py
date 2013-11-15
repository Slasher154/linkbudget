__author__ = 'thanatv'

# Class to keep link calculation result


class LinkCalcResult(object):
    def __init__(self):
        self.uplink = UplinkResult()
        self.satellite = SatelliteResult()
        self.downlink = DownlinkResult()
        self.cn_total = 0

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
        self.eirp = 0
        self.gt = 0
        self.path_loss = 0
        self.k = -228.6
        self.noise_bw = 0
        self.cn = 0


class SatelliteResult(object):
    def __init__(self):
        pass


class DownlinkResult(object):
    def __init__(self):
        self.eirp = 0
        self.gt = 0
        self.path_loss = 0
        self.k = -228.6
        self.noise_bw = 0
        self.cn = 0

result = LinkCalcResult()
result.display()
