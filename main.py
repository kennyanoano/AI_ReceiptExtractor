import os
import json
from tkinter import Tk, Label, Button, Entry, filedialog, StringVar, Frame
from text_extractor import gen_chat_response_with_gpt4
from PIL import Image
from pdf2image import convert_from_path

def load_api_key():
    if os.path.exists("settings.json"):
        with open("settings.json", "r") as f:
            try:
                settings = json.load(f)
                return settings.get("api_key", "")
            except json.JSONDecodeError:
                return ""
    return ""

def save_api_key(api_key):
    settings = {"api_key": api_key}
    with open("settings.json", "w") as f:
        json.dump(settings, f)


def write_to_text_file(file_path, text):
    with open(file_path, 'a') as file:
        file.write(text + "\n")

def select_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        folder_entry.delete(0, 'end')
        folder_entry.insert(0, folder_path)

def process_images(api_key):
    folder_path = folder_entry.get()
    if not folder_path:
        print("フォルダが選択されていません。")
        return
    
    valid_extensions = ['.jpg', '.png']
    #valid_extensions = ['.jpg', '.png', '.pdf']#pdfにいつか対応したい

    output_text_file = os.path.join(folder_path, 'results.txt')
    image_files = [f for f in os.listdir(folder_path) if os.path.splitext(f)[1].lower() in valid_extensions]

    max_size = (1600, 1600)  # Define max_size here

    for image_file in image_files:
        image_path = os.path.join(folder_path, image_file)
        try:
            if image_path.lower().endswith('.pdf'):
                images = convert_from_path(image_path)
                for i, img in enumerate(images):
                    img_path = f"{image_path[:-4]}_{i}.png"
                    img.save(img_path)
                    process_single_image(img_path, image_file, api_key, output_text_file, max_size)
            else:
                process_single_image(image_path, image_file, api_key, output_text_file, max_size)
        except Exception as e:
            print(f"Error processing {image_file}: {str(e)}")
            with open(os.path.join(folder_path, 'error_log.txt'), 'a') as log_file:
                log_file.write(f"Error processing {image_file}: {str(e)}\n")

def process_single_image(image_path, image_file, api_key, output_text_file, max_size):
    with Image.open(image_path) as img:
        if img.size[0] > max_size[0] or img.size[1] > max_size[1]:
            img.thumbnail(max_size)
            img.save(image_path)  # Resize and overwrite the image

    result = gen_chat_response_with_gpt4(image_path, api_key)
    write_to_text_file(output_text_file, f"{image_file}, {result}")

def main():
    global folder_entry, api_key_entry
    root = Tk()
    root.title("フォルダ内のレシート画像から一括情報抽出")

    Label(root, text="フォルダパス:").pack(side="top", fill="x", padx=20, pady=10)
    folder_entry = Entry(root, width=50)
    folder_entry.pack(side="top", fill="x", padx=20, pady=10)

    Button(root, text="フォルダ選択", command=select_folder).pack(side="top", fill="x", padx=20, pady=10)
    Button(root, text="画像処理開始", command=lambda: process_images(api_key_var.get())).pack(side="top", fill="x", padx=20, pady=10)

    api_key_frame = Frame(root)
    api_key_frame.pack(side="top", fill="x", padx=20, pady=10)
    Label(api_key_frame, text="APIキー:").pack(side="left")
    api_key_var = StringVar()
    api_key_var.set(load_api_key())
    api_key_entry = Entry(api_key_frame, width=50, textvariable=api_key_var, show="*")
    api_key_entry.pack(side="left", fill="x", expand=True)

    def on_close():
        api_key = api_key_var.get()
        save_api_key(api_key)
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)

    root.mainloop()

if __name__ == "__main__":
    main()
