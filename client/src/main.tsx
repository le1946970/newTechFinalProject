// import React from 'react'
import * as ReactDOM from 'react-dom/client';  // Correct import for React 18 and later
import App from './App';  // No '.tsx' extension needed
import './index.css';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import Graph_Choice from "../pages/Graph_Choice";  // No '.tsx' extension needed
import Home from "../pages/Home";  // No '.tsx' extension needed
import Display_Graph from "../pages/Display_Graph";  // No '.tsx' extension needed

ReactDOM.createRoot(document.getElementById('root')!).render(
  <BrowserRouter>
    <Routes>
      <Route index element={<App />} />
      <Route path="/graphs" element={<Graph_Choice />} />
      <Route path="/home" element={<Home />} />
      <Route path="/display_graph" element={<Display_Graph />} />
    </Routes>
  </BrowserRouter>
);
