# Diversity Prompt 1
python generate_images_dalle.py -g -if ./output/events_year_culture_gender_roles_factchecked_processed_dedup_26perculture_balanced.csv -o ./img_output/ --cot_model 'gpt4o' -d --fai_vk # --test
cd FairFace
python predict.py --csv ./output/events_year_culture_gender_roles_factchecked_processed_dedup_26perculture_balanced_imggen_diverse_fai_vk.csv
cd ..
python organize_fairface_results_new.py -ff ./FairFace/output/events_year_culture_gender_roles_factchecked_processed_dedup_26perculture_balanced_imggen_diverse_fai_vk_output_raw.csv -of ./output/events_year_culture_gender_roles_factchecked_processed_dedup_26perculture_balanced_imggen_diverse_fai_vk.csv -g

# Diversity Prompt 2
python generate_images_dalle.py -g -if ./output/events_year_culture_gender_roles_factchecked_processed_dedup_26perculture_balanced.csv -o ./img_output/ --cot_model 'gpt4o' -d  -dpt '2' --fai_vk # --test
cd FairFace
python predict.py --csv ./output/events_year_culture_gender_roles_factchecked_processed_dedup_26perculture_balanced_imggen_diverse2_fai_vk.csv
cd ..
python organize_fairface_results_new.py -ff ./FairFace/output/events_year_culture_gender_roles_factchecked_processed_dedup_26perculture_balanced_imggen_diverse2_fai_vk_output_raw.csv -of ./output/events_year_culture_gender_roles_factchecked_processed_dedup_26perculture_balanced_imggen_diverse2_fai_vk.csv -g
