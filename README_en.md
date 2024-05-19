# AI Receipt Batch Processing Tool

This tool uses the OpenAI API to extract information from receipt images and save the results to a text file. 

## Key Features
- Uses AI to enable anyone to import receipts in any format, simply by specifying the folder in Japanese.
- Intended use case: Upload receipt images to a OneDrive folder organized by month, then run this script at the end of the month.

## System Requirements
- Python 3.8 or later
- Modules listed in `requirements.txt`
- Internet connection (required to access the OpenAI API)

## Setup
1. Install Python and install the required libraries from `requirements.txt` (or run the provided executable if you're unfamiliar with Python).
2. Obtain an OpenAI API key (you can find instructions by searching online).

## Usage
1. Run `main.py`, the `領収書処理.bat` file, or the provided executable.
2. The GUI will open, prompting you to enter your OpenAI API key (which will be saved to `settings.json` after you close the window).
3. Click the "フォルダ選択" button to select the folder containing the receipt images.
4. Click the "処理開始" button to start processing the images.
5. Once the processing is complete, a `results.txt` file will be generated in the selected folder, containing the extracted information. If any errors occur, an `error_log.txt` file will also be created.

## Output Format
The extracted data is saved to `results.txt` in the following format:
```
IMG_2853.jpg, 2024/05/12, ショップA, 雑貨, 4505, 消耗品費
IMG_XXX(略)
```

**The extracted information can be easily customized!**
Click the "詳細設定" button to see the text that is sent to the AI. You can modify this to extract the information you need, change the delimiter, or add/remove fields as desired.

## Considerations
- This tool only supports `.jpg` and `.png` image files.
- There are costs associated with using the OpenAI API, so be sure to check their pricing before using the tool. To help keep costs down, the tool includes image resizing functionality, which you can adjust in the "詳細設定" menu.
- The API key is saved to the `settings.json` file, so be sure to remove it if you're using the tool on a shared computer.
- For users unfamiliar with Python, an executable file is provided in the `dist` folder, but it may run slowly.
- This tool was created by an amateur with the help of AI, so there may be some issues or limitations.

## References
https://qiita.com/miso_taku/items/559f771b5b259a2f7bd7
