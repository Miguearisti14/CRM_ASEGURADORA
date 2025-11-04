document.addEventListener("DOMContentLoaded", function () {
    if (!window.datosReportes) return;

    const { productosLabels, productosCount, estadosLabels, estadosCount } = window.datosReportes;

    // Gráfico de pólizas por producto
    const ctxPolizas = document.getElementById("graficoPolizas");
    new Chart(ctxPolizas, {
        type: "pie",
        data: {
            labels: productosLabels,
            datasets: [
                {
                    data: productosCount,
                    backgroundColor: [
                        "#42a5f5",
                        "#66bb6a",
                        "#ffa726",
                        "#ab47bc",
                        "#ef5350",
                        "#26c6da",
                        "#8d6e63"
                    ],
                },
            ],
        },
        options: {
            plugins: {
                legend: {
                    position: "bottom",
                },
            },
        },
    });

    // Gráfico de reclamaciones por estado
    const ctxReclamaciones = document.getElementById("graficoReclamaciones");
    new Chart(ctxReclamaciones, {
        type: "bar",
        data: {
            labels: estadosLabels,
            datasets: [
                {
                    label: "Cantidad",
                    data: estadosCount,
                    backgroundColor: "#1976d2",
                },
            ],
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: { stepSize: 1 },
                },
            },
            plugins: {
                legend: { display: false },
            },
        },
    });
});
