// import {OpenAI} from "@langchain/openai";
import { ChatOpenAI } from "@langchain/openai";
import { ChatPromptTemplate } from "@langchain/core/prompts";
import { StringOutputParser } from "@langchain/core/output_parsers";

const chatModel = new ChatOpenAI({});
const outputParser = new StringOutputParser();
const prompt = ChatPromptTemplate.fromMessages([
  ["system", "You are a world class technical documentation writer."],
  ["user", "{input}"],
]);
const chain = prompt.pipe(chatModel);

const llmChain = prompt.pipe(chatModel).pipe(outputParser);

export const run = async() =>{
  // const res = await chatModel.invoke("what is LangSmith?");
  const res = await llmChain.invoke({
    input: "what is LangSmith?",
  });
  console.log(JSON.stringify(res, null, 2));
};
	      	
run();		

