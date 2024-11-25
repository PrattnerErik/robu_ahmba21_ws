class FuelCalculator:

    def __init__(self, drivenKM, consumptionL):
        self._drivenKM = drivenKM
        self._consumptionL = consumptionL

        if drivenKM <= 0.0:
            raise ValueError("KM kau net klana gleich null sei")
        if consumptionL <= 0.0:
            raise ValueError("L kau net klana gleich null sei")
        
        self._calc()
    
    def _calc(self):
        self._avrConsumption = 100.0*self._consumptionL / self._drivenKM
    
    def getAvrConsumption(self):
        return self._avrConsumption
    
    def __str__(self):
        return "heheheha"

class FuelUI:
    def __init__(self):
        try:
            self._input()
            self._calc()
            self._output()
        except Exception as e:
            print(e)
    
    def _input(self):
        print("fuel consumption calculator")
        print("===========================")

        self._drivenKM = float(input(f"{'km driven: ':15s}"))
        self._consumptionL = float(input(f"{'l consumed: ':15s}"))
    
    def _calc(self):
        self._fuelcalc = FuelCalculator(self._drivenKM, self._consumptionL)
        return self._fuelcalc.getAvrConsumption()
    
    def _output(self):
        print("Durchscnittsverbrauch pro 100km: %4.2f" % self._fuelcalc.getAvrConsumption())
        print(self._fuelcalc)

FuelUI()
