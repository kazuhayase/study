"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.run = void 0;
const text_1 = require("langchain/document_loaders/fs/text");
// Or, in web environments:
// import { WebPDFLoader } from "langchain/document_loaders/web/pdf";
// const blob = new Blob(); // e.g. from a file input
// const loader = new WebPDFLoader(blob);
const openai_1 = require("@langchain/openai");
const hub_1 = require("langchain/hub");
const retrieval_1 = require("langchain/chains/retrieval");
const combine_documents_1 = require("langchain/chains/combine_documents");
//import { RetrievalQAChain, loadQAStuffChain } from "langchain/chains";
const text_splitter_1 = require("langchain/text_splitter");
//import { RecursiveCharacterTextSplitter } from "langchain/text_splitter";
//import { HNSWLib } from "@langchain/community/vectorstores/hnswlib";
const chroma_1 = require("@langchain/community/vectorstores/chroma");
const prompts_1 = require("@langchain/core/prompts");
const run = async () => {
    const textBook = '/home/kazuyoshi/MEGAsync/ebooks/Actuary-ebook/hoken1-ch1.txt';
    const pdfBook = '/home/kazuyoshi/MEGAsync/ebooks/Actuary-ebook/hoken1-ch1.pdf';
    //const book = '/home/kazuyoshi/MEGAsync/ebooks/Actuary-ebook/保険1（生命保険） 日本アクチュアリー会.pdf';
    const retrievalQuery = "営業保険料に関わる要素を抽出してください。";
    const qaQuery = "営業保険料に関わる要素を1つ選択して100字程度に要約してください。";
    //const loader = new PDFloader("/home/kazuyoshi/MEGAsync/ebooks/Actuary-ebook/保険1（生命保険） 日本アクチュアリー会.pdf");
    const loader = new text_1.TextLoader(textBook);
    //const loader = new PDFLoader(pdfBook);
    const pages = await loader.load();
    const docs = await new text_splitter_1.CharacterTextSplitter({
        chunkSize: 5000,
        chunkOverlap: 0,
    }).splitDocuments(pages);
    console.log("#docs =  ", docs.length);
    const embeddings = new openai_1.OpenAIEmbeddings();
    const dbConfig = {
        collectionName: "a-test-collection",
        url: "http://localhost:8000", // Optional, will default to this value
        collectionMetadata: {
            "hnsw:space": "cosine",
        }, // Optional, can be used to specify the distance method of the embedding space https://docs.trychroma.com/usage-guide#changing-the-distance-function
    };
    const vectorStore = await chroma_1.Chroma.fromDocuments(docs, embeddings, dbConfig);
    const retriever = await vectorStore.asRetriever();
    const contextDocs = await retriever.getRelevantDocuments(retrievalQuery);
    console.log("length = ", contextDocs.length);
    for (let i = 0; i < contextDocs.length; i++) {
        const currentDoc = contextDocs[i];
        console.log("i= ", i);
        console.log("metadata = ", currentDoc.metadata);
        //    console.log(currentDoc.pageContent);
    }
    console.log("*** initialize & execute QA chain  ***");
    const retrievalQAChatPrompt = await (0, hub_1.pull)("langchain-ai/retrieval-qa-chat");
    const llm = new openai_1.ChatOpenAI({ modelName: "gpt-4-1106-preview" });
    //const historyAwareCombineDocsChain = await createStuffDocumentsChain({
    const combineDocsChain = await (0, combine_documents_1.createStuffDocumentsChain)({
        llm: llm,
        prompt: prompts_1.ChatPromptTemplate.fromMessages([
            [
                "system",
                `Answer the user's questions based on the below context. When it makes sense, provide a link to the source in markdown format.
      
      Context:
      
      {context}`,
            ],
            new prompts_1.MessagesPlaceholder("chat_history"),
            ["user", "{input}"],
        ]),
    });
    const retrievalChain = await (0, retrieval_1.createRetrievalChain)({
        retriever,
        combineDocsChain,
    });
    const response = await retrievalChain.invoke({ input: qaQuery });
    console.log(response.answer);
};
exports.run = run;
(0, exports.run)();
// // 環境変数
// require("dotenv").config();
//# sourceMappingURL=index.js.map