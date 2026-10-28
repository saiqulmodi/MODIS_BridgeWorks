// Proximity & Raycast Stress Inspection System
class StressScanner {
    constructor(canvas, onInspect) {
        this.canvas = canvas;
        this.onInspect = onInspect;
        this.selectedNode = null;
        this.bindEvents();
    }

    bindEvents() {
        this.canvas.addEventListener("click", (e) => {
            const rect = this.canvas.getBoundingClientRect();
            const mouseX = e.clientX - rect.left;
            const mouseY = e.clientY - rect.top;

            // Check proximity to existing nodes (within 15px radius)
            if (window.activeBridgeNodes) {
                let hit = null;
                for (const node of window.activeBridgeNodes) {
                    const dist = Math.hypot(node.x - mouseX, node.y - mouseY);
                    if (dist < 18) {
                        hit = node;
                        break;
                    }
                }
                if (hit) {
                    this.selectedNode = hit;
                    this.openProfile(hit);
                }
            }
        });
    }

    openProfile(node) {
        const modal = document.getElementById("quiz-modal");
        if (!modal) return;
        
        const cat = document.getElementById("modal-q-category");
        const txt = document.getElementById("modal-q-text");
        const opts = document.getElementById("modal-options");
        const fb = document.getElementById("modal-feedback");

        cat.innerText = "Structural Diagnosis & Statics Profile";
        txt.innerHTML = `
            <strong>Joint Node #${node.id || 'N1'}</strong><br>
            • Axial Tension: <span style="color:#38bdf8;">${node.tension || '120 kN'}</span><br>
            • Compressive Force: <span style="color:#f59e0b;">${node.compression || '85 kN'}</span><br>
            • Material: ${node.material || 'High-Tensile Galvanized Steel'}<br>
            • Status: ${node.stable ? '✓ Equilibrium Maintained' : '⚠ Near Yield Limit'}
        `;
        opts.innerHTML = `<button class="option-btn" onclick="document.getElementById('quiz-modal').style.display='none'">Close Inspector</button>`;
        fb.style.display = "none";
        modal.style.display = "flex";

        if (window.Speech) {
            window.Speech.speak(`Joint node inspected. Axial tension is ${node.tension || '120 kilo Newtons'}. Equilibrium maintained.`);
        }
    }
}
window.StressScanner = StressScanner;
