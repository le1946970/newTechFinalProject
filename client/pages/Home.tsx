import React, { useState, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { toast, ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

function First() {
  const navigate = useNavigate();
  const [file, setFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState<boolean>(false); // Tracks upload loading state
  const fileInputRef = useRef<HTMLInputElement | null>(null); // Ref to the file input

  // Notify the user using Toastify
  const showToast = (message: string, type: "success" | "error") => {
    const options = {
      position: "top-right" as const,
      autoClose: 3000,
      theme: "colored",
    };

    if (type === "success") {
      toast.success(message, options);
    } else {
      toast.error(message, options);
    }
  };

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files.length > 0) {
      setFile(event.target.files[0]);
    }
  };

  const handleFileUpload = async () => {
    if (!file) {
      showToast("Please select a CSV file first!", "error");
      return;
    }

    setIsUploading(true); // Set uploading state
    const reader = new FileReader();

    reader.onload = async (event) => {
      const fileData = event.target?.result;
      if (!fileData || typeof fileData !== "string") {
        setIsUploading(false); // Reset state in case of error
        return;
      }

      const payload = {
        fileData: fileData.split(",")[1], // Remove the Base64 prefix
        fileName: file.name,
      };

      try {
        const response = await fetch("/api/upload", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(payload),
        });

        if (response.ok) {
          showToast("File uploaded and processed successfully!", "success");
          setFile(null); // Clear the file state after successful upload

          // Reset the file input field
          if (fileInputRef.current) {
            fileInputRef.current.value = ""; // Clear the input field
          }
        } else {
          showToast("Failed to upload file.", "error");
        }
      } catch (error) {
        console.error("Error uploading file:", error);
        showToast("Error uploading file.", "error");
      } finally {
        setIsUploading(false); // Reset uploading state
      }
    };

    reader.readAsDataURL(file);
  };

  return (
    <div className="container text-center">
      {/* Toastify container */}
      <ToastContainer />

      <div className="row">
        <div className="text-center">
          <img src={"../footflow1.png"} alt="logo" className="img-fluid" />
        </div>
      </div>
      <div className="row font-italic">
        <div className="text-center">
          <h5>
            "Footflow" creates easy-to-read graphs that give you a clear picture
            of your store's foot traffic. Using modern tools, we turn data into
            insights that help you make smarter decisions. Let us simplify your
            data with effective, straightforward visuals.
          </h5>
          <button
            type="button"
            className="btn btn-danger mt-4"
            onClick={() => navigate("/graphs")}
          >
            Explore Data
          </button>
          <br />
          <br />
          <div className="mb-3">
            <label htmlFor="formFile" className="form-label">Import new invoices' data!</label>
            <input className="form-control" type="file" id="formFile" accept=".csv" onChange={handleFileChange} ref={fileInputRef} />
          </div>
          <button
            type="button"
            className={`btn btn-custom-darker-gray mt-4 ${isUploading ? "disabled" : ""}`}
            onClick={handleFileUpload}
            disabled={isUploading}
          >
            {isUploading ? (
              <span
                className="spinner-border spinner-border-sm"
                role="status"
                aria-hidden="true"
              ></span>
            ) : (
              "Upload CSV"
            )}
          </button>


          <br />
        </div>
      </div>
    </div>
  );
}

export default First;
