const text = document.getElementById("text");
let phraseText = document.getElementById("phraseText").value;
let phrase = document.getElementById("phrase").value;
text.innerHTML = phrase;

let curr = 0
let firstKeyPress = true;
let sec = 0;
let len = phraseText.split(" ").length;
let countdown = document.getElementById("sec");
let wordNum = 0;
let mistakes = 0;
let inputLetters = [];

function onKeyPress(e) {
    let validLetters = [' ', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '!', "?", ".", ","]; 
    let pressedKey = e.key;
    let characterToFill = phraseText[curr];
    if (validLetters.includes(pressedKey) === true) {
        
        if (firstKeyPress === true) {
            startTimer();
            firstKeyPress = false;
            document.getElementById("logo").style.visibility = "hidden"
        }

        const char = document.getElementById(curr.toString());
        
        if (document.getElementById("ic")) {
            document.getElementById("ic").remove();
        }
        let cursor = document.createElement("span")
        cursor.className = "input-cursor"
        cursor.id = "ic"
        char.append(cursor)
        
        if (pressedKey == characterToFill) {
            if (pressedKey == " ") {
                wordNum++;
            }
            char.style.color = "#f6f5f5";
            curr++
            inputLetters.push(pressedKey);
        } else {
            char.style.color = "#ff4754";
            mistakes++;
        }
    }

    if (curr === phraseText.length) {
        const v = document.getElementById("victory")
        v.innerText = "Completed!"
    }
}

function over() {
    document.getElementById("text").style.position = "absolute";
    document.getElementById("text").style.visibility = "hidden";
    document.getElementById("text").style.zIndex = "0";
    document.getElementById("end").style.position = "relative";
    document.getElementById("end").style.top = "0";
    document.getElementById("end").style.left = "0";
    document.removeEventListener("keydown", onKeyPress)
    countdown.innerHTML = ""
    let accuracy = Math.floor(((inputLetters.length - mistakes) / inputLetters.length) * 100)
    if (accuracy < 0) {
        accuracy = 0;
    }
    document.getElementById("acc").innerText = `Accuracy: ${accuracy}%`; 
}

function startTimer() {
    sec++;
    countdown.innerText = 30 - sec;
    if (document.getElementById("victory").innerText != "Completed!" && sec != 30) {
        setTimeout(`startTimer()`, 1000);
    } else {
        over();
        if (sec == 30) {
            let wpm = Math.floor(wordNum / (sec / 60));
            let wpmText = document.getElementById("wpm");
            const http = new XMLHttpRequest();
            const url = `${window.location.href}wpm/${wpm}`;
            http.open("GET", url);
            http.send();
            wpmText.innerText = `${wpm} words per minute!`;
        } else {
            let wpm = Math.floor(len / (sec / 60));
            let wpmText = document.getElementById("wpm");
            wpmText.innerText = `${wpm} words per minute!`
        }
    }
}

document.addEventListener("keydown", onKeyPress)