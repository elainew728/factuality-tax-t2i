python generate_images_dalle.py -r -if ./output/events_year_culture_race_roles_factchecked_processed_dedup_100perculture.csv -o ./img_output/ # --test
cd FairFace
python predict.py --csv ./output/events_year_culture_race_roles_factchecked_processed_dedup_100perculture_imggen.csv
cd ..
python organize_fairface_results_new.py -ff ./FairFace/output/events_year_culture_race_roles_factchecked_processed_dedup_100perculture_imggen_output_raw.csv -of ./output/events_year_culture_race_roles_factchecked_processed_dedup_100perculture_imggen.csv -r