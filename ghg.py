

class GHGPredictor:

    def __init__(self):
        self.CO2_FACTOR = 3.67
        self.N2O_FACTOR = 1.57
        self.GWP_C = 1
        self.GWP_M = 25
        self.GWP_N = 298
        self.D = 20
        self.EF_INPUTS_Z = 0.01
        self.EF_ORGSOILS_Z = 8
        self.EF_LIMESTONE = 0.12
        self.EF_DOLOMITE = 0.13
        self.FRAC_GASF = 0.1
        self.FRAC_GASM = 0.2

    '''Diesel fuel only'''
    def fuel_ghg_emissions(self, fuel_liters):
        '''
        Calculates the emisson produced by fuel consumption in equivalent to CO2

        Diesel fuel energy content per litre = 36 292.24
            - https://www.eia.gov/energyexplained/units-and-calculators/british-thermal-units.php

            Args
                fuel_litres Litrres per year
        '''
        diesel_energy_content_per_litre = 36292.24
        # TODO: Naci combustion faktore
        co2 = (15444.41 * diesel_energy_content_per_litre + 0) * fuel_liters * 0.001
        ch4 = (104.52 * diesel_energy_content_per_litre + 0) * fuel_liters * 0.001
        n2o = (0.25 * diesel_energy_content_per_litre + 0) * fuel_liters * 0.001

        return co2 * self.GWP_C + ch4 * self.GWP_M + n2o * self.GWP_N

    def managed_soils_ghg(self, synth_n2o, organic_n2o, residue_n2o, field_area):
        '''
        Args
            synth_n2o Synthetic fertilizers applied over a year in kg
            organic_n2o Organic fertilizers applied over a year in kg
            residue_n2o 

        '''
        n2o_inputs = (synth_n2o + organic_n2o + residue_n2o) * self.EF_INPUTS_Z
        n2o_organic_soils = field_area * EF_ORGSOILS_Z
        direct_n2o = (n2o_inputs + n2o_organic_soils) * N2O_FACTOR

        # TODO: Naci faktor koji fali tu
        indirect_n2o = (synth_n2o * FRAC_GASF + organic_n2o * FRAC_GASM * 1) * N2O_FACTOR


        # TODO: Sta je 'liming'?
        # TODO: Ima nesto za pirinac sto nam nije najjasnije
        return (direct_n2o + indirect_n2o) * GWP_N

    def pesticide_ghg(self):
        pass