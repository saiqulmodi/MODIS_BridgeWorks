// Blueprint Clues, Materials & Batch Q/A Engine
const Topics = [
    { 
        id: 1, 
        name: "Tension Fibers", 
        classReq: "Class 1–7 (NCERT / STEM)", 
        filterKey: "1–7",
        blueprint: {
            product: "Living Root & Bamboo Suspension Span",
            span: "15 meters",
            materials: ["Ficus Root Tendrils", "Bamboo Splints", "Hemp Rope Lashing", "Cut Riverstone Abutments"],
            clues: [
                "Clue 1 (Anchor Bedrock): Anchor tensile cables deep into rock outcrops so horizontal cable pull does not pull the bank inward.",
                "Clue 2 (Cable Sag): Maintain a minimum 8% center sag ratio. Pulling cables flat creates destructive horizontal forces.",
                "Clue 3 (Triangulated Walkway): Cross-lash bamboo slats beneath the deck to prevent twisting under crosswinds."
            ]
        }
    },
    { 
        id: 2, 
        name: "Coplanar Trusses", 
        classReq: "Class 8–10 (Forces)", 
        filterKey: "8–10",
        blueprint: {
            product: "Riveted Steel Cantilever Truss",
            span: "450 meters",
            materials: ["Rolled Steel Channels", "Hot-Driven Rivets", "Roller Bearings", "Reinforced Pier Pedestals"],
            clues: [
                "Clue 1 (Pin-Joints): Members carry only axial tension or compression. Avoid bending moments at joint nodes.",
                "Clue 2 (Expansion Joints): Install roller bearings at one abutment to allow thermal expansion (ΔL = α·L·ΔT)."
            ]
        }
    },
    { 
        id: 3, 
        name: "Parabolic Thrust", 
        classReq: "Class 11–12 (Elasticity)", 
        filterKey: "11–12",
        blueprint: {
            product: "High-Strength Steel Arch",
            span: "467 meters",
            materials: ["High-Yield Structural Steel E350", "Prestressed Tendons", "Expansion Finger Girders"],
            clues: [
                "Clue 1 (Parabolic Catenary): Under uniform horizontal load, a parabolic arch experiences pure compression along its line of thrust.",
                "Clue 2 (Thermal Stresses): Constrained arch members experience internal stress σ = Y·α·ΔT."
            ]
        }
    },
    { 
        id: 4, 
        name: "Stay Dynamics", 
        classReq: "JEE Advanced", 
        filterKey: "JEE",
        blueprint: {
            product: "Cable-Stayed Marine Span",
            span: "5,600 meters",
            materials: ["High-Tensile Galvanized Steel Cables", "Diamond Concrete Pylon", "Hollow Box Girders"],
            clues: [
                "Clue 1 (Closed Box Section): Resists wind-induced torsional twisting via high polar moment of inertia (J).",
                "Clue 2 (Euler Limits): Slender pylon towers must avoid axial compressive buckling limits (P_cr = π²EI/L²)."
            ]
        }
    },
    { 
        id: 5, 
        name: "Matrix Dissipation", 
        classReq: "IIT Mechanics", 
        filterKey: "IIT",
        blueprint: {
            product: "Hyperstatic Oceanic Corridor",
            span: "25,000 meters",
            materials: ["Carbon-Fiber Tendons", "Tuned Mass Dampers", "Underwater Scour Caissons"],
            clues: [
                "Clue 1 (Dynamic FEM): Compute global matrix stiffness equilibrium [K]{u} = {F}.",
                "Clue 2 (Resonance Dampers): Install anti-phase tuned mass dampers to dissipate vortex harmonic resonance."
            ]
        }
    }
];

const REWARD_CORRECT = 5000;    // +₹5,000 on correct answer
const REWARD_ATTENDANCE = 500;  // +₹500 on attending/attempting

class CivicEconomyState {
    constructor() {
        this.treasury = parseInt(localStorage.getItem("bridgeworks_treasury") || "50000000");
        this.subsidies = parseInt(localStorage.getItem("bridgeworks_subsidies") || "0");
        this.score = parseInt(localStorage.getItem("bridgeworks_score") || "0");
        this.currentTopic = 1;
    }
    addCorrectAward() {
        const total = REWARD_ATTENDANCE + REWARD_CORRECT;
        this.treasury += total;
        this.subsidies += total;
        this.score += 4;
        this.save();
        this.updateHUD();
        return total;
    }
    applyIncorrectPenalty() {
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

    // Highlight tab
    document.querySelectorAll(".stage-tab").forEach((tab, idx) => {
        if (idx === topicId - 1) tab.classList.add("active");
        else tab.classList.remove("active");
    });

    // 1. Render Blueprint Clues & Materials Box
    renderBlueprintLab(topic);

    // 2. Filter Question Batch
    const bank = (typeof QuizBank !== "undefined") ? QuizBank : [];
    currentBatch = bank.filter(q => q.tier.includes(topic.filterKey));
    batchIndex = 0;

    // 3. Render Active Question Card
    renderActiveQuestion();
}

function renderBlueprintLab(topic) {
    const bpContainer = document.getElementById("blueprint-lab");
    if (!bpContainer || !topic.blueprint) return;

    const bp = topic.blueprint;
    bpContainer.innerHTML = `
        <div style="background:#1e293b; border:1px solid #334155; border-radius:8px; padding:16px; margin-bottom:16px;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                <h4 style="margin:0; color:#38bdf8;">🛠️ Structural Blueprint: ${bp.product} (${bp.span})</h4>
                <span class="badge">${topic.classReq}</span>
            </div>
            <div style="margin:10px 0;">
                <strong style="font-size:13px; color:#cbd5e1;">Required Materials to Build:</strong>
                <div style="display:flex; gap:8px; flex-wrap:wrap; margin-top:6px;">
                    ${bp.materials.map(m => `<span style="background:#0f172a; border:1px solid #475569; padding:4px 10px; border-radius:6px; font-size:12px; color:#38bdf8;">${m}</span>`).join("")}
                </div>
            </div>
            <div style="margin-top:10px; background:#0f172a; padding:10px 14px; border-radius:6px; border-left:3px solid #f59e0b;">
                <strong style="color:#f59e0b; font-size:13px;">Engineering Clues & Statics Rules:</strong>
                <ul style="margin:6px 0 0 16px; font-size:13px; color:#94a3b8; line-height:1.5;">
                    ${bp.clues.map(c => `<li>${c}</li>`).join("")}
                </ul>
            </div>
        </div>
    `;
}

function renderActiveQuestion() {
    const container = document.getElementById("active-question-card");
    const progressEl = document.getElementById("batch-progress");
    const titleEl = document.getElementById("active-topic-title");

    if (!container) return;
    if (titleEl && activeTopicObj) {
        titleEl.innerText = `📖 ${activeTopicObj.name} Academic Q/A (${activeTopicObj.classReq})`;
    }

    if (currentBatch.length === 0) {
        container.innerHTML = `<p style="color:#94a3b8; padding:20px; text-align:center;">No questions found for this topic.</p>`;
        if (progressEl) progressEl.innerText = "";
        return;
    }

    if (batchIndex >= currentBatch.length) {
        container.innerHTML = `
            <div style="text-align:center; padding:26px;">
                <h3 style="color:#38bdf8; margin-bottom:8px;">🎉 Class Curriculum Batch Cleared!</h3>
                <p style="color:#94a3b8; margin-bottom:16px;">All foundation concepts for ${activeTopicObj.name} completed. Engineering awards added to your treasury.</p>
                <button class="stage-tab active" style="margin:0 auto; display:inline-block; padding:10px 22px;" onclick="loadTopicBatch(${activeTopicObj.id})">↻ Replay Batch</button>
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
        <p style="font-size: 16px; line-height:1.5; margin: 12px 0;">${q.question}</p>
        ${q.clue ? `<div style="background:#0f172a; padding:8px 12px; border-radius:6px; margin-bottom:12px; font-size:12px; color:#fbbf24;">💡 <strong>Physics Clue:</strong> ${q.clue}</div>` : ""}
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
