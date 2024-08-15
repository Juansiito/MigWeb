document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM cargado para trasladosBodegas.js");
    const inventarioLista = document.getElementById('inventarioLista');
    const trasladosInventarioPanel = document.getElementById('trasladosInventarioPanel');
    const tablaTraslados = document.querySelector('#detallesTrasladoTable tbody');
    const modal = document.getElementById('referenciasModal');
    const span = document.getElementsByClassName("close")[0];
    const buscarReferenciaInput = document.getElementById('buscarReferencia');

    // Botones
    const btnNuevoTraslado = document.getElementById('btnNuevoTraslado');
    const btnGuardarTraslado = document.getElementById('btnGuardarTraslado');
    const btnEditarTraslado = document.getElementById('btnEditarTraslado');
    const btnCancelarTraslado = document.getElementById('btnCancelarTraslado');
    const btnBuscarTraslado = document.getElementById('btnBuscarTraslado');
    const btnCerrarTraslado = document.getElementById('btnCerrarTraslado');

    function mostrarTrasladosInventario() {
        console.log("Mostrando Traslados a Bodegas");
        ocultarTodosPaneles();
        if (trasladosInventarioPanel) {
            trasladosInventarioPanel.style.display = 'block';
            cargarBodegasDisponibles();
            cargarConsecutivosTraslados();
            inicializarTablaTraslados();
        } else {
            console.error("El panel de Traslados de Inventario no se encontró");
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
        const newRow = tablaTraslados.insertRow();
        for (let i = 0; i < 11; i++) {
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
            tablaTraslados.removeChild(newRow);
            actualizarTotales();
        };
        deleteCell.appendChild(deleteBtn);
    }

    function inicializarTablaTraslados() {
        console.log("Inicializando tabla de traslados");
        tablaTraslados.innerHTML = '';
        agregarFilaVacia();
        actualizarTotales();
    }

    tablaTraslados.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && e.target.cellIndex === 0) {
            e.preventDefault();
            console.log("Enter presionado en la primera columna (evento de tabla)");
            abrirModalReferencias();
        }
    });

    function abrirModalReferencias() {
        console.log("Intentando abrir modal de referencias");
        const idBodegaOrigen = document.getElementById('bodegaOrigenTraslado').value;
        if (!idBodegaOrigen) {
            Swal.fire({
                title: 'Atención',
                text: 'Por favor, seleccione una bodega de origen primero.',
                icon: 'warning',
                confirmButtonText: 'Entendido',
                customClass: {
                    confirmButton: 'btn btn-primary'
                }
            });
            return;
        }
        
        const modal = document.getElementById('busquedaReferenciasModal');
        if (modal) {
            modal.style.display = "block";
            cargarReferenciasTraslados();
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
                const selectBodegaOrigen = document.getElementById('bodegaOrigenTraslado');
                const selectBodegaDestino = document.getElementById('bodegaDestinoTraslado');
                selectBodegaOrigen.innerHTML = '<option value="">Seleccione una bodega</option>';
                selectBodegaDestino.innerHTML = '<option value="">Seleccione una bodega</option>';
                data.forEach(bodega => {
                    const option = document.createElement('option');
                    option.value = bodega.IdBodega;
                    option.textContent = bodega.Descripcion;
                    selectBodegaOrigen.appendChild(option.cloneNode(true));
                    selectBodegaDestino.appendChild(option);
                });
            })
            .catch(error => console.error('Error al cargar bodegas:', error));
    }

    function cargarConsecutivosTraslados() {
        console.log("Cargando consecutivos de traslados de inventario");
        fetch('http://127.0.0.1:5000/api/consecutivos_traslados_inventario')
            .then(response => response.json())
            .then(data => {
                console.log("Consecutivos cargados:", data);
                const select = document.getElementById('consecutivoTraslado');
                select.innerHTML = '<option value="">Seleccione un consecutivo</option>';
                data.forEach(consecutivo => {
                    const option = document.createElement('option');
                    option.value = consecutivo.IdConsecutivo;
                    option.textContent = `${consecutivo.Descripcion} - ${consecutivo.Prefijo}${consecutivo.Actual.padStart(2, '0')}`;
                    select.appendChild(option);
                });
    
                if (data.length > 0) {
                    select.value = data[0].IdConsecutivo;
                    actualizarNumeroTraslado(data[0]);
                }
            })
            .catch(error => console.error('Error al cargar consecutivos:', error));
    }

    function actualizarNumeroTraslado(consecutivo) {
        console.log("Actualizando número de traslado", consecutivo);
        const numeroTraslado = document.getElementById('numeroTraslado');
        numeroTraslado.value = `${consecutivo.Prefijo}${consecutivo.Actual.padStart(2, '0')}`;
    }

    document.getElementById('consecutivoTraslado').addEventListener('change', function() {
        const selectedOption = this.options[this.selectedIndex];
        const [descripcion, numero] = selectedOption.textContent.split(' - ');
        document.getElementById('numeroTraslado').value = numero;
    });

    function cargarReferenciasTraslados(filtro = '') {
        const idBodega = document.getElementById('bodegaEntrada').value;
        console.log(`Cargando referencias para bodega ${idBodega} con filtro "${filtro}"`);
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

    function seleccionarReferencia(referencia) {
        console.log("Referencia seleccionada:", referencia);
        
        const saldoDisponible = parseFloat(referencia.saldo) || 0;
        console.log("Saldo disponible:", saldoDisponible);
    
        if (saldoDisponible <= 0) {
            Swal.fire({
                title: 'Inventario Insuficiente',
                text: `La referencia ${referencia.IdReferencia} no tiene inventario disponible. Saldo disponible: ${saldoDisponible}, por favor verifique!`,
                icon: 'warning',
                confirmButtonText: 'Entendido'
            });
            return;
        }
    
        agregarProductoATabla(referencia, saldoDisponible);
        document.getElementById('busquedaReferenciasModal').style.display = 'none';
    }

    function agregarProductoATabla(referencia, saldoDisponible) {
        const tbody = document.querySelector('#detallesTrasladoTable tbody');
        const newRow = tbody.insertRow();
        newRow.innerHTML = `
            <td>${referencia.IdReferencia}</td>
            <td>${referencia.Referencia}</td>
            <td>${referencia.IdUnidad}</td>
            <td contenteditable="true">1</td>
            <td contenteditable="true">${referencia.PrecioVenta1}</td>
            <td contenteditable="true">${referencia.IVA}</td>
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
        row.cells[10].textContent = subtotal.toFixed(2);
        console.log(`Subtotal actualizado: ${subtotal.toFixed(2)}`);
        actualizarTotales
    }

    function actualizarTotales() {
        console.log("Iniciando actualización de totales");
        let totalUnidades = 0;
        let subtotal = 0;
        let totalIVA = 0;
        let totalImpoconsumo = 0;
        let totalIPC = 0;
        let totalIBUA = 0;
        let totalICUI = 0;
    
        document.querySelectorAll('#detallesTrasladoTable tbody tr').forEach(row => {
            const cantidad = parseFloat(row.cells[3].textContent) || 0;
            const valor = parseFloat(row.cells[4].textContent) || 0;
            const iva = parseFloat(row.cells[5].textContent) || 0;
            const impoconsumo = parseFloat(row.cells[6].textContent) || 0;
            const ipc = parseFloat(row.cells[7].textContent) || 0;
            const imp_ibua = parseFloat(row.cells[8].textContent) || 0;
            const imp_icui = parseFloat(row.cells[9].textContent) || 0;
    
            totalUnidades += cantidad;
            const subtotalFila = cantidad * valor;
            subtotal += subtotalFila;
            totalIVA += subtotalFila * (iva / 100);
            totalImpoconsumo += cantidad * impoconsumo;
            totalIPC += cantidad * ipc;
            totalIBUA += cantidad * imp_ibua;
            totalICUI += cantidad * imp_icui;
    
            console.log(`Fila - Cantidad: ${cantidad}, Valor: ${valor}, Subtotal: ${subtotalFila}`);
        });
    
        const totalDocumento = subtotal + totalIVA + totalImpoconsumo + totalIPC + totalIBUA + totalICUI;
    
        console.log(`Totales calculados:`, {
            totalUnidades,
            subtotal,
            totalIVA,
            totalImpoconsumo,
            totalIPC,
            totalIBUA,
            totalICUI,
            totalDocumento
        });
    
        document.getElementById('totalUnidadesTraslados').value = totalUnidades.toFixed(2);
        document.getElementById('subtotalTraslados').value = subtotal.toFixed(2);
        document.getElementById('totalIVATraslados').value = totalIVA.toFixed(2);
        document.getElementById('totalImpoconsumoTraslados').value = totalImpoconsumo.toFixed(2);
        document.getElementById('totalICUITraslados').value = totalICUI.toFixed(2);
        document.getElementById('totalIBUATraslados').value = totalIBUA.toFixed(2);
        document.getElementById('totalIPCTraslados').value = totalIPC.toFixed(2);
        document.getElementById('totalDocumentoTraslados').value = totalDocumento.toFixed(2);
    
        console.log("Totales actualizados en los campos");
    }

    function nuevoTraslado() {
        console.log("Iniciando nuevo traslado");
        limpiarFormularioTraslado();
        document.getElementById('fechaTraslado').valueAsDate = new Date();
        document.getElementById('fechaCreacionTraslado').valueAsDate = new Date();
        document.querySelector('#detallesTrasladoTable').style.display = 'table';
        inicializarTablaTraslados();
        habilitarCamposTraslado(true);
        cargarUltimoConsecutivoTraslado();
        console.log("Nuevo traslado inicializado");
    }

    function guardarTraslado() {
        console.log("Guardando traslado");
        
        let inventarioInsuficiente = false;
        const productosInsuficientes = [];

        document.querySelectorAll('#detallesTrasladoTable tbody tr').forEach((row) => {
            const idReferencia = row.cells[0].textContent;
            const cantidad = parseFloat(row.cells[3].textContent) || 0;
            const saldoDisponible = parseFloat(row.dataset.saldoDisponible) || 0;

            if (cantidad > saldoDisponible) {
                inventarioInsuficiente = true;
                productosInsuficientes.push({
                    idReferencia,
                    saldoDisponible,
                    cantidadIngresada: cantidad
                });
            }
        });

        if (inventarioInsuficiente) {
            let mensaje = "No hay suficiente inventario para los siguientes productos:\n\n";
            productosInsuficientes.forEach(producto => {
                mensaje += `La referencia ${producto.idReferencia} no tiene inventario disponible. Saldo disponible: ${producto.saldoDisponible}, Cantidad ingresada: ${producto.cantidadIngresada}, por favor verifique!\n`;
            });
            Swal.fire(mensaje);
            return;
        }

        const fechaActual = new Date();
        const traslado1 = {
            Numero: document.getElementById('numeroTraslado').value,
            Mes: obtenerMes(document.getElementById('fechaTraslado').value),
            Anulado: document.getElementById('anuladoTraslado').checked ? 1 : 0,
            IdBodegaOrigen: document.getElementById('bodegaOrigenTraslado').value,
            IdBodegaDestino: document.getElementById('bodegaDestinoTraslado').value,
            Observaciones: document.getElementById('observacionesTraslado').value,
            FechaCreacion: fechaActual.toISOString(),
            IdUsuario: 'MIG', // Asume que tienes el usuario actual
            IdConsecutivo: document.getElementById('consecutivoTraslado').value,
            fecha: document.getElementById('fechaTraslado').value,
            subtotal: document.getElementById('subtotalTraslados').value,
            total_iva: document.getElementById('totalIVATraslados').value,
            total_impoconsumo: document.getElementById('totalImpoconsumoTraslados').value,
            total_ipc: document.getElementById('totalIPCTraslados').value,
            total_ibua: document.getElementById('totalIBUATraslados').value,
            total_icui: document.getElementById('totalICUITraslados').value,
            total: document.getElementById('totalDocumentoTraslados').value    
        };

        const traslados2 = [];
        document.querySelectorAll('#detallesTrasladoTable tbody tr').forEach((row, index) => {
            traslados2.push({
                ID: `${traslado1.Numero}_${(index + 1).toString().padStart(3, '0')}`,
                Numero: traslado1.Numero,
                IdReferencia: row.cells[0].textContent,
                Descripcion: row.cells[1].textContent,
                Cantidad: parseFloat(row.cells[3].textContent) || 0,
                Valor: parseFloat(row.cells[4].textContent) || 0,
                IVA: parseFloat(row.cells[5].textContent) || 0,
                impoconsumo: parseFloat(row.cells[6].textContent) || 0,
                ipc: parseFloat(row.cells[7].textContent) || 0,
                imp_ibua: parseFloat(row.cells[8].textContent) || 0,
                imp_icui: parseFloat(row.cells[9].textContent) || 0,
                idunidad: row.cells[2].textContent,
            });
        });

        console.log('Datos a enviar:', JSON.stringify({ traslado1, traslados2 }, null, 2));

        fetch('http://127.0.0.1:5000/api/guardar_traslado', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ traslado1, traslados2 })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                Swal.fire('Traslado guardado con éxito');
                actualizarConsecutivoTraslado();
                limpiarFormularioTraslado();
                habilitarCamposTraslado(false);
            } else {
                Swal.fire('Error al guardar el traslado: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            Swal.fire('Error al guardar el traslado');
        });
    }

    function editarTraslado() {
        console.log("Editando traslado");
        habilitarCamposTraslado(true);
    }

    function cancelarTraslado() {
        console.log("Cancelando traslado");
        limpiarFormularioTraslado();
        habilitarCamposTraslado(false);
    }

    function buscarTraslado() {
        console.log("Buscando traslado");
        // Implementar lógica para buscar traslados
    }

    function cerrarTraslado() {
        console.log("Cerrando panel de traslados");
        trasladosInventarioPanel.style.display = 'none';
    }

    function limpiarFormularioTraslado() {
        console.log("Limpiando formulario de traslado");
        document.getElementById('trasladoInventarioForm').reset();
        inicializarTablaTraslados();
        
        ['totalUnidadesTraslados', 'subtotalTraslados', 'totalIVATraslados', 
         'totalImpoconsumoTraslados', 'totalICUITraslados', 'totalIBUATraslados', 
         'totalIPCTraslados', 'totalDocumentoTraslados'].forEach(id => {
            document.getElementById(id).value = '0.00';
        });
        
        console.log("Formulario limpiado y totales actualizados");
    }

    function habilitarCamposTraslado(habilitar) {
        const campos = document.querySelectorAll('#trasladoInventarioForm input, #trasladoInventarioForm select, #trasladoInventarioForm textarea');
        campos.forEach(campo => campo.disabled = !habilitar);
        
        btnNuevoTraslado.disabled = habilitar;
        btnGuardarTraslado.disabled = !habilitar;
        btnEditarTraslado.disabled = true;
        btnCancelarTraslado.disabled = !habilitar;
    }

    function cargarUltimoConsecutivoTraslado() {
        fetch('http://127.0.0.1:5000/api/ultimo_consecutivo_traslados')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById('numeroTraslado').value = data.ultimoConsecutivo;
            } else {
                console.error('Error al cargar el último consecutivo:', data.message);
            }
        })
        .catch(error => console.error('Error:', error));
    }

    function actualizarConsecutivoTraslado() {
        fetch('http://127.0.0.1:5000/api/actualizar_consecutivo_traslados', {
            method: 'POST'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById('numeroTraslado').value = data.nuevoConsecutivo;
                cargarConsecutivosTraslados();
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
    btnNuevoTraslado.addEventListener('click', nuevoTraslado);
    btnGuardarTraslado.addEventListener('click', guardarTraslado);
    btnEditarTraslado.addEventListener('click', editarTraslado);
    btnCancelarTraslado.addEventListener('click', cancelarTraslado);
    btnBuscarTraslado.addEventListener('click', buscarTraslado);
    btnCerrarTraslado.addEventListener('click', cerrarTraslado);

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
            
            if (text === "Traslados a Bodegas") {
                console.log("Clic en Traslados a Bodegas detectado");
                mostrarTrasladosInventario();
            }
        });
    } else {
        console.error("El elemento inventarioLista no se encontró");
    }

    const btnTrasladosBodegas = document.getElementById('btnTrasladosBodegas');
    if (btnTrasladosBodegas) {
        console.log("Botón de Traslados a Bodegas encontrado");
        btnTrasladosBodegas.addEventListener('click', function() {
            console.log("Clic en botón de Traslados a Bodegas");
            mostrarTrasladosInventario();
        });
    } else {
        console.error("El botón de Traslados a Bodegas no se encontró");
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
        cargarReferenciasTraslados(this.value);
    });

    document.getElementById('btnBuscarReferencia').addEventListener('click', function() {
        const filtro = document.getElementById('buscarReferencia').value;
        cargarReferenciasTraslados(filtro);
    });

    document.querySelector('#detallesTrasladoTable').addEventListener('input', function(e) {
        if (e.target.cellIndex >= 3 && e.target.cellIndex <= 9) {
            console.log("Cambio detectado en la tabla");
            const row = e.target.closest('tr');
            actualizarSubtotalFila(row);
        }
    });
    
    document.querySelector('#detallesTrasladoTable').addEventListener('click', function(e) {
        if (e.target && e.target.classList.contains('btn-eliminar')) {
            e.target.closest('tr').remove();
            actualizarTotales();
        }
    });

    // Manejo de edición en línea para la tabla de traslados
    tablaTraslados.addEventListener('dblclick', function(e) {
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
                actualizarSubtotalFila(cell.closest('tr'));
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
    habilitarCamposTraslado(false);

    console.log("Configuración de Traslados a Bodegas completada");
});