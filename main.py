import os
import sys
from tkinter import Tk, Label, Button, Entry, filedialog
from text_extractor import gen_chat_response_with_gpt4
from PIL import Image

def write_to_text_file(file_path, text):
    """
    指定されたファイルパスにテキストを追記する。
    
    Args:
    file_path (str): テキストを追記するファイルのパス。
    text (str): ファイルに追記するテキスト。
    """
    with open(file_path, 'a') as file:
        file.write(text + "\n")

def select_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        folder_entry.delete(0, 'end')
        folder_entry.insert(0, folder_path)

def process_images():
    folder_path = folder_entry.get()
    if not folder_path:
        print("フォルダが選択されていません。")
        return
    
    valid_extensions = ['.jpg', '.png']
    output_text_file = os.path.join(folder_path, 'results.txt')
    image_files = [f for f in os.listdir(folder_path) if os.path.splitext(f)[1].lower() in valid_extensions]

    max_size = (1600, 1600)  # ここで許容する最大サイズを設定

    for image_file in image_files:
        image_path = os.path.join(folder_path, image_file)
        try:
            with Image.open(image_path) as img:
                if img.size[0] > max_size[0] or img.size[1] > max_size[1]:
                    img.thumbnail(max_size)
                    img.save(image_path)  # 縮小した画像を上書き保存

            result = gen_chat_response_with_gpt4(image_path)
            write_to_text_file(output_text_file, f"{image_file}, {result}")
        except Exception as e:
            print(f"Error processing {image_file}: {str(e)}")
            with open(os.path.join(folder_path, 'error_log.txt'), 'a') as log_file:
                log_file.write(f"Error processing {image_file}: {str(e)}\n")

def main():
    global folder_entry
    root = Tk()
    root.title("フォルダ内のレシート画像から一括情報抽出")

    Label(root, text="フォルダパス:").pack(side="top", fill="x", padx=20, pady=10)
    folder_entry = Entry(root, width=50)
    folder_entry.pack(side="top", fill="x", padx=20, pady=10)

    Button(root, text="フォルダ選択", command=select_folder).pack(side="top", fill="x", padx=20, pady=10)
    Button(root, text="画像処理開始", command=process_images).pack(side="top", fill="x", padx=20, pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
    main()