import React from "react";
import { useState } from "react";
import FilledStar from "./FilledStar";
import NotFilledStar from "./NotFilledStar";
import "../styles/Swan.scss";

function Swan({ data, chosen, setChosen, id_, service}) {
  console.log(data)
  const [featured, setFeatured] = useState(data? data['highlighted'] : '');
 

  return (
    <div
      key={Number(id_)}
      onClick={()=>{setChosen(id_)}}
      className={
        "swan " + (chosen.toString() === id_.toString() ? "chosen" : "")
      }
    >
      <div className="swanTop">
        <div className="swanLeft">
          <div className="name">{data['image_id']+'.jpeg'}</div>
          {data['process'] === 0 ? (
            <div className="process">
              <p className="processText">Распознано</p>
              <img src="Icons/Ok.svg" />
            </div>
          ) : data['process'] === 1 ? (
            <div className="process">
              <p className="processText">Частично</p>
              <img src="Icons/Normal.svg" />
            </div>
          ) : (
            <div className="process">
              <p className="processText">Не распознано</p>
              <img src="Icons/Not.svg" />
            </div>
          )}
          <div className="date">{data['date']}</div>
        </div>
        <div className="swanRight">
          <div
            className="star"
            onClick={() => {
              service.highlightImage(data['image_id'])
              setFeatured(!featured);
            }}
          >
            {featured ? <FilledStar /> : <NotFilledStar />}
          </div>
          <div className="bin"  onClick={()=>{service.deleteImage(id_)}}>
            <img src="Icons/trash.svg" />
          </div>
        </div>
      </div>
      <div className="swanBottom">
        <div className="swanInfo">Лебеди: {data['swans_count']}</div>
        <div className="swanInfo">Шипуны: {data['shipuns_count']}</div>
        <div className="swanInfo">Кликуны: {data['clikuns_count']}</div>
        <div className="swanInfo">Малые: {data['small_count']}</div>
        <div className="swanInfo">
          Нераспознанные: {data['unrecognized_count']}
        </div>
      </div>
    </div>
  );
}

export default Swan;
