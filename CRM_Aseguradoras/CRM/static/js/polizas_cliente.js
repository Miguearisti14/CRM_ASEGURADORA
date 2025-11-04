document.addEventListener('DOMContentLoaded', function () {
    const clienteSelect = document.getElementById('cliente');
    const polizaSelect = document.getElementById('poliza');

    clienteSelect.addEventListener('change', function () {
        const clienteDNI = this.value;
        polizaSelect.innerHTML = '<option value="">Selecciona una póliza</option>';

        if (!clienteDNI) return;

        fetch(`/polizas-cliente/${clienteDNI}/`)
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    console.error('Error:', data.error);
                    return;
                }

                data.forEach(poliza => {
                    const option = document.createElement('option');
                    option.value = poliza.id;
                    option.textContent = `${poliza.producto} - N°: ${poliza.id}`;
                    polizaSelect.appendChild(option);
                });
            })
            .catch(error => {
                console.error('Error:', error);
                polizaSelect.innerHTML = '<option value="">Error al cargar pólizas</option>';
            });
    });
});
