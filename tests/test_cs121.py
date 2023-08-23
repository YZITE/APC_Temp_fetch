from APC_Temp_fetch import Cs121

def test_cs121v3():
    with open("tests/cs121v3.html") as dat:
        datx = Cs121.parse(dat)
        assert datx == {'Status': ('01', 'UPS STATUS OK'), 'Input Voltage': ('02', '237 V'), 'Input Frequency': ('03', '50.0 Hz'), 'Output Voltage': ('04', '230 V'), 'Output Frequency': ('05', 'N/A'), 'Load': ('06', '13 %'), 'Seconds on Battery': ('07', '0'), 'Battery Voltage': ('08', '108.96 V'), 'Battery Capacity': ('09', '100.0 %'), 'Autonomy Time': ('10', '425.59 minutes'), 'Battery Temperature': ('11', '25.0')}
        assert Cs121.extract(datx) == '25.0'

def test_cs121v5():
    with open("tests/cs121v5.html") as dat:
        datx = Cs121.parse(dat)
        assert datx == {'Status': ('01', 'UPS STATUS OK'), 'Input Voltage': ('02', '235 V'), 'Input Frequency': ('03', '50.0 Hz'), 'Output Voltage': ('04', '231 V'), 'Output Frequency': ('05', 'N/A'), 'Load': ('06', '23 %'), 'Seconds on Battery': ('07', '0'), 'Battery Voltage': ('08', '2.24 V'), 'Battery Capacity': ('09', '100.0 %'), 'Autonomy Time': ('10', '202.71 _dw("minutes'), 'UPS Temperature': ('11', '27.0')}
        assert Cs121.extract(datx) == '27.0'
