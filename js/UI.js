// UI Manager: 5-Stage Evolution Tabs and Material Palette
const Stages = [
    { id: 1, name: "Stage 1: Bamboo & Living Root", span: "15m", grant: "₹25 Lakhs", classReq: "Class 1–7" },
    { id: 2, name: "Stage 2: Howrah Cantilever", span: "450m", grant: "₹2.5 Cr", classReq: "Class 8–10" },
    { id: 3, name: "Stage 3: Chenab Arch Bridge", span: "467m", grant: "₹15 Cr", classReq: "Class 11–12" },
    { id: 4, name: "Stage 4: Bandra-Worli Sea Link", span: "5,600m", grant: "₹50 Cr", classReq: "JEE / IIT Tier" },
    { id: 5, name: "Stage 5: Oceanic Hyper-Megastructure", span: "25,000m", grant: "₹250 Cr", classReq: "Advanced Engineering" }
];

class CivicEconomyState {
    constructor() {
        this.treasury = 50000000;
        this.subsidies = 0;
        this.currentStage = 4; // Starts on Bandra-Worli Sea Link
    }
    addGrant(val) {
        this.treasury += val;
        this.subsidies += val;
        this.updateHUD();
    }
    applyPenalty(val) {
        this.treasury = Math.max(0, this.treasury - val);
        this.updateHUD();
    }
    setStage(idx) {
        this.currentStage = idx;
        document.querySelectorAll(".stage-tab").forEach((tab, tIdx) => {
            if (tIdx === idx - 1) tab.classList.add("active");
            else tab.classList.remove("active");
        });
        window.quizEngine.startCheckpoint(Stages[idx - 1].name, () => {
            alert(`Checkpoint Cleared! Now building ${Stages[idx - 1].name}`);
        });
    }
    updateHUD() {
        document.getElementById("hud-treasury").innerText = "₹" + this.treasury.toLocaleString('en-IN');
        document.getElementById("hud-subsidies").innerText = "₹" + this.subsidies.toLocaleString('en-IN');
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
        btn.innerHTML = `<strong>${s.name}</strong><br><small style="color:#94a3b8;">${s.classReq} | ${s.grant}</small>`;
        btn.onclick = () => window.civicEconomy.setStage(s.id);
        tabContainer.appendChild(btn);
    });
}
window.addEventListener("DOMContentLoaded", () => {
    initTabs();
    window.civicEconomy.updateHUD();
});
