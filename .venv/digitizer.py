import os
import json
import fitz
import cv2
import numpy as np
from paddleocr import PaddleOCR


class DocumentDigitizer:

    def __init__(self, lang='ch', device='cpu', output_dir='./ocr_output'):
        self.ocr = PaddleOCR(
            use_textline_orientation=True,
            lang=lang,
            device=device,
            enable_mkldnn=False
        )
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.pages_data = []

    def pdf_to_images(self, pdf_path, zoom=2.0):
        doc = fitz.open(pdf_path)
        images = []
        for page_index in range(len(doc)):
            page = doc[page_index]
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat)
            img = np.frombuffer(pix.samples, dtype=np.uint8)
            img = img.reshape(pix.height, pix.width, pix.n)
            if pix.n == 4:
                img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
            elif pix.n == 3:
                img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            images.append((page_index + 1, img))
        doc.close()
        print(f"[PDF] 共加载 {len(images)} 页")
        return images

    def ocr_image(self, img_array):
        result = self.ocr.predict(img_array)
        lines = []
        if not result:
            return lines

        res = result[0]
        texts = res.get('rec_texts', []) if hasattr(res, 'get') else getattr(res, 'rec_texts', [])
        scores = res.get('rec_scores', []) if hasattr(res, 'get') else getattr(res, 'rec_scores', [])
        polys = res.get('rec_polys', []) if hasattr(res, 'get') else getattr(res, 'rec_polys', [])

        for text, score, poly in zip(texts, scores, polys):
            lines.append({
                "text": text,
                "confidence": round(float(score), 4),
                "box": [[int(p[0]), int(p[1])] for p in poly]
            })
        return lines

    def process_pdf(self, pdf_path):
        doc_name = os.path.splitext(os.path.basename(pdf_path))[0]
        images = self.pdf_to_images(pdf_path)

        full_text_parts = []
        for page_num, img in images:
            print(f"  正在识别第 {page_num} 页...")
            lines = self.ocr_image(img)

            page_text = "\n".join([l["text"] for l in lines])
            full_text_parts.append(f"===== 第 {page_num} 页 =====\n{page_text}")

            self.pages_data.append({
                "doc_name": doc_name,
                "page": page_num,
                "lines": lines
            })

        txt_path = os.path.join(self.output_dir, f"{doc_name}_ocr.txt")
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write("\n\n".join(full_text_parts))
        print(f"[保存] 文本文件 → {txt_path}")

        json_path = os.path.join(self.output_dir, f"{doc_name}_ocr.json")
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(self.pages_data, f, ensure_ascii=False, indent=2)
        print(f"[保存] JSON 文件 → {json_path}")

        return txt_path, json_path

    def process_image_folder(self, image_dir):
        valid_ext = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff')
        images = sorted([f for f in os.listdir(image_dir)
                         if f.lower().endswith(valid_ext)])

        full_text_parts = []
        for idx, img_name in enumerate(images, start=1):
            img_path = os.path.join(image_dir, img_name)
            img = cv2.imread(img_path)
            print(f"  正在识别第 {idx} 张: {img_name}...")
            lines = self.ocr_image(img)

            page_text = "\n".join([l["text"] for l in lines])
            full_text_parts.append(
                f"===== 第 {idx} 页 ({img_name}) =====\n{page_text}"
            )

            self.pages_data.append({
                "doc_name": os.path.basename(image_dir),
                "page": idx,
                "source_file": img_name,
                "lines": lines
            })

        folder_name = os.path.basename(image_dir.rstrip('/\\'))
        txt_path = os.path.join(self.output_dir, f"{folder_name}_ocr.txt")
        json_path = os.path.join(self.output_dir, f"{folder_name}_ocr.json")

        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write("\n\n".join(full_text_parts))
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(self.pages_data, f, ensure_ascii=False, indent=2)

        print(f"[保存] 文本文件 → {txt_path}")
        print(f"[保存] JSON 文件 → {json_path}")
        return txt_path, json_path


if __name__ == "__main__":
    digitizer = DocumentDigitizer(
        lang='ch',
        device='cpu',
        output_dir='./ocr_output'
    )
    #处理扫描pdf
    #digitizer.process_pdf('./智能体开发实战_课程实验任务书_27题版_修订稿.pdf')
    #处理图片文件夹
    #digitizer.process_image_folder('./tangshi/')