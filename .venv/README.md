AI扫描资料数字化：基于PaddleOCR+nanobot的扫描pdf/图片文件夹OCR识别与智能检索工具。

功能： 
  1.扫描pdf/图片文件夹OCR识别
  2.输出按页码对应的纯文本和结构化json
  3.接入nanobot实现文档智能问答与检索

环境：
  python3.12.6, cpu

安装：
  git clone 
  cd document-ocr
  pip install -r requirements.txt

使用方法：
  1.把待扫描pdf/图片文件夹放入scan_files/
  2.运行USE.py,结果保存于ocr_output
  3.执行 nanobot agent ,用nanobot检索