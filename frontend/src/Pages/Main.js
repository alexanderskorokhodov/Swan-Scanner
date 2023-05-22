import SearchBar from "../Components/SearchBar";
import Swan from "../Components/Swan";
import SwanResult from "../Components/SwanResult";
import "../styles/Main.scss";
import React, { useEffect, useState } from "react";
import Service from "../Service";
import { useForm } from "react-hook-form";
import axios from "axios";

import FileBase64 from 'react-file-base64';
// import info from 'database.json';

const sorting = {'дата': 'date', 'избранное': 'highlighted', 'результат': 'process'}

function Main() {

  const [search, setSearch] = useState('')

  const service = new Service()
  const [chosenId, setChosenId] = useState(1);

  function handleClick(id_) {
    setChosenId(id_.toString());
    setSwansUI(swansUpdate(id_.toString()))
  }


  useEffect(()=>{
    service.load_data().then((res)=>{setSwans(JSON.parse(res.data[0]))})
  }, [])

  

  const [sort, setSort] = useState('результат')

  
  // Functions to preview multiple images
  const handleFileChange = async (files) => {
    if (files) {
      console.log()
      let index_ =  Object.keys(swans).length !== 0 ? Number(Object.keys(swans).reduce((a, b) => Number(a) > Number(b) ? a : b)) + 1 : 0
      
      for (let index = 0; index < files.length; index++) {
        const base64 = files[index];
        console.log(base64)
        await service.sendImage(index_ + index, base64.base64, base64.name).then(response=>{console.log(response)});
        console.log(index_, index,index_+index)
        };

      }
    }
  ;
  const [swans, setSwans] = useState({});
  function swansUpdate(chosen) {
    console.log(sort, 'UI update')
    let b = [];
    var items = Object.keys(swans).map(function(key) {
      return [key, swans[key]];
    });
    let sorts = sorting[sort]
    // Sort the array based on the second element
    items.sort(function(first, second) {
      if (sorts === 'date'){
        // let [time1, time2]  = [Number(first[1][sorts].slice(-5, -3)) * 12 + Number(first[1][sorts].slice(-2)),  Number(second[1][sorts].slice(-5, -3)) * 12 + Number(first[1][sorts].slice(-2))]
        let [d1, d2] = [Number(first[1][sorts].slice(0, 3)), Number(second[1][sorts].slice(0, 3))]
        let [m1, m2] = [Number(first[1][sorts].slice(4, 6)), Number(second[1][sorts].slice(4, 6))]
        let [y1, y2] = [Number(first[1][sorts].slice(7, 11)), Number(second[1][sorts].slice(7, 11))]
        let [fi, se] = [y1 * 365 * 24 + m1 * 30 * 24 + d1 * 24 , y2 * 365 * 24 + m2 * 30 * 24 + d2 * 24 ]
        return -se + fi
      }
      return second[1][sorts] - first[1][sorts];
    });
    console.log(items)
    for (let index = 0; index < items.length; index++) {
      const element = items[index];
      // if (element[1]['notes'].includes(search) ){
        b.push(
          <Swan
            chosen={chosen ? chosen : chosenId}
            data={element[1]}
            setChosen={handleClick}
            id_={element[0]}
            service={service}
          />)
        // );}
    }
    console.log(b)
    return <div className="swanDataset">{b}</div>;
  }
  const [swansUI, setSwansUI] = useState(swansUpdate(''));
  console.log(sort)
  useEffect(
    () => {
      setSwansUI(swansUpdate(''))
    },
    [chosenId, 
    sort, search,  swans]
  );
  return (
    <div className="app">
      <div className="bar">
        {/* <p className="putoshka">Putoshka: Swan Scanner</p> */}
        <p className="putoshka">Обработанные фото</p>
      </div>
      <div className="main">
        <div className="left">
          {/* <p className='title'>Обработанные фото</p> */}
          <SearchBar setSearch={setSearch} setSort={setSort} />
          {swansUI}
        </div>
        <div className="right">
          <SwanResult data={swans[chosenId.toString()]} id_={chosenId} service={service}/>
          <label class="input-file">
            <FileBase64 multiple={true} onDone={(files)=>handleFileChange(files)} onChange={(e) => e.target.files} />
        
	   	      <span>Добавить фотографии</span>
 	        </label>
          </div>
      </div>
    </div>
  );
}

export default Main;
