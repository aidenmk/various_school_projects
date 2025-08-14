class Plant:
    def __init__(self, species, moisture_use, drought_tolerance, shade_tolerance,
                 leaf_retention, coarse_soil_tolerance, fine_soil_tolerance,
                 medium_soil_tolerance, growth_period):
        self.species = species
        self.moisture_use = moisture_use  # e.g. "Low", "Medium", "High", "None"
        self.drought_tolerance = drought_tolerance  # e.g. "Low", "Medium", "High", "None"
        self.shade_tolerance = shade_tolerance  # e.g. "Tolerant", "Intolerant", "Intermediate", "None"
        self.leaf_retention = leaf_retention  # "Yes" / "No"
        self.growth_period = growth_period  # e.g. "Summer and Fall"
        
        
        soil_tolerance = {'coarse': 'No',
                          'fine': 'No',
                          'medium': 'No'}

        if coarse_soil_tolerance == "Yes":
            soil_tolerance['coarse'] = 'Yes'
        if fine_soil_tolerance == 'Yes':
            soil_tolerance['fine'] = 'Yes'
        if medium_soil_tolerance == 'Yes':
            soil_tolerance['medium'] = 'Yes'

        self.soil_tolerance = soil_tolerance  # dict: {'coarse': 'Yes', 'fine': 'No', 'medium': 'Yes'}

