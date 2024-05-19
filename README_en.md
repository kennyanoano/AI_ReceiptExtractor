Here is the English version of the README:

### README - Receipt Image Extraction Tool

This tool uses the OpenAI API to extract information from receipt images in a specified folder, and saves the results to a text file.

The intended use case is to have a OneDrive folder with monthly subfolders, where receipt images are uploaded, and then run this script at the end of each month. Since OneDrive is synced locally, you can input the local path for the folder.

#### System Requirements
- Python 3.8 or higher
- Modules listed in requirements.txt
- Internet connection (required to access the OpenAI API)

#### Setup
1. Install Python and install the required libraries from requirements.txt (or run the exe if you don't know how to do this).
2. Obtain an OpenAI API key in advance (you can search for instructions on how to do this).

#### Usage
1. Run main.py or the `領収書処理.bat` file, or the exe.
   ```bash
   python main.py
   ```
2. Enter the OpenAI API key in the window that appears (the key will be saved to the `settings.json` file after closing the window).
3. A GUI will open, click the "Select Folder" button and choose the folder containing the receipt images.
4. Click the "Start Image Processing" button to begin processing the images.
5. Once the processing is complete, a `results.txt` file will be generated in the selected folder, containing the extracted information. If any errors occur, an `error_log.txt` file will also be generated.

#### Output Format
The extracted data is saved to the `results.txt` file in the following format:
```
IMG_2853.jpg, 2024/05/12, Shop A, Miscellaneous, 4505, Consumables
IMG_XXX(略)
```
**You can easily customize the information extracted!**
Open the `text_extractor.py` file and modify the prompt part like this:
```
    PROMPT_TEMPLATE = "XXXXX"
```

#### Notes
- This tool only supports `.jpg` and `.png` image files.
- There will be API usage fees, so please check the OpenAI pricing before using the tool. You can try it with a small number of images first to estimate the cost (it should be less than 10 yen per image for GPT-4-based models).
- The API key is saved in the `settings.json` file, so be sure to delete it if the computer is accessed by multiple people.
- For people who don't know Python, there is an exe file in the `dist` folder, but it's very slow to start up, so be careful. To create your own exe, use the command: `pyinstaller --onefile --windowed main.py`.
- This tool was created by an amateur, so there may be issues.

#### References
https://qiita.com/miso_taku/items/559f771b5b259a2f7bd7