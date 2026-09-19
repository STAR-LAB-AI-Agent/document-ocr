---
name: ocr-digitizer
description: 对扫描 PDF、图片进行 OCR，生成可检索文本并保留页码，支持接入 Nanobot 问答。
version: 1.0.0
---

# OCR 文档数字化技能

## 用途
将扫描 PDF 或图片转为可检索文本，输出纯文本和 JSON，保留页码、坐标、置信度。

## 何时使用
- 用户要求对扫描件做 OCR
- 需要生成可搜索文本
- 需要保留页码对应关系
- 需要基于扫描文档问答或检索

## 输入
- PDF 路径：`./scan_files/xxx.pdf`
- 图片文件夹：`./scan_files/xxx/`
- 可选参数：`lang`（默认 ch）、`device`（cpu 或 gpu:0）、`output_dir`

## 输出
- `ocr_output/文件名_ocr.txt`：按 `===== 第 N 页 =====` 分隔
- `ocr_output/文件名_ocr.json`：含 `text`、`confidence`、`box`、`page`

## 使用方法
```bash
python USE.py          # 批量处理
python digitizer.py      # 单文件
nanobot agent                # 问答