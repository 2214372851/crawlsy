from pathlib import Path

import chardet
import mimetypes


def is_text_file_mimetypes(file_path: Path):
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type is not None and mime_type.startswith('text')


def is_text_file_chardet(file_path: Path):
    try:
        with file_path.open('rb') as f:
            raw_data = f.read(1024)  # 读取前1024个字节
            result = chardet.detect(raw_data)
            encoding = result['encoding']
            confidence = result['confidence']
            # 如果检测到的编码置信度高于某个阈值，认为是文本文件
            return confidence > 0.9 and encoding is not None
    except Exception as e:
        print(f"Error: {e}")
        return False


def is_text_file(file_path: Path):
    return is_text_file_mimetypes(file_path) or is_text_file_chardet(file_path)


def is_valid_filename(filename: str):
    return bool(filename) and not any(c in filename for c in '\\/:*?"<>|')
