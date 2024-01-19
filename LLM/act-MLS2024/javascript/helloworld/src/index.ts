//let str: string = "Hello World!";
//console.log(str);

//console.log(global.module);

// //import { OpenAI } from "@langchain/llms";
// import { OpenAI } from "@langchain/openai";

import { PDFLoader } from "langchain/document_loaders/fs/pdf";

import { OpenAI, OpenAIEmbeddings } from "@langchain/openai";
import { RetrievalQAChain, loadQAStuffChain } from "langchain/chains";
import { CharacterTextSplitter } from "langchain/text_splitter";
import { HNSWLib } from "@langchain/community/vectorstores/hnswlib";


export const run = async () => {

const splitter = new CharacterTextSplitter({
  chunkSize: 1536,
  chunkOverlap: 200,
});

const jimDocs = await splitter.createDocuments(
  [`My favorite color is blue.`],
  [],
  {
    chunkHeader: `DOCUMENT NAME: Jim Interview\n\n---\n\n`,
    appendChunkOverlapHeader: true,
  }
);

const pamDocs = await splitter.createDocuments(
  [`My favorite color is red.`],
  [],
  {
    chunkHeader: `DOCUMENT NAME: Pam Interview\n\n---\n\n`,
    appendChunkOverlapHeader: true,
  }
);

const vectorStore = await HNSWLib.fromDocuments(
  jimDocs.concat(pamDocs),
  new OpenAIEmbeddings()
);

const model = new OpenAI({ temperature: 0 });

const chain = new RetrievalQAChain({
  combineDocumentsChain: loadQAStuffChain(model),
  retriever: vectorStore.asRetriever(),
  returnSourceDocuments: true,
});
const res = await chain.call({
  query: "What is Pam's favorite color?",
});

console.log(JSON.stringify(res, null, 2));

};
run();

// // 環境変数
// require("dotenv").config();

// export const run = async () => {
//   // LLMの準備
//   const llm = new OpenAI({ temperature: 0.9 });

//  // // LLMの呼び出し
// //  const res = await llm.call(
// //    "コンピュータゲームを作る日本語の新会社名をを1つ提案してください"
// //  );
// //  console.log(res);


// //const loader = new PDFLoader("src/document_loaders/example_data/example.pdf", {
// const loader = new PDFLoader("/home/kazu/Books/Actuary-ebook/hoken1-ch1.pdf",{
//   splitPages: false,
// });

// const docs = await loader.load();


// };
// run();
