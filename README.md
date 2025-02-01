# The Factuality Tax of Diversity-Intervened Text-to-Image Generation: Benchmark and Fact-Augmented Intervention
*Yixin Wan, Di Wu, Haoran Wang, Kai-Wei Chang*

The Official Code Repository of the **EMNLP 2024 Main** Paper: [The Factuality Tax of Diversity-Intervened Text-to-Image Generation: Benchmark and Fact-Augmented Intervention](https://arxiv.org/abs/2407.00377v1)

### Generating the DoFaiR Dataset
We provide the code for generating the evaluation dataset in DoFaiR.
The data construction pipeline of DoFaiR adopts an iterative loop consisting of the following steps:
1. Generate historical events and participants from seed information
2. Create queries for retrieving factual information
3. Utilize the factual knowledge to label the ground truth demographic distribution of the participants.

Alternatively, in the ```./data/``` folder, we provide the final version of the cleaned and fact-checked DoFaiR dataset that you can directly use for evaluation.

#### Generating DoFaiR-Gender
* To run data generation for DoFaiR Gender, first add your OpenAI account configurations in ```./generation_util.py```.
* Then, run the following command to first generate raw events and participants from seed information:
```
sh ./scripts/run_generate_events_by_years_cultures_gender.sh
```
