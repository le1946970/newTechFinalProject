//import React from 'react'
import { toast } from "react-toastify";
import { useNavigate } from "react-router-dom";
import { useState } from "react";

function Graph_Choice() {
    const navigate = useNavigate();
    const [loadingGraph, setLoadingGraph] = useState<number | null>(null); // Tracks which graph is loading

    const handleBack = () => {
        navigate("/home");
    };

    async function handleGraph(graphNumber: number) {
        setLoadingGraph(graphNumber); // Set loading state for the specific graph
        const url = `/graph${graphNumber}`;
        try {
            const response = await fetch(url);
            console.log('response: ', response);

            const blobed = await response.blob();
            console.log('blobed: ', blobed);

            const reader = new FileReader();
            reader.onloadend = () => {
                const base64String = reader.result as string;
                localStorage.setItem("source", `/graph${graphNumber}`)
                localStorage.setItem("image", base64String);
                navigate("/display_graph");
            };

            reader.readAsDataURL(blobed);
        } catch (err) {
            console.log(err);
            toast.error("Server error");
        } finally {
            setLoadingGraph(null); // Reset loading state
        }
    }

    async function handleGraph1(graphNumber: number) {
        setLoadingGraph(graphNumber); // Set loading state for the specific graph
        const url = `/graph1Choice`;
        try {
            const response = await fetch(url);
            console.log('response: ', response);

            const blobed = await response.blob();
            console.log('blobed: ', blobed);

            const reader = new FileReader();
            reader.onloadend = () => {
                const base64String = reader.result as string;
                localStorage.setItem("source", `/graph${graphNumber}`)
                localStorage.setItem("image", base64String);
                navigate("/display_graph");
            };

            reader.readAsDataURL(blobed);
        } catch (err) {
            console.log(err);
            toast.error("Server error");
        } finally {
            setLoadingGraph(null); // Reset loading state
        }
    }

    return (
        <div className="container">
            <div className="row">
                <div className="col-md-6"></div>
                <div className="col-md-6 d-flex justify-content-end align-items-center">
                    <button type="button" className="btn btn-danger mt-2" onClick={handleBack}>Back</button>
                </div>
            </div>
            <h2 className='text-center mt-2'>Possible Graphs to be Generated</h2>
            <h5 className='text-center mb-3'>Pick one of the following graphs and our team will generate them for you</h5>
            {/* Graph Options */}
            <div className="row">
                {/* Graph 1 */}
                <div className="col-md-6">
                    <div className="card">
                        <h2 className="card-text text-center">Foottraffic vs Sales</h2>
                        <img src={"../sample_graphs/graph1.png"} className="card-img-top" alt="Line Graph Example" />
                        <div className="card-body d-grid gap-2">
                            {/* Dropdown */}
                            <select
                                className="form-select mb-3"
                                aria-label="Select a month"
                                onChange={(e) => console.log(`Selected month: ${e.target.value}`)}
                            >
                                <option value="" selected disabled>Pick a Month</option>
                                <option value="January">January</option>
                                <option value="February">February</option>
                                <option value="March">March</option>
                                <option value="April">April</option>
                                <option value="May">May</option>
                                <option value="June">June</option>
                                <option value="July">July</option>
                                <option value="August">August</option>
                                <option value="September">September</option>
                                <option value="October">October</option>
                                <option value="November">November</option>
                                <option value="December">December</option>
                            </select>
                            {/* Graph selection */}
                            <button
                                className={`btn btn-danger text-center ${loadingGraph === 1 ? "disabled" : ""}`}
                                onClick={() => handleGraph1(1)}
                                disabled={loadingGraph === 1}
                            >
                                {loadingGraph === 1 ? (
                                    <span className="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                                ) : (
                                    "Select Graph"
                                )}
                            </button>
                        </div>
                    </div>
                </div>
                {/* Graph 2 */}
                <div className="col-md-6">
                    <div className="card">
                        <h2 className="card-text text-center">Most Popular Payment Method</h2>
                        <img src={"../sample_graphs/graph2.png"} className="card-img-top" alt="Pie Graph Example" />
                        <div className="card-body d-grid gap-2">
                            <button
                                className={`btn btn-danger text-center ${loadingGraph === 2 ? "disabled" : ""}`}
                                onClick={() => handleGraph(2)}
                                disabled={loadingGraph === 2}
                            >
                                {loadingGraph === 2 ? (
                                    <span className="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                                ) : (
                                    "Select Graph"
                                )}
                            </button>
                            <button
                                className={`rainbow-button ${loadingGraph === 5 ? "disabled" : ""}`}
                                onClick={() => handleGraph(5)}
                                disabled={loadingGraph === 5}
                            >
                                {loadingGraph === 5 ? (
                                    <span className="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                                ) : (
                                    "Select *Special* Graph"
                                )}
                            </button>

                        </div>
                    </div>
                </div>
            </div>
            <div className="row">
                {/* Graph 3 */}
                <div className="col-md-6">
                    <div className="card">
                        <h2 className="card-text text-center">Most Popular Items Sold</h2>
                        <img src={"../sample_graphs/graph3.png"} className="card-img-top" alt="Line Graph Example" />
                        <div className="card-body d-grid gap-2">
                            <button
                                className={`btn btn-danger text-center ${loadingGraph === 3 ? "disabled" : ""}`}
                                onClick={() => handleGraph(3)}
                                disabled={loadingGraph === 3}
                            >
                                {loadingGraph === 3 ? (
                                    <span className="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                                ) : (
                                    "Select Graph"
                                )}
                            </button>
                        </div>
                    </div>
                </div>
                {/* Graph 4 */}
                <div className="col-md-6">
                    <div className="card">
                        <h2 className="card-text text-center">Average Quantity of Items Bought per Order</h2>
                        <img src={"../sample_graphs/graph4.png"} className="card-img-top" alt="Pie Graph Example" />
                        <div className="card-body d-grid gap-2">
                            <button
                                className={`btn btn-danger text-center ${loadingGraph === 4 ? "disabled" : ""}`}
                                onClick={() => handleGraph(4)}
                                disabled={loadingGraph === 4}
                            >
                                {loadingGraph === 4 ? (
                                    <span className="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                                ) : (
                                    "Select Graph"
                                )}
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Graph_Choice;
