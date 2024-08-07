// src/components/Chat.js
import React, { useState, useEffect } from "react";
import io from "socket.io-client";
//import Langchain from "langchain";
import { OpenAI, OpenAIEmbeddings } from "@langchain/openai";
import { RetrievalQAChain, loadQAStuffChain } from "langchain/chains";
import { CharacterTextSplitter } from "langchain/text_splitter";
import { HNSWLib } from "@langchain/community/vectorstores/hnswlib";

const Chat = async() => {
  const [messages, setMessages] = useState([]);
    const [input, setInput] = useState("");


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
    const langchain = new RetrievalQAChain({
  combineDocumentsChain: loadQAStuffChain(model),
  retriever: vectorStore.asRetriever(),
  returnSourceDocuments: true,
});
  const socket = io("http://localhost:3001");
 useEffect(() => {
  socket.on("message", async (msg) => {
    const translatedMessage = await langchain.translate(msg.text, msg.lang);
    setMessages((prevMessages) => [...prevMessages, translatedMessage]);
  });
}, []);

    const sendMessage = async (e) => {
  e.preventDefault();
  if (input) {
    const translatedMessage = await langchain.translate(input, "en");
    socket.emit("message", { text: translatedMessage, lang: "en" });
    setInput("");
  }
};
return (
  <div>
    <ul>
      {messages.map((msg, idx) => (
        <li key={idx}>{msg}</li>
      ))}
    </ul>
    <form onSubmit={sendMessage}>
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
      />
      <button type="submit">Send</button>
    </form>
  </div>
);
}

export default Chat;
//export sendMessage;
    
