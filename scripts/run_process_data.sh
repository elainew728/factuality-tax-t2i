# Gender
python process_generated_files.py -g -if ./data/events_year_culture_gender_roles_factchecked.jsonl -of ./data/events_year_culture_gender_roles_factchecked_processed.csv
python clean_data.py -g
# Race
python process_generated_files.py -r -if ./data/events_year_culture_race_roles_factchecked.jsonl -of ./data/events_year_culture_race_roles_factchecked_processed.csv
python clean_data.py -r