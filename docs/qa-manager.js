// Q/A Bank Manager: +4 / -1 Scoring, 3-Hour Reset Timer, and Trilingual TTS
const TIMER_KEY = "bridgeworks_level_start_time";
const THREE_HOURS_MS = 3 * 60 * 60 * 1000;

let score = parseInt(localStorage.getItem("bridgeworks_score") || "0");
let totalSubsidies = parseInt(localStorage.getItem("bridgeworks_subsidies") || "0");

// Initialize 3-Hour Level Timer
let levelStartTime = localStorage.getItem(TIMER_KEY);
if (!levelStartTime) {
    levelStartTime = Date.now().toString();
    localStorage.setItem(TIMER_KEY, levelStartTime);
}

function updateTimerDisplay() {
    const elapsed = Date.now() - parseInt(levelStartTime);
    const remaining = THREE_HOURS_MS - elapsed;
    const resetBtn = document.getElementById("reset-btn");
    const timerSpan = document.getElementById("timer-display");

    if (remaining <= 0) {
        if (resetBtn) resetBtn.disabled = false;
        if (timerSpan) timerSpan.innerText = "Score Reset: Unlocked!";
    } else {
        if (resetBtn) resetBtn.disabled = true;
        const hrs = Math.floor(remaining / (1000 * 60 * 60));
        const mins = Math.floor((remaining % (1000 * 60 * 60)) / (1000 * 60));
        const secs = Math.floor((remaining % (1000 * 60)) / 1000);
        if (timerSpan) timerSpan.innerText = `Reset unlocks in: ${hrs}h ${mins}m ${secs}s`;
    }
}
setInterval(updateTimerDisplay, 1000);

function resetScore() {
    const elapsed = Date.now() - parseInt(levelStartTime);
    if (elapsed >= THREE_HOURS_MS) {
        score = 0;
        totalSubsidies = 0;
        levelStartTime = Date.now().toString();
        localStorage.setItem(TIMER_KEY, levelStartTime);
        localStorage.setItem("bridgeworks_score", "0");
        localStorage.setItem("bridgeworks_subsidies", "0");
        document.getElementById("score").innerText = "0";
        document.getElementById("treasury").innerText = "₹0";
        alert("Level score reset. Next reset available in 3 hours.");
    }
}

// Trilingual Speech Synthesis (EN, HI, BN)
function readAloud(text, lang = "en-IN") {
    if (!('speechSynthesis' in window)) return;
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = lang;
    utterance.rate = 0.95;
    window.speechSynthesis.speak(utterance);
}

fetch("data/questions.json")
    .then(r => r.json())
    .then(data => renderQuestions(data))
    .catch(err => console.error("Error loading questions:", err));

function renderQuestions(questions) {
    const container = document.getElementById("quiz-container");
    container.innerHTML = "";
    document.getElementById("score").innerText = score;
    document.getElementById("treasury").innerText = "₹" + totalSubsidies.toLocaleString('en-IN');

    questions.forEach((q, idx) => {
        const card = document.createElement("div");
        card.className = "card";
        card.innerHTML = `
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div><span class="badge">${q.tier}</span> <strong>${q.category}</strong></div>
                <button class="voice-btn" onclick="readAloud('${encodeURIComponent(q.question).replace(/'/g, "%27")}')">🔊 Read</button>
            </div>
            <p style="font-size: 17px; margin-top: 12px;">${q.question}</p>
            <div id="opts-${idx}">
                ${q.options.map((opt, oIdx) => `
                    <button class="option-btn" onclick="checkAnswer(${idx}, ${oIdx}, ${q.correct}, ${q.subsidy}, '${encodeURIComponent(q.explanation).replace(/'/g, "%27")}')">${opt}</button>
                `).join("")}
            </div>
            <div id="fb-${idx}" class="feedback"></div>
        `;
        container.appendChild(card);
    });
}

function checkAnswer(qIdx, selected, correct, subsidy, explanationEnc) {
    const fb = document.getElementById(`fb-${qIdx}`);
    const btns = document.querySelectorAll(`#opts-${qIdx} button`);
    btns.forEach(b => b.disabled = true);
    const explanation = decodeURIComponent(explanationEnc);

    if (selected === correct) {
        score += 4;
        totalSubsidies += subsidy;
        fb.style.display = "block";
        fb.style.background = "#14532d";
        fb.innerHTML = `✓ Correct (+4)! Engineering Grant Unlocked: +₹${subsidy.toLocaleString('en-IN')}<br><small>${explanation}</small>`;
    } else {
        score = Math.max(0, score - 1);
        fb.style.display = "block";
        fb.style.background = "#7f1d1d";
        fb.innerHTML = `✗ Incorrect (-1). Audit penalty incurred.<br><small>${explanation}</small>`;
    }
    localStorage.setItem("bridgeworks_score", score);
    localStorage.setItem("bridgeworks_subsidies", totalSubsidies);
    document.getElementById("score").innerText = score;
    document.getElementById("treasury").innerText = "₹" + totalSubsidies.toLocaleString('en-IN');
}
