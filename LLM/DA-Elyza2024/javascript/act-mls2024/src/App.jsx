import React from "react";
import Select from 'react-select';
import axios from "axios";

function App() {
    const [data, setData] = React.useState('');
    const [query, setQuery] = React.useState(false);
    //const [kw, setKw] = React.useState('営業保険料');
    //onst [txt, setTxt] = React.useState('hoken1_seiho');
    const [kw, setKw] = React.useState('PMO');
    const [txt, setTxt] = React.useState('digital_agency_standard_guidelines');
    const kamoku=[
	{value: 'digital_agency_standard_guidelines', label: 'デジタル社会推進標準ガイドライン'},
	{value: 'hoken1_seiho', label: '保険1(生命保険)'},
	{value: 'hoken2_seiho', label: '保険2(生命保険)'},
	{value: 'sonpo', label: '損保'},
	{value: 'nenkin', label: '年金'},
    ]
    //const url = "http://localhost:8000/kw/" ; #batting with HTTP Toolkit
    const url = "http://localhost:9000/kw/" ;
    
    const changeKw = (e) => {
	setKw(e.target.value);
    }

    const changeTxt = (e) => {
	setTxt(e.value);
    }

    const ClearData = () => {
	setQuery(false);
	setData('');
	GetData()
    }
    const GetData = () => {
	if (kw && txt) {
	    setQuery(true);
	    axios.get(url+'?kw='+kw+'&txt='+txt).then((res) => {
		setData(res.data);
	    });
	}
    };
    
    return (
      <div>
	  <div>
	      <h1>Digital Agency Elyza Platform RAG test page </h1> 
	      <h2> デジタル社会推進標準ガイドライン等の教科書PDFを参照し100字程度で要約する </h2>
	  </div>
	  <label>
	      参照する教科書を選択し、要約したい言葉（例; PMO) {query ? '' : 'を入力しボタンを押して下さい。'}<br />

	      教科書
	      <Select placeholder="デジタル社会推進標準ガイドライン"
		      onChange={changeTxt} options={kamoku} 
	      />
	      
	      <form onSubmit={(e) => {e.preventDefault(); GetData()}}>
		  <input type="text" placeholder="PMO" value={kw}
			 onChange={changeKw}
		  />
	      </form>
	  </label>
	  {data ?  <div>  {data.a} <br /> <button onClick={ClearData}> 次の質問をする </button></div> : 
	   query ? <div> LLMと会話中 <img id="loadingImage" src="./icon_loader_a_ww_01_s1.gif" alt="loading" /></div> : 
	   <button onClick={GetData}> LLMに聞く </button>
	  }
      </div>
    );
}

export default App;
