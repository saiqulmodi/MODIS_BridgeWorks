// Pure Academic Mechanics Tabs & Interactive Batch Q/A Runner
const Topics = [
    { id: 1, name: "Tension Fibers", classReq: "Class 1–7", filterKey: "1–7", grant: "₹25 Lakhs" },
    { id: 2, name: "Coplanar Trusses", classReq: "Class 8–10", filterKey: "8–10", grant: "₹2.5 Cr" },
    { id: 3, name: "Parabolic Thrust", classReq: "Class 11–12", filterKey: "11–12", grant: "₹15 Cr" },
    { id: 4, name: "Stay Dynamics", classReq: "JEE Advanced", filterKey: "JEE", grant: "₹50 Cr" },
    { id: 5, name: "Matrix Dissipation", classReq: "IIT Mechanics", filterKey: "IIT", grant: "₹250 Cr" }
];

class CivicEconomyState {
    constructor() {
        this.treasury = parseInt(localStorage.getItem("bridgeworks_treasury") || "50000000");
        this.subsidies = parseInt(localStorage.getItem("bridgeworks_subsidies") || "0");
        this.score = parseInt(localStorage.getItem("bridgeworks_score") || "0");
        this.currentTopic = 1;
    }
    addGrant(val) {
        this.treasury += val;
        this.subsidies += val;
        this.score += 4;
        this.save();
        this.updateHUD();
    }
    applyPenalty(val) {
        this.treasury = Math.max(0, this.treasury - val);
        this.score = Math.max(0, this.score - 1);
        this.save();
        this.updateHUD();
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

// Batch Quiz Runner State
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

    // Highlight active tab
    document.querySelectorAll(".stage-tab").forEach((tab, idx) => {
        if (idx === topicId - 1) tab.classList.add("active");
        else tab.classList.remove("active");
    });

    // Filter questions mapped to this class level
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

    // Check if batch finished
    if (batchIndex >= currentBatch.length) {
        container.innerHTML = `
            <div style="text-align:center; padding:30px;">
                <h3 style="color:#38bdf8; margin-bottom:10px;">🎉 Batch Completed!</h3>
                <p style="color:#94a3b8; margin-bottom:18px;">All concepts for ${activeTopicObj.name} cleared. Engineering grants added to your treasury.</p>
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
            <div><span class="badge">${q.tier}</span> <strong style="color:#38bdf8; margin-left:6px;">${q.category}</strong></div>
            <button class="voice-btn" onclick="Speech.speak('${encodeURIComponent(q.question).replace(/'/g, "%27")}')">🔊 Read Aloud</button>
        </div>
        <p style="font-size: 16px; line-height:1.5; margin: 14px 0;">${q.question}</p>
        <div id="batch-options">
            ${q.options.map((opt, oIdx) => `
                <button class="option-btn" onclick="handleBatchAnswer(${oIdx}, ${q.correct}, ${q.subsidy}, '${encodeURIComponent(q.explanation).replace(/'/g, "%27")}')">${opt}</button>
            `).join("")}
        </div>
        <div id="batch-feedback" class="feedback"></div>
    `;
}

function handleBatchAnswer(selected, correct, subsidy, explanationEnc) {
    const fb = document.getElementById("batch-feedback");
    const btns = document.querySelectorAll("#batch-options button");
    btns.forEach(b => b.disabled = true);
    const explanation = decodeURIComponent(explanationEnc);

    if (selected === correct) {
        fb.style.display = "block";
        fb.style.background = "#14532d";
        fb.innerHTML = `✓ Correct (+4 Points)! Award Unlocked: +₹${subsidy.toLocaleString('en-IN')}<br><small style="font-weight:normal; margin-top:4px; display:inline-block;">${explanation}</small>`;
        if (window.Sound) window.Sound.subsidyGranted();
        window.civicEconomy.addGrant(subsidy);
    } else {
        fb.style.display = "block";
        fb.style.background = "#7f1d1d";
        fb.innerHTML = `✗ Incorrect (-1 Point). Audit penalty: -₹25,000.<br><small style="font-weight:normal; margin-top:4px; display:inline-block;">${explanation}</small>`;
        if (window.Sound) window.Sound.auditPenalty();
        window.civicEconomy.applyPenalty(25000);
    }

    // Auto-advance to next question after 2.2 seconds (like EcosSynthetica)
    setTimeout(() => {
        batchIndex++;
        renderActiveQuestion();
    }, 2200);
}

window.addEventListener("DOMContentLoaded", () => {
    initTabs();
    window.civicEconomy.updateHUD();
    // Default load first batch
    loadTopicBatch(1);
});
