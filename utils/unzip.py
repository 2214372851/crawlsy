import zipfile
from pathlib import Path
import logging

logger = logging.getLogger('django')


def zip(file_path: str | Path, zip_filename: str = None):
    """
    压缩文件或文件夹
    :param zip_filename:
    :param file_path:
    :return:
    """
    if not zip_filename:
        zip_filename = file_path + '.zip'
    with zipfile.ZipFile(zip_filename, 'w') as zip_obj:
        path = Path(file_path)
        if path.is_file():
            zip_obj.write(path, arcname=path.relative_to(path.parent))
        else:
            for i in path.rglob('*'):
                zip_obj.write(i, arcname=i.relative_to(path))
    return zip_filename


def support_gbk(zip_file: zipfile.ZipFile):
    name_to_info = zip_file.NameToInfo
    # copy map first
    for name, info in name_to_info.copy().items():

        try:
            real_name = name.encode('cp437').decode('gbk')  # zipfile默认使用的是cp437解码,而windows默认使用gbk；则先用cp437编码，再用gbk解码
        except:
            logger.error(f'support_gbk error: {name}', exc_info=True)
        if real_name != name:
            info.filename = real_name
            del name_to_info[name]
            name_to_info[real_name] = info
    return zip_file


def unzip(zip_filename: str | Path, unzip_path: str = None):
    zip_filename = Path(zip_filename)
    if not zip_filename.exists():
        logger.error(f'The file does not exist: {zip_filename}')
        return
    if not unzip_path:
        unzip_path = zip_filename.parent / zip_filename.stem
    with support_gbk(zipfile.ZipFile(zip_filename, "r")) as zip_obj:
        zip_obj.extractall(path=unzip_path)
