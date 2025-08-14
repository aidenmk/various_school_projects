import random
import datetime
from sqlalchemy import create_engine
import pandas as pd
from plant import Plant

class BootstrapPlant(Plant):
    def __init__(self, species, moisture_use, drought_tolerance, shade_tolerance,
                         leaf_retention, coarse_soil_tolerance, fine_soil_tolerance,
                         medium_soil_tolerance, growth_period):
                         
        super().__init__(species, moisture_use, drought_tolerance, shade_tolerance,
                         leaf_retention, coarse_soil_tolerance, fine_soil_tolerance,
                         medium_soil_tolerance, growth_period)
        self.last_watered = None

    def simulate_environment(self):
        tempf = random.uniform(-20, 120)
        lower = tempf - 30 
        if tempf > 100:
            upper = tempf
        else:
            upper = tempf + 30
        temp_avrg = random.uniform(lower, upper)

        return {
            'season': random.randint(1, 12),  # 1=Jan, 12=Dec
            'temperature_f': tempf,
            '36hr_avrg_temp': temp_avrg,
            'humidity': random.uniform(0, 100),
            'shade': random.uniform(0, 24),  # hrs/day
            'altitude_m': random.randint(0, 3100),
            'wind': random.uniform(0, 30)  # mph
        }

    def get_trait_dependent_interval(self, base_interval):
        # Moisture Use — higher moisture needs = shorter interval
        if self.moisture_use == 'High':
            base_interval -= 12
        elif self.moisture_use == 'Medium':
            base_interval -= 6
        elif self.moisture_use == 'Low':
            base_interval += 6
        elif self.moisture_use == 'None':
            base_interval += 12

        # Drought Tolerance
        if self.drought_tolerance == 'High':
            base_interval += 12
        elif self.drought_tolerance == 'Medium':
            base_interval += 6
        elif self.drought_tolerance == 'Low':
            base_interval -= 6
        elif self.drought_tolerance == 'None':
            base_interval -= 12

        # Shade Tolerance
        if self.shade_tolerance == 'Tolerant':
            base_interval += 4
        elif self.shade_tolerance == 'Intermediate':
            base_interval += 2
        elif self.shade_tolerance == 'Intolerant':
            base_interval -= 4
        elif self.shade_tolerance == 'None':
            base_interval -= 6

        # Leaf Retention
        if self.leaf_retention == 'Yes':
            base_interval += 2
        elif self.leaf_retention == 'No':
            base_interval -= 2

        # TODO: change this. Soil tolerance — fewer soil types tolerated = shorter interval
        tolerated_soils = sum(1 for v in self.soil_tolerance.values() if v.lower() == 'yes')
        if tolerated_soils == 0:
            base_interval -= 8
        elif tolerated_soils == 1:
            base_interval -= 4
        elif tolerated_soils == 2:
            base_interval += 2
        elif tolerated_soils == 3:
            base_interval += 4

        # Growth period — shorter growing period = less frequent watering
        growth_modifiers = {
            'Year Round': 6,
            'Spring, Summer, Fall': 4,
            'Spring and Summer': 3,
            'Summer and Fall': 3,
            'Spring and Fall': 2,
            'Fall, Winter and Spring': 1,
            'Spring': 0,
            'Summer': 0,
            'Fall': 0,
            'None': -6
        }
        base_interval += growth_modifiers.get(self.growth_period, 0)

        return base_interval

    def get_env_dependent_interval(self, base_interval, env):
        # Temperature
        if env['temperature_f'] > 86:
            base_interval -= 8
        elif env['temperature_f'] < 40:
            base_interval += 8

        # Humidity
        if env['humidity'] < 30:
            base_interval -= 4
        elif env['humidity'] > 70:
            base_interval += 2

        # Shade hours
        if env['shade'] > 12:
            base_interval += 6
        elif env['shade'] < 6:
            base_interval -= 4

        # Wind — higher wind dries soil faster
        if env['wind'] > 20:
            base_interval -= 4
        elif env['wind'] < 5:
            base_interval += 2

        # Altitude — higher altitude may reduce watering need
        if env['altitude_m'] > 2000:
            base_interval += 4
        elif env['altitude_m'] < 500:
            base_interval -= 2

        return base_interval
    
    def compare_last_water(self, base_interval):
        max_minutes = 92 * 60  # 92 hours
        self.last_watered = datetime.timedelta(minutes=random.randint(0, max_minutes))

        if self.last_watered > datetime.timedelta(days=3):
            base_interval -= 8
        elif self.last_watered > datetime.timedelta(days=2.5):
            base_interval -= 5
        elif self.last_watered > datetime.timedelta(days=2):
            base_interval -= 3
        elif self.last_watered > datetime.timedelta(days=1.5):
            base_interval -= 2
        elif self.last_watered > datetime.timedelta(days=1):
            base_interval -= 1
        return base_interval


    def estimate_watering_interval(self, env=None):
        if env is None:
            env = self.simulate_environment()

        base_interval = 48  # start at 48 hours
        base_interval = self.get_trait_dependent_interval(base_interval)
        base_interval = self.get_env_dependent_interval(base_interval, env)
        base_interval = self.compare_last_water(base_interval)

        return max(0, base_interval)

    def generate_sample(self):
        env = self.simulate_environment()
        interval = self.estimate_watering_interval(env)
        return {
            'plant': self.species,
            'last_water': self.last_watered,
            'environment': env,
            'estimated_watering_interval_hrs': interval
        }

def get_species_dict():
    db_url = ("postgresql+psycopg2://postgres:5253"
                "@localhost:5432/bonsai_app"
             )
    engine = create_engine(db_url)
    cols = ['Moisture Use', 'Drought Tolerance','Shade Tolerance','Adapted to Coarse Textured Soils',
            'Adapted to Fine Textured Soils','Adapted to Medium Textured Soils','Leaf Retention',
            'Active Growth Period']
    
    query = 'SELECT * FROM plant_traits;'
    df = pd.read_sql(query, engine)

    nested_dict = {}
    for index, row in df.iterrows():
        row_key = df.loc[index, 'Plant']  # first column as main key
        nested_dict[row_key] = {
            cols[i]: df.loc[index, cols[i]] for i in range(0, len(cols))
        }

    return nested_dict
     
def run_sim(sample_count):
    """
    species_type_dict below is a dict containing values as species name,
    keys as a dict of attributes.
    """
    species_type_dict = get_species_dict()

    sim_data = {}
    k=0
    for species_type in species_type_dict.keys():
        keys = list(species_type_dict[species_type])
        plant = BootstrapPlant(
            species=species_type,
            moisture_use=species_type_dict[species_type][keys[0]],
            drought_tolerance=species_type_dict[species_type][keys[1]],
            shade_tolerance=species_type_dict[species_type][keys[2]],
            leaf_retention=species_type_dict[species_type][keys[3]],
            coarse_soil_tolerance=species_type_dict[species_type][keys[4]],
            fine_soil_tolerance=species_type_dict[species_type][keys[5]],
            medium_soil_tolerance=species_type_dict[species_type][keys[6]],
            growth_period=species_type_dict[species_type][keys[7]]
        )

        # Generate sample_count plant watering intervals/simulations for each species
        i = 0
        sim_data[species_type] = {}
        while i < sample_count:
            sample = plant.generate_sample()
            sim_data[species_type][i] = sample
            i += 1

        if k >= 100: 
            print(f'100 species done, time: {datetime.datetime.now()}')
            k=0
        k+=1
    return sim_data

def store_sim_data(sim_data):
    db_url = ("postgresql+psycopg2://postgres:5253"
            "@localhost:5432/bonsai_app"
    )
    engine = create_engine(db_url)

    # Flatten into a list of rows
    rows = []
    for species, entries in sim_data.items():
        for i, row in entries.items():
            flat_row = {
                "species": species,
                "id": i,
                "last_water_dt_object": row["last_water"],
                "last_water_minutes": (row["last_water"].total_seconds() / 60)/60,
                "estimated_watering_interval_hrs": row["estimated_watering_interval_hrs"],
            }
            # Merge environment keys into flat_row
            flat_row.update(row["environment"])
            rows.append(flat_row)

    df = pd.DataFrame(rows)

    # Clean up column names for SQL (can't start with a digit)
    df.rename(columns={"36hr_avrg_temp": "avrg_temp_36hr"}, inplace=True)

    # Write to PostgreSQL (replace table if exists)
    df.to_sql("plants_btstrp", engine, if_exists="replace", index=False)

def main():
    sim_data = run_sim(sample_count=10)
    store_sim_data(sim_data)

if __name__ == '__main__':
    main()