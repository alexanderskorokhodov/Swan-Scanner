import React, {useState, useEffect} from "react";
import FilledStar from "./FilledStar";
import NotFilledStar from "./NotFilledStar";

function SwanResult({data, service, id_}){
    
    const [featured, setFeatured] = useState(data ? data['highlighted'] : false)
    console.log(data)

    return <div className="scanner">
    <div className="imgFrame">
      <img className="leb" src={data ? "Images/"+data['image_id']+'.jpeg' : ""}/>
    </div>
    <div className="scanInformation">
      <div className="row">
        <div className="imgNaming">
          <div className="swansCount">
            <p className="swansCountElement">Шипуны {data ? data['shipuns_count'] : '-'}</p>
            <p className="swansCountElement">Кликуны {data ? data['clikuns_count'] : '-'}</p>
            <p className="swansCountElement">Малые {data ? data['small_count'] : '-'}</p>
          </div>
          <p className="swanTitle">{data ? data['image_id']+'.jpeg' : '-'}</p>
        </div>
        <div className="featured">
            <div className="star" onClick={()=>{service.highlightImage(data['id']);setFeatured(!featured);}}>
                {data ? (featured ? <FilledStar/> : <NotFilledStar/>): ''}
            </div>
        </div>
      </div>
      <div className="row">
        <div className="date">
          <p className="element">{data ? data['date'] : '-'}</p>
        </div>
        <div className="result">
          <p className="element">распознано: {data ? data['swans_count'] : '-'} не распознано: {data ? data['unrecognized_count']: '-'}</p>
        </div>
      </div>
      <div className="notes">
        {data !== undefined ? <textarea placeholder="Добавить заметку" defaultValue={data['notes']} onChange={(e)=>{service.rewriteNote(data['image_id'], e.target.value)}}></textarea>: <></>}
      </div>
    </div>
  </div>
}

export default SwanResult;