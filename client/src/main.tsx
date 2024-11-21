//import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import './index.css'
import { BrowserRouter, Route, Routes } from 'react-router-dom'
import Graph_Choice from "../pages/Graph_Choice.tsx"
import Home from "../pages/Home.tsx"
import Display_Graph from "../pages/Display_Graph.tsx"



ReactDOM.createRoot(document.getElementById('root')!).render(
  <BrowserRouter>
    <Routes>
      <Route index element={<App />} />
      <Route path="/graphs" element={<Graph_Choice />} />
      <Route path="/home" element={<Home/>} />
      <Route path="/display_graph" element={<Display_Graph/>} />


    </Routes>
  </BrowserRouter >
)
