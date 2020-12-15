import zipfile
import os


def create_zip(folder, zipfile_temp):
    '''
    Function purpose: create a zip file
    Input: filepath
    Source: https://thispointer.com/python-how-to-create-a-zip-archive-from-multiple-files-or-directory/
    '''
    with zipfile.ZipFile(zipfile_temp, "w") as zipObj:
        # Iterate over all the files in directory
        for folderName, subfolders, filenames in os.walk(folder):
            for filename in filenames:
                # create complete filepath of file in directory
                file_root = os.path.abspath(folderName)
                filePath = os.path.join(file_root, filename)
                zipObj.write(filePath)


def parse_coordinates(result):
    bboxStr = result[result.find("[") + 1:result.find("]")]
    bboxList = [float(i) for i in bboxStr.split(',')]
    return bboxList
