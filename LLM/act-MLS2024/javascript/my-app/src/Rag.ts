import { TextLoader } from "langchain/document_loaders/fs/text";

import { PDFLoader } from "langchain/document_loaders/fs/pdf";
// Or, in web environments:
// import { WebPDFLoader } from "langchain/document_loaders/web/pdf";
// const blob = new Blob(); // e.g. from a file input
// const loader = new WebPDFLoader(blob);

import { ChatOpenAI, OpenAIEmbeddings } from "@langchain/openai";
import { pull } from "langchain/hub";
import { createRetrievalChain } from "langchain/chains/retrieval";
import { createStuffDocumentsChain } from "langchain/chains/combine_documents";

//import { RetrievalQAChain, loadQAStuffChain } from "langchain/chains";
import { CharacterTextSplitter } from "langchain/text_splitter";
//import { RecursiveCharacterTextSplitter } from "langchain/text_splitter";
//import { HNSWLib } from "@langchain/community/vectorstores/hnswlib";
import { Chroma } from "@langchain/community/vectorstores/chroma";

import {
  ChatPromptTemplate,
  MessagesPlaceholder,
  PromptTemplate,
  SystemMessagePromptTemplate,
  AIMessagePromptTemplate,
  HumanMessagePromptTemplate,
} from "@langchain/core/prompts";
import {
  AIMessage,
  HumanMessage,
  SystemMessage,
} from "@langchain/core/messages";


export const run = async () => {

const textBook = '/home/kazuyoshi/MEGAsync/ebooks/Actuary-ebook/hoken1-ch1.txt';
const pdfBook = '/home/kazuyoshi/MEGAsync/ebooks/Actuary-ebook/hoken1-ch1.pdf';
//const book = '/home/kazuyoshi/MEGAsync/ebooks/Actuary-ebook/保険1（生命保険） 日本アクチュアリー会.pdf';

const retrievalQuery = "営業保険料に関わる要素を抽出してください。";
const  qaQuery = "営業保険料に関わる要素を1つ選択して100字程度に要約してください。";

//const loader = new PDFloader("/home/kazuyoshi/MEGAsync/ebooks/Actuary-ebook/保険1（生命保険） 日本アクチュアリー会.pdf");

const loader = new TextLoader(textBook);
//const loader = new PDFLoader(pdfBook);
const pages = await loader.load();
const docs = await new CharacterTextSplitter({
      chunkSize: 5000,
      chunkOverlap: 0,
      }).splitDocuments(pages);

console.log("#docs =  ", docs.length);

const embeddings = new OpenAIEmbeddings();
const dbConfig = {
  collectionName: "a-test-collection",
  url: "http://localhost:8000", // Optional, will default to this value
  collectionMetadata: {
    "hnsw:space": "cosine",
  }, // Optional, can be used to specify the distance method of the embedding space https://docs.trychroma.com/usage-guide#changing-the-distance-function
};
const vectorStore = await Chroma.fromDocuments(docs, embeddings,dbConfig);
const retriever = await vectorStore.asRetriever();
const contextDocs = await retriever.getRelevantDocuments(retrievalQuery);
console.log("length = ", contextDocs.length);
for (let i = 0; i < contextDocs.length; i++){
    const currentDoc = contextDocs[i];
    console.log("i= ", i);
    console.log("metadata = ", currentDoc.metadata);
//    console.log(currentDoc.pageContent);
    }

console.log("*** initialize & execute QA chain  ***");

const retrievalQAChatPrompt = await pull("langchain-ai/retrieval-qa-chat");
const llm = new ChatOpenAI({modelName: "gpt-4-1106-preview"});
//const historyAwareCombineDocsChain = await createStuffDocumentsChain({
const combineDocsChain = await createStuffDocumentsChain({
      llm: llm,
      prompt: ChatPromptTemplate.fromMessages([
    [
      "system",
      `Answer the user's questions based on the below context. When it makes sense, provide a link to the source in markdown format.
      
      Context:
      
      {context}`,
    ],
    new MessagesPlaceholder("chat_history"),
    ["user", "{input}"],
  ]),
});

const retrievalChain = await createRetrievalChain({
  retriever,
  combineDocsChain,
});
const response = await retrievalChain.invoke({ input: qaQuery });
console.log(response.answer);
};
run();

// // 環境変数
// require("dotenv").config();



