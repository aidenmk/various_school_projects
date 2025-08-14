import argparse
import os
import yaml
import pandas as pd
from sqlalchemy import create_engine

def load_config(config_path):
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)
    
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=str, default='psql_login_info.yml',
                        help='path to yml with login info to psql')

    args, remaining_argv = parser.parse_known_args()

    defaults = {}
    if os.path.exists(args.config):
        defaults = load_config(args.config)
    
    parser = argparse.ArgumentParser(description='Contains login info for psql')
    parser.add_argument('--dbname', type=str, default=defaults.get('dbname'))
    parser.add_argument('--user', type=str, default=defaults.get('user'))
    parser.add_argument('--password', type=str, default=defaults.get('password'))
    parser.add_argument('--host', type=str, default=defaults.get('host'))
    parser.add_argument('--port', type=int, default=defaults.get('port'))
    args = parser.parse_args(remaining_argv)

    # Create the SQLAlchemy database URL string
    db_url = (
        f"postgresql+psycopg2://{args.user}:{args.password}"
        f"@{args.host}:{args.port}/{args.dbname}"
    )

    
    # Create SQLAlchemy engine
    engine = create_engine(db_url)

    query = """
    SELECT commonname 
    FROM usdatreelist
    WHERE commonname NOT IN (
        SELECT commonname FROM excluded_plants
    );
    """

    species_df = pd.read_sql(query, engine)
    species_df.drop_duplicates(inplace=True)
    species_list = species_df['commonname'].tolist()

    attributes_list = [
        'Moisture Use',
        'Drought Tolerance',
        'Shade Tolerance',
        'Adapted to Coarse Textured Soils',
        'Adapted to Fine Textured Soils',
        'Adapted to Medium Textured Soils',
        'Leaf Retention',
        'Active Growth Period'
    ]

    export_data = {
        'species': species_list,
        'attributes': attributes_list
    }

    with open('species_attributes.yml', 'w') as file:
        yaml.dump(export_data, file, sort_keys=False)

if __name__ == '__main__':
    main()
