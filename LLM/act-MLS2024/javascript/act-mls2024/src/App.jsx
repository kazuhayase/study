import React from "react";
import axios from "axios";

function App() {
    const [data, setData] = React.useState('');
    const [query, setQuery] = React.useState(false);
    const [kw, setKw] = React.useState('営業保険料');
    const url = "http://localhost:8000/kw/" ;
    
    const changeKw = (e) => {
	setKw(e.target.value);
    }

    const ClearData = () => {
	setQuery(false);
	setData('');
	setKw('');
    }
    const GetData = () => {
	setQuery(true);
	axios.get(url+kw).then((res) => {
	    setData(res.data);
	});
    };
    
    return (
      <div>
	  <div>
	      <h1>[Actuary] Moon Light Seminar 2024 LLM </h1> 
	      <h2>生保1教科書を参照し100字程度で要約する </h2>
	  </div>
	  <label>
	      要約したい言葉（例; 営業保険料) {query ? '' : 'を入力しボタンを押して下さい'}<br />
	      <form onSubmit={(e) => {e.preventDefault(); GetData()}}>
		  <input type="text" placeholder="営業保険料" value={kw}
			 onChange={changeKw}
		  />
	      </form>
	  </label>
	  {data ?  <div>  {data.a} <br /> <button onClick={ClearData}> Clear (次の質問をする) </button></div> : 
	   query ? <div> LLMと会話中 <img id="loadingImage" src="./icon_loader_a_ww_01_s1.gif" alt="loading" /></div> : 
	   <button onClick={GetData}> LLMに聞く </button>
	  }
      </div>
    );
}

export default App;
