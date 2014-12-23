winmiscw = 20;
winmisch = 40;

function popUp(URL,w,h) {
l = (screen.width / 2) - (w / 2) - (winmiscw / 2);
t = (screen.height / 2) - (h / 2) - (winmisch / 2);
day = new Date();
id = day.getTime();
eval("page" + id + " = window.open(URL, '" + id + "', 'toolbar=0,scrollbars=0,location=0,statusbar=0,menubar=0,resizable=1,width=' + w + ',height=' + h + ',left=' + l + ',top=' + t + ' ');");
}

// note: see /intake/memplan.html for a working implementation
function getFilename() {
var filename = location.pathname.substring(location.pathname.lastIndexOf('\/')+1);
var root = sprintf("%s",filename);
document.write('this file is:' + filename);
}

