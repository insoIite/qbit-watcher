

def parse_file(file_to_download):
    # file_to_download = "folder1/folder2/myfile.ext"
    file_split = file_to_download.split('/')
    # retrieve filename
    file_name = file_split[-1]
    # remove file_name
    file_split.pop()
    file_path = '/'.join(file_split)
    return (file_path, file_name)

def get_size_format(x, y):
    if int(y/1024/1024) > 0:
        current = x / 1024 / 1024
        total = y / 1024 / 1024
        fsize = "MB"
    elif int(y/1024) > 0:
        current = x / 1024
        total = y / 1024
        fsize = "KB"
    else:
        current = x
        total = y
        fsize = "B"
    return (current, total, fsize)
