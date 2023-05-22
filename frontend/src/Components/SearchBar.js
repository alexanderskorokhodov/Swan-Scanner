import React from "react";

function SearchBar({setSort, setSearch}) {
  return (
    <div className="searchBar">
      <input placeholder="Поиск" className="search" onChange={(e)=>{setSearch(e.target.value)}}/>
      <select className="sort" onChange={(e)=>{setSort(e.target.value)}}>
        
        <option>результат</option>
        <option>дата</option>
        <option>избранное</option>
      </select>
    </div>
  );
}

export default SearchBar;
