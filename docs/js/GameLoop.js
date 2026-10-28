// Pure Canvas 2D Solver for Bandra-Worli Sea Link
class SeaLinkCanvas {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas.getContext("2d");
        this.w = this.canvas.width = 960;
        this.h = this.canvas.height = 540;
        this.waterLevel = Math.floor(this.h * 0.78);
        this.pylonHeight = Math.floor(this.h * 0.52);
        this.pylonX = this.w / 2;
        this.tick = 0;
        this.deckNodes = [];
        for (let x = 140; x <= this.w - 140; x += 40) {
            this.deckNodes.push({ x: x, y: this.waterLevel - 55 });
        }
    }
    render() {
        this.tick++;
        const ctx = this.ctx;
        ctx.fillStyle = "#0f172a";
        ctx.fillRect(0, 0, this.w, this.h);

        // Marine Swell
        ctx.fillStyle = "#1e3a5f";
        ctx.beginPath();
        ctx.moveTo(0, this.h);
        for (let x = 0; x <= this.w; x += 15) {
            const y = this.waterLevel + Math.sin(x * 0.025 + this.tick * 0.05) * 5;
            ctx.lineTo(x, y);
        }
        ctx.lineTo(this.w, this.h);
        ctx.fill();

        // Diamond Pylon
        const cx = this.pylonX;
        const topY = this.waterLevel - this.pylonHeight;
        const midY = this.waterLevel - this.pylonHeight / 2;
        const deckCrossY = this.waterLevel - 55;

        ctx.fillStyle = "#cbd5e1";
        ctx.beginPath();
        ctx.moveTo(cx, topY);
        ctx.lineTo(cx - 50, midY);
        ctx.lineTo(cx, deckCrossY);
        ctx.lineTo(cx + 50, midY);
        ctx.closePath();
        ctx.fill();

        // Lower Pylon Legs
        ctx.beginPath();
        ctx.moveTo(cx - 50, midY);
        ctx.lineTo(cx, deckCrossY);
        ctx.lineTo(cx - 35, this.waterLevel + 20);
        ctx.fill();
        ctx.beginPath();
        ctx.moveTo(cx + 50, midY);
        ctx.lineTo(cx, deckCrossY);
        ctx.lineTo(cx + 35, this.waterLevel + 20);
        ctx.fill();

        // Stay Cables
        ctx.strokeStyle = "#e2e8f0";
        ctx.lineWidth = 1;
        for (const pt of this.deckNodes) {
            if (Math.abs(pt.x - cx) > 25 && Math.abs(pt.x - cx) < 360) {
                ctx.beginPath();
                ctx.moveTo(cx, topY + 12);
                ctx.lineTo(pt.x, pt.y);
                ctx.stroke();
            }
        }

        // Roadway Deck
        ctx.strokeStyle = "#f59e0b";
        ctx.lineWidth = 4;
        ctx.beginPath();
        ctx.moveTo(this.deckNodes[0].x, this.deckNodes[0].y);
        ctx.lineTo(this.deckNodes[this.deckNodes.length - 1].x, this.deckNodes[this.deckNodes.length - 1].y);
        ctx.stroke();

        requestAnimationFrame(() => this.render());
    }
}
window.addEventListener("DOMContentLoaded", () => {
    if (document.getElementById("seaLinkCanvas")) {
        const sim = new SeaLinkCanvas("seaLinkCanvas");
        sim.render();
    }
});
