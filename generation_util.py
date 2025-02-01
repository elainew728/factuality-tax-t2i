from openai import OpenAI
from ratelimiter import RateLimiter
from retrying import retry
import urllib
import base64

### --- ### 
# Replace the placeholder with your own API setting
OPENAI_API_KEY = $YOUR_OPENAI_API_KEY$
ORGANIZATION = $YOUR_OPENAI_ORGANIZATION$
### --- ### 

client = OpenAI(api_key=OPENAI_API_KEY, organization=ORGANIZATION)

@retry(stop_max_attempt_number=10)
@RateLimiter(max_calls=1200, period=60)
def generate_chatgpt(utt):
    response = client.chat.completions.create(
        model="gpt-4o-2024-05-13",
        response_format={ "type": "json_object" },
        messages=[
            {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
            {"role": "user", "content": utt}
        ]
    )
    print(response.choices[0].message.content)
    return response.choices[0].message.content

@retry(stop_max_attempt_number=10)
@RateLimiter(max_calls=1200, period=60)
def generate_chatgpt_text(utt):
    response = client.chat.completions.create(
        model="gpt-4o-2024-05-13",
        messages=[
            {'role': 'system', 'content': "You are a helpful assistant designed to output JSON that answers the following question with proper reference to the provided documents. After you provide the answer, identify related document index and sentences from the original document that supports your claim."},
            {"role": "user", "content": utt}
        ]
    )
    print(response.choices[0].message.content)
    return response.choices[0].message.content

@retry(stop_max_attempt_number=10)
@RateLimiter(max_calls=1200, period=60)
def generate_chatgpt_original(utt, model='gpt4o'):
    if model == 'gpt4o':
        model = "gpt-4o-2024-05-13"
    elif model =='gpt3.5':
        model = "gpt-3.5-turbo-0125"
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": utt}
        ]
    )
    return response.choices[0].message.content


def save_img_from_url(url, fname):
    urllib.request.urlretrieve(url, fname)
    return

# getting Dalle-3's generation
@retry(stop_max_delay=3000, wait_fixed=1000)
@RateLimiter(max_calls=600, period=60)
def get_dalle_response(prompt):
    response = client.images.generate(
    model="dall-e-3",
    prompt=prompt,
    size="1024x1024",
    quality="standard",
    n=1,
    )

    return response.data[0].url

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')