document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM completamente cargado para Salidas a Bodegas");

    const inventarioLista = document.getElementById('inventarioLista');
    const salidasInventarioPanel = document.getElementById('salidasInventarioPanel');
    const tablaSalidas = document.querySelector('#detallesSalidaTable tbody');
    const modal = document.getElementById('referenciasModal');
    const span = document.getElementsByClassName("close")[0];
    const buscarReferenciaInput = document.getElementById('buscarReferencia');

    // Botones
    const btnNuevoSalida = document.getElementById('btnNuevoSalida');
    const btnGuardarSalida = document.getElementById('btnGuardarSalida');
    const btnEditarSalida = document.getElementById('btnEditarSalida');
    const btnCancelarSalida = document.getElementById('btnCancelarSalida');
    const btnBuscarSalida = document.getElementById('btnBuscarSalida');
    const btnCerrarSalida = document.getElementById('btnCerrarSalida');

    function mostrarSalidasInventario() {
        console.log("Función mostrarSalidasInventario llamada");
        ocultarTodosPaneles();
        if (salidasInventarioPanel) {
            salidasInventarioPanel.style.display = 'block';
            console.log("Panel de Salidas mostrado");
            cargarBodegasDisponibles();
            cargarConsecutivosSalidasInventario();
            inicializarTablaSalidas();
        } else {
            console.error("El panel de Salidas de Inventario no se encontró");
        }
    }

    function ocultarTodosPaneles() {
        console.log("Ocultando todos los paneles");
        const paneles = document.querySelectorAll('.panel');
        paneles.forEach(panel => {
            panel.style.display = 'none';
            console.log(`Panel ocultado: ${panel.id}`);
        });
    }

    function agregarFilaVacia() {
        console.log("Agregando fila vacía");
        const newRow = tablaSalidas.insertRow();
        for (let i = 0; i < 10; i++) {
            const cell = newRow.insertCell();
            if (i === 0) {
                cell.setAttribute('tabindex', '0');
                cell.addEventListener('keydown', function(e) {
                    if (e.key === 'Enter') {
                        e.preventDefault();
                        console.log("Enter presionado en la primera columna");
                        abrirModalReferencias();
                    }
                });
            }
        }
        // Añadir botón de eliminar
        const deleteCell = newRow.insertCell();
        const deleteBtn = document.createElement('button');
        deleteBtn.textContent = 'X';
        deleteBtn.className = 'btn-eliminar';
        deleteBtn.onclick = function() {
            tablaSalidas.removeChild(newRow);
            actualizarTotales();
        };
        deleteCell.appendChild(deleteBtn);
    }

    function inicializarTablaSalidas() {
        console.log("Inicializando tabla de salidas");
        tablaSalidas.innerHTML = '';
        agregarFilaVacia();
    }

    tablaSalidas.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && e.target.cellIndex === 0) {
            e.preventDefault();
            console.log("Enter presionado en la primera columna (evento de tabla)");
            abrirModalReferencias();
        }
    });

    function abrirModalReferencias() {
        console.log("Abriendo modal de referencias");
        const idBodega = document.getElementById('bodegaSalida').value;
        if (!idBodega) {
            Swal.fire({
                title: 'Atención',
                text: 'Por favor, seleccione una bodega primero.',
                icon: 'warning',
                confirmButtonText: 'Entendido'
            });
            return;
        }
        const modal = document.getElementById('busquedaReferenciasModal');
        if (modal) {
            modal.style.display = "block";
            cargarReferencias();
        } else {
            console.error("El modal de referencias no se encontró");
        }
    }

    function cargarBodegasDisponibles() {
        console.log("Cargando bodegas disponibles");
        fetch('http://127.0.0.1:5000/api/bodegas_disponibles')
            .then(response => response.json())
            .then(data => {
                console.log("Bodegas cargadas:", data);
                const selectBodega = document.getElementById('bodegaSalida');
                selectBodega.innerHTML = '<option value="">Seleccione una bodega</option>';
                data.forEach(bodega => {
                    const option = document.createElement('option');
                    option.value = bodega.IdBodega;
                    option.textContent = bodega.Descripcion;
                    selectBodega.appendChild(option);
                });
            })
            .catch(error => console.error('Error al cargar bodegas:', error));
    }

    function cargarConsecutivosSalidasInventario() {
        console.log("Cargando consecutivos de salidas de inventario");
        fetch('http://127.0.0.1:5000/api/consecutivos_salidas_inventario')
            .then(response => response.json())
            .then(data => {
                console.log("Consecutivos cargados:", data);
                const select = document.getElementById('consecutivoSalida');
                select.innerHTML = '<option value="">Seleccione un consecutivo</option>';
                data.forEach(consecutivo => {
                    const option = document.createElement('option');
                    option.value = consecutivo.IdConsecutivo;
                    option.textContent = `${consecutivo.Descripcion} - ${consecutivo.Prefijo}${consecutivo.Actual.padStart(2, '0')}`;
                    select.appendChild(option);
                });
    
                if (data.length > 0) {
                    select.value = data[0].IdConsecutivo;
                    actualizarNumeroSalida(data[0]);
                }
            })
            .catch(error => console.error('Error al cargar consecutivos:', error));
    }

    function actualizarNumeroSalida(consecutivo) {
        console.log("Actualizando número de salida", consecutivo);
        const numeroSalida = document.getElementById('numeroSalida');
        numeroSalida.value = `${consecutivo.Prefijo}${consecutivo.Actual.padStart(2, '0')}`;
    }

    document.getElementById('consecutivoSalida').addEventListener('change', function() {
        const selectedOption = this.options[this.selectedIndex];
        const [descripcion, numero] = selectedOption.textContent.split(' - ');
        document.getElementById('numeroSalida').value = numero;
    });

    function cargarReferencias(filtro = '') {
        const idBodega = document.getElementById('bodegaSalida').value;
        if (!idBodega) {
            Swal.fire("Por favor, seleccione una bodega primero.");
            return;
        }
    
        console.log("Cargando referencias con filtro:", filtro);
        fetch(`http://127.0.0.1:5000/api/referencias?filtro=${encodeURIComponent(filtro)}&idBodega=${idBodega}`)
            .then(response => response.json())
            .then(data => {
                console.log("Referencias cargadas:", data);
                const tabla = document.querySelector('#referenciasTable tbody');
                tabla.innerHTML = '';
                data.forEach(ref => {
                    let row = tabla.insertRow();
                    row.innerHTML = `
                        <td>${ref.IdReferencia}</td>
                        <td>${ref.Referencia}</td>
                        <td>${ref.PrecioVenta1}</td>
                        <td>${ref.IVA}</td>
                        <td>${ref.Ubicacion}</td>
                        <td>${ref.idbodega}</td>
                        <td>${ref.IdUnidad}</td>
                    `;
                    row.addEventListener('click', () => seleccionarReferencia(ref));
                });
            })
            .catch(error => console.error('Error al cargar referencias:', error));
    }

    // Función para seleccionar una referencia
    function seleccionarReferencia(referencia) {
        console.log("Referencia seleccionada:", referencia);
        
        const saldoDisponible = parseFloat(referencia.Saldo);
        if (saldoDisponible <= 0) {
            Swal.fire({
                title: 'Inventario Insuficiente',
                text: `La referencia ${referencia.IdReferencia} no tiene inventario disponible. Saldo disponible: ${saldoDisponible}, por favor verifique!`,
                icon: 'error',
                confirmButtonText: 'Entendido'
            });
            return;
        }
    
        agregarProductoATabla(referencia, saldoDisponible);
        document.getElementById('busquedaReferenciasModal').style.display = 'none';
    }

    // Función para agregar un producto a la tabla
    function agregarProductoATabla(referencia, saldoDisponible) {
        const tbody = document.querySelector('#detallesSalidaTable tbody');
        const newRow = tbody.insertRow();
        newRow.innerHTML = `
            <td>${referencia.IdReferencia}</td>
            <td>${referencia.Referencia}</td>
            <td>${referencia.IdUnidad}</td>
            <td contenteditable="true">1</td>
            <td contenteditable="true">${referencia.PrecioVenta1}</td>
            <td contenteditable="true">0</td>
            <td contenteditable="true">0</td>
            <td contenteditable="true">0</td>
            <td contenteditable="true">0</td>
            <td>${referencia.PrecioVenta1}</td>
            <td><button class="btn-eliminar">X</button></td>
        `;

        newRow.dataset.saldoDisponible = saldoDisponible;

        newRow.querySelector('.btn-eliminar').addEventListener('click', function() {
            tbody.removeChild(newRow);
            actualizarTotales();
        });

        const editableCells = newRow.querySelectorAll('td[contenteditable="true"]');
        editableCells.forEach(cell => {
            cell.addEventListener('input', () => {
                actualizarSubtotalFila(newRow);
                actualizarTotales();
            });
        });

        actualizarSubtotalFila(newRow);
        actualizarTotales();
    }

    function actualizarSubtotalFila(row) {
        const cantidad = parseFloat(row.cells[3].textContent) || 0;
        const valor = parseFloat(row.cells[4].textContent) || 0;
        const subtotal = cantidad * valor;
        row.cells[9].textContent = subtotal.toFixed(2);
        actualizarTotales(); // Llamamos a actualizarTotales después de cambiar el subtotal
    }

    function actualizarTotales() {
        let totalUnidades = 0;
        let subtotal = 0;
        let totalImpoconsumo = 0;
        let totalIPC = 0;
        let totalIBUA = 0;
        let totalICUI = 0;
    
        document.querySelectorAll('#detallesSalidaTable tbody tr').forEach(row => {
            const cantidad = parseFloat(row.cells[3].textContent) || 0;
            const valor = parseFloat(row.cells[4].textContent) || 0;
            const impoconsumo = parseFloat(row.cells[5].textContent) || 0;
            const ipc = parseFloat(row.cells[6].textContent) || 0;
            const imp_ibua = parseFloat(row.cells[7].textContent) || 0;
            const imp_icui = parseFloat(row.cells[8].textContent) || 0;
    
            totalUnidades += cantidad;
            subtotal += cantidad * valor;
            totalImpoconsumo += impoconsumo;
            totalIPC += ipc;
            totalIBUA += imp_ibua;
            totalICUI += imp_icui;
        });
    
        const totalDocumento = subtotal + totalImpoconsumo + totalIPC + totalIBUA + totalICUI;
    
        document.getElementById('totalUnidadesSalida').value = totalUnidades.toFixed(2);
        document.getElementById('subtotalSalida').value = subtotal.toFixed(2);
        document.getElementById('totalImpoconsumoSalida').value = totalImpoconsumo.toFixed(2);
        document.getElementById('totalIPCSalida').value = totalIPC.toFixed(2);
        document.getElementById('totalIBUASalida').value = totalIBUA.toFixed(2);
        document.getElementById('totalICUISalida').value = totalICUI.toFixed(2);
        document.getElementById('totalDocumentoSalida').value = totalDocumento.toFixed(2);
    }

    function nuevoSalida() {
        console.log("Iniciando nueva salida");
        limpiarFormularioSalida();
        document.getElementById('fechaSalida').valueAsDate = new Date();
        document.getElementById('fechaCreacionSalida').valueAsDate = new Date();
        document.querySelector('#detallesSalidaTable').style.display = 'table';
        inicializarTablaSalidas();
        habilitarCamposSalida(true);
        cargarUltimoConsecutivoSalida();
    }

    // Función para guardar la salida
    function guardarSalida() {
        console.log("Guardando salida");
        
        const fechaActual = new Date();
        const salida1 = {
            Numero: document.getElementById('numeroSalida').value,
            Mes: obtenerMes(document.getElementById('fechaSalida').value),
            Anulado: document.getElementById('anuladoSalida').checked ? 1 : 0,
            IdBodega: document.getElementById('bodegaSalida').value,
            CuentaDebito: '',
            CuentaCredito: '',
            Observaciones: document.getElementById('observacionesSalida').value,
            FechaCreacion: fechaActual.toISOString(),
            IdUsuario: 'MIG', // Asume que tienes el usuario actual
            Recibe: '',
            idproyecto: '',
            fechamodificacion: fechaActual.toISOString(),
            IdConsecutivo: document.getElementById('consecutivoSalida').value,
            op: fechaActual.toISOString().split('T')[0],
            fecha: document.getElementById('fechaSalida').value,
            subtotal: parseFloat(document.getElementById('subtotalSalida').value) || 0,
            total_iva: parseFloat(document.getElementById('totalIVASalida').value) || 0,
            total_impoconsumo: parseFloat(document.getElementById('totalImpoconsumoSalida').value) || 0,
            total_ipc: parseFloat(document.getElementById('totalIPCSalida').value) || 0,
            total_ibua: parseFloat(document.getElementById('totalIBUASalida').value) || 0,
            total_icui: parseFloat(document.getElementById('totalICUISalida').value) || 0,
            total: parseFloat(document.getElementById('totalDocumentoSalida').value) || 0
        };
    
        const salidas2 = [];
        document.querySelectorAll('#detallesSalidaTable tbody tr').forEach((row, index) => {
            const idReferencia = row.cells[0].textContent.trim();
            if (idReferencia) {  // Solo agregar si hay un IdReferencia
                salidas2.push({
                    ID: `${salida1.Numero}_${(index + 1).toString().padStart(3, '0')}`,
                    Numero: salida1.Numero,
                    IdReferencia: idReferencia,
                    Descripcion: row.cells[1].textContent.trim(),
                    Cantidad: parseFloat(row.cells[3].textContent) || 0,
                    Valor: parseFloat(row.cells[4].textContent) || 0,
                    IVA: 0,
                    Descuento: 0,
                    lote: '',
                    idunidad: row.cells[2].textContent.trim(),
                    impoconsumo: parseFloat(row.cells[5].textContent) || 0,
                    ipc: parseFloat(row.cells[6].textContent) || 0,
                    imp_ibua: parseFloat(row.cells[7].textContent) || 0,
                    imp_icui: parseFloat(row.cells[8].textContent) || 0
                });
            }
        });
    
        console.log('Datos a enviar:', JSON.stringify({ salida1, salidas2 }, null, 2));
    
        fetch('http://127.0.0.1:5000/api/guardar_salida', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ salida1, salidas2 })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                Swal.fire({
                    title: 'Éxito',
                    text: 'Salida guardada con éxito',
                    icon: 'success',
                    confirmButtonText: 'OK'
                });
                actualizarConsecutivoSalida(); // Llamar aquí después de guardar
                limpiarFormularioSalida();
                habilitarCamposSalida(false);
            } else {
                Swal.fire({
                    title: 'Error',
                    text: 'Error al guardar la salida: ' + data.message,
                    icon: 'error',
                    confirmButtonText: 'OK'
                });
            }
        })
        .catch(error => {
            console.error('Error:', error);
            Swal.fire({
                title: 'Error',
                text: 'Error al guardar la salida',
                icon: 'error',
                confirmButtonText: 'OK'
            });
        });
    }

    function editarSalida() {
        console.log("Editando salida");
        habilitarCamposSalida(true);
    }

    function cancelarSalida() {
        console.log("Cancelando salida");
        limpiarFormularioSalida();
        habilitarCamposSalida(false);
    }

    function buscarSalida() {
        console.log("Buscando salida");
        // Implementar lógica para buscar salidas
    }

    function cerrarSalida() {
        console.log("Cerrando panel de salidas");
        salidasInventarioPanel.style.display = 'none';
    }

    function limpiarFormularioSalida() {
        console.log("Limpiando formulario de salida");
        document.getElementById('salidaInventarioForm').reset();
        inicializarTablaSalidas();
        
        ['totalUnidadesSalida', 'subtotalSalida', 'totalIVASalida', 'totalImpoconsumoSalida', 'totalICUISalida', 'totalIBUASalida', 'totalIPCSalida', 'totalDocumentoSalida'].forEach(id => {
            document.getElementById(id).value = '0.00';
        });
    }

    function habilitarCamposSalida(habilitar) {
        const campos = document.querySelectorAll('#salidaInventarioForm input, #salidaInventarioForm select, #salidaInventarioForm textarea');
        campos.forEach(campo => campo.disabled = !habilitar);
        
        btnNuevoSalida.disabled = habilitar;
        btnGuardarSalida.disabled = !habilitar;
        btnEditarSalida.disabled = true;
        btnCancelarSalida.disabled = !habilitar;
    }

    function cargarUltimoConsecutivoSalida() {
        fetch('http://127.0.0.1:5000/api/ultimo_consecutivo_salidas')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById('numeroSalida').value = data.ultimoConsecutivo;
            } else {
                console.error('Error al cargar el último consecutivo:', data.message);
            }
        })
        .catch(error => console.error('Error:', error));
    }

    function actualizarConsecutivoSalida() {
        fetch('http://127.0.0.1:5000/api/actualizar_consecutivo_salidas_inventario', {
            method: 'POST'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById('numeroSalida').value = data.nuevoConsecutivo;
                // Actualizar también el select de consecutivos
                const selectConsecutivo = document.getElementById('consecutivoSalida');
                const selectedOption = selectConsecutivo.options[selectConsecutivo.selectedIndex];
                if (selectedOption) {
                    const [descripcion, _] = selectedOption.textContent.split(' - ');
                    selectedOption.textContent = `${descripcion} - ${data.nuevoConsecutivo}`;
                }
            } else {
                console.error('Error al actualizar consecutivo:', data.message);
            }
        })
        .catch(error => console.error('Error:', error));
    }

    function obtenerMes(fecha) {
        const date = new Date(fecha);
        return `${date.getFullYear()}${(date.getMonth() + 1).toString().padStart(2, '0')}`;
    }

    // Event Listeners
    btnNuevoSalida.addEventListener('click', nuevoSalida);
    btnGuardarSalida.addEventListener('click', guardarSalida);

    // Event Listeners (continuación)
    btnEditarSalida.addEventListener('click', editarSalida);
    btnCancelarSalida.addEventListener('click', cancelarSalida);
    btnBuscarSalida.addEventListener('click', buscarSalida);
    btnCerrarSalida.addEventListener('click', cerrarSalida);

    if (inventarioLista) {
        inventarioLista.addEventListener('click', function(e) {
            console.log("Clic en inventarioLista");
            const targetElement = e.target.closest('li');
            if (!targetElement) {
                console.log("No se encontró un elemento li");
                return;
            }

            const text = targetElement.textContent.trim();
            console.log("Texto del elemento clickeado:", text);
            
            if (text === "Salidas a Bodegas") {
                console.log("Clic en Salidas a Bodegas detectado");
                mostrarSalidasInventario();
            }
        });
    } else {
        console.error("El elemento inventarioLista no se encontró");
    }

    const btnSalidasBodegas = document.getElementById('btnSalidasBodegas');
    if (btnSalidasBodegas) {
        console.log("Botón de Salidas a Bodegas encontrado");
        btnSalidasBodegas.addEventListener('click', function() {
            console.log("Clic en botón de Salidas a Bodegas");
            mostrarSalidasInventario();
        });
    } else {
        console.error("El botón de Salidas a Bodegas no se encontró");
    }

    // Manejo del modal de referencias
    if (span) {
        span.onclick = function() {
            modal.style.display = "none";
        }
    }

    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }

    buscarReferenciaInput.addEventListener('input', function() {
        cargarReferencias(this.value);
    });

    document.getElementById('btnBuscarReferencia').addEventListener('click', function() {
        const filtro = document.getElementById('buscarReferencia').value;
        cargarReferencias(filtro);
    });

    // Manejo de edición en línea para la tabla de salidas
    tablaSalidas.addEventListener('dblclick', function(e) {
        const cell = e.target;
        if (cell.cellIndex >= 3 && cell.cellIndex <= 9) { // Solo celdas editables
            const originalContent = cell.textContent;
            cell.contentEditable = true;
            cell.focus();

            function finishEditing() {
                cell.contentEditable = false;
                if (isNaN(parseFloat(cell.textContent))) {
                    cell.textContent = originalContent;
                }
                actualizarTotales();
            }

            cell.addEventListener('blur', finishEditing, { once: true });
            cell.addEventListener('keydown', function(e) {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    finishEditing();
                }
            });
        }
    });

    // Inicialización
    habilitarCamposSalida(false);

    console.log("Configuración de Salidas a Bodegas completada");
});