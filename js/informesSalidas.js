document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM fully loaded for Salidas de Inventario');

    const btnInformes = document.getElementById('btnInformes');
    const informesPanel = document.getElementById('informesPanel');
    const btnCerrarInformes = informesPanel.querySelector('.btn-close');
    const informesList = document.getElementById('informesList');
    const informesSalidasPanel = document.getElementById('informesSalidasPanel');
    const tableBody = document.querySelector('#salidasInventarioTable tbody');
    const searchInput = document.getElementById('searchInput');

    const formSalidasInventario = document.getElementById('salidasInventarioForm');
    const btnBuscarSalidas = document.getElementById('btnBuscarSalidas');

    function cargarPanelInformes() {
        console.log('Cargando panel de informes');
        informesPanel.style.display = 'block';
    }

    function cerrarPanelInformes() {
        console.log('Cerrando panel de informes');
        informesPanel.style.display = 'none';
    }

    function cargarPanelSalidasInventarioInformes() {
        console.log('Cargando panel de salidas de inventario');
        informesSalidasPanel.style.display = 'block';
        informesPanel.style.display = 'none';
    }

    function cerrarPanelSalidasInventarioInformes() {
        console.log('Cerrando panel de salidas de inventario');
        informesSalidasPanel.style.display = 'none';
    }

    btnInformes.addEventListener('click', cargarPanelInformes);
    btnCerrarInformes.addEventListener('click', cerrarPanelInformes);

    // Manejar clics en los elementos del submenú
    informesList.addEventListener('click', function(event) {
        const subMenuItem = event.target.closest('.sub-menu li');
        if (subMenuItem) {
            const informeType = subMenuItem.textContent.trim();
            console.log('Tipo de informe seleccionado:', informeType);
            if (informeType === 'Salidas de inventario') {
                cargarPanelSalidasInventarioInformes();
            }
            // Aquí puedes agregar más condiciones para otros tipos de informes
        }
    });

    // Configurar el panel de Salidas de Inventario
    const btnCerrarSalidasInventario = document.querySelector('#informesSalidasPanel .btn-close');

    if (btnCerrarSalidasInventario) {
        btnCerrarSalidasInventario.addEventListener('click', cerrarPanelSalidasInventarioInformes);
    } else {
        console.error('Botón de cerrar salidas de inventario no encontrado');
    }

    if (formSalidasInventario) {
        formSalidasInventario.addEventListener('submit', function(e) {
            e.preventDefault();
            console.log('Formulario de salidas de inventario enviado');
            buscarSalidas();
        });
    } else {
        console.error('Formulario de salidas de inventario no encontrado');
    }

    if (btnBuscarSalidas) {
        btnBuscarSalidas.addEventListener('click', function(e) {
            e.preventDefault();
            console.log('Botón de búsqueda clickeado');
            buscarSalidas();
        });
    } else {
        console.error('Botón de búsqueda no encontrado');
    }

    function buscarSalidas() {
        const fechaInicio = document.getElementById('fechaInicio').value;
        const fechaFin = document.getElementById('fechaFin').value;
        console.log('Iniciando búsqueda con fechas:', fechaInicio, fechaFin);
    
        if (fechaInicio && fechaFin) {
            const url = `http://127.0.0.1:5000/api/salidas_inventario_informes?fecha_inicio=${fechaInicio}&fecha_fin=${fechaFin}`;
            console.log('URL de la solicitud:', url);
    
            fetch(url)
                .then(response => {
                    console.log('Respuesta recibida:', response);
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    return response.json();
                })
                .then(data => {
                    console.log('Datos recibidos:', data);
                    if (data.salidas && Array.isArray(data.salidas)) {
                        mostrarSalidasInformes(data.salidas);
                    } else {
                        console.error('Estructura de datos inesperada:', data);
                        throw new Error('Los datos recibidos no tienen el formato esperado');
                    }
                })
                .catch(error => {
                    console.error('Error al cargar salidas:', error);
                    Swal.fire('Error', `Hubo un error al cargar los datos: ${error.message}`, 'error');
                });
        } else {
            console.error('Fechas no seleccionadas');
            Swal.fire('Error', 'Por favor, seleccione ambas fechas antes de buscar.', 'error');
        }
    }

    function mostrarSalidasInformes(salidas) {
        const tableBody = document.querySelector('#salidasInventarioTable tbody');
        tableBody.innerHTML = '';
        
        if (salidas.length === 0) {
            tableBody.innerHTML = '<tr><td colspan="7">No se encontraron datos para el rango de fechas seleccionado.</td></tr>';
            return;
        }
    
        salidas.forEach(salida => {
            const row = `
                <tr>
                    <td>${salida.Numero}</td>
                    <td>${salida.Fecha}</td>
                    <td>${salida.IdReferencia}</td>
                    <td>${salida.Descripcion}</td>
                    <td>${salida.Cantidad.toFixed(2)}</td>
                    <td>${salida.Valor.toFixed(2)}</td>
                    <td>${salida.Total.toFixed(2)}</td>
                </tr>
            `;
            tableBody.innerHTML += row;
        });
    }

    // Función de búsqueda
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            console.log('Búsqueda realizada:', this.value);
            const searchTerm = this.value.toLowerCase();
            const rows = tableBody.querySelectorAll('tr');
            
            rows.forEach(row => {
                const text = row.textContent.toLowerCase();
                row.style.display = text.includes(searchTerm) ? '' : 'none';
            });
        });
    } else {
        console.error('Campo de búsqueda no encontrado');
    }

    console.log('Configuración de eventos completada para Salidas de Inventario');
});