// Academic Physics & Structural Mechanics Progression
const Stages = [
    { id: 1, name: "Stage 1: Tensile Fibers", desc: "Line of Action & Rigidity", grant: "₹25 Lakhs", classReq: "Class 1–7 (Basics)" },
    { id: 2, name: "Stage 2: Coplanar Trusses", desc: "Concurrent Equilibrium", grant: "₹2.5 Cr", classReq: "Class 8–10 (Forces)" },
    { id: 3, name: "Stage 3: Parabolic Thrust", desc: "Elastic Moduli & Thermal Stress", grant: "₹15 Cr", classReq: "Class 11–12 (Solids)" },
    { id: 4, name: "Stage 4: Stay Dynamics", desc: "Axial Torsion & Buckling", grant: "₹50 Cr", classReq: "JEE Main / Advanced" },
    { id: 5, name: "Stage 5: Matrix Dissipation", desc: "Continuous Systems & FEM", grant: "₹250 Cr", classReq: "IIT / NIT Mechanics" }
];

class CivicEconomyState {
    constructor() {
        this.treasury = 50000000;
        this.subsidies = 0;
        this.currentStage = 4;
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
            alert(`Checkpoint Cleared! Now testing ${Stages[idx - 1].name}`);
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
        btn.innerHTML = `<strong>${s.name}</strong><br><small style="color:#94a3b8;">${s.classReq}</small>`;
        btn.onclick = () => window.civicEconomy.setStage(s.id);
        tabContainer.appendChild(btn);
    });
}
window.addEventListener("DOMContentLoaded", () => {
    initTabs();
    window.civicEconomy.updateHUD();
});
