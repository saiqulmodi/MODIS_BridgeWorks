// UI Manager: 5-Stage Evolution & Subject Q/A Lab Modal
const Stages = [
    { id: 1, name: "Stage 1: Tension Fibers", classReq: "Class 1–7 (Equilibrium)", grant: "₹25 Lakhs" },
    { id: 2, name: "Stage 2: Coplanar Trusses", classReq: "Class 8–10 (Vector Statics)", grant: "₹2.5 Cr" },
    { id: 3, name: "Stage 3: Parabolic Thrust", classReq: "Class 11–12 (Elastic Solids)", grant: "₹15 Cr" },
    { id: 4, name: "Stage 4: Stay Dynamics", classReq: "JEE Advanced (Torsion)", grant: "₹50 Cr" },
    { id: 5, name: "Stage 5: Matrix Dissipation", classReq: "IIT Tier (FEM / Dynamics)", grant: "₹250 Cr" }
];

class CivicEconomyState {
    constructor() {
        this.treasury = parseInt(localStorage.getItem("bridgeworks_treasury") || "50000000");
        this.subsidies = parseInt(localStorage.getItem("bridgeworks_subsidies") || "0");
        this.currentStage = 4;
    }
    addGrant(val) {
        this.treasury += val;
        this.subsidies += val;
        localStorage.setItem("bridgeworks_treasury", this.treasury);
        localStorage.setItem("bridgeworks_subsidies", this.subsidies);
        this.updateHUD();
    }
    applyPenalty(val) {
        this.treasury = Math.max(0, this.treasury - val);
        localStorage.setItem("bridgeworks_treasury", this.treasury);
        this.updateHUD();
    }
    setStage(idx) {
        this.currentStage = idx;
        document.querySelectorAll(".stage-tab").forEach((tab, tIdx) => {
            if (tIdx === idx - 1) tab.classList.add("active");
            else tab.classList.remove("active");
        });
        if (window.quizEngine) {
            window.quizEngine.startCheckpoint(idx, () => {
                alert(`Stage ${idx} Checkpoint Cleared! Ready for construction testing.`);
            });
        }
    }
    updateHUD() {
        const tEl = document.getElementById("hud-treasury");
        const sEl = document.getElementById("hud-subsidies");
        if (tEl) tEl.innerText = "₹" + this.treasury.toLocaleString('en-IN');
        if (sEl) sEl.innerText = "₹" + this.subsidies.toLocaleString('en-IN');
    }
}
window.civicEconomy = new CivicEconomyState();

function initTabs() {
    const tabContainer = document.getElementById("stage-tabs");
    if (!tabContainer) return;
    tabContainer.innerHTML = "";
    Stages.forEach(s => {
        const btn = document.createElement("button");
        btn.className = `stage-tab ${s.id === 4 ? "active" : ""}`;
        btn.innerHTML = `<strong>${s.name}</strong><br><small style="color:#94a3b8;">${s.classReq}</small>`;
        btn.onclick = () => window.civicEconomy.setStage(s.id);
        tabContainer.appendChild(btn);
    });
}

// Subject Lab Filtering Modal Functions
function openSubjectLab() {
    document.getElementById("subject-lab-modal").style.display = "flex";
    filterSubjectLab("ALL");
}

function closeSubjectLab() {
    document.getElementById("subject-lab-modal").style.display = "none";
}

function filterSubjectLab(tier) {
    const container = document.getElementById("subject-lab-questions");
    container.innerHTML = "";
    const bank = (typeof QuizBank !== "undefined") ? QuizBank : [];
    const filtered = (tier === "ALL") ? bank : bank.filter(q => q.tier.includes(tier));

    filtered.forEach((q, idx) => {
        const card = document.createElement("div");
        card.className = "card";
        card.style.margin = "10px 0";
        card.innerHTML = `
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div><span class="badge">${q.tier}</span> <strong>${q.category}</strong></div>
                <button class="voice-btn" onclick="Speech.speak('${encodeURIComponent(q.question).replace(/'/g, "%27")}')">🔊 Read</button>
            </div>
            <p style="font-size: 15px; margin: 10px 0;">${q.question}</p>
            <div id="slab-opts-${idx}">
                ${q.options.map((opt, oIdx) => `
                    <button class="option-btn" onclick="checkSubjectLabAnswer(${idx}, ${oIdx}, ${q.correct}, ${q.subsidy}, '${encodeURIComponent(q.explanation).replace(/'/g, "%27")}')">${opt}</button>
                `).join("")}
            </div>
            <div id="slab-fb-${idx}" class="feedback"></div>
        `;
        container.appendChild(card);
    });
}

function checkSubjectLabAnswer(qIdx, selected, correct, subsidy, explanationEnc) {
    const fb = document.getElementById(`slab-fb-${qIdx}`);
    const btns = document.querySelectorAll(`#slab-opts-${qIdx} button`);
    btns.forEach(b => b.disabled = true);
    const explanation = decodeURIComponent(explanationEnc);

    if (selected === correct) {
        fb.style.display = "block";
        fb.style.background = "#14532d";
        fb.innerHTML = `✓ Correct (+4)! Academic Grant Unlocked: +₹${subsidy.toLocaleString('en-IN')}<br><small>${explanation}</small>`;
        if (window.Sound) window.Sound.subsidyGranted();
        window.civicEconomy.addGrant(subsidy);
    } else {
        fb.style.display = "block";
        fb.style.background = "#7f1d1d";
        fb.innerHTML = `✗ Incorrect (-1). Audit penalty incurred.<br><small>${explanation}</small>`;
        if (window.Sound) window.Sound.auditPenalty();
        window.civicEconomy.applyPenalty(25000);
    }
}

window.addEventListener("DOMContentLoaded", () => {
    initTabs();
    window.civicEconomy.updateHUD();
});
