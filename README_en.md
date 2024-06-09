### README - AI Receipt Batch Processing

This tool is a program that uses the OpenAI API to read and categorize receipts. Specifically, it extracts information from receipt images in a specified folder and saves the results to a text file.

One of its features is that it uses OpenAI's intelligent AI, allowing anyone to import data in any format by specifying it in Japanese. The cost is around 1 yen per receipt processed, so it's easy on your wallet.

The intended use case is to upload receipt/invoice images to a monthly folder on a cloud service like OneDrive, and then run this script at the end of the month. Since cloud services also sync images locally, you can enter the local path for the input folder.

#### System Requirements
- Python 3.8 or higher
- Modules listed in requirements.txt
- Internet connection (required to access the OpenAI API)

#### Preparation
1. Install Python and the necessary libraries from requirements.txt (if you don't know how, run the exe)
2. Obtain an OpenAI API key in advance (search online for how to do this)

#### Usage
1. Run main.py, `領収書処理.bat`, or the exe file
   ```bash
   python main.py
   ```
2. A GUI will open, enter your OpenAI API key in the bottom window (it will be saved as settings.json after closing the file)
3. Click the "Select" button and choose the folder where the receipt images are saved.
4. Click the "Start Processing" button to begin processing the images (this will take time!).
5. Once processing is complete, a `results.txt/csv` file will be generated in the selected folder, containing the extracted information. If errors occur, an `error_log.txt` file will be generated in the same folder.

#### Output Format
The extracted data will be saved in `results.txt` and `results.csv` in the following format:
```
IMG_2853.jpg, 2024/05/12,Shop A,Miscellaneous,4505,Consumables
IMG_XXX(abbreviated)
```
**The information to be extracted can be easily customized!**
Press the "Advanced Settings" button to see the text you're asking the AI for, and rewrite it to get what you want! If you don't like comma-separated values, you can use slashes, add tax information, or freely customize it.

#### Notes
- This tool only supports `.jpg` and `.png` image files.
- Regarding data confidentiality, since the information is exchanged with the AI via the API, the input information will not be used for training or leaked.
- API usage fees will be incurred, so please check OpenAI's pricing structure before use. To prevent excessive processing costs, image resizing is included. This can be changed from the Advanced Settings (default is 1800, which costs around 1 yen per image).
- The API key is saved in settings.json, so be sure to delete the file if using a shared PC.
- For those unfamiliar with Python, an exe file is included in the dist folder! However, it's very slow to start, so be careful. To create an exe yourself, use `pyinstaller --onefile --windowed main.py`.
- This is a tool created by an amateur with the help of AI, so there may be some issues.

#### Reference
https://qiita.com/miso_taku/items/559f771b5b259a2f7bd7