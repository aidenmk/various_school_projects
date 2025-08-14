import argparse
import os
import yaml
import json
import pandas as pd
from sqlalchemy import create_engine

def load_config(config_path):
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)
    
def create_df_from_json(path):
    with open(path, 'r') as file:
        data = json.load(file)

    df = pd.DataFrame.from_dict(data, orient='index')
    df.reset_index(inplace=True)
    df.rename(columns={"index": "Plant"}, inplace=True)
    print(df)
    return df

def SendDFToSQL(df, args):
    db_url = (
        f"postgresql+psycopg2://{args.user}:{args.password}"
        f"@{args.host}:{args.port}/{args.dbname}"
    )
    engine = create_engine(db_url)
    df.to_sql("plant_traits", engine, if_exists="replace", index=False)

# --- Parse all arguments with YAML override ---
def parse_args():
    # Step 1: Parse --config and --jsonfilepath early
    base_parser = argparse.ArgumentParser(add_help=False)
    base_parser.add_argument('--config', type=str, default='psql_login_info.yml')
    base_parser.add_argument('--jsonfilepath', type=str, default='species_data.json')
    early_args, remaining_argv = base_parser.parse_known_args()

    # Step 2: Load YAML config
    defaults = {}
    if os.path.exists(early_args.config):
        defaults = load_config(early_args.config)

    # Step 3: Merge defaults (YAML) and early parsed args (jsonfilepath)
    defaults.setdefault('jsonfilepath', early_args.jsonfilepath)

    # Step 4: Final parser
    parser = argparse.ArgumentParser(
        parents=[base_parser],
        description='Load plant data from JSON to PostgreSQL'
    )
    parser.set_defaults(**defaults)
    parser.add_argument('--dbname', type=str)
    parser.add_argument('--user', type=str)
    parser.add_argument('--password', type=str)
    parser.add_argument('--host', type=str)
    parser.add_argument('--port', type=int)

    return parser.parse_args(remaining_argv)

def main():
    args = parse_args()
    df = create_df_from_json(args.jsonfilepath)
    SendDFToSQL(df, args)

if __name__ == '__main__':
    main()
   