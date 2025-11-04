// === Función para crear gráfico genérico ===
function crearGrafico(idCanvas, data, labelCampo, valorCampo, tipo = 'bar', colores = null) {
    const ctx = document.getElementById(idCanvas);
    if (!ctx) return;

    const etiquetas = data.map(item => item[labelCampo] || 'Sin dato');
    const valores = data.map(item => item[valorCampo]);

    new Chart(ctx, {
        type: tipo,
        data: {
            labels: etiquetas,
            datasets: [{
                label: 'Total',
                data: valores,
                backgroundColor: colores || [
                    '#1976d2', '#64b5f6', '#81c784', '#ffb74d', '#e57373', '#9575cd'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: { legend: { display: false } },
            scales: { y: { beginAtZero: true } }
        }
    });
}

// === Crear los tres gráficos ===
document.addEventListener('DOMContentLoaded', function () {
    try {
        console.log('dataReclamaciones', dataReclamaciones);
        console.log('dataCanales', dataCanales);
        console.log('dataInteracciones', dataInteracciones);
    } catch (e) {
        console.error('Variables de datos no definidas en plantilla:', e);
        return;
    }

    function parseSerie(arr) {
        if (!arr) return { labels: [], values: [] };
        if (Array.isArray(arr)) {
            const labels = arr.map(x => x.descripcion || x.label || x.name || '');
            const values = arr.map(x => Number(x.count || x.value || x.y || 0));
            return { labels, values };
        }
        // si vino un objeto literal {label: value}
        if (typeof arr === 'object') {
            const labels = Object.keys(arr);
            const values = labels.map(k => Number(arr[k] || 0));
            return { labels, values };
        }
        return { labels: [], values: [] };
    }

    const palette = [
        '#4caf50', '#2196f3', '#ff9800', '#9c27b0', '#f44336', '#03a9f4',
        '#8bc34a', '#ffc107', '#e91e63', '#00bcd4'
    ];

    // Reclamaciones por estado (pie)
    (function () {
        const cfg = parseSerie(dataReclamaciones);
        if (!cfg.labels.length) return;
        const ctx = document.getElementById('graficoReclamaciones');
        if (!ctx) return;
        new Chart(ctx, {
            type: 'pie',
            data: {
                labels: cfg.labels,
                datasets: [{
                    data: cfg.values,
                    backgroundColor: palette
                }]
            },
            options: {
                responsive: true,
                plugins: { legend: { position: 'bottom' } }
            }
        });
    })();

    // Canales de venta (bar)
    (function () {
        const cfg = parseSerie(dataCanales);
        if (!cfg.labels.length) return;
        const ctx = document.getElementById('graficoCanales');
        if (!ctx) return;
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: cfg.labels,
                datasets: [{
                    label: 'Cantidad',
                    data: cfg.values,
                    backgroundColor: palette.slice(0, cfg.labels.length)
                }]
            },
            options: {
                responsive: true,
                scales: { y: { beginAtZero: true } },
                plugins: { legend: { display: false } }
            }
        });
    })();

    // Interacciones por tipo (doughnut)
    (function () {
        const cfg = parseSerie(dataInteracciones);
        if (!cfg.labels.length) return;
        const ctx = document.getElementById('graficoInteracciones');
        if (!ctx) return;
        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: cfg.labels,
                datasets: [{
                    data: cfg.values,
                    backgroundColor: palette
                }]
            },
            options: {
                responsive: true,
                plugins: { legend: { position: 'bottom' } }
            }
        });
    })();
});
