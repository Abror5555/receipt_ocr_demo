# Receipt Processing Project

This repository contains a Python script to process receipts from an image, extract text using Tesseract OCR and PaddleOCR, and save the results in JSON format.

## Prerequisites


- **Tesseract OCR**: Install it manually from the official source: [Tesseract OCR Download](https://github.com/tesseract-ocr/tesseract/releases)

## Setup Instructions

### Linux

1. **Create a Virtual Environment**:
   ```bash
   python3 -m venv venv
   ```

2. **Activate the Virtual Environment**:
   ```bash
   source venv/bin/activate
   ```

3. **Install Dependencies**:
   Install the required packages from `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

### Windows

1. **Create a Virtual Environment**:
   ```cmd
   python -m venv venv
   ```

2. **Activate the Virtual Environment**:
   ```cmd
   venv\Scripts\activate
   ```

3. **Install Dependencies**:
   Install the required packages from `requirements.txt`:
   ```cmd
   pip install -r requirements.txt
   ```

4. **Install Tesseract OCR**:
   Download and install Tesseract OCR from [Tesseract OCR Download](https://github.com/tesseract-ocr/tesseract/releases). After installation, ensure the Tesseract executable path (`C:\Program Files\Tesseract-OCR\tesseract.exe`) is correctly set in the script or added to your system PATH.



## Usage

1. Place your input image (e.g., `sample-receipts.png`) in the project directory.
2. Run one of the following scripts based on your preference:
   ```bash
   python process_receipts_tesseract.py
   ```
   - Output files (images and JSON) will be saved in the `output_TesseractORC_result` folder.
   ```bash
   python process_receipts_paddleocr.py
   ```
   - Output files (images and JSON) will be saved in the `output_PaddleOCR_result` folder.
   ```bash
   python process_receipts_combined.py
   ```
   - Output files (images and JSON) will be saved in the `output_Combined_result_of_TesseractOCR_and_PaddleOCR` folder.
