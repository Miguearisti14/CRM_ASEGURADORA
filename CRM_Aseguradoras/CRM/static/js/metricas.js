// Funciones utilitarias
function parseSerie(arr, labelKey = 'descripcion', valueKey = 'count') {
    if (!arr) return { labels: [], values: [] };
    if (typeof arr === 'string') {
        try { arr = JSON.parse(arr); } catch { return { labels: [], values: [] }; }
    }
    if (Array.isArray(arr)) {
        const labels = arr.map(x => x[labelKey] ?? x.mes ?? x.label ?? 'Sin dato');
        const values = arr.map(x => Number(x[valueKey] ?? x.count ?? 0));
        return { labels, values };
    }
    if (typeof arr === 'object') {
        const labels = Object.keys(arr);
        const values = labels.map(k => Number(arr[k] ?? 0));
        return { labels, values };
    }
    return { labels: [], values: [] };
}

function colores(n) {
    const palette = [
        '#4caf50', '#2196f3', '#ff9800', '#9c27b0', '#f44336', '#03a9f4',
        '#8bc34a', '#ffc107', '#e91e63', '#00bcd4', '#607d8b', '#795548'
    ];
    return Array.from({ length: n }, (_, i) => palette[i % palette.length]);
}

document.addEventListener('DOMContentLoaded', function () {
    // Reclamaciones (pie)
    (function () {
        const cfg = parseSerie(dataReclamaciones);
        if (!cfg.labels.length) return;
        const ctx = document.getElementById('graficoReclamaciones').getContext('2d');
        new Chart(ctx, {
            type: 'pie',
            data: { labels: cfg.labels, datasets: [{ data: cfg.values, backgroundColor: colores(cfg.labels.length) }] },
            options: { responsive: true, plugins: { legend: { position: 'bottom' } } }
        });
    })();

    // Canales (bar)
    (function () {
        const cfg = parseSerie(dataCanales);
        if (!cfg.labels.length) return;
        const ctx = document.getElementById('graficoCanales').getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: { labels: cfg.labels, datasets: [{ label: 'Cantidad', data: cfg.values, backgroundColor: colores(cfg.labels.length) }] },
            options: { responsive: true, scales: { y: { beginAtZero: true } }, plugins: { legend: { display: false } } }
        });
    })();

    // Interacciones (doughnut)
    (function () {
        const cfg = parseSerie(dataInteracciones);
        if (!cfg.labels.length) return;
        const ctx = document.getElementById('graficoInteracciones').getContext('2d');
        new Chart(ctx, {
            type: 'doughnut',
            data: { labels: cfg.labels, datasets: [{ data: cfg.values, backgroundColor: colores(cfg.labels.length) }] },
            options: { responsive: true, plugins: { legend: { position: 'bottom' } } }
        });
    })();

    // Pólizas por producto (bar horizontal si muchas categorías)
    (function () {
        const cfg = parseSerie(dataPolizasTipo);
        if (!cfg.labels.length) return;
        const ctx = document.getElementById('graficoPolizasTipo').getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: { labels: cfg.labels, datasets: [{ label: 'Pólizas', data: cfg.values, backgroundColor: colores(cfg.labels.length) }] },
            options: { responsive: true, indexAxis: 'y', scales: { x: { beginAtZero: true } }, plugins: { legend: { display: false } } }
        });
    })();

    // Pólizas próximas a vencer (bar)
    (function () {
        const cfg = parseSerie(dataPolizasProximas);
        const canvas = document.getElementById('graficoProximasVencer');
        if (!canvas) return;

        if (!cfg.labels.length) {
            // Mostrar mensaje vacío
            const card = canvas.closest('.grafico-card');
            if (card) {
                // Oculta el canvas si no hay datos
                canvas.style.display = 'none';
                const msg = document.createElement('div');
                msg.className = 'empty-state';
                msg.textContent = 'No hay pólizas próximas a vencer';
                card.appendChild(msg);
            }
            return;
        }

        const ctx = canvas.getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: { labels: cfg.labels, datasets: [{ label: 'Próximas a vencer', data: cfg.values, backgroundColor: colores(cfg.labels.length) }] },
            options: { responsive: true, scales: { y: { beginAtZero: true } }, plugins: { legend: { display: false } } }
        });
    })();

    // Pólizas nuevas por mes (line)
    (function () {
        const cfg = parseSerie(dataPolizasNuevas, 'mes', 'count');
        if (!cfg.labels.length) return;
        const ctx = document.getElementById('graficoPolizasNuevas').getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: cfg.labels,
                datasets: [{
                    label: 'Nuevas por mes',
                    data: cfg.values,
                    backgroundColor: 'rgba(37,99,235,0.12)',
                    borderColor: '#2563eb',
                    fill: true,
                    tension: 0.3,
                    pointRadius: 4
                }]
            },
            options: {
                responsive: true,
                scales: { y: { beginAtZero: true, ticks: { precision: 0 } } },
                plugins: { legend: { display: false } }
            }
        });
    })();

    // Pólizas por producto (histograma vertical)
    (function () {
        const el = document.getElementById('graficoPolizasTipo');
        if (!el) return;
        const cfg = parseSerie(dataPolizasTipo);
        if (!cfg.labels.length) return;
        new Chart(el.getContext('2d'), {
            type: 'bar',
            data: {
                labels: cfg.labels,
                datasets: [{
                    label: 'Pólizas',
                    data: cfg.values,
                    backgroundColor: colores(cfg.labels.length),
                    maxBarThickness: 60,
                    borderRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: { title: { display: true, text: 'Producto' }, ticks: { autoSkip: false, maxRotation: 45 } },
                    y: { beginAtZero: true, title: { display: true, text: 'Cantidad' }, ticks: { precision: 0 } }
                },
                plugins: { legend: { display: false } }
            }
        });
    })();

    // Pólizas próximas a vencer (30 días) - barras verticales
    (function () {
        const el = document.getElementById('graficoProximasVencer');
        if (!el) return;
        const cfg = parseSerie(dataPolizasProximas);
        if (!cfg.labels.length) return;
        new Chart(el.getContext('2d'), {
            type: 'bar',
            data: {
                labels: cfg.labels,
                datasets: [{
                    label: 'Próximas a vencer',
                    data: cfg.values,
                    backgroundColor: colores(cfg.labels.length),
                    maxBarThickness: 60,
                    borderRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: { beginAtZero: true, ticks: { precision: 0 } }
                },
                plugins: { legend: { display: false } }
            }
        });
    })();

    // Pólizas nuevas por mes (línea)
    (function () {
        const el = document.getElementById('graficoPolizasNuevas');
        if (!el) return;
        const cfg = parseSerie(dataPolizasNuevas, 'mes', 'count');
        if (!cfg.labels.length) return;
        new Chart(el.getContext('2d'), {
            type: 'line',
            data: {
                labels: cfg.labels,
                datasets: [{
                    label: 'Nuevas por mes',
                    data: cfg.values,
                    backgroundColor: 'rgba(37,99,235,0.12)',
                    borderColor: '#2563eb',
                    fill: true,
                    tension: 0.3,
                    pointRadius: 3
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: { y: { beginAtZero: true, ticks: { precision: 0 } } },
                plugins: { legend: { display: false } }
            }
        });
    })();
});
