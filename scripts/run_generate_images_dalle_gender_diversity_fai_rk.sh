# Diversity Prompt 1
python generate_images_dalle.py -g -if ./output/events_year_culture_gender_roles_factchecked_processed_dedup_26perculture_balanced.csv -o ./img_output/ --cot_model 'gpt4o' -d --fai_rk # --test
cd FairFace
python predict.py --csv ./factuality-tax-t2i/output/events_year_culture_gender_roles_factchecked_processed_dedup_26perculture_balanced_imggen_diverse_fai_rk.csv
cd ..
python organize_fairface_results_new.py -ff ./FairFace/output/events_year_culture_gender_roles_factchecked_processed_dedup_26perculture_balanced_imggen_diverse_fai_rk_output_raw.csv -of ./output/events_year_culture_gender_roles_factchecked_processed_dedup_26perculture_balanced_imggen_diverse_fai_rk.csv -g

# Diversity Prompt 2
python generate_images_dalle.py -g -if ./output/events_year_culture_gender_roles_factchecked_processed_dedup_26perculture_balanced.csv -o ./img_output/ --cot_model 'gpt4o' -d -dpt '2' --fai_rk # --test
cd FairFace
python predict.py --csv ./factuality-tax-t2i/output/events_year_culture_gender_roles_factchecked_processed_dedup_26perculture_balanced_imggen_diverse2_fai_rk.csv
cd ..
python organize_fairface_results_new.py -ff ./FairFace/output/events_year_culture_gender_roles_factchecked_processed_dedup_26perculture_balanced_imggen_diverse2_fai_rk_run1_output_raw.csv -of ./output/events_year_culture_gender_roles_factchecked_processed_dedup_26perculture_balanced_imggen_diverse2_fai_rk_run1.csv -g
