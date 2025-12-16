const { contextBridge, ipcRenderer } = require("electron");

contextBridge.exposeInMainWorld("memoAPI", {
  saveText: (text) => ipcRenderer.send("save-text", text),
  requestDelete: () => ipcRenderer.send("delete-memo"),
  sendColorUpdate: (colors) => ipcRenderer.send("update-color", colors),
  onSetText: (callback) =>
    ipcRenderer.on("set-text", (_, text) => callback(text)),
  onSetColors: (callback) =>
    ipcRenderer.on("set-colors", (_, colors) => callback(colors)),
  onOpenColorPicker: (callback) =>
    ipcRenderer.on("open-color-picker", (_, data) => callback(data)),
});
