from pypdf import PdfReader

### langchain.document_loaders PyPDFLoader Advanced encoding /90ms-RKSJ-H not implemented yet
### pypdf; Advanced encoding /90ms-RKSJ-H, /90ms-RKSJ-V not implemented yet
### pypdf が /90ms-RKSJ-H, /90ms-RKSJ-V に対応していないので、難しい
### 仕方ないので、pdftotext でテキストファイルにしてやってみたら、一応動いた

#reader= PdfReader('/home/kazu/Books/Actuary-ebook/hoken1-ch1.pdf')
reader= PdfReader('/home/kazu/Books/Actuary-ebook/hoken1-ch1-uncomp.txt')
number_of_pages = len(reader.pages)
page = reader.pages[0]
text = page.extract_text()

print('#pages:', number_of_pages)
print('page: ', page)
print('text: ', text)
