import cv2
import json
import os
from paddleocr import PaddleOCR
import pytesseract
from pathlib import Path

# Tesseract パス (Windows 用)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# PaddleOCR設定
p_ocr = PaddleOCR(
    use_doc_orientation_classify=False, 
    use_doc_unwarping=False, 
    use_textline_orientation=False
)

# Tesseract設定
t_ocr = pytesseract

# 写真から領収書を切り抜く
def split_receipts(image_path):
    img = cv2.imread(image_path)
    height, width = img.shape[:2]
    regions = [
        (62, 75, 379, 638),  # 1-レシート
        (498, 112, 826, 803),  # 2-レシート
        (840, 108, 1167, 816),  # 3-レシート
        (46, 643, 485, 1636),  # 4-レシート
        (503, 832, 949, 1646)  # 5-レシート
    ]
    output_dir = "output_Combined_result_of_TesseractOCR_and_PaddleOCR"
    os.makedirs(output_dir, exist_ok=True)
    receipts = []
    for i, (x1, y1, x2, y2) in enumerate(regions):
        receipt = img[y1:y2, x1:x2]
        receipt_path = os.path.join(output_dir, f"receipt_{i+1}.png")
        cv2.imwrite(receipt_path, receipt)
        receipts.append(receipt_path)
    return receipts

# データ分析と整理
def parse_receipt_text(paddle_text, tesseract_text):
    data = {"text": {}}
    all_lines = paddle_text + tesseract_text  # 2つのOCR結果を結合します
    
    # Birinchi qatorni "名前" sifatida olamiz
    if all_lines:
        data["text"]["名前"] = all_lines[0].strip()
        # Qolgan qatorlarni ro'yxat sifatida saqlaymiz
        remaining_lines = all_lines[1:]
        if remaining_lines:
            data["text"]["残りのテキスト"] = [line.strip() for line in remaining_lines if line.strip()]

    return data

# データを解析してJSONに保存する
def process_receipt(receipt_path):
    # PaddleOCR
    result_paddle = p_ocr.predict(receipt_path)
    
    # PaddleOCR tizimini saqlash
    output_dir = os.path.dirname(receipt_path)
    for res in result_paddle:
        res.print()
        res.save_to_img(output_dir)
        res.save_to_json(output_dir)
    
    # PaddleOCR JSONファイルの読み取りと処理
    input_json_path = os.path.join(output_dir, f"{Path(receipt_path).stem}_res.json")
    with open(input_json_path, "r", encoding="utf-8") as file:
        paddle_data = json.load(file)
    
    # rec_textsフィールドの抽出
    rec_texts = paddle_data.get("rec_texts", [])
    
    # スクリーンキャプチャ（オプション）
    # print("Topilgan matnlar (PaddleOCR):")
    # for i, text in enumerate(rec_texts, 1):
    #     print(f"{i}. {text}")
    
    # JSONファイルを削除する
    os.remove(input_json_path)
    
    # Tesseract
    text_tess = t_ocr.image_to_string(receipt_path, lang='jpn').splitlines()
    
    # データ分析
    data = parse_receipt_text(rec_texts, text_tess)
    
    # JSONファイルに保存
    json_path = os.path.join(output_dir, f"{Path(receipt_path).stem}_parsed.json")
    os.makedirs(os.path.dirname(json_path), exist_ok=True)
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# 基本的なプロセス
if __name__ == "__main__":
    image_path = "sample-receipts.png"  # Mijoz yuborgan rasm nomi
    receipts = split_receipts(image_path)
    for receipt in receipts:
        process_receipt(receipt)