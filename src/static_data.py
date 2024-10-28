import os
import shutil


def copyContent(src, dest):
    if not os.path.exists(src):
        raise ReferenceError("Invalid path")
    
    if not os.path.exists(dest):
        os.mkdir(dest)


    for content in os.listdir(src):
        content_path = os.path.join(src, content)
        dest_path = os.path.join(dest, content)
    
        if os.path.isdir(content_path):
            copyContent(content_path, dest_path)
        
        else:
            shutil.copy2(content_path, dest_path)
    

def deleteContent(dest):
    if os.path.exists(dest):
        for content in os.listdir(dest):
            content_path = os.path.join(dest, content)
            if os.path.isfile(content_path) or os.path.islink(content_path):
                os.unlink(content_path)
            
            elif os.path.isdir(content_path):
                shutil.rmtree(content_path)

    




    