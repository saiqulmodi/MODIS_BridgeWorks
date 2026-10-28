// Desktop & Touch Interaction Controls
class InputControls {
    constructor(canvas, onNodePlaced) {
        this.canvas = canvas;
        this.onNodePlaced = onNodePlaced;
        this.scale = 1.0;
        this.offsetX = 0;
        this.offsetY = 0;
        this.isPanning = false;
        this.startX = 0;
        this.startY = 0;
        this.bindEvents();
    }
    bindEvents() {
        this.canvas.addEventListener("mousedown", (e) => {
            if (e.button === 2) { // Right click pan
                this.isPanning = true;
                this.startX = e.clientX - this.offsetX;
                this.startY = e.clientY - this.offsetY;
            } else if (e.button === 0 && this.onNodePlaced) {
                const rect = this.canvas.getBoundingClientRect();
                const x = (e.clientX - rect.left - this.offsetX) / this.scale;
                const y = (e.clientY - rect.top - this.offsetY) / this.scale;
                this.onNodePlaced(Math.round(x), Math.round(y));
            }
        });
        window.addEventListener("mousemove", (e) => {
            if (this.isPanning) {
                this.offsetX = e.clientX - this.startX;
                this.offsetY = e.clientY - this.startY;
            }
        });
        window.addEventListener("mouseup", () => { this.isPanning = false; });
        this.canvas.addEventListener("wheel", (e) => {
            e.preventDefault();
            const zoomFactor = e.deltaY < 0 ? 1.08 : 0.92;
            this.scale = Math.min(Math.max(0.6, this.scale * zoomFactor), 2.5);
        });
        // Prevent default context menu on right click
        this.canvas.addEventListener("contextmenu", (e) => e.preventDefault());
    }
}
window.InputControls = InputControls;
