import os
from digitizer import DocumentDigitizer

def batch_process(input_dir, output_dir='./ocr_output'):
    digitizer = DocumentDigitizer(lang='ch', device='cpu', output_dir=output_dir)
    pdf_files = []
    image_dirs = []

    for name in os.listdir(input_dir):
        path = os.path.join(input_dir, name)
        if name.lower().endswith('.pdf'):
            pdf_files.append(path)
        elif os.path.isdir(path):
            image_dirs.append(path)

    print(f"发现 {len(pdf_files)} 个 PDF，{len(image_dirs)} 个图片文件夹")

    for pdf_path in pdf_files:
        print(f"\n{'='*50}")
        print(f"处理 PDF: {os.path.basename(pdf_path)}")
        print('='*50)
        digitizer.process_pdf(pdf_path)

    for img_dir in image_dirs:
        print(f"\n{'='*50}")
        print(f"处理图片文件夹: {os.path.basename(img_dir)}")
        print('='*50)
        digitizer.process_image_folder(img_dir)

    print(f"\n全部完成！共处理 {len(pdf_files)} 个 PDF + {len(image_dirs)} 个文件夹")
    print(f"输出目录: {os.path.abspath(output_dir)}")

if __name__ == "__main__":
    batch_process('./scan_files')