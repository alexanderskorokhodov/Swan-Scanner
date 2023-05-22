//styles
import "./styles/App.scss";
// import "./styles/themes.scss";

import React from "react";
// import useColorScheme from "./scripts/useColorScheme";

// components
// import Footer from "./components/Footer";

// pages
import Main from "./Pages/Main";

// router
import { BrowserRouter, Route, Routes } from "react-router-dom";


function App() {

  // theme references
  // const isDark = useColorScheme('dark');
  // const theme = isDark ? 'dark' : 'light';

  return (
    <div className={`App`}>
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<Main/>} />
          </Routes>
        </BrowserRouter>
    </div>
  );
}

export default App;
