const express = require('express');
const app = express();
const morgan = require('morgan');
const path = require('path');
const controller = require('./controllers/graph.controller');
const uploadController = require('./controllers/uploadController'); 
const bodyParser = require("body-parser");
const fs = require('fs');

app.use(morgan('tiny'));
app.use(express.json());
app.use(bodyParser.json({ limit: "50mb" }));
app.use(bodyParser.urlencoded({ limit: "50mb", extended: true }));

// Serve static files (e.g., front-end assets)
app.use("/", express.static(path.join(__dirname, 'dist')));

// Upload route to handle file upload and invoke Python script
app.post("/api/upload", uploadController.uploadFile);

// Graph routes that execute Python scripts for generating graphs
app.get('/graph1', async function(req, res) {
    try {
        const python_output = await controller.run_graph1();
        const imagePath = path.resolve(__dirname, python_output.slice(0, -2));

        // Send the generated image to the client
        await new Promise((resolve, reject) => {
            res.sendFile(imagePath, (err) => {
                if (err) {
                    reject(err);
                } else {
                    resolve();
                }
            });
        });

        // Clean up the generated image after sending it to the client
        fs.unlinkSync(imagePath);
    } catch (e) {
        console.log(e);
        res.send({ 'message': e });
    }
});

app.get('/graph2', async function(req, res) {
    try {
        const python_output = await controller.run_graph2();
        const imagePath = path.resolve(__dirname, python_output.slice(0, -2));

        // Send the generated image to the client
        await new Promise((resolve, reject) => {
            res.sendFile(imagePath, (err) => {
                if (err) {
                    reject(err);
                } else {
                    resolve();
                }
            });
        });

        // Clean up the generated image after sending it to the client
        fs.unlinkSync(imagePath);
    } catch (e) {
        console.log(e);
        res.send({ 'message': e });
    }
});

app.get('/graph5', async function(req, res) {
    try {
        const python_output = await controller.run_graph5();
        const imagePath = path.resolve(__dirname, python_output.slice(0, -2));

        // Send the generated image to the client
        await new Promise((resolve, reject) => {
            res.sendFile(imagePath, (err) => {
                if (err) {
                    reject(err);
                } else {
                    resolve();
                }
            });
        });

        // Clean up the generated image after sending it to the client
        fs.unlinkSync(imagePath);
    } catch (e) {
        console.log(e);
        res.send({ 'message': e });
    }
});

app.get('/graph3', async function(req, res) {
    try {
        const python_output = await controller.run_graph3();
        const imagePath = path.resolve(__dirname, python_output.slice(0, -2));

        // Send the generated image to the client
        await new Promise((resolve, reject) => {
            res.sendFile(imagePath, (err) => {
                if (err) {
                    reject(err);
                } else {
                    resolve();
                }
            });
        });

        // Clean up the generated image after sending it to the client
        fs.unlinkSync(imagePath);
    } catch (e) {
        console.log(e);
        res.send({ 'message': e });
    }
});

app.get('/graph4', async function(req, res) {
    try {
        const python_output = await controller.run_graph4();
        const imagePath = path.resolve(__dirname, python_output.slice(0, -2));

        // Send the generated image to the client
        await new Promise((resolve, reject) => {
            res.sendFile(imagePath, (err) => {
                if (err) {
                    reject(err);
                } else {
                    resolve();
                }
            });
        });

        // Clean up the generated image after sending it to the client
        fs.unlinkSync(imagePath);
    } catch (e) {
        console.log(e);
        res.send({ 'message': e });
    }
});

const port = process.env.PORT || 8080;
app.listen(port, () => {
    console.log("Server listening on port " + port);
});
