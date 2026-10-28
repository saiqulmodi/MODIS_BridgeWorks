// Pure Academic Mechanics Tabs & Interactive Batch Q/A Runner
const Topics = [
    { id: 1, name: "Tension Fibers", classReq: "Class 1–7", filterKey: "1–7" },
    { id: 2, name: "Coplanar Trusses", classReq: "Class 8–10", filterKey: "8–10" },
    { id: 3, name: "Parabolic Thrust", classReq: "Class 11–12", filterKey: "11–12" },
    { id: 4, name: "Stay Dynamics", classReq: "JEE Advanced", filterKey: "JEE" },
    { id: 5, name: "Matrix Dissipation", classReq: "IIT Mechanics", filterKey: "IIT" }
];

const REWARD_CORRECT = 5000;      // ₹5,000 on correct answer
const REWARD_ATTENDANCE = 500;    // ₹500 on attending/attempting

class CivicEconomyState {
    constructor() {
        this.treasury = parseInt(localStorage.getItem("bridgeworks_treasury") || "50000000");
        this.subsidies = parseInt(localStorage.getItem("bridgeworks_subsidies") || "0");
        this.score = parseInt(localStorage.getItem("bridgeworks_score") || "0");
        this.currentTopic = 1;
    }
    addCorrectAward() {
        // Attendance (500) + Correct Bonus (5000) = 5500
        const totalGain = REWARD_ATTENDANCE + REWARD_CORRECT;
        this.treasury += totalGain;
        this.subsidies += totalGain;
        this.score += 4;
        this.save();
        this.updateHUD();
        return totalGain;
    }
    applyIncorrectPenalty() {
        // Attendance incentive (+500), but score penalty (-1)
        this.treasury += REWARD_ATTENDANCE;
        this.subsidies += REWARD_ATTENDANCE;
        this.score = Math.max(0, this.score - 1);
        this.save();
        this.updateHUD();
        return REWARD_ATTENDANCE;
    }
    save() {
        localStorage.setItem("bridgeworks_treasury", this.treasury);
        localStorage.setItem("bridgeworks_subsidies", this.subsidies);
        localStorage.setItem("bridgeworks_score", this.score);
    }
    updateHUD() {
        const tEl = document.getElementById("hud-treasury");
        const sEl = document.getElementById("hud-subsidies");
        const scEl = document.getElementById("hud-score");
        if (tEl) tEl.innerText = "₹" + this.treasury.toLocaleString('en-IN');
        if (sEl) sEl.innerText = "₹" + this.subsidies.toLocaleString('en-IN');
        if (scEl) scEl.innerText = this.score;
    }
}
window.civicEconomy = new CivicEconomyState();

let currentBatch = [];
let batchIndex = 0;
let activeTopicObj = null;

function initTabs() {
    const tabContainer = document.getElementById("stage-tabs");
    if (!tabContainer) return;
    tabContainer.innerHTML = "";
    Topics.forEach(t => {
        const btn = document.createElement("button");
        btn.className = `stage-tab ${t.id === 1 ? "active" : ""}`;
        btn.innerHTML = `<strong>${t.name}</strong><br><small style="color:#94a3b8;">${t.classReq}</small>`;
        btn.onclick = () => loadTopicBatch(t.id);
        tabContainer.appendChild(btn);
    });
}

function loadTopicBatch(topicId) {
    const topic = Topics.find(t => t.id === topicId) || Topics[0];
    activeTopicObj = topic;

    document.querySelectorAll(".stage-tab").forEach((tab, idx) => {
        if (idx === topicId - 1) tab.classList.add("active");
        else tab.classList.remove("active");
    });

    const bank = (typeof QuizBank !== "undefined") ? QuizBank : [];
    currentBatch = bank.filter(q => q.tier.includes(topic.filterKey));
    batchIndex = 0;

    renderActiveQuestion();
}

function renderActiveQuestion() {
    const container = document.getElementById("active-question-card");
    const progressEl = document.getElementById("batch-progress");
    const titleEl = document.getElementById("active-topic-title");

    if (!container) return;

    if (titleEl && activeTopicObj) {
        titleEl.innerText = `📖 ${activeTopicObj.name} (${activeTopicObj.classReq})`;
    }

    if (currentBatch.length === 0) {
        container.innerHTML = `<p style="color:#94a3b8; padding:20px; text-align:center;">No questions found for this topic.</p>`;
        if (progressEl) progressEl.innerText = "";
        return;
    }

    if (batchIndex >= currentBatch.length) {
        container.innerHTML = `
            <div style="text-align:center; padding:30px;">
                <h3 style="color:#38bdf8; margin-bottom:10px;">🎉 Batch Completed!</h3>
                <p style="color:#94a3b8; margin-bottom:18px;">All concepts for ${activeTopicObj.name} cleared. Total rewards added to your treasury.</p>
                <button class="stage-tab active" style="margin:0 auto; display:inline-block; padding:10px 20px;" onclick="loadTopicBatch(${activeTopicObj.id})">↻ Replay Batch</button>
            </div>
        `;
        if (progressEl) progressEl.innerText = "Completed";
        return;
    }

    const q = currentBatch[batchIndex];
    if (progressEl) progressEl.innerText = `Question ${batchIndex + 1} of ${currentBatch.length}`;

    container.innerHTML = `
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
            <div>
                <span class="badge">${q.tier}</span>
                <strong style="color:#38bdf8; margin-left:6px;">${q.category}</strong>
                <span style="color:#10b981; font-size:12px; margin-left:8px;">(Attending: +₹500 | Correct: +₹5,000)</span>
            </div>
            <button class="voice-btn" onclick="Speech.speak('${encodeURIComponent(q.question).replace(/'/g, "%27")}')">🔊 Read Aloud</button>
        </div>
        <p style="font-size: 16px; line-height:1.5; margin: 14px 0;">${q.question}</p>
        <div id="batch-options">
            ${q.options.map((opt, oIdx) => `
                <button class="option-btn" onclick="handleBatchAnswer(${oIdx}, ${q.correct}, '${encodeURIComponent(q.explanation).replace(/'/g, "%27")}')">${opt}</button>
            `).join("")}
        </div>
        <div id="batch-feedback" class="feedback"></div>
    `;
}

function handleBatchAnswer(selected, correct, explanationEnc) {
    const fb = document.getElementById("batch-feedback");
    const btns = document.querySelectorAll("#batch-options button");
    btns.forEach(b => b.disabled = true);
    const explanation = decodeURIComponent(explanationEnc);

    if (selected === correct) {
        const gained = window.civicEconomy.addCorrectAward();
        fb.style.display = "block";
        fb.style.background = "#14532d";
        fb.innerHTML = `✓ Correct (+4 Points)! Award Granted: +₹5,000 + ₹500 Attendance = <strong>+₹${gained.toLocaleString('en-IN')}</strong><br><small style="font-weight:normal; margin-top:4px; display:inline-block;">${explanation}</small>`;
        if (window.Sound) window.Sound.subsidyGranted();
    } else {
        window.civicEconomy.applyIncorrectPenalty();
        fb.style.display = "block";
        fb.style.background = "#7f1d1d";
        fb.innerHTML = `✗ Incorrect (-1 Point). Attendance Grant Added: <strong>+₹500</strong>.<br><small style="font-weight:normal; margin-top:4px; display:inline-block;">${explanation}</small>`;
        if (window.Sound) window.Sound.auditPenalty();
    }

    setTimeout(() => {
        batchIndex++;
        renderActiveQuestion();
    }, 2200);
}

window.addEventListener("DOMContentLoaded", () => {
    initTabs();
    window.civicEconomy.updateHUD();
    loadTopicBatch(1);
});
