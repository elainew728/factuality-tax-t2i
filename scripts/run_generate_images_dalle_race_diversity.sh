# Diversity Prompt 1
python generate_images_dalle.py -r -if ./output/events_year_culture_race_roles_factchecked_processed_dedup_100perculture.csv -o ./img_output/ -d # --test
cd FairFace
python predict.py --csv ./output/events_year_culture_race_roles_factchecked_processed_dedup_100perculture_imggen_diverse.csv
cd ..
python organize_fairface_results_new.py -ff ./FairFace/output/events_year_culture_race_roles_factchecked_processed_dedup_100perculture_imggen_diverse_output_raw.csv -of ./output/events_year_culture_race_roles_factchecked_processed_dedup_100perculture_imggen_diverse.csv -r

# Diversity Prompt 2
python generate_images_dalle.py -r -if ./output/events_year_culture_race_roles_factchecked_processed_dedup_100perculture.csv -o ./img_output/ -d -dpt '2' # --test
cd FairFace
python predict.py --csv ./output/events_year_culture_race_roles_factchecked_processed_dedup_100perculture_imggen_diverse2.csv
cd ..
python organize_fairface_results_new.py -ff ./FairFace/output/events_year_culture_race_roles_factchecked_processed_dedup_100perculture_imggen_diverse2_output_raw.csv -of ./output/events_year_culture_race_roles_factchecked_processed_dedup_100perculture_imggen_diverse2.csv -r