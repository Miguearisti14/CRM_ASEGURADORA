document.addEventListener("DOMContentLoaded", () => {
    const departamentoSelect = document.getElementById("departamento");
    const ciudadSelect = document.getElementById("ciudad");

    departamentoSelect.addEventListener("change", async () => {
        const departamentoId = departamentoSelect.value;

        // Reiniciar opciones
        ciudadSelect.innerHTML = '<option value="">Cargando...</option>';

        if (departamentoId) {
            try {
                const response = await fetch(`/ajax/ciudades/${departamentoId}/`);
                const ciudades = await response.json();

                ciudadSelect.innerHTML = '<option value="">Selecciona una ciudad</option>';
                ciudades.forEach(ciudad => {
                    const option = document.createElement("option");
                    option.value = ciudad.id;
                    option.textContent = ciudad.descripcion;
                    ciudadSelect.appendChild(option);
                });
            } catch (error) {
                ciudadSelect.innerHTML = '<option value="">Error al cargar ciudades</option>';
                console.error("Error cargando ciudades:", error);
            }
        } else {
            ciudadSelect.innerHTML = '<option value="">Selecciona primero un departamento</option>';
        }
    });
});
