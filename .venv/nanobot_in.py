import asyncio
import json
import os
from nanobot import Nanobot
from digilizer import DocumentDigitizer


async def process_with_nanobot(pdf_path, output_dir='./ocr_output'):
    digitizer = DocumentDigitizer(lang='ch', output_dir=output_dir)
    txt_path, json_path = digitizer.process_pdf(pdf_path)

    with open(txt_path, 'r', encoding='utf-8') as f:
        ocr_text = f.read()

    async with Nanobot.from_config() as bot:
        summary_prompt = (
            f"以下是一份扫描文档的 OCR 识别结果，请生成简洁的中文摘要，"
            f"并提取关键信息（日期、金额、人名、机构名等）：\n\n{ocr_text[:3000]}"
        )
        result = await bot.run(summary_prompt, session_key="ocr-summary")
        print("=== 文档摘要 ===")
        print(result.content)

        summary_path = os.path.join(output_dir, "summary.txt")
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write(result.content)
        print(f"\n[保存] 摘要 → {summary_path}")

        question = "文档的第 3 页主要讲了什么内容？"
        qa_prompt = (
            f"以下是文档的 OCR 文本（含页码标记）：\n\n{ocr_text}\n\n"
            f"请回答：{question}"
        )
        answer = await bot.run(qa_prompt, session_key="ocr-qa")
        print(f"\n=== 问答 ===\n问：{question}\n答：{answer.content}")

    return txt_path, json_path, summary_path


if __name__ == "__main__":
    asyncio.run(process_with_nanobot('./智能体开发实战_课程实验任务书_27题版_修订稿.pdf'))