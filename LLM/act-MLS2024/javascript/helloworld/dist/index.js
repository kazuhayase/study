"use strict";
//let str: string = "Hello World!";
//console.log(str);
Object.defineProperty(exports, "__esModule", { value: true });
exports.run = void 0;
//console.log(global.module);
const llms_1 = require("langchain/llms");
// 環境変数
require("dotenv").config();
const run = async () => {
    // LLMの準備
    const llm = new llms_1.OpenAI({ temperature: 0.9 });
    // LLMの呼び出し
    const res = await llm.call("コンピュータゲームを作る日本語の新会社名をを1つ提案してください");
    console.log(res);
};
exports.run = run;
(0, exports.run)();
//# sourceMappingURL=index.js.map