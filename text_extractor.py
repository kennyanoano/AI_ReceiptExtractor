import base64
import json
from openai import OpenAI

SYSTEM_ROLE_CONTENT = "このシステムは提供された画像の内容を説明を生成します。画像を識別し視覚情報をテキスト形式で提供します。"
#PROMPT_TEMPLATE = "画像から、取引年月日(yyyy/mm/ddのみ時間なし)、店舗名、合計金額(通貨記号は削除)を抽出し表形式(|)で出力せよ"
PROMPT_TEMPLATE = "画像から、取引年月日(yyyy/mm/ddのみ時間なし)、店舗名、合計金額(通貨記号は削除)を抽出しカンマ区切り(,)でreturnせよ"


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

def gen_chat_response_with_gpt4(image_path):
    openai_client = OpenAI(api_key=get_gpt_openai_apikey())
    image_base64 = encode_image(image_path)
    messages = create_message(SYSTEM_ROLE_CONTENT, PROMPT_TEMPLATE, image_base64)

    response = openai_client.chat.completions.create(
        model='gpt-4o-2024-05-13',
        messages = messages,
        temperature = 0.1,
    )

    return response.choices[0].message.content

#使い方
#result = gen_chat_response_with_gpt4(image_path)
#print(result)
#結果のサンプル
#2022/01/22,Seria,660

if __name__ == "__main__":
    # テスト用の画像ファイルパスを指定
    
    extracted_text = gen_chat_response_with_gpt4(test_image_path)
    print(extracted_text)
