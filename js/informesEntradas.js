document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM fully loaded para Informes de Entradas de Inventario');

    const btnInformes = document.getElementById('btnInformes');
    const informesPanel = document.getElementById('informesPanel');
    const btnCerrarInformes = informesPanel.querySelector('.btn-close');
    const informesList = document.getElementById('informesList');
    const informesEntradasPanel = document.getElementById('informesEntradasPanel');
    const tableBody = document.querySelector('#entradasInventarioTable tbody');
    const searchInput = document.getElementById('searchInput');
    const url = `http://127.0.0.1:5000/api/entradas_informes?fecha_inicio=${fechaInicio}&fecha_fin=${fechaFin}`;
    const formEntradasInventario = document.getElementById('entradasInventarioForm');
    const btnBuscarEntradas = document.getElementById('btnBuscarEntradas');

    function cargarPanelInformes() {
        console.log('Cargando panel de informes');
        informesPanel.style.display = 'block';
    }

    function cerrarPanelInformes() {
        console.log('Cerrando panel de informes');
        informesPanel.style.display = 'none';
    }

    function cargarPanelEntradasInventarioInformes() {
        console.log('Cargando panel de entradas de inventario');
        informesEntradasPanel.style.display = 'block';
        informesPanel.style.display = 'none';
    }

    function cerrarPanelEntradasInventarioInformes() {
        console.log('Cerrando panel de entradas de inventario');
        informesEntradasPanel.style.display = 'none';
    }

    btnInformes.addEventListener('click', cargarPanelInformes);
    btnCerrarInformes.addEventListener('click', cerrarPanelInformes);

    // Manejar la expansión del menú de Inventario
    informesList.addEventListener('click', function(event) {
        const mainItem = event.target.closest('.main-item');
        if (mainItem) {
            console.log('Clic en elemento principal del menú');
            const subMenu = mainItem.nextElementSibling;
            const chevron = mainItem.querySelector('.fas');

            if (subMenu.style.display === 'none' || subMenu.style.display === '') {
                subMenu.style.display = 'block';
                chevron.classList.remove('fa-chevron-down');
                chevron.classList.add('fa-chevron-up');
            } else {
                subMenu.style.display = 'none';
                chevron.classList.remove('fa-chevron-up');
                chevron.classList.add('fa-chevron-down');
            }
        }
    });

    // Manejar clics en los elementos del submenú
    informesList.addEventListener('click', function(event) {
        const subMenuItem = event.target.closest('.sub-menu li');
        if (subMenuItem) {
            const informeType = subMenuItem.textContent.trim();
            console.log('Tipo de informe seleccionado:', informeType);
            if (informeType === 'Entradas de inventario') {
                cargarPanelEntradasInventarioInformes();
            }
            // Aquí puedes agregar más condiciones para otros tipos de informes
        }
    });

    // Añadir efecto hover
    const allItems = informesPanel.querySelectorAll('.main-item, .sub-menu li');
    allItems.forEach(item => {
        item.addEventListener('mouseenter', function() {
            this.style.backgroundColor = '#e9ecef';
        });
        item.addEventListener('mouseleave', function() {
            this.style.backgroundColor = '';
        });
    });

    // Configurar el panel de Entradas de Inventario
    const btnCerrarEntradasInventario = document.querySelector('#informesEntradasPanel .btn-close');

    if (btnCerrarEntradasInventario) {
        btnCerrarEntradasInventario.addEventListener('click', cerrarPanelEntradasInventarioInformes);
    } else {
        console.error('Botón de cerrar entradas de inventario no encontrado');
    }

    if (formEntradasInventario) {
        formEntradasInventario.addEventListener('submit', function(e) {
            e.preventDefault();
            console.log('Formulario de entradas de inventario enviado');
            buscarEntradas();
        });
    } else {
        console.error('Formulario de entradas de inventario no encontrado');
    }

    if (btnBuscarEntradas) {
        btnBuscarEntradas.addEventListener('click', function(e) {
            e.preventDefault();
            console.log('Botón de búsqueda clickeado');
            buscarEntradas();
        });
    } else {
        console.error('Botón de búsqueda no encontrado');
    }

    function buscarEntradas() {
        const fechaInicio = document.getElementById('fechaInicio').value;
        const fechaFin = document.getElementById('fechaFin').value;
        console.log('Iniciando búsqueda con fechas:', fechaInicio, fechaFin);
    
        if (fechaInicio && fechaFin) {
            const url = `http://127.0.0.1:5000/api/entradas_informes?fecha_inicio=${fechaInicio}&fecha_fin=${fechaFin}`;
            console.log('URL de la solicitud:', url);
    
            fetch(url)
                .then(response => {
                    console.log('Respuesta recibida. Status:', response.status);
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    return response.json();
                })
                .then(data => {
                    console.log('Datos recibidos:', JSON.stringify(data, null, 2));
                    if (data.entradas) {
                        console.log('Número de entradas recibidas:', data.entradas.length);
                        mostrarEntradasInformes(data.entradas);
                    } else {
                        console.error('Estructura de datos inesperada:', data);
                        throw new Error('Los datos recibidos no tienen el formato esperado');
                    }
                })
                .catch(error => {
                    console.error('Error al cargar entradas:', error);
                    console.error('Tipo de error:', error.name);
                    console.error('Mensaje de error:', error.message);
                    console.error('Stack trace:', error.stack);
                    Swal.fire('Error', `Hubo un error al cargar los datos: ${error.message}. Por favor, revise la consola para más detalles.`, 'error');
                });
        } else {
            console.error('Fechas no seleccionadas');
            Swal.fire('Error', 'Por favor, seleccione ambas fechas antes de buscar.', 'error');
        }
    }

    function mostrarEntradasInformes(entradas) {
        const tableBody = document.querySelector('#entradasInventarioTable tbody');
        tableBody.innerHTML = '';
        
        if (entradas.length === 0) {
            tableBody.innerHTML = '<tr><td colspan="7">No se encontraron datos para el rango de fechas seleccionado.</td></tr>';
            return;
        }
    
        entradas.forEach(entrada => {
            const row = `
                <tr>
                    <td>${entrada.Numero}</td>
                    <td>${entrada.Fecha}</td>
                    <td>${entrada.IdReferencia}</td>
                    <td>${entrada.Descripcion}</td>
                    <td>${entrada.Cantidad.toFixed(2)}</td>
                    <td>${entrada.Valor.toFixed(2)}</td>
                    <td>${entrada.Total.toFixed(2)}</td>
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

    console.log('Configuración de eventos completada para Informes de Entradas de Inventario');
});