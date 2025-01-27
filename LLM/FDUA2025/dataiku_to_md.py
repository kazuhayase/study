# This Python file uses the following encoding: utf-8
import getpass
import os
import json

import pandas as pd
import numpy as np
try:
    from PIL import Image
    from io import BytesIO
    import pytesseract
    import re
    import math
    #import cv2
    import matplotlib.pyplot as plt
    import pymupdf4llm
except Exception as e:
    raise Exception("Be sure to set the right code env. {}".format(e))

from pathlib import Path

def markdown_from_pdf(path):
    #test_file = input_folder.get_path() + input_filenames[test_index]
    test_file = path
    print("Filename: %s" % (test_file))
    md_text = pymupdf4llm.to_markdown(test_file, page_chunks = True)
    cols=['metadata', 'text']
    md_ret=dict()
    for num, body in enumerate(md_text):
        row=dict()
        for col in cols:
            row[col] = body[col]
        md_ret[num] = row
    return md_ret

# load prompty as langchain ChatPromptTemplate
# Important Note: Langchain only support mustache templating. Add 
#  template: mustache
# to your prompty and use mustache syntax.
md=dict()
folder = Path(__file__).parent.absolute().as_posix()
#print(folder)
#test_pdf = folder + "/documents/documents/6.pdf"
pathlist = Path(folder).glob('documents/documents/*.pdf')
for path in pathlist:
    # because path is object not string
    path_in_str = path.as_posix()
    print(path_in_str)
    md[path_in_str] = markdown_from_pdf(path_in_str)
    print(md[path_in_str][0])  # 最初のページを表示


pd.DataFrame(md)