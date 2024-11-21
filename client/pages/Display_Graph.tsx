//import React from 'react'

import { useEffect, useState } from "react"
import { useNavigate } from "react-router-dom";

function Display_Graph() {
    const [graph, setGraph] = useState<string | null>('')
    const navigate = useNavigate();

    useEffect(() => {
        const storageImg = localStorage.getItem("image")
        if (storageImg) {
            setGraph(storageImg)
        }
    }, [])

    const handleBack = () => {
        navigate("/graphs");
    }

    const handleDownload = () => {
        if (graph){
            const link = document.createElement('a')
            link.href = graph
            link.download = "graph.png"
            link.click()
        }
    }

    return (
        <div>
            <button onClick={handleBack}>Back</button><br/>
            {graph ? (
                <img src={graph} alt="Saved" style={{width:'1000px'}} />
            ) : (
                <p>No image found</p>
            )}

            <div><button onClick={handleDownload}>Download</button></div>
        </div>
    )
}

export default Display_Graph