// Web Speech API: Trilingual TTS (English, Hindi, Bengali)
const Speech = {
    speak(text, lang = "en-IN") {
        if (!('speechSynthesis' in window)) return;
        window.speechSynthesis.cancel();
        const msg = new SpeechSynthesisUtterance(text);
        msg.lang = lang;
        msg.rate = 0.95;
        window.speechSynthesis.speak(msg);
    }
};
if (typeof module !== "undefined") module.exports = Speech;
