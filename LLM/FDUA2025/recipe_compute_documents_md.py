# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu
#from typing import Dict

try:
    import pymupdf4llm
except Exception as e:
    raise Exception("Be sure to set the right code env. {}".format(e))


# Read recipe inputs
documents = dataiku.Folder("30vSJnnK")
input_filenames = documents.list_paths_in_partition()
documents_info = documents.get_info()


# Compute recipe outputs
# TODO: Write here your actual code that computes the outputs
# NB: DSS supports several kinds of APIs for reading and writing data. Please see doc.

cols=['metadata', 'text', 'tables']

def markdown_from_index(test_index):
    test_file = documents.get_path() + input_filenames[test_index]
    print("Filename: %s" % (test_file))
    md_text = pymupdf4llm.to_markdown(test_file, page_chunks = True)
    md_ret=dict()
    for col in cols:
        md_ret[col]=list()

    for p, body in enumerate(md_text):
        md_ret['page'] = p
        md_ret['filename'] = test_file
        md_ret['index'] = f'{test_file}:{p}'
        for col in cols:
            md_ret[col].append(body[col])
    return md_ret
    
md=dict()
data = dict()
for col in cols:
    data[col]=list()
    
for idx, filename in enumerate(input_filenames):
    #print("Index: %s => Filename: %s" % (idx, filename))
    md[idx] = markdown_from_index(idx)
    for col in cols:
        for page in md[idx][col]:
            data[col].append(page) 
    
documents_md_df = pd.DataFrame(data)

# Write recipe outputs
# Dataset documents_md renamed to documents_md_backup by admin on 2025-01-27 20:45:00
# Dataset documents_md_backup renamed to documents_md by admin on 2025-01-27 20:46:05
documents_md = dataiku.Dataset("documents_md_page")
documents_md.write_with_schema(documents_md_df)
