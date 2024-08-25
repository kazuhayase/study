## https://qiita.com/Isaka-code/items/f45a9a8288710aa807d9

from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma

## メインの処理
if __name__ == "__main__":
    file_path = "path_to_your_pdf_file.pdf"
    retrieval_query = "Exercisesを抽出してください。"
    qa_query = "Exerciseを1題選択し日本語に翻訳してください。"

    # 1. PDFを読み込む
    pages = PyPDFLoader(file_path).load()

    # 2. ドキュメントをチャンクに分割
    docs = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0).split_documents(pages)

    # 3. 埋め込みモデルの初期化
    embeddings = OpenAIEmbeddings()

    # 4. ベクトルストアにドキュメントを格納
    retriever = Chroma.from_documents(docs, embeddings).as_retriever()

    # 5. ドキュメントを抽出
    context_docs = retriever.get_relevant_documents(retrieval_query)
    print(f"len = {len(context_docs)}") # 抽出したドキュメントの数

    first_doc = context_docs[0] # 1つ目のドキュメント
    print(f"metadata = {first_doc.metadata}") # 1つ目のドキュメントのメタデータ
    print(first_doc.page_content) # 1つ目のドキュメントの中身

    # 6. QAチェーンの初期化と実行
    qa_chain =RetrievalQA.from_chain_type(llm=ChatOpenAI(model_name="gpt-4-1106-preview", chain_type="stuff", retriever=retriever))
    result = qa_chain.run(qa_query)
    print(result)

