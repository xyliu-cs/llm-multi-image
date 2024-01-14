import os
import base64
import json
import requests

OPENAI_API_TOKEN = ""  #  OpenAI API token here
os.environ["OPENAI_API_KEY"] = OPENAI_API_TOKEN

proxies = {
    "http": "http://172.31.64.1:7890",
    "https": "http://172.31.64.1:7890",
}

# Path to the image files
image_folder = '/home/liu/images'
output_file_path = 'gpt_answers.json'
qa_pairs = 'question_answer_pairs.json'
api_key = os.getenv('OPENAI_API_KEY')
with open('prompt.txt', 'r') as f:
    base_prompt = f.read()   # control the answer format, not few shots


# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

json_output = []
# Process each subfolder
with open(qa_pairs, 'r') as file:
    data = json.load(file)

    # Calculate the length of 1/5 of the data
    first_batch = len(data) // 5

    # go through each question
    for item_idx in range(first_batch*4, first_batch*5):
        user_content = []
        item = data[item_idx]

        image_group = item['image_group']
        question = item['question']
        question_id = item['question_id']
        question_type = item['question_type']
        base_answer = item['answer']
        annotator_1 = item['user1_answer']


        # append base64 images 
        full_image_path_set = [f"{image_folder}/{image}" for image in item['image_required']]
        # print(len(full_image_path_set))
        for image in full_image_path_set:
            b64_img = encode_image(image)
            img_dict = { "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{b64_img}"   # remember to change the image types accordingly
                            }
                        }
            user_content.append(img_dict)

        # append question prompt
        question_prompt=f"\nNow, based on the provided images, answer: {question}"
        prompt_dict = {"type": "text","text": base_prompt + question_prompt}
        user_content.append(prompt_dict)


        # construct request
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        payload = {
            "model": "gpt-4-vision-preview",
            "messages": [
                {
                    "role": "user",
                    "content": user_content
                }
            ],
            "max_tokens": 300
        }

        # send openai request
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload, proxies=proxies)

        # parse answers
        res_dict = response.json()
        answer = res_dict['choices'][0]['message']['content']
        answer_split = answer.split(";;;")
        short_answer = answer_split[0]
        long_answer = answer_split[1]


        json_entry = {
            "question_id": question_id,
            "question": question,
            "question_type": question_type,
            "image_group": image_group,
            "base_answer": base_answer,
            "annotator_1": annotator_1,
            "gpt-short-ans": short_answer,
            "correctness": 0,
            "gpt-long-ans": long_answer,
        }

        # Open the output file in append mode and write the entry
        with open(output_file_path, 'a') as outfile:
            # Check if it's the first entry to avoid leading comma
            if item_idx != 0:
                outfile.write(",\n")
            json.dump(json_entry, outfile, indent=4)

        print(f"Processed question {question_id}")


# with open(output_file_path, 'w') as outfile:
#     json.dump(json_output, outfile, indent=4)

print(f"JSON file created at {output_file_path}")