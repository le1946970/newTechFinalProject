const {spawn} = require('child_process');

// This is probably the worst code I wrote in a while but I don't care, I gotta be done in a few hours.

// run the python script and return the std output, if there are no errors.
async function run_graph1() {
    // executing the python script
    const python = await spawn('python3', ['./Python_Scripts/graph1.py']); // execute the python script
    
    let std = ''; // the script's STD output
    let stderr = ''; // the scipt's error output, if there is any.

    // gets the scripts logs
    python.stdout.on('data', function(data) {
        std += data.toString();
    });

    python.stderr.on('data', (data) => {
        stderr += data.toString();
    });

    // return a promise of the python logs, or an error if the python code can't execute properly.
    return new Promise((resolve, reject) => {
        python.on('close', (code) => {
            if (code === 0) {
                resolve(std);
            } else {
                reject('Error while running python code. console output: ' + stderr);
            }
        });
    });
}

async function run_graph2(){
    // executing the python script
    const python = await spawn('python3', ['./Python_Scripts/graph2.py']); // execute the python script
    
    let std = ''; // the script's STD output
    let stderr = ''; // the script's error output, if there are any

    // gets the scripts logs
    python.stdout.on('data', function(data) {
        std += data.toString();
    });

    python.stderr.on('data', (data) => {
        stderr += data.toString();
    });

    // return a promise of the python logs, or an error if the python code can't execute properly.
    return new Promise((resolve, reject) => {
        python.on('close', (code) => {
            if (code === 0) {
                resolve(std);
            } else {
                reject('Error while running python code. console output: ' + stderr);
            }
        });
    });
}

async function run_graph5(){
    // executing the python script
    const python = await spawn('python3', ['./Python_Scripts/graph5.py']); // execute the python script
    
    let std = ''; // the script's STD output
    let stderr = ''; // the script's error output, if there are any

    // gets the scripts logs
    python.stdout.on('data', function(data) {
        std += data.toString();
    });

    python.stderr.on('data', (data) => {
        stderr += data.toString();
    });

    // return a promise of the python logs, or an error if the python code can't execute properly.
    return new Promise((resolve, reject) => {
        python.on('close', (code) => {
            if (code === 0) {
                resolve(std);
            } else {
                reject('Error while running python code. console output: ' + stderr);
            }
        });
    });
}

async function run_graph3(){
    const python = await spawn('python3', ['./Python_Scripts/graph3.py']); // execute the python script

    let std = ''; // the script's STD output
    let stderr = ''; // the script's stderr output

    // gets the scripts logs
    python.stdout.on('data', function(data) {
        std += data.toString();
    });

    python.stderr.on('data', (data) => {
        stderr += data.toString();
    });

    // return a promise of the python logs, or an error if the python code can't execute properly.
    return new Promise((resolve, reject) => {
        python.on('close', (code) => {
            if (code === 0) {
                resolve(std);
            } else {
                reject('Error while running python code. console output: ' + stderr);
            }
        });
    });

}

async function run_graph4(){
    const python = await spawn('python3', ['./Python_Scripts/graph4.py']);

    let std = ''; // the script's STD output
    let stderr = ''; // the script's stderr output

    // gets the scripts logs
    python.stdout.on('data', function(data) {
        std += data.toString();
    });

    python.stderr.on('data', (data) => {
        stderr += data.toString();
    });

    // return a promise of the python logs, or an error if the python code can't execute properly.
    return new Promise((resolve, reject) => {
        python.on('close', (code) => {
            if (code === 0) {
                resolve(std);
            } else {
                reject('Error while running python code. console output: ' + stderr);
            }
        });
    });
}

module.exports = {run_graph1, run_graph2, run_graph5, run_graph3, run_graph4,};