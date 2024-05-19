import base64
import json
from openai import OpenAI

SYSTEM_ROLE_CONTENT = "このシステムは提供された画像の内容を説明を生成します。画像を識別し視覚情報をテキスト形式で提供します。"
PROMPT_TEMPLATE = "画像から、取引年月日(yyyy/mm/ddのみ時間なし)、店舗名、商品名(要約)、合計金額(通貨記号は削除)、推測される勘定科目名を抽出しカンマ区切り(,)でreturnせよ"

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

def gen_chat_response_with_gpt4(image_path, api_key):
    openai_client = OpenAI(api_key=api_key)
    image_base64 = encode_image(image_path)
    messages = create_message(SYSTEM_ROLE_CONTENT, PROMPT_TEMPLATE, image_base64)

    # Adding a new prompt to extract the account name based on the product name
    #account_name_prompt = "商品名から推測される勘定科目名をreturn"
    #messages[1]['content'].append({
    #    'type': 'text',
    #    'text': account_name_prompt
    #})

    response = openai_client.chat.completions.create(
        model='gpt-4o-2024-05-13',
        messages=messages,
        temperature=0.1,
    )


    # レスポンスから必要な情報を抽出
    if response and response.choices:
        extracted_data = response.choices[0].message.content
    #    account_name = response.choices[1].message.content if len(response.choices) > 1 else "No account name found"
    else:
        extracted_data = "No data extracted"
    #    account_name = "No account name found"

    #return extracted_data, account_name
    return extracted_data

