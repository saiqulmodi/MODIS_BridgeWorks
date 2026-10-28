// In-Game Quiz Runner connected to js/quizbank.js & Web Speech read-aloud
class QuizEngine {
    constructor() {
        this.currentQuestions = [];
        this.currentIndex = 0;
        this.active = false;
        this.onCompleteCallback = null;
    }

    startCheckpoint(stageId, onComplete) {
        this.onCompleteCallback = onComplete;
        const bank = (typeof QuizBank !== "undefined") ? QuizBank : [];
        this.currentQuestions = bank.filter(q => q.stage === stageId);
        if (this.currentQuestions.length === 0) this.currentQuestions = bank.slice(0, 3);
        this.currentIndex = 0;
        this.active = true;
        this.renderModal();
    }

    renderModal() {
        const modal = document.getElementById("quiz-modal");
        if (!modal) return;
        
        if (this.currentIndex >= this.currentQuestions.length) {
            modal.style.display = "none";
            this.active = false;
            if (this.onCompleteCallback) this.onCompleteCallback(true);
            return;
        }

        const q = this.currentQuestions[this.currentIndex];
        document.getElementById("modal-q-category").innerText = `${q.tier} | ${q.category}`;
        document.getElementById("modal-q-text").innerText = q.question;
        
        const optsDiv = document.getElementById("modal-options");
        optsDiv.innerHTML = "";
        q.options.forEach((opt, idx) => {
            const btn = document.createElement("button");
            btn.className = "option-btn";
            btn.innerText = opt;
            btn.onclick = () => this.handleAnswer(idx, q.correct, q.subsidy, q.explanation);
            optsDiv.appendChild(btn);
        });

        document.getElementById("modal-feedback").style.display = "none";
        modal.style.display = "flex";
    }

    handleAnswer(selected, correct, subsidy, explanation) {
        const fb = document.getElementById("modal-feedback");
        fb.style.display = "block";
        const buttons = document.querySelectorAll("#modal-options button");
        buttons.forEach(b => b.disabled = true);

        if (selected === correct) {
            fb.style.background = "#14532d";
            fb.innerHTML = `✓ Correct (+4)! Academic Grant Unlocked: +₹${subsidy.toLocaleString('en-IN')}<br><small>${explanation}</small>`;
            if (window.Sound) window.Sound.subsidyGranted();
            if (window.civicEconomy) window.civicEconomy.addGrant(subsidy);
        } else {
            fb.style.background = "#7f1d1d";
            fb.innerHTML = `✗ Incorrect (-1). Audit penalty incurred.<br><small>${explanation}</small>`;
            if (window.Sound) window.Sound.auditPenalty();
            if (window.civicEconomy) window.civicEconomy.applyPenalty(25000);
        }

        setTimeout(() => {
            this.currentIndex++;
            this.renderModal();
        }, 1800);
    }
}
window.quizEngine = new QuizEngine();
