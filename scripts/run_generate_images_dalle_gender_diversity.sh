# Diversity Prompt 1
python generate_images_dalle.py -g -if ./output/events_year_culture_gender_roles_factchecked_processed_dedup_26perculture_balanced.csv -o ./img_output/ -d # --test
cd FairFace
python predict.py --csv ./factuality-tax-t2i/output/events_year_culture_gender_roles_factchecked_processed_dedup_26perculture_balanced_imggen_diverse.csv
cd ..
python organize_fairface_results_new.py -ff ./FairFace/output/events_year_culture_gender_roles_factchecked_processed_dedup_26perculture_balanced_imggen_diverse_output_raw.csv -of ./output/events_year_culture_gender_roles_factchecked_processed_dedup_26perculture_balanced_imggen_diverse.csv -g

# Diversity Prompt 2
python generate_images_dalle.py -g -if ./output/events_year_culture_gender_roles_factchecked_processed_dedup_26perculture_balanced.csv -o ./img_output/ -d -dpt '2' # --test
cd FairFace
python predict.py --csv ./factuality-tax-t2i/output/events_year_culture_gender_roles_factchecked_processed_dedup_26perculture_balanced_imggen_diverse2.csv
cd ..
python organize_fairface_results_new.py -ff ./FairFace/output/events_year_culture_gender_roles_factchecked_processed_dedup_26perculture_balanced_imggen_diverse2_output_raw.csv -of ./output/events_year_culture_gender_roles_factchecked_processed_dedup_26perculture_balanced_imggen_diverse2.csv -g
