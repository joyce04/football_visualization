const { app, session, BrowserWindow } = require('electron');
const path = require('path');

// Keep a global reference of the mainWindowdow object, if you don't, the mainWindowdow will
// be closed automatically when the JavaScript object is garbage collected.
var mainWindow = null;
var subpy = null;

function createWindow() {
    // Create the browser mainWindow
    mainWindow = new BrowserWindow({
        width: 1300,
        height: 950,
        // transparent: true, // transparent header bar
        // icon: __dirname + '/web/resource/icon.png',
        // fullscreen: true,
        // opacity:0.8,
        // darkTheme: true,
        // frame: false,
        resizeable: true,
        show: false
    });

    const ses = mainWindow.webContents.session.clearCache(function() {});

    // Load the index page
    mainWindow.loadFile('./web/init.html')

    // Open the DevTools.
    mainWindow.webContents.openDevTools();

    // Emitted when the mainWindow is closed.
    mainWindow.on('closed', () => {
        // Dereference the mainWindow object
        mainWindow = null;
    });

    mainWindow.once('ready-to-show', () => {
        mainWindow.show()
    })
}

function addAppEventListeners() {
    // disable menu
    app.on('browser-window-created', (e, window) => {
        window.setMenu(null);
    });

    // ------- app terminated
    app.on('window-all-closed', () => {
        // On macOs it is common for application and their icon
        // to stay active until the user quits explicitly with Cmd + q
        if (process.platform !== 'darwin') {
            app.quit()
        }
    });

    app.on('quit', () => {
        // kill the python server on exit
        subpy.kill('SIGINT');
    });
}

// This method will be called when Electron has finished
// initialization and is ready to create browser mainWindow.
// Some APIs can only be used after this event occurs.
app.on('ready', () => {
    // spawn server(dev)
    // subpy = require('child_process').spawn('python3', [__dirname + '/py_source/run_app.py']);
    
    // spawn server(op)
    subpy = require('child_process').spawn(__dirname + '/run_flask.exe');

    createWindow();
    addAppEventListeners();
});
