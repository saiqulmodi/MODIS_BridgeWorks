// In-Game Checkpoint Quiz Runner (+4 / -1 Scoring & Unlock System)
class QuizEngine {
    constructor() {
        this.currentQuestions = [];
        this.currentIndex = 0;
        this.active = false;
        this.onCompleteCallback = null;
    }

    startCheckpoint(tierName, onComplete) {
        this.onCompleteCallback = onComplete;
        fetch("data/questions.json")
            .then(r => r.json())
            .then(allQ => {
                // Shuffle and pick 5 questions
                const filtered = allQ.sort(() => 0.5 - Math.random()).slice(0, 5);
                this.currentQuestions = filtered;
                this.currentIndex = 0;
                this.active = true;
                this.renderModal();
            })
            .catch(e => console.error("Could not load quiz questions:", e));
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
            fb.innerHTML = `✓ Correct (+4)! Engineering Grant Unlocked: +₹${subsidy.toLocaleString('en-IN')}<br><small>${explanation}</small>`;
            window.civicEconomy.addGrant(subsidy);
        } else {
            fb.style.background = "#7f1d1d";
            fb.innerHTML = `✗ Incorrect (-1). Audit penalty incurred.<br><small>${explanation}</small>`;
            window.civicEconomy.applyPenalty(25000);
        }

        setTimeout(() => {
            this.currentIndex++;
            this.renderModal();
        }, 1800);
    }
}
window.quizEngine = new QuizEngine();
