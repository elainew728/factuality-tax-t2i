# Diversity Prompt 1
CUDA_VISIBLE_DEVICES=6 python generate_images_sd.py -g -if ./output/events_year_culture_gender_roles_factchecked_processed_dedup_26perculture_balanced.csv -o ./img_output/ -d # --test
CUDA_VISIBLE_DEVICES=7 python generate_images_sd.py -r -if ./output/events_year_culture_race_roles_factchecked_processed_dedup_100perculture.csv -o ./img_output/ -d # --test
cd FairFace
python predict.py --csv ./output/sd3_events_year_culture_gender_roles_factchecked_processed_dedup_26perculture_balanced_diversity_imggen.csv
cd ..
python organize_fairface_results_new.py -ff ./FairFace/output/sd3_events_year_culture_gender_roles_factchecked_processed_dedup_26perculture_balanced_diversity_imggen_output_raw.csv -of ./output/sd3_events_year_culture_gender_roles_factchecked_processed_dedup_26perculture_balanced_diversity_imggen.csv -g

# Diversity Prompt 2
python generate_images_sd.py -g -if ./output/events_year_culture_gender_roles_factchecked_processed_dedup_26perculture_balanced.csv -o ./img_output/ -d -dpt '2' # --test
cd FairFace
python predict.py --csv ./output/events_year_culture_gender_roles_factchecked_processed_dedup_26perculture_balanced_imggen_diverse2.csv
cd ..
python organize_fairface_results_new.py -ff ./FairFace/output/events_year_culture_gender_roles_factchecked_processed_dedup_26perculture_balanced_imggen_diverse2_output_raw.csv -of ./output/events_year_culture_gender_roles_factchecked_processed_dedup_26perculture_balanced_imggen_diverse2.csv -g
