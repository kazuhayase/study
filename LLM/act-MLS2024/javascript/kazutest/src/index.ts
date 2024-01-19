// import {OpenAI} from "@langchain/openai";
import { ChatOpenAI } from "@langchain/openai";

const chatModel = new ChatOpenAI({});
export const run = async() =>{
       const res = await chatModel.invoke("what is LangSmith?");
       console.log(JSON.stringify(res, null, 2));
};
	      	
run();		

