CUDA_VISIBLE_DEVICES=7 python generate_images_sd.py -r -if ./output/events_year_culture_race_roles_factchecked_processed_dedup_100perculture.csv -o ./img_output/ # --test
cd FairFace
CUDA_VISIBLE_DEVICES=7 python predict.py --csv ./output/sd3_events_year_culture_race_roles_factchecked_processed_dedup_100perculture_default_imggen.csv
cd ..
python organize_fairface_results_new.py -ff ./FairFace/output/sd3_events_year_culture_race_roles_factchecked_processed_dedup_100perculture_default_imggen_output_raw.csv -of ./output/sd3_events_year_culture_race_roles_factchecked_processed_dedup_100perculture_default_imggen.csv -r