

class GHGPredictor():

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
        self.fuelEFC = 15443.41
        self.fuelEFM = 104.52
        self.fuelEFN = 0.25
        self.FRAC_LEACH = 0.3 # Default value (range: 0.1 - 0.8)
        self.LEACHING_RUNOFF_EMISSIONS = 0.025 # Default value (range: 0.002 - 0.12)

        # Liters per hectar of pesticides
        
    '''Diesel fuel only'''
    def fuel_ghg_emissions(self, fuel_liters, unit = "g"):
        '''
        Calculates the emisson produced by fuel consumption in CO2 equivalent value.
        Based on furmulae in paper:
              - Myriah D. Johnson, Christopher T. Rutland, James W. Richardson, Joe L. Outlaw
                & Clair J. Nixon (2016) Greenhouse Gas Emissions from U.S. Grain Farms, Journal 
                of Crop Improvement, 30:4, 447-477
        Some factors were used without explicitely being stated in this paper, so they were pulled
        from outside sources:                
              -Diesel fuel energy content per litre = 36 292.24
                    - https://www.eia.gov/energyexplained/units-and-calculators/british-thermal-units.php
              -Fuel combustion factors:
                    - https://19january2017snapshot.epa.gov/sites/production/files/2015-07/documents/emission-factors_2014.pdf
                    - CO2: 10.21 kg CO2 / gallon fuel = 3.1664 kg CO2/ kg fuel = 3166.4 g CO2/ kg fuel
                    - CH4: 1.44 g CH4 / gallon fuel = 0.4466 g CH4 / kg fuel
                    - N20: 0.26 g N2O / galon fuel = 0.0806 h N2O / kg fuel
                    
        Note: 1 gallon of diesel fuel = 3.2245 kg of diesel fuel
        Args:
              - fuel_litres: Litres of fuel spent per year
        Returns:
              - Amount of CO2 equivalent ghg emissions (in entered units)
        '''
        diesel_energy_content_per_litre = 36292.24
        co2_combustion_factor = 3166.4
        ch4_combustion_factor = 0.4466
        n2o_combustion_factor = 0.0806 
        
        co2 = (self.fuelEFC * diesel_energy_content_per_litre + co2_combustion_factor) * fuel_liters * 0.001
        ch4 = (self.fuelEFM * diesel_energy_content_per_litre + ch4_combustion_factor) * fuel_liters * 0.001
        n2o = (self.fuelEFN * diesel_energy_content_per_litre + n2o_combustion_factor) * fuel_liters * 0.001
        out = co2 * self.GWP_C + ch4 * self.GWP_M + n2o * self.GWP_N
        if unit == "g":
              return out
        elif unit == "kg":
              return out*1e-3
        elif unit == "t":
              return out*1e-6
        else:
              print("Invalid unit parameter. Choose from \{ 'g', 'kg', 't' \}")
              
    def managed_soils_ghg(self, synth_n2o, organic_n2o, field_area, residue_n2o = 0):
        '''
        Calculating CO2 equivalent emmisions from various practices and natural soil content.
        Based on furmulae in paper:
              - Myriah D. Johnson, Christopher T. Rutland, James W. Richardson, Joe L. Outlaw
                & Clair J. Nixon (2016) Greenhouse Gas Emissions from U.S. Grain Farms, Journal 
                of Crop Improvement, 30:4, 447-477
        
        Note: In source paper C02 emissions from liming practices were taken into account, as well
        as CH4 from rice cultivations. These aren't present in provided dataset, and are, therefore
        excluded.
        
        Direct N2O emissions are calculated from applied synthetic and organic fertilizers, soil residues,
        as well as N2O emmisions from soil organic content present in the field. 
        
        Indirecct N2O emissions are calculated from amount of synthetic and organic fertilizers that
        volatilizes as ammonia and N0x in soils, with additional factor of emmisions from animal waste
        
        Final result is sum of these two values scaled with CO2 equivalence factor.
        Args
        
              - synth_n2o:   Synthetic fertilizers applied over a year in kg
              - organic_n2o: Organic fertilizers applied over a year in kg
              - residue_n2o: Amount of residue from previous crop left on field
              - field_area:  Area of managed field

        '''
        # TODO: Residue needs to be specified. How?
        n2o_inputs = (synth_n2o + organic_n2o + residue_n2o) * self.EF_INPUTS_Z
        n2o_organic_soils = field_area * self.EF_ORGSOILS_Z
        direct_n2o = (n2o_inputs + n2o_organic_soils) * self.N2O_FACTOR

        # TODO: Nismo uspeli da pronadjemo koji faktor je u pitanju na mestu jedinice
        indirect_n2o = (synth_n2o * self.FRAC_GASF + organic_n2o * self.FRAC_GASM * 1) * self.N2O_FACTOR  \
                        + self.nitrogen_leaching(synth_n2o, organic_n2o)

        return (direct_n2o + indirect_n2o) * self.GWP_N

    def nitrogen_leaching(self, synth_n2o, organic_n2o):
        '''
        NEX: amount of N excreted by livestock (kg N/yr). Calculated from FAO livestock populations
                and N excretion/animal data (Mosier et al., 1998) 
            - Des Participants, L. (2001). Good practice guidance and uncertainty management in national greenhouse gas inventories. Order.
            - https://www.ipcc-nggip.iges.or.jp/public/gp/bgp/4_6_Indirect_N2O_Agriculture.pdf?fbclid=IwAR3lZM7CCUyN-_K0pRNj5zU_EtkRvbO1up46xPrqAwaKJW91EeVmwgheAMk
            - Cini nam se da je ovo prirodno djubrivo + ostale "izlucevine" zivotinja

        '''
        NEX = organic_n2o # Po pretpostavci iz komentara

        return (synth_n2o + NEX ) * self.FRAC_LEACH * self.LEACHING_RUNOFF_EMISSIONS
        
    # TODO:
    def pesticide_ghg(self):
        '''
        Problem: Nije poznat aktivni sastojak
            Ima faktor za "Atrazine" herbicit u radu 
                - Myriah D. Johnson, Christopher T. Rutland, James W. Richardson, Joe L.
                    Outlaw & Clair J. Nixon (2016) Greenhouse Gas Emissions from U.S. Grain Farms, Journal of Crop
                    Improvement, 30:4, 447-477, DOI: 10.1080/15427528.2016.1174180
        '''
        pass