import aspose.pdf as pdf

# Get the input file name from the user.
input_file_name = input("Enter the input PDF file name: ")

# Load the input PDF document.
document = pdf.Document(input_file_name)

# Initialize the TeXSaveOptions.
tex_save_options = pdf.TeXSaveOptions()

# Convert the PDF to TEX file.
document.save("output.tex", tex_save_options)

print("Rendering process completed.")


# import pdfplumber
# import pandoc

# # PDF ファイルを読み込みます。
# pdf = pdfplumber.open("pdf_file.pdf")

# # PDF ファイルのテキストを取得します。
# text = pdf.pages[0].extract_text()

# # テキストを LaTeX 形式に変換します。
# latex = pandoc.to_latex(text)

# # LaTeX 形式のテキストを書き出します。
# with open("latex_file.tex", "w") as f:
#     f.write(latex)

    
