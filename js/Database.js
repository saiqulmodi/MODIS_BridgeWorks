// Materials, Landmarks, and Statics Database
const Database = {
    landmarks: {
        bandra_worli: {
            id: "bandra_worli",
            name: "Bandra-Worli Sea Link",
            location: "Mumbai, Maharashtra",
            span_m: 5600,
            style: "Cable-Stayed Bridge with Precast Concrete Box Girders",
            pylons: "Twin Diamond Concrete Towers (128m high)",
            cables: "High-Tensile Galvanized Steel Stay Cables",
            context: "Connects Bandra in Western Suburbs to Worli in South Mumbai across Mahim Bay, reducing peak commute times from 60+ minutes to under 10 minutes.",
            grant: 50000000
        }
    },
    materials: {
        timber: { name: "Hardwood Timber", cost_m: 1500, max_tension: 40000, max_compression: 30000, density: 700 },
        steel: { name: "High-Yield Structural Steel", cost_m: 12000, max_tension: 250000, max_compression: 220000, density: 7850 },
        concrete: { name: "Prestressed Concrete Girder", cost_m: 28000, max_tension: 50000, max_compression: 450000, density: 2400 },
        stay_cable: { name: "High-Tensile Stay Cable Strand", cost_m: 45000, max_tension: 850000, max_compression: 0, density: 7800 }
    }
};
if (typeof module !== "undefined") module.exports = Database;
