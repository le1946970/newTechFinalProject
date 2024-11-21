const fs = require("fs");
const path = require("path");
const { spawn } = require("child_process");

// Function to execute the Python script for data import
async function runImportPythonScript(filePath) {
  const python = spawn("python3", ["./Python_Scripts/import_file.py", filePath]); // Adjust the path to your Python script

  let stdOutput = ""; // Standard output from Python script
  let stdError = "";  // Error output from Python script, if any

  // Capture Python script logs
  python.stdout.on("data", (data) => {
    stdOutput += data.toString();
  });

  python.stderr.on("data", (data) => {
    console.error(`Python script error: ${data}`);
    stdError += data.toString();
  });

  // Return a promise for the script's completion
  return new Promise((resolve, reject) => {
    python.on("close", (code) => {
      if (code === 0) {
        resolve(stdOutput); // Resolve with Python script's output if successful
      } else {
        reject(`Python script failed with code ${code}. Error: ${stdError}`);
      }
    });
  });
}

// Upload File Logic
exports.uploadFile = async (req, res) => {
  try {
    const { fileData, fileName } = req.body;

    if (!fileData || !fileName) {
      return res.status(400).send("No file data or file name provided.");
    }

    // Decode Base64 file data
    const buffer = Buffer.from(fileData, "base64");
    const filePath = path.join(__dirname, "../uploads", fileName);

    // Ensure the uploads directory exists
    if (!fs.existsSync(path.join(__dirname, "../uploads"))) {
      fs.mkdirSync(path.join(__dirname, "../uploads"));
    }

    // Save file temporarily to the server
    fs.writeFileSync(filePath, buffer);

    // Run the Python script
    try {
      const output = await runImportPythonScript(filePath);
      console.log("Python script completed:", output);
      fs.unlinkSync(filePath); // Clean up the temporary file
      res.status(200).send("File processed successfully.");
    } catch (error) {
      console.error("Error executing Python script:", error);
      fs.unlinkSync(filePath); // Clean up the temporary file
      res.status(500).send("Error processing the file.");
    }
  } catch (error) {
    console.error("Unexpected server error:", error);
    res.status(500).send("Server error.");
  }
};
