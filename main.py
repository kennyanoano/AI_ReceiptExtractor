import os
import json
from tkinter import Tk, Label, Button, Entry, filedialog, StringVar, Frame, BooleanVar, IntVar, Checkbutton,  Toplevel, ttk,messagebox
from text_extractor import gen_chat_response_with_gpt4

# Define a default prompt template at the beginning of your script
PROMPT_TEMPLATE = "画像から、取引年月日(yyyy/mm/ddのみ時間なし)、店舗名、商品名(要約)、合計金額(通貨記号は削除)、推測される勘定科目名を抽出しカンマ区切り(,)でreturnせよ"

# グローバル変数として先に宣言
global prompt_template_var
prompt_template_var = None

# グローバル変数として先に宣言
global api_key_var, max_size_var, resize_enabled_var
api_key_var = None
max_size_var = None
resize_enabled_var = None

def load_settings():
    default_settings = {
        "api_key": "",
        "max_size": 2048,
        "resize_enabled": True,
        "prompt_template": PROMPT_TEMPLATE  # Use the defined default prompt template
    }
    if os.path.exists("settings.json"):
        with open("settings.json", "r") as f:
            try:
                settings = json.load(f)
                return {**default_settings, **settings}
            except json.JSONDecodeError:
                return default_settings
    return default_settings

def save_settings(api_key, max_size, resize_enabled, prompt_template):
    settings = {
        "api_key": api_key,
        "max_size": max_size,
        "resize_enabled": resize_enabled,
        "prompt_template": prompt_template
    }
    with open("settings.json", "w") as f:
        json.dump(settings, f)

def write_to_text_file(file_path, text):
    with open(file_path, 'a') as file:
        file.write(text + "\n")

def select_folder(folder_entry):
    folder_path = filedialog.askdirectory()
    if folder_path:
        folder_entry.delete(0, 'end')
        folder_entry.insert(0, folder_path)

def process_images(api_key, max_size, resize_enabled, folder_entry, progress_var, root):
    settings = load_settings()  # settings をロード
    folder_path = folder_entry.get()
    if not folder_path:
        print("フォルダが選択されていません。")
        return
    
    valid_extensions = ['.jpg', '.png']
    output_text_file = os.path.join(folder_path, 'results.txt')
    image_files = [f for f in os.listdir(folder_path) if os.path.splitext(f)[1].lower() in valid_extensions]
    total_images = len(image_files)
    for index, image_file in enumerate(image_files):
        image_path = os.path.join(folder_path, image_file)
        try:
            process_single_image(image_path, image_file, api_key, output_text_file, max_size, resize_enabled, settings["prompt_template"])
            # プログレスバーを更新
            progress_var.set((index + 1) / total_images * 100)
            root.update_idletasks()  # UIを更新
        except Exception as e:
            print(f"Error processing {image_file}: {str(e)}")
            with open(os.path.join(folder_path, 'error_log.txt'), 'a') as log_file:
                log_file.write(f"Error processing {image_file}: {str(e)}\n")
    messagebox.showinfo("完了", "画像の処理が完了しました。")

def process_single_image(image_path, image_file, api_key, output_text_file, max_size, resize_enabled, prompt_template):
    from PIL import Image
    import tempfile
    import shutil
    temp_dir = tempfile.mkdtemp()  # 一時ディレクトリを作成
    temp_image_path = os.path.join(temp_dir, image_file)  # 一時ファイルのパス

    with Image.open(image_path) as img:
        if resize_enabled and (img.size[0] > max_size or img.size[1] > max_size):
            img.thumbnail((max_size, max_size))
            img.save(temp_image_path)  # リサイズした画像を一時ファイルに保存
        else:
            shutil.copy(image_path, temp_image_path)  # リサイズ不要の場合、元の画像をコピー

    try:
        result = gen_chat_response_with_gpt4(temp_image_path, api_key, prompt_template)  # 一時ファイルを使用
        write_to_text_file(output_text_file, f"{image_file}, {result}")
    finally:
        shutil.rmtree(temp_dir)  # 一時ディレクトリを削除

def open_advanced_settings():
    global prompt_template_var, max_size_var, resize_enabled_var
    settings = load_settings()

    advanced_settings_window = Toplevel()  # Toplevelを使用する
    advanced_settings_window.title("詳細設定")

    Label(advanced_settings_window, text="レシートから抽出したい情報をAIにお願いする:").pack(side="top", fill="x", padx=20, pady=10)
    prompt_template_var = StringVar(advanced_settings_window, value=settings.get("prompt_template", PROMPT_TEMPLATE))
    Entry(advanced_settings_window, width=50, textvariable=prompt_template_var).pack(side="top", fill="x", padx=20, pady=10)

    # 最大画像サイズのUIを詳細設定に追加
    Label(advanced_settings_window, text="最大画像サイズ:").pack(side="top", fill="x", padx=20, pady=10)
    max_size_var = IntVar(value=settings["max_size"])
    Entry(advanced_settings_window, width=10, textvariable=max_size_var).pack(side="top", fill="x", padx=20, pady=10)

    # リサイズ有効のチェックボックスを詳細設定に追加
    resize_enabled_var = BooleanVar(value=settings["resize_enabled"])
    Checkbutton(advanced_settings_window, text="リサイズ有効", variable=resize_enabled_var).pack(side="top", fill="x", padx=20, pady=10)

    Button(advanced_settings_window, text="保存して閉じる", command=lambda: save_advanced_settings(advanced_settings_window)).pack(side="top", fill="x", padx=20, pady=10)
    Button(advanced_settings_window, text="デフォルトに戻す", command=lambda: reset_to_default(prompt_template_var)).pack(side="top", fill="x", padx=20, pady=10)

    advanced_settings_window.mainloop()


def reset_to_default(variable):
    variable.set(PROMPT_TEMPLATE)

def save_advanced_settings(window):
    settings = {
        "api_key": api_key_var.get(),  # Assuming api_key_var is accessible globally
        "prompt_template": prompt_template_var.get(),
        "max_size": max_size_var.get(),
        "resize_enabled": resize_enabled_var.get()
    }
    save_settings(settings["api_key"], settings["max_size"], settings["resize_enabled"], settings["prompt_template"])
    window.destroy()

def main():
    global api_key_var, prompt_template_var, max_size_var, resize_enabled_var  # max_size_var と resize_enabled_var を追加
    settings = load_settings()
    
    root = Tk()
    root.title("AI_レシート一括処理")

    # Add a button to open advanced settings, positioned at the top right
    Button(root, text="詳細設定", command=open_advanced_settings).pack(anchor="ne", padx=20, pady=10)

    # Folder path UI
    folder_frame = Frame(root)
    folder_frame.pack(side="top", fill="x", padx=20, pady=10)
    Label(folder_frame, text="folder:").pack(side="left")
    folder_entry = Entry(folder_frame, width=40)
    folder_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
    Button(folder_frame, text="選択", command=lambda: select_folder(folder_entry)).pack(side="left")

    # プログレスバーのUIを追加
    progress_var = IntVar()
    progress_bar = ttk.Progressbar(root, maximum=100, variable=progress_var, mode='determinate')
    progress_bar.pack(side="top", fill="x", padx=20, pady=10)

    # Start processing button
    Button(root, text="レシート一括処理開始", command=lambda: process_images(api_key_var.get(), max_size_var.get(), resize_enabled_var.get(), folder_entry, progress_var, root)).pack(side="top", fill="x", padx=20, pady=10)

    # API Key UI at the bottom
    api_key_frame = Frame(root)
    api_key_frame.pack(side="bottom", fill="x", padx=20, pady=10)
    Label(api_key_frame, text="APIキー:").pack(side="left")
    api_key_var = StringVar(value=settings["api_key"])
    api_key_entry = Entry(api_key_frame, width=50, textvariable=api_key_var, show="*")
    api_key_entry.pack(side="left", fill="x", expand=True)

    # Initialize max_size_var and resize_enabled_var
    max_size_var = IntVar(value=settings["max_size"])
    resize_enabled_var = BooleanVar(value=settings["resize_enabled"])

    def on_close():
        save_settings(api_key_var.get(), max_size_var.get(), resize_enabled_var.get(), settings["prompt_template"])
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()

if __name__ == "__main__":
    main()
