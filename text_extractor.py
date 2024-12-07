#opneAIとのやり取りの部分
import base64
import json
from openai import OpenAI

SYSTEM_ROLE_CONTENT = "このシステムは提供された画像の内容の説明を生成します。画像を識別し視覚情報をテキスト形式で提供します。"

def get_gpt_openai_apikey():
    with open("secret.json") as f:
        secret = json.load(f)
    return secret["OPENAI_API_KEY"]

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    return f"data:image/jpeg;base64,{encoded_string}"

def create_message(system_role, prompt, image_base64):
    message = [
        {
            'role': 'system',
            'content': system_role
        },
        {
            'role': 'user',
            'content': [
                {
                    'type': 'text',
                    'text': prompt
                },
                {
                    'type': 'image_url',
                    'image_url': {
                        'url': image_base64
                    }
                },
            ]
        },
    ]
    return message

def gen_chat_response_with_gpt4(image_path, api_key, prompt_template):
    openai_client = OpenAI(api_key=api_key)
    image_base64 = encode_image(image_path)
    messages = create_message(SYSTEM_ROLE_CONTENT, prompt_template, image_base64)

    response = openai_client.chat.completions.create(
        model='gpt-4o',
        messages=messages,
        temperature=0,
    )

    if response and response.choices:
        extracted_data = response.choices[0].message.content
    else:
        extracted_data = "No data extracted"

    #return extracted_data, account_name
    return extracted_data