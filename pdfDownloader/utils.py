
import zipfile

def upzip(file_path,save_path,pwd):
    # 创建文件句柄
    file = zipfile.ZipFile(file_path, 'r')
    # 提取压缩文件中的内容，注意密码必须是bytes格式，path表示提取到哪
    file.extractall(path=save_path, pwd=pwd.encode('utf-8'))
    return True