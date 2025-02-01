# Diversity Prompt 1
python generate_images_dalle.py -r -if ./output/events_year_culture_race_roles_factchecked_processed_dedup_100perculture.csv -o ./img_output/ --cot_model 'gpt4o' -d --fai_vk # --test
cd FairFace
python predict.py --csv ./output/events_year_culture_race_roles_factchecked_processed_dedup_100perculture_imggen_diverse_fai_vk.csv
cd ..
python organize_fairface_results_new.py -ff ./FairFace/output/events_year_culture_race_roles_factchecked_processed_dedup_100perculture_imggen_diverse_fai_vk_output_raw.csv -of ./output/events_year_culture_race_roles_factchecked_processed_dedup_100perculture_imggen_diverse_fai_vk.csv -r

# Diversity Prompt 2
python generate_images_dalle.py -r -if ./output/events_year_culture_race_roles_factchecked_processed_dedup_100perculture.csv -o ./img_output/ --cot_model 'gpt4o' -d -dpt '2' --fai_vk # --test
cd FairFace
python predict.py --csv ./output/events_year_culture_race_roles_factchecked_processed_dedup_100perculture_imggen_diverse2_fai_vk.csv
cd ..
python organize_fairface_results_new.py -ff ./FairFace/output/events_year_culture_race_roles_factchecked_processed_dedup_100perculture_imggen_diverse2_fai_vk_output_raw.csv -of ./output/events_year_culture_race_roles_factchecked_processed_dedup_100perculture_imggen_diverse2_fai_vk.csv -r