python process_generated_files.py -g -if ./output/events_year_culture_gender_roles_factchecked.jsonl -of ./output/events_year_culture_gender_roles_factchecked_processed.csv
python generate_images_dalle.py -g -if ./output/events_year_culture_gender_roles_factchecked_processed_dedup_26perculture_balanced.csv -o ./img_output/ # --test
cd FairFace
python predict.py --csv ./factuality-tax-t2i/output/events_year_culture_gender_roles_factchecked_processed_dedup_26perculture_balanced_imggen.csv
cd ..
python organize_fairface_results_new.py -ff ./FairFace/output/events_year_culture_gender_roles_factchecked_processed_dedup_26perculture_balanced_imggen_output_raw.csv -of ./output/events_year_culture_gender_roles_factchecked_processed_dedup_26perculture_balanced_imggen.csv -g
