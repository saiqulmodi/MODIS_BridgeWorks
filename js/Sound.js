// Web Audio API: Procedural Sound Synthesizer (Zero External Audio Files)
const Sound = {
    ctx: null,
    init() {
        if (!this.ctx) this.ctx = new (window.AudioContext || window.webkitAudioContext)();
    },
    playTone(freq, type, duration) {
        try {
            this.init();
            const osc = this.ctx.createOscillator();
            const gain = this.ctx.createGain();
            osc.type = type;
            osc.frequency.setValueAtTime(freq, this.ctx.currentTime);
            gain.gain.setValueAtTime(0.15, this.ctx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.01, this.ctx.currentTime + duration);
            osc.connect(gain);
            gain.connect(this.ctx.destination);
            osc.start();
            osc.stop(this.ctx.currentTime + duration);
        } catch(e) {}
    },
    cableSnap() { this.playTone(180, "sawtooth", 0.4); },
    subsidyGranted() { this.playTone(587.33, "sine", 0.3); },
    auditPenalty() { this.playTone(110, "square", 0.5); }
};
if (typeof module !== "undefined") module.exports = Sound;
