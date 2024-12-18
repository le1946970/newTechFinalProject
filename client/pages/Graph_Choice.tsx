import { toast } from "react-toastify";
import { useNavigate } from "react-router-dom";
import { useState } from "react";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";

function Graph_Choice() {
    const navigate = useNavigate();
    const [loadingGraph, setLoadingGraph] = useState<number | null>(null); // Tracks which graph is loading
    const [selectedDate, setSelectedDate] = useState<Date | null>(null); // Explicitly typed as Date or null
    const today = new Date(); // Get the current date

    const handleBack = () => {
        navigate("/home");
    };

    async function handleGraph(graphNumber: number) {
        setLoadingGraph(graphNumber); // Set loading state for the specific graph
        const url = `/graph${graphNumber}`;
        try {
            const response = await fetch(url);
            const blobed = await response.blob();

            const reader = new FileReader();
            reader.onloadend = () => {
                const base64String = reader.result as string;
                localStorage.setItem("source", `/graph${graphNumber}`);
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

    async function handleGraph1() {
        if (!selectedDate) {
            toast.error("No date selected");
            return;
        }

        await httpReq(selectedDate);
    }

    async function httpReq(date: Date){
        setLoadingGraph(1); // Set loading state for the specific graph
        const formattedDate = date.toISOString().split("T")[0]; // Extract yy-MM-dd
        const url = `/graph1?date=${formattedDate}`; // Use the formatted date
        try {
            const response = await fetch(url);

            console.log('response: ', response)
            if (response.status == 400){
                console.log("No datee")
                toast.error("No date selectedd")
                return
            }

            const blobed = await response.blob();

            const reader = new FileReader();
            reader.onloadend = () => {
                const base64String = reader.result as string;
                localStorage.setItem("source", `/graph${1}`);
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
                            {/* Date Picker */}
                            <div className="row mb-4">
                                <div className="col-md-12 text-center">
                                    <label htmlFor="datePicker" className="form-label">Select a Date:</label>
                                    <DatePicker
                                        selected={selectedDate}
                                        onChange={(date: Date | null) => setSelectedDate(date)}
                                        dateFormat="yyyy-MM-dd"
                                        maxDate={today} // Prevent future dates
                                        className="form-control"
                                        placeholderText="Click to select a date"
                                    />
                                </div>
                            </div>
                            <button
                                className={`btn btn-danger text-center ${loadingGraph === 1 ? "disabled" : ""}`}
                                onClick={() => handleGraph1()}
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
                        <h2 className="card-text text-center">Most Popular Items Sold on average</h2>
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
                                    "Select Graph (overall average)"
                                )}
                            </button>
                            <button
                                className={`btn btn-danger text-center ${loadingGraph === 6 ? "disabled" : ""}`}
                                onClick={() => handleGraph(6)}
                                disabled={loadingGraph === 6}
                            >
                                {loadingGraph === 6 ? (
                                    <span className="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                                ) : (
                                    "Select Graph (average per day of the week)"
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
