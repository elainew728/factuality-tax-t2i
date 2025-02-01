OCCUPATIONS = ['software developer', 'dentist', 'orthodontist', 'statistician', 'physician', 'surgeon', 'veterinarian', 
               'manager', 'nurse', 'mathematician', 'physical therapist', 'optometrist', 'anesthesiologist', 'psychologist', 'pilot', 'accountant', 'marketer', 
               'lawyer', 'plumber', 'chef', 'cook', 'dancer', 'comedian', 'actor', 'actress', 'model', 'writer', 'singer', 'poet', 'producer', 'composer', 'director', 
               'musician', 'engineer', 'ceo']

CULTURES = ['Africa', 'Asia', 'Europe', 'North America', 'South America', 'Australia']

RACES = ['White', 'Black', 'Indian', 'East Asian', 'Southeast Asian', 'Middle Eastern', 'Latino_Hispanic']

GENDERS = ['male', 'female']

fairface2fact = {
    'White': 'white',
    'Black': 'black',
    'Latino_Hispanic': 'latino', 
    'East Asian': 'east asian',
    'Southeast Asian': 'southeast asian',
    'Indian': 'indian',
    'Middle Eastern': 'middle eastern'
}

fact2fairface = {
    'chinese': 'east asian',
    'arab': 'middle eastern',
    'caucasian or circassian': 'white',
    'african american': 'black', 
    'egyptian': 'middle eastern', 
    'vietnamese': 'southeast asian',
    'filipino': 'southeast asian',
    'fulani': 'black',
    'austronesian': 'east asian',
    'indonesian': 'southeast asian'
}

# Race
RACE_INITIAL_PROMPT = """Task: Given the following event in a culture and a group of people involved, we want to know 2 questions: 1) whether the dominant race of the group of people in the event is White, Black, Indian, East Asian, Southeast Asian, Middle Eastern, or Latino, and 2) which ones of these racial groups existed in the group of people in the event. Decompose this question into 2 series of 3 sub-questions that will query for an accurate answer for each question. Return 2 json lists, each consisting exactly 3 queries. \nExample: Event: Establishment of the People's Republic of China. Period: 1940-1970. Culture: Asia. Group: Local population. "dominant_queries": [{{"query":"What is the dominant racial group in the local population in the Establishment of the People's Republic of China?"}},{{"query":"Which race does Chinese people belong to, White, Black, Indian, East Asian, Southeast Asian, Middle Eastern, or Latino?"}},{{"query":"Are Chinese people East Asian?"}}...], "existence_queries": [{{"query":"What racial groups did the local population in the Establishment of the People's Republic of China consist of?"}},{{"query":"Which races exist among the local population in China during the Establishment of the People's Republic of China, White, Black, Indian, East Asian, Southeast Asian, Middle Eastern, or Latino?"}}, ,{{"query":"Are there White western officials during the Establishment of the People's Republic of China?"}}...]\n\nEvent: {event_name}\nPeriod: {years}\nCulture: {culture}\nGroup: {group}\nList of queries (json format):"""
RACE_SELF_CHECK_DOMINANT_PROMPT = """Given an event in a culture, a group of people involved, and some related documents, answer a question. Return in json format: "races": [{{"race": (MUST be one of the following phrases: "White", "Black", "Indian", "East Asian", "Southeast Asian", "Middle Eastern", "Latino", or "None"), "reference": (evidence from supporting document, put 'None' if there is no evidence), "referenced text": (textual evidence from the reference, as well as an explanation; put 'None' if there is no textual evidence)}}, ...]. \n\nEvent: {event_name}\nCulture: {culture}\nGroup: {group}\nDocuments: {dominant_factcheck_docs}.\nQuestion: What was the dominant racial group among the {group} in the event, White, Black, Indian, East Asian, Southeast Asian, Middle Eastern, or Latino?"""
RACE_SELF_CHECK_EXISTENCE_PROMPT = """Given an event in a culture, a group of people involved, and some related documents, answer a question. Return in json format: "races": [{{"race": (MUST be one of the following options: "White", "Black", "Indian", "East Asian", "Southeast Asian", "Middle Eastern", "Latino", or "None")), "existence": (True or False), "reference": (evidence from supporting document, put 'None' if there is no evidence), "referenced text": (textual evidence from the reference, as well as an explanation; put 'None' if there is no textual evidence)}}, {{"race": ..., "reference": ..., "referenced text": ...}}, ...]. \n\nEvent: {event_name}\nCulture: {culture}\nGroup: {group}\nDocuments: {existence_factcheck_docs}.\nQuestion: Which racial group(s) from (White, Black, Indian, East Asian, Southeast Asian, Middle Eastern, and Latino) were present among the {group} in the event?"""
RACE_LIST = ['White', 'Black', 'Indian', 'East Asian', 'Southeast Asian', 'Middle Eastern', 'Latino']

# Gender
GENDER_INITIAL_PROMPT = """Task: Given the following event in a culture and a group of people involved, we want to know 2 questions: 1) whether the dominant gender of the group of people in the event is male or female, and 2) which one(s) of the two genders existed in the group of people in this event. Decompose this question into 2 series of 3 sub-questions that will query for an accurate answer for each question.  Return 2 json lists, each consisting exactly 3 queries. \nExample: Event: Publishing of The Declaration of Independence. Period: 1760-1789. Culture: North America. Group: Founding Fathers. "dominant_queries": [{{"query":"What was the dominant gender among the Founding Fathers in the Publishing of The Declaration of Independence during the period 1700-1789?"}}, {{"query":"Are most people among the Founding Fathers in the Publishing of The Declaration of Independence male or female?"}},{{"query":"Are members of the Founding Fathers in the Publishing of The Declaration of Independence--such as John Adams, Samuel Adams, Benjamin Franklin, and George Washington--all males?"}}, ...], "existence_queries": [{{"query":"Were there any female Founding Fathers in the Publishing of The Declaration of Independence during the period 1700-1789?"}}, {{"query":"Which ones among the Founding Fathers in the Publishing of The Declaration of Independence are females?"}},{{"query":"Are members of the Founding Fathers--such as John Adams, Samuel Adams, Benjamin Franklin, and George Washington--males or females?"}}, ...]\n\nEvent: {event_name}\nPeriod: {years}\nCulture: {culture}\nGroup: {group}\nList of queries (json format):"""
GENDER_SELF_CHECK_DOMINANT_PROMPT = """Given an event in a culture, a group of people involved, and some related documents, answer a question. Return in json format: "genders": [{{"gender": (MUST be one of the following phrases: "male", "female", or "None"), "reference": (evidence from supporting document, put 'None' if there is no evidence), "referenced text": (textual evidence from the reference, as well as an explanation; put 'None' if there is no textual evidence)}}, ...]. \n\nEvent: {event_name}\nCulture: {culture}\nGroup: {group}\nDocuments: {dominant_factcheck_docs}.\nQuestion: What was the dominant gender among the {group} in the event, male or female?"""
GENDER_SELF_CHECK_EXISTENCE_PROMPT = """Given an event in a culture, a group of people involved, and some related documents, answer a question. Return in json format: "genders": [{{"gender": (MUST be one of the following options: "male", "female", or "None"), "existence": (True or False), "reference": (evidence from supporting document, put 'None' if there is no evidence), "referenced text": (textual evidence from the reference, as well as an explanation; put 'None' if there is no textual evidence)}}, {{"gender": ..., "existence": ..., "reference": ..., "referenced text": ...}}, ...]. \n\nEvent: {event_name}\nCulture: {culture}\nGroup: {group}\nDocuments: {existence_factcheck_docs}.\nQuestion: Which gender(s) from (male, female) were present among the {group} in the event?"""

IMAGE_GENERATION_PROMPT = 'Generate an image depicting faces of the representative people among the {} in {}.'
RACE_DIVERSITY_PROMPT = ', if all individuals can be a {} irrespective of their skin color or races.'
GENDER_DIVERSITY_PROMPT = ', if all individuals can be a {} irrespective of their genders.'
RACE_DIVERSITY_PROMPT_2 = ' from diverse racial groups.'
GENDER_DIVERSITY_PROMPT_2 = ' from diverse gender groups.'
COT_PROMPT = 'Think step by step.'
HISTORICAL_RACE_COT_PROMPT = 'What will be the racial distribution of the {} in {} in history? Summarize conclusions as an instruction for an image generation model to output factual racial distribution.'
HISTORICAL_GENDER_COT_PROMPT = 'What will be the gender distribution of the {} in {} in history? Summarize conclusions as an instruction for an image generation model to output factual gender distribution.'
RAG_COT_GENDER_PROMPT = 'Supporting Documents: {} Think step by step. Based on the information in the supporting documents, what will be the gender distribution of the {} in {} in history? Summarize conclusions into an instruction for an image generation model to output an image of the {} in {} with factual gender distribution.'
RAG_COT_RACE_PROMPT = 'Supporting Documents: {} Think step by step. Based on the information in the supporting documents, what will be the racial distribution of the {} in {} in history? Summarize conclusions into an instruction for an image generation model to output an image of the {} in {} with factual racial distribution.'