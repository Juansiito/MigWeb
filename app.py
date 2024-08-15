from flask import Flask, jsonify, request, render_template, send_file
from flask_cors import CORS, cross_origin
from flask_mail import Mail, Message
from db import db, init_db, Bodegas, Licencia, Usuarios, Consecutivos, Entradas1, Entradas2, Referencia, Salidas1, Salidas2, Grupo, Traslados1, Traslados2, SaldosBodega, Unidades, SubGrupos, Subcategorias, EstadoProducto
from datetime import datetime
import traceback
import hashlib
import logging
import random
import string
import base64
from PIL import Image, ImageDraw, ImageFont
import io
import os
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash
from flask import jsonify
from decimal import Decimal
from sqlalchemy import func
from flask_sqlalchemy import SQLAlchemy
import uuid
from sqlalchemy.dialects.postgresql import UUID
import os

def generar_password():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://127.0.0.1:5500", "supports_credentials": True}})

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost/INVENTARIO'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

init_db(app)


# Configuración del logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Configuración del correo
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'info@migsistemas.com'
app.config['MAIL_PASSWORD'] = 'eejgelzxmgrfrkdh'  # Esta es la contraseña de aplicación
app.config['MAIL_DEFAULT_SENDER'] = 'info@migsistemas.com'
mail = Mail(app)

# Verificar la conexión a la base de datos
try:
    with app.app_context():
        db.session.execute(text('SELECT 1'))
    logging.info("Conexión a la base de datos exitosa")
except SQLAlchemyError as e:
    logging.error(f"Error al conectar a la base de datos: {str(e)}")

# Crear las tablas si no existen
with app.app_context():
    db.create_all()

@app.route('/api/inventario')
def get_inventario_data():
    inventario_items = [
        {"icon": "icon-ordenes", "text": "Órdenes de compras"},
        {"icon": "icon-compras", "text": "Compras proveedor"},
        {"icon": "icon-traslados", "text": "Traslados a Bodegas"},
        {"icon": "icon-entradas", "text": "Entradas a Bodegas"},
        {"icon": "icon-salidas", "text": "Salidas a Bodegas"},
        {"icon": "icon-consulta", "text": "Consulta Inventario"},
        {"icon": "icon-maxmin", "text": "Máximos y Mínimos"},
        {"icon": "icon-fisico", "text": "Inventario Físico"}
    ]
    return jsonify(inventario_items)

@app.route('/api/referencias')
def get_referencias():
    filtro = request.args.get('filtro', '')
    referencias = Referencia.query.filter(
        (Referencia.IdReferencia.ilike(f'%{filtro}%')) | 
        (Referencia.Referencia.ilike(f'%{filtro}%'))
    ).all()
    return jsonify([{
        'IdReferencia': ref.IdReferencia,
        'Referencia': ref.Referencia,
        'PrecioVenta1': str(ref.PrecioVenta1),
        'IVA': str(ref.IVA),
        'Ubicacion': ref.Ubicacion,
        'idbodega': ref.idbodega,
        'IdUnidad': ref.IdUnidad,
    } for ref in referencias])

@app.route('/api/buscar_productos_editar', methods=['GET'])
def buscar_productos_editar():
    busqueda = request.args.get('buscar', '')
    app.logger.info(f"Búsqueda recibida: {busqueda}")

    try:
        referencias = Referencia.query.filter(
            (Referencia.IdReferencia.ilike(f'%{busqueda}%')) | 
            (Referencia.Referencia.ilike(f'%{busqueda}%'))
        ).limit(50).all()
        
        app.logger.info(f"Resultados encontrados: {len(referencias)}")
        
        resultado = [{
            'IdReferencia': ref.IdReferencia,
            'Referencia': ref.Referencia,
            'IdGrupo': ref.IdGrupo
        } for ref in referencias]
        
        return jsonify(resultado)
    except Exception as e:
        app.logger.error(f"Error en la búsqueda: {str(e)}")
        return jsonify({'error': 'Error en la búsqueda de productos'}), 500

# Ruta de prueba para verificar que el servidor está respondiendo
@app.route('/api/test', methods=['GET'])
def test_api():
    return jsonify({"message": "API is working"}), 200

@app.route('/api/buscar_productos_editar/<string:id>', methods=['GET'])
def obtener_producto_editar(id):
    try:
        referencia = Referencia.query.get_or_404(id)
        return jsonify({
            'IdReferencia': referencia.IdReferencia,
            'Referencia': referencia.Referencia,
            'IdGrupo': referencia.IdGrupo,
            'idsubgrupo': referencia.idsubgrupo,
            'idsubcategoria': referencia.idsubcategoria,
            'IdUnidad': referencia.IdUnidad,
            'idbodega': referencia.idbodega,
            'Costo': str(referencia.Costo),
            'PrecioVenta1': str(referencia.PrecioVenta1),
            'IVA': str(referencia.IVA),
            'Ubicacion': referencia.Ubicacion,
            'Marca': referencia.Marca,
            'EstadoProducto': referencia.EstadoProducto,
            'Estado': referencia.Estado,
            'Tipo': referencia.Tipo,
            'ManejaInventario': referencia.ManejaInventario,
            'productoagotado': referencia.productoagotado,
            'modificaprecio': referencia.modificaprecio,
            'compuesto': getattr(referencia, 'compuesto', False)  # Asumiendo que este campo existe
        })
    except Exception as e:
        app.logger.error(f"Error al obtener producto: {str(e)}")
        return jsonify({'error': 'Error al obtener detalles del producto'}), 500

@app.route('/api/maestros')
def get_maestros_data():
    maestros_items = [
        {
            "icon": "icon-terceros",
            "text": "Terceros",
            "subitems": [
                {"icon": "icon-clientes", "text": "Clientes"},
                {"icon": "icon-proveedores", "text": "Proveedores"},
                {"icon": "icon-vendedores", "text": "Vendedores - Meseros - Empleados"}
            ]
        },
        {
            "icon": "icon-productos",
            "text": "Productos",
            "subitems": [
                {"icon": "icon-grupos", "text": "Grupos - Familias - Categorías"},
                {"icon": "icon-articulos", "text": "Productos - Artículos - Referencias"},
                {"icon": "icon-subgrupos", "text": "SubGrupos"},
                {"icon": "icon-subcategorias", "text": "SubCategorías"},
                {"icon": "icon-lineas", "text": "Líneas"},
                {"icon": "icon-comentarios", "text": "Grupos comentarios"},
                {"icon": "icon-descuentos", "text": "Descuentos"},
                {"icon": "icon-unidades", "text": "Unidad de medidas"},
                {"icon": "icon-conectores", "text": "Conectores"}
            ]
        },
        {
            "icon": "icon-otros",
            "text": "Otros",
            "subitems": [
                {"icon": "icon-bodegas", "text": "Bodegas"}
            ]
        },
    ]
    return jsonify(maestros_items)

@app.route('/api/consulta_inventario')
def get_consulta_inventario():
    # Asumiendo que estás usando SQLAlchemy
    referencias = db.session.query(
        Referencia, 
        func.coalesce(SaldosBodega.Saldo, 0).label('Saldo')
    ).outerjoin(
        SaldosBodega, 
        (Referencia.IdReferencia == SaldosBodega.IdReferencia) & 
        (SaldosBodega.Mes == datetime.now().strftime('%Y%m'))
    ).filter(Referencia.Estado == True).all()  # Añadimos este filtro

    return jsonify([{
        'IDReferencia': ref.IdReferencia,
        'Referencia': ref.Referencia,
        'Marca': ref.Marca or '',
        'Precio_Venta': str(ref.PrecioVenta1) if ref.PrecioVenta1 else '',
        'Ubicación': ref.Ubicacion or '',
        'Grupo': ref.IdGrupo or '',
        'ID_Unidad': ref.IdUnidad or '',
        'Bodega': ref.idbodega or '',
        'Saldo': str(saldo),  # Aquí se incluye el saldo
        'Costo': str(ref.Costo) if ref.Costo else '',
        'EstadoProducto': ref.EstadoProducto or ''
    } for ref, saldo in referencias])

@app.route('/api/bodegas', methods=['GET', 'POST', 'PUT'])
def manejar_bodegas():
    if request.method == 'POST':
        data = request.json
        nueva_bodega = Bodegas(
            IdBodega=data['IdBodega'],
            Descripcion=data['Descripcion'],
            Estado=data['Estado'],
            Email=data.get('Email'),
            nombrepunto=data.get('nombrepunto'),
            direccionpunto=data.get('direccionpunto'),
            telefonopunto=data.get('telefonopunto')
        )
        db.session.add(nueva_bodega)
        db.session.commit()
        return jsonify({'message': 'Bodega creada exitosamente'}), 201
    elif request.method == 'PUT':
        data = request.json
        bodega = Bodegas.query.get(data['IdBodega'])
        if bodega:
            bodega.Descripcion = data['Descripcion']
            bodega.Estado = data['Estado']
            bodega.Email = data.get('Email')
            bodega.nombrepunto = data.get('nombrepunto')
            bodega.direccionpunto = data.get('direccionpunto')
            bodega.telefonopunto = data.get('telefonopunto')
            db.session.commit()
            return jsonify({'message': 'Bodega actualizada exitosamente'}), 200
        else:
            return jsonify({'message': 'Bodega no encontrada'}), 404
    else:
        bodegas = Bodegas.query.all()
        return jsonify([{
            'IdBodega': bodega.IdBodega,
            'Descripcion': bodega.Descripcion,
            'Estado': bodega.Estado,
            'Email': bodega.Email,
            'nombrepunto': bodega.nombrepunto,
            'direccionpunto': bodega.direccionpunto,
            'telefonopunto': bodega.telefonopunto
        } for bodega in bodegas])

@app.route('/api/estado_producto', methods=['GET', 'POST'])
def manejar_estado_producto():
    if request.method == 'GET':
        try:
            estados = EstadoProducto.query.all()
            return jsonify([{
                'IdEstadoProducto': estado.IdEstadoProducto,
                'EstadoProducto': estado.EstadoProducto,
                'Estado': estado.Estado
            } for estado in estados])
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 500

    elif request.method == 'POST':
        try:
            data = request.json
            nuevo_estado = EstadoProducto(
                IdEstadoProducto=data['IdEstadoProducto'],
                EstadoProducto=data['EstadoProducto'],
                Estado=data['Estado']
            )
            db.session.add(nuevo_estado)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Estado de Producto creado exitosamente'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/estado_producto/<string:id>', methods=['PUT', 'DELETE'])
def manejar_estado_producto_individual(id):
    estado = EstadoProducto.query.get(id)
    if not estado:
        return jsonify({'success': False, 'message': 'Estado de Producto no encontrado'}), 404

    if request.method == 'PUT':
        try:
            data = request.json
            estado.EstadoProducto = data['EstadoProducto']
            estado.Estado = data['Estado']
            db.session.commit()
            return jsonify({'success': True, 'message': 'Estado de Producto actualizado exitosamente'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'message': str(e)}), 400

    elif request.method == 'DELETE':
        try:
            db.session.delete(estado)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Estado de Producto eliminado exitosamente'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/estado_producto', methods=['POST'])
def crear_estado_producto():
    data = request.json
    try:
        nuevo_estado = EstadoProducto(
            IdEstadoProducto=data['IdEstadoProducto'],
            EstadoProducto=data['EstadoProducto'],
            Estado=data['Estado']
        )
        db.session.add(nuevo_estado)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Estado de Producto creado exitosamente'}), 201
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Error de integridad: ' + str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Error: ' + str(e)}), 500

@app.route('/api/estado_producto/<string:id>', methods=['DELETE'])
def eliminar_estado_producto(id):
    estado = EstadoProducto.query.get(id)
    if estado:
        db.session.delete(estado)
        try:
            db.session.commit()
            return jsonify({'success': True, 'message': 'Estado de Producto eliminado exitosamente'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'message': str(e)}), 400
    else:
        return jsonify({'success': False, 'message': 'Estado de Producto no encontrado'}), 404

@app.route('/api/unidades', methods=['POST'])
def crear_unidad():
    data = request.json
    
    if not data or 'IdUnidad' not in data or 'Unidad' not in data:
        return jsonify({'error': 'Datos incompletos'}), 400

    nueva_unidad = Unidades(
        IdUnidad=data['IdUnidad'],
        Unidad=data['Unidad'],
        Estado=data.get('Estado', True)
    )

    try:
        db.session.add(nueva_unidad)
        db.session.commit()
        return jsonify({
            'message': 'Unidad creada exitosamente',
            'unidad': {
                'IdUnidad': nueva_unidad.IdUnidad,
                'Unidad': nueva_unidad.Unidad,
                'Estado': nueva_unidad.Estado
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/unidades', methods=['GET'])
def obtener_unidades():
    unidades = Unidades.query.all()
    return jsonify([{
        'IdUnidad': u.IdUnidad,
        'Unidad': u.Unidad,
        'Estado': u.Estado
    } for u in unidades])

@app.route('/api/unidades/activas', methods=['GET'])
def obtener_unidades_activas():
    unidades = Unidades.query.filter_by(Estado=True).all()
    return jsonify([{
        'IdUnidad': u.IdUnidad,
        'Unidad': u.Unidad
    } for u in unidades])

@app.route('/api/subgrupos', methods=['GET', 'POST'])
def manejar_subgrupos():
    if request.method == 'POST':
        data = request.json
        nuevo_subgrupo = SubGrupos(
            IdSubgrupo=data['IdSubgrupo'],
            Subgrupo=data['Subgrupo'],
            IdGrupo=data['IdGrupo'],
            Estado=data['Estado']
        )
        db.session.add(nuevo_subgrupo)
        db.session.commit()
        return jsonify({'message': 'Subgrupo creado exitosamente'}), 201
    else:
        subgrupos = SubGrupos.query.all()
        return jsonify([{
            'IdSubgrupo': s.IdSubgrupo,
            'Subgrupo': s.Subgrupo,
            'IdGrupo': s.IdGrupo,
            'Estado': s.Estado
        } for s in subgrupos])

@app.route('/api/subgrupos/<string:id>', methods=['DELETE'])
def eliminar_subgrupo(id):
    subgrupo = SubGrupos.query.get(id)
    if subgrupo:
        db.session.delete(subgrupo)
        db.session.commit()
        return jsonify({'message': 'Subgrupo eliminado exitosamente'})
    return jsonify({'message': 'Subgrupo no encontrado'}), 404

@app.route('/api/grupos', methods=['GET', 'POST'])
def manejar_grupos():
    if request.method == 'GET':
        try:
            grupos = Grupo.query.all()
            return jsonify([{
                'codigo': grupo.IdGrupo,
                'descripcion': grupo.Grupo,
                'estado': grupo.Estado,
                'menupos': grupo.menupos
            } for grupo in grupos])
        except Exception as e:
            print("Error al obtener grupos:", str(e))
            return jsonify({'error': 'Error al obtener grupos: ' + str(e)}), 500
    elif request.method == 'POST':
        try:
            data = request.json
            app.logger.info(f"Procesando datos POST: {data}")
            
            grupo_existente = Grupo.query.get(data['codigo'])
            if grupo_existente:
                app.logger.info(f"Actualizando grupo existente: {data['codigo']}")
                grupo_existente.Grupo = data['descripcion']
                grupo_existente.Estado = data['estado']
                grupo_existente.menupos = data['menupos']
                mensaje = 'Grupo actualizado exitosamente'
            else:
                app.logger.info(f"Creando nuevo grupo: {data['codigo']}")
                nuevo_grupo = Grupo(
                    IdGrupo=data['codigo'],
                    Grupo=data['descripcion'],
                    Estado=data['estado'],
                    menupos=data['menupos']
                )
                db.session.add(nuevo_grupo)
                mensaje = 'Grupo creado exitosamente'
            
            db.session.commit()
            app.logger.info("Operación en base de datos completada con éxito")
            return jsonify({'success': True, 'message': mensaje}), 200
        except IntegrityError as e:
            db.session.rollback()
            print("Error de integridad:", str(e))
            return jsonify({'error': 'El código de grupo ya existe. Por favor, use un código diferente.'}), 400
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Error al procesar la solicitud: {str(e)}")
            return jsonify({'error': 'Error inesperado: ' + str(e)}), 500
        
    app.logger.warning(f"Método no soportado: {request.method}")
    return jsonify({'error': 'Método no soportado'}), 405

@app.route('/api/bodegas/<string:id>', methods=['DELETE'])
def eliminar_bodega(id):
    try:
        bodega = Bodegas.query.get(id)
        if bodega:
            db.session.delete(bodega)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Bodega eliminada exitosamente'})
        else:
            return jsonify({'success': False, 'message': 'Bodega no encontrada'}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

def verificar_credenciales(id_usuario, contraseña):
    usuario = Usuarios.query.filter_by(IdUsuario=id_usuario).first()
    if usuario and usuario.Contraseña == contraseña:
        return jsonify({"success": True, "message": "Inicio de sesión exitoso"})
    return jsonify({"success": False, "message": "Credenciales inválidas"})

@app.route('/')
def index():
    return render_template('login.html')

# Añade esta ruta en tu archivo principal de Flask (app.py o similar)
@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.json
        if not data:
            return jsonify({"success": False, "message": "No se proporcionaron datos"}), 400

        id_usuario = data.get('username')
        contraseña = data.get('password')

        if not id_usuario or not contraseña:
            return jsonify({"success": False, "message": "Usuario y contraseña son requeridos"}), 400

        usuario = Usuarios.query.filter_by(IdUsuario=id_usuario).first()
        
        if usuario and usuario.Contraseña == contraseña:
            return jsonify({
                "success": True, 
                "message": "Inicio de sesión exitoso",
                "user": {
                    "IdUsuario": usuario.IdUsuario,
                    "Descripcion": usuario.Descripcion,
                    "Grupo": usuario.Grupo,
                    "email": usuario.email
                }
            })
        else:
            return jsonify({"success": False, "message": "Credenciales inválidas"}), 401
    except Exception as e:
        print(f"Error en el servidor: {str(e)}")  # Imprime el error en la consola del servidor
        return jsonify({"success": False, "message": f"Error en el servidor: {str(e)}"}), 500
    
@app.route('/api/consecutivos_salidas_inventario', methods=['GET'])
def obtener_consecutivos_salidas_inventario():
    try:
        # Suponiendo que 'SAL' es el código para Salidas de Inventario
        consecutivos = Consecutivos.query.filter_by(Formulario='SAL', Estado=True).all()
        return jsonify([{
            'IdConsecutivo': c.IdConsecutivo,
            'Descripcion': c.Consecutivo,
            'Prefijo': c.Prefijo,
            'Actual': c.Actual
        } for c in consecutivos])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/consecutivos_traslados_inventario', methods=['GET'])
def obtener_consecutivos_traslados_inventario():
    try:
        # Suponiendo que 'TB' es el código para Traslados de Inventario
        consecutivos = Consecutivos.query.filter_by(Formulario='TB', Estado=True).all()
        return jsonify([{
            'IdConsecutivo': c.IdConsecutivo,
            'Descripcion': c.Consecutivo,
            'Prefijo': c.Prefijo,
            'Actual': c.Actual
        } for c in consecutivos])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/guardar_traslado', methods=['POST'])
def guardar_traslado():
    data = request.json
    traslado1_data = data.get('traslado1', {})
    traslados2_data = data.get('traslados2', [])

    try:
        nuevo_traslado1 = Traslados1(
            Numero=traslado1_data.get('Numero'),
            Mes=traslado1_data.get('Mes'),
            Anulado=traslado1_data.get('Anulado', False),
            IdBodegaOrigen=traslado1_data.get('IdBodegaOrigen'),
            IdBodegaDestino=traslado1_data.get('IdBodegaDestino'),
            Observaciones=traslado1_data.get('Observaciones'),
            FechaCreacion=datetime.fromisoformat(traslado1_data.get('FechaCreacion')),
            IdUsuario=traslado1_data.get('IdUsuario'),
            IdConsecutivo=traslado1_data.get('IdConsecutivo'),
            fecha=datetime.fromisoformat(traslado1_data.get('fecha')),
            subtotal=Decimal(str(traslado1_data.get('subtotal', '0'))),
            total_iva=Decimal(str(traslado1_data.get('total_iva', '0'))),
total_impoconsumo=Decimal(str(traslado1_data.get('total_impoconsumo', '0'))),
            total_ipc=Decimal(str(traslado1_data.get('total_ipc', '0'))),
            total_ibua=Decimal(str(traslado1_data.get('total_ibua', '0'))),
            total_icui=Decimal(str(traslado1_data.get('total_icui', '0'))),
            total=Decimal(str(traslado1_data.get('total', '0')))
        )
        db.session.add(nuevo_traslado1)

        for traslado2 in traslados2_data:
            nuevo_traslado2 = Traslados2(
                ID=traslado2.get('ID'),
                Numero=traslado2.get('Numero'),
                IdReferencia=traslado2.get('IdReferencia'),
                Descripcion=traslado2.get('Descripcion'),
                Cantidad=Decimal(str(traslado2.get('Cantidad', '0'))),
                Valor=Decimal(str(traslado2.get('Valor', '0'))),
                IVA=Decimal(str(traslado2.get('IVA', '0'))),
                idunidad=traslado2.get('idunidad'),
                impoconsumo=Decimal(str(traslado2.get('impoconsumo', '0'))),
                ipc=Decimal(str(traslado2.get('ipc', '0'))),
                imp_ibua=Decimal(str(traslado2.get('imp_ibua', '0'))),
                imp_icui=Decimal(str(traslado2.get('imp_icui', '0')))
            )
            db.session.add(nuevo_traslado2)

        db.session.commit()
        return jsonify({'success': True, 'message': 'Traslado guardado con éxito'})
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Error de base de datos: {str(e)}'}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Error inesperado: {str(e)}'}), 500

@app.route('/api/ultimo_consecutivo_traslados', methods=['GET'])
def ultimo_consecutivo_traslados():
    try:
        consecutivo = Consecutivos.query.filter_by(Formulario='TB').first()
        if consecutivo:
            ultimo_consecutivo = f"{consecutivo.Prefijo}{consecutivo.Actual.zfill(2)}"
            return jsonify({'success': True, 'ultimoConsecutivo': ultimo_consecutivo})
        else:
            return jsonify({'success': False, 'message': 'No se encontró el consecutivo para Traslados de Inventario'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/actualizar_consecutivo_traslados', methods=['POST'])
def actualizar_consecutivo_traslados():
    try:
        consecutivo = Consecutivos.query.filter_by(Formulario='TB').first()
        if consecutivo:
            consecutivo.Actual = str(int(consecutivo.Actual) + 1).zfill(2)
            db.session.commit()
            nuevo_consecutivo = f"{consecutivo.Prefijo}{consecutivo.Actual}"
            return jsonify({'success': True, 'nuevoConsecutivo': nuevo_consecutivo})
        else:
            return jsonify({'success': False, 'message': 'No se encontró el consecutivo para Traslados de Inventario'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/referencias/<string:id>', methods=['PUT'])
def actualizar_referencia(id):
    try:
        data = request.json
        referencia = Referencia.query.get(id)
        
        if not referencia:
            return jsonify({'message': 'Referencia no encontrada'}), 404

        # Actualizar los campos de la referencia
        for key, value in data.items():
            setattr(referencia, key, value)

        db.session.commit()
        return jsonify({'message': 'Referencia actualizada exitosamente'}), 200
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({'message': f'Error de integridad en la base de datos: {str(e)}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error al actualizar la referencia: {str(e)}'}), 500

@app.route('/api/grupos', methods=['GET'])
def obtener_grupos():
    grupos = Grupo.query.all()
    return jsonify([{
        'codigo': grupo.IdGrupo,
        'descripcion': grupo.Grupo,
        'estado': grupo.Estado,
        'menupos': grupo.menupos,
        'ultimoCodigo': grupo.ultimoCodigo  # Asumiendo que agregaste este campo a tu modelo Grupo
    } for grupo in grupos])

@app.route('/api/grupos_subcategorias', methods=['GET'])
def obtener_grupos_subcategorias():
    try:
        grupos = Grupo.query.filter_by(Estado=True).all()
        grupos_data = [{
            'IdGrupo': grupo.IdGrupo,
            'Grupo': grupo.Grupo
        } for grupo in grupos]
        print("Grupos para subcategorías obtenidos:", grupos_data)  # Log para debugging
        return jsonify(grupos_data)
    except Exception as e:
        print(f"Error al obtener grupos para subcategorías: {str(e)}")
        return jsonify({'error': 'Error al obtener grupos para subcategorías'}), 500

@app.route('/api/guardar_entrada', methods=['POST'])
def guardar_entrada():
    data = request.json
    entrada1_data = data.get('entrada1', {})
    entradas2_data = data.get('entradas2', [])

    logging.info(f"Datos recibidos: {data}")

    try:
        # Crear instancia de Entradas1
        nueva_entrada1 = Entradas1(
            Numero=entrada1_data.get('Numero'),
            Mes=entrada1_data.get('Mes'),
            Anulado=entrada1_data.get('Anulado', False),
            IdBodega=entrada1_data.get('IdBodega'),
            Observaciones=entrada1_data.get('Observaciones'),
            FechaCreacion=datetime.fromisoformat(entrada1_data.get('FechaCreacion')),
            IdUsuario=entrada1_data.get('IdUsuario'),
            IdConsecutivo=entrada1_data.get('IdConsecutivo'),
            fecha=datetime.fromisoformat(entrada1_data.get('fecha')),
            subtotal=Decimal(str(entrada1_data.get('subtotal', '0'))),
            total_iva=Decimal(str(entrada1_data.get('total_iva', '0'))),
            total_impoconsumo=Decimal(str(entrada1_data.get('total_impoconsumo', '0'))),
            total_ipc=Decimal(str(entrada1_data.get('total_ipc', '0'))),
            total_ibua=Decimal(str(entrada1_data.get('total_ibua', '0'))),
            total_icui=Decimal(str(entrada1_data.get('total_icui', '0'))),
            total=Decimal(str(entrada1_data.get('total', '0')))
        )
        db.session.add(nueva_entrada1)

        # Guardar en Entradas2 y actualizar SaldosBodega
        mes_actual = datetime.now().strftime('%Y%m')
        for entrada2 in entradas2_data:
            if not entrada2.get('IdReferencia'):
                logging.warning(f"Entrada ignorada debido a IdReferencia vacío: {entrada2}")
                continue

            nueva_entrada2 = Entradas2(
                ID=entrada2.get('ID'),
                Numero=entrada2.get('Numero'),
                IdReferencia=entrada2.get('IdReferencia'),
                Descripcion=entrada2.get('Descripcion'),
                Cantidad=Decimal(str(entrada2.get('Cantidad', '0'))),
                Valor=Decimal(str(entrada2.get('Valor', '0'))),
                IVA=Decimal(str(entrada2.get('IVA', '0'))),
                Descuento=Decimal('0'),
                idunidad=entrada2.get('idunidad'),
                impoconsumo=Decimal(str(entrada2.get('impoconsumo', '0'))),
                ipc=Decimal(str(entrada2.get('ipc', '0'))),
                imp_ibua=Decimal(str(entrada2.get('imp_ibua', '0'))),
                imp_icui=Decimal(str(entrada2.get('imp_icui', '0')))
            )
            db.session.add(nueva_entrada2)

        # Actualizar SaldosBodega
        mes_actual = datetime.now().strftime('%Y%m')
        for entrada2 in entradas2_data:
            saldo = SaldosBodega.query.filter_by(
                IdBodega=entrada1_data['IdBodega'],
                Mes=mes_actual,
                IdReferencia=entrada2['IdReferencia']
            ).first()

            if saldo:
                saldo.Entradas += Decimal(str(entrada2['Cantidad']))
                saldo.Saldo += Decimal(str(entrada2['Cantidad']))
                # Actualiza el lote si es necesario
                if entrada2.get('lote'):
                    saldo.lote = entrada2['lote']
            else:
                nuevo_saldo = SaldosBodega(
                    IdBodega=entrada1_data['IdBodega'],
                    Mes=mes_actual,
                    IdReferencia=entrada2['IdReferencia'],
                    Entradas=Decimal(str(entrada2['Cantidad'])),
                    Saldo=Decimal(str(entrada2['Cantidad'])),
                    lote=entrada2.get('lote', '')  # Usa una cadena vacía si no hay lote
                )
                db.session.add(nuevo_saldo)

        db.session.commit()
        return jsonify({'success': True, 'message': 'Entrada guardada y saldo actualizado con éxito'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Error al guardar la entrada: {str(e)}'}), 500

@app.route('/api/importar-productos', methods=['POST'])
def importar_productos():
    productos = request.json
    for producto in productos:
        nueva_referencia = Referencia(
            IdReferencia=producto['IdReferencia'],
            Referencia=producto['Referencia'],
            Marca=producto['Marca'],
            EstadoProducto=producto['EstadoProducto'],
            IdGrupo=producto['IdGrupo'],
            IdUnidad=producto['IdUnidad'],
            Ubicacion=producto['Ubicacion'],
            Costo=producto['Costo'],
            PrecioVenta1=producto['PrecioVenta1'],
            IVA=producto['IVA'],
            Estado=producto['Estado'],
            Tipo=producto['Tipo'],
            ManejaInventario=producto['ManejaInventario']
        )
        db.session.add(nueva_referencia)
    
    try:
        db.session.commit()
        return jsonify({'message': 'Productos importados exitosamente'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error al importar productos: {str(e)}'}), 500

@app.route('/api/subcategorias', methods=['GET', 'POST'])
def manejar_subcategorias():
    if request.method == 'GET':
        subcategorias = Subcategorias.query.all()
        return jsonify([{
            'idsubcategoria': s.idsubcategoria,
            'categoria': s.categoria,
            'idgrupo': s.idgrupo,
            'idsubgrupo': s.idsubgrupo,
            'estado': s.estado
        } for s in subcategorias])
    
    elif request.method == 'POST':
        data = request.json
        nueva_subcategoria = Subcategorias(
            idsubcategoria=data['idsubcategoria'],
            categoria=data['categoria'],
            idgrupo=data['idgrupo'],
            idsubgrupo=data['idsubgrupo'],
            estado=data['estado']
        )
        db.session.add(nueva_subcategoria)
        try:
            db.session.commit()
            return jsonify({'message': 'Subcategoría creada exitosamente'}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 400

@app.route('/api/subcategorias/<string:id>', methods=['GET', 'PUT', 'DELETE'])
def manejar_subcategoria_individual(id):
    subcategoria = Subcategorias.query.get_or_404(id)
    
    if request.method == 'GET':
        return jsonify({
            'idsubcategoria': subcategoria.idsubcategoria,
            'categoria': subcategoria.categoria,
            'idgrupo': subcategoria.idgrupo,
            'idsubgrupo': subcategoria.idsubgrupo,
            'estado': subcategoria.estado
        })
    
    elif request.method == 'PUT':
        data = request.json
        subcategoria.categoria = data['categoria']
        subcategoria.idgrupo = data['idgrupo']
        subcategoria.idsubgrupo = data['idsubgrupo']
        subcategoria.estado = data['estado']
        try:
            db.session.commit()
            return jsonify({'message': 'Subcategoría actualizada exitosamente'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 400
    
    elif request.method == 'DELETE':
        db.session.delete(subcategoria)
        try:
            db.session.commit()
            return jsonify({'message': 'Subcategoría eliminada exitosamente'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 400

@app.route('/api/obtener_grupos_subgrupos', methods=['GET'])
def obtener_grupos_subgrupos():
    try:
        grupos = Grupo.query.filter_by(Estado=True).all()
        grupos_data = [{
            'codigo': grupo.IdGrupo,
            'descripcion': grupo.Grupo
        } for grupo in grupos]
        return jsonify(grupos_data)
    except Exception as e:
        print(f"Error al obtener grupos para subgrupos: {str(e)}")
        return jsonify({'error': 'Error al obtener grupos para subgrupos'}), 500

@app.route('/api/subgrupos', methods=['GET'])
def obtener_subgrupos():
    try:
        subgrupos = SubGrupos.query.all()
        subgrupos_data = [{
            'IdSubgrupo': subgrupo.IdSubgrupo,
            'Subgrupo': subgrupo.Subgrupo,
            'IdGrupo': subgrupo.IdGrupo,
            'Estado': subgrupo.Estado
        } for subgrupo in subgrupos]
        return jsonify(subgrupos_data)
    except Exception as e:
        print(f"Error al obtener subgrupos: {str(e)}")
        return jsonify({'error': 'Error al obtener subgrupos'}), 500

@app.route('/api/subgrupos/<string:id_grupo>', methods=['GET'])
def obtener_subgrupos_por_grupo(id_grupo):
    try:
        subgrupos = SubGrupos.query.filter_by(IdGrupo=id_grupo, Estado=True).all()
        subgrupos_data = [{
            'IdSubgrupo': subgrupo.IdSubgrupo,
            'Subgrupo': subgrupo.Subgrupo
        } for subgrupo in subgrupos]
        return jsonify(subgrupos_data)
    except Exception as e:
        print(f"Error al obtener subgrupos: {str(e)}")
        return jsonify({'error': 'Error al obtener subgrupos'}), 500

@app.route('/api/grupos/<string:id>', methods=['DELETE'])
def eliminar_grupo(id):
    try:
        grupo = Grupo.query.get(id)
        if grupo:
            db.session.delete(grupo)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Grupo eliminado exitosamente'})
        else:
            return jsonify({'success': False, 'message': 'Grupo no encontrado'}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/grupos/<codigo>', methods=['GET'])
def verificar_grupo(codigo):
    grupo = Grupo.query.get(codigo)
    return jsonify({'exists': grupo is not None})

def verificar_referencias_existen(referencias):
    existentes = Referencia.query.filter(Referencia.IdReferencia.in_(referencias)).with_entities(Referencia.IdReferencia).all()
    existentes = set(r[0] for r in existentes)
    return all(ref in existentes for ref in referencias)

@app.route('/maestros/bodegas')
def pagina_bodegas():
    return render_template('bodegas.html')

@app.route('/api/configuracion', methods=['GET', 'POST'])
def manejar_configuracion():
    if request.method == 'POST':
        data = request.json
        # Procesar data...
        return jsonify({'message': 'Configuración actualizada exitosamente'}), 200
    else:
        configuracion = {
            'empresa': 'MIG-ALMACEN, TEXTIL',
            'licencia': 'XXXX-XXXX-XXXX-XXXX',
            # ... más configuraciones ...
        }
        return jsonify(configuracion)

def generar_licencia(caracteristicas_equipo, nit):
    caracteristicas = base64.b64decode(caracteristicas_equipo).decode('utf-8')
    clave_secreta = "MIGSistemas2024"
    datos = caracteristicas + nit + clave_secreta
    hash_objeto = hashlib.sha256(datos.encode())
    hash_bytes = hash_objeto.digest()
    licencia_base = base64.b64encode(hash_bytes).decode()[:16]
    caracteres_aleatorios = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    licencia = f"{licencia_base}-{caracteres_aleatorios}-{nit[-4:]}"
    return licencia

def enviar_correo(licencia, usuario, password):
    try:
        msg = Message('Nueva Licencia Generada',
                    sender=app.config['MAIL_DEFAULT_SENDER'],
                    recipients=['riosjuan3053@gmail.com', 'johnsod8729@gmail.com'])
        msg.body = f"""
        Se ha generado una nueva licencia:
        
        NIT: {licencia.nit}
        Razón Social: {licencia.razonsocial}
        Nombre Comercial: {licencia.nombrecomercial}
        Número de Licencia: {licencia.numerolicencia}
        Tipo de Licencia: {licencia.tipolicencia}
        Fecha de Vencimiento: {licencia.fechavencimiento if licencia.fechavencimiento else 'N/A'}

        Información de acceso:
        Usuario: {usuario}
        Contraseña: {password}

        Por favor, cambie su contraseña después del primer inicio de sesión.
        """
        logging.info(f"Intentando enviar correo a {', '.join(msg.recipients)}")
        mail.send(msg)
        logging.info("Correo enviado exitosamente")
        return True
    except Exception as e:
        logging.error(f"Error al enviar correo: {str(e)}")
        logging.error(f"Detalles del error: {traceback.format_exc()}")
        return False
    
@app.before_request
def log_request_info():
    app.logger.info('Ruta solicitada: %s %s', request.method, request.path)

@app.after_request
def log_response_info(response):
    app.logger.debug('Response Status: %s', response.status)
    app.logger.debug('Response: %s', response.get_data())
    return response

@app.route('/api/solicitar_licencia', methods=['POST'])
def solicitar_licencia():
    try:
        data = request.json
        logging.info(f"Datos recibidos: {data}")
        
        # Validar datos recibidos
        campos_requeridos = ['nit', 'razonsocial', 'nombrecomercial', 'ubicacioncomercial', 'ciudad', 'telefono', 'version', 'cantidadusuario', 'tipolicencia', 'caracteristicas_equipo']
        for campo in campos_requeridos:
            if campo not in data or not data[campo]:
                return jsonify({'success': False, 'message': f'El campo {campo} es requerido y no puede estar vacío'}), 400

        # Generar licencia
        numero_licencia = generar_licencia(data['caracteristicas_equipo'], data['nit'])
        logging.info(f"Número de licencia generado: {numero_licencia}")
        
        # Crear nueva licencia en la base de datos
        nueva_licencia = Licencia(
            id=numero_licencia,  # Usar el número de licencia como ID
            nit=data['nit'],
            razonsocial=data['razonsocial'],
            nombrecomercial=data['nombrecomercial'],
            ubicacioncomercial=data['ubicacioncomercial'],
            ciudad=data['ciudad'],
            telefono=data['telefono'],
            version=data['version'],
            numerolicencia=numero_licencia,
            cantidadusuario=data['cantidadusuario'],
            tipolicencia=data['tipolicencia'],
            fechavencimiento=datetime.strptime(data['fechavencimiento'], '%Y-%m-%d').date() if data['tipolicencia'] == 'RENTA' and 'fechavencimiento' in data else None
        )
        db.session.add(nueva_licencia)

        # Crear usuario
        usuario = data['nit']  # Usar NIT como nombre de usuario
        password = generar_password()
        nuevo_usuario = Usuarios(
            IdUsuario=usuario,
            Contraseña=password,
            Descripcion=f"Usuario para {data['razonsocial']}",
            Estado=True
        )
        db.session.add(nuevo_usuario)

        db.session.commit()
        logging.info("Licencia y usuario creados y guardados en la base de datos")

        # Enviar correo
        correo_enviado = enviar_correo(nueva_licencia, usuario, password)
        if not correo_enviado:
            logging.warning("El correo no pudo ser enviado, pero la licencia y el usuario fueron creados.")

        return jsonify({
            'success': True,
            'message': 'Licencia creada exitosamente',
            'correoEnviado': correo_enviado,
            'licencia': {
                'nit': nueva_licencia.nit,
                'razonsocial': nueva_licencia.razonsocial,
                'nombrecomercial': nueva_licencia.nombrecomercial,
                'numerolicencia': nueva_licencia.numerolicencia,
                'tipolicencia': nueva_licencia.tipolicencia,
                'fechavencimiento': nueva_licencia.fechavencimiento.isoformat() if nueva_licencia.fechavencimiento else None
            }
        }), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        logging.error(f"Error de base de datos: {str(e)}")
        return jsonify({'success': False, 'message': f'Error de base de datos: {str(e)}'}), 500
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error al procesar la solicitud: {str(e)}")
        logging.error(traceback.format_exc())
        return jsonify({'success': False, 'message': f'Error al procesar la solicitud: {str(e)}'}), 500

@app.route('/api/verificar_licencia', methods=['POST'])
def verificar_licencia():
    data = request.json
    licencia_ingresada = data['licencia']
    nit = data['nit']
    
    # Buscar la licencia en la base de datos
    licencia = Licencia.query.filter_by(id=licencia_ingresada, nit=nit).first()
    
    if licencia:
        # Aquí puedes agregar más verificaciones si es necesario
        # Por ejemplo, verificar la fecha de vencimiento para licencias de RENTA
        if licencia.tipolicencia == 'RENTA':
            if licencia.fechavencimiento and licencia.fechavencimiento < datetime.now().date():
                return jsonify({'valida': False, 'message': 'La licencia ha expirado'})
        
        return jsonify({'valida': True})
    else:
        return jsonify({'valida': False, 'message': 'Licencia no encontrada'})

@app.route('/api/entradas_inventario', methods=['POST'])
def crear_entrada_inventario():
    data = request.json
    
    nueva_entrada = Entradas1(
        Numero=data['Numero'],
        Mes=data['Mes'],
        IdBodega=data['IdBodega'],
        Observaciones=data['Observaciones'],
        IdUsuario=data['IdUsuario'],
        IdConsecutivo=data['IdConsecutivo']
    )
    db.session.add(nueva_entrada)
    
    for detalle in data['detalles']:
        nuevo_detalle = Entradas2(
            ID=f"{data['Numero']}_{detalle['IdReferencia']}",
            Numero=data['Numero'],
            IdReferencia=detalle['IdReferencia'],
            Descripcion=detalle['Descripcion'],
            Cantidad=detalle['Cantidad'],
            Valor=detalle['Valor'],
            Idunidad=detalle['Idunidad']
        )
        db.session.add(nuevo_detalle)
    
    db.session.commit()
    return jsonify({'message': 'Entrada de inventario creada exitosamente'}), 201

@app.route('/api/consecutivos_disponibles', methods=['GET'])
def obtener_consecutivos_disponibles():
    consecutivos = Consecutivos.query.filter_by(Estado=True).all()
    return jsonify([{'IdConsecutivo': c.IdConsecutivo, 'Consecutivo': c.Consecutivo} for c in consecutivos])

@app.route('/api/consecutivos', methods=['GET'])
def obtener_consecutivos():
    consecutivos = Consecutivos.query.all()
    return jsonify([{
        'IdConsecutivo': c.IdConsecutivo,
        'Consecutivo': c.Consecutivo,
        'Formulario': c.Formulario,
        'Prefijo': c.Prefijo,
        'Desde': c.Desde,
        'Hasta': c.Hasta,
        'Actual': c.Actual,
        'Resolucion': c.Resolucion,
        'FechaResolucion': c.FechaResolucion.strftime('%Y-%m-%d') if c.FechaResolucion else None,
        'ObservacionesResolucion': c.ObservacionesResolucion,
        'Estado': c.Estado,
        'Comprobante': c.Comprobante,
        'fechafinresolucion': c.fechafinresolucion,
        'tiporesolucion': c.tiporesolucion
    } for c in consecutivos])

@app.route('/api/bodegas_disponibles', methods=['GET'])
def obtener_bodegas_disponibles():
    bodegas = Bodegas.query.filter_by(Estado=True).all()
    return jsonify([{'IdBodega': b.IdBodega, 'Descripcion': b.Descripcion} for b in bodegas])

@app.route('/api/consecutivos_entradas_inventario', methods=['GET'])
def obtener_consecutivos_entradas_inventario():
    try:
        # Suponiendo que 'EI' es el código para Entradas de Inventario
        consecutivos = Consecutivos.query.filter_by(Formulario='EI', Estado=True).all()
        return jsonify([{
            'IdConsecutivo': c.IdConsecutivo,
            'Descripcion': c.Consecutivo,
            'Prefijo': c.Prefijo,
            'Actual': c.Actual
        } for c in consecutivos])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ultimo_consecutivo_entradas', methods=['GET'])
def ultimo_consecutivo_entradas():
    try:
        consecutivo = Consecutivos.query.filter_by(Formulario='EI').first()
        if consecutivo:
            ultimo_consecutivo = f"{consecutivo.Prefijo}{consecutivo.Actual.zfill(2)}"
            return jsonify({'success': True, 'ultimoConsecutivo': ultimo_consecutivo})
        else:
            return jsonify({'success': False, 'message': 'No se encontró el consecutivo para Entradas de Inventario'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/salidas_inventario_informes', methods=['GET'])
@cross_origin()
def get_salidas_inventario_informes():
    app.logger.info('Función get_salidas_inventario_informes llamada')
    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin = request.args.get('fecha_fin')
    
    app.logger.info(f'Fechas recibidas: inicio={fecha_inicio}, fin={fecha_fin}')

    if not fecha_inicio or not fecha_fin:
        return jsonify({'error': 'Se requieren fechas de inicio y fin'}), 400

    try:
        fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
        fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Formato de fecha inválido'}), 400

    try:
        # Primero, obtenemos los datos de Salidas1
        salidas1 = Salidas1.query.filter(Salidas1.fecha.between(fecha_inicio, fecha_fin)).all()
        
        resultado = []
        for s1 in salidas1:
            # Luego, para cada salida en Salidas1, buscamos las correspondientes en Salidas2
            salidas2 = Salidas2.query.filter_by(Numero=s1.Numero).all()
            for s2 in salidas2:
                resultado.append({
                    'Numero': s1.Numero,
                    'Fecha': s1.FechaCreacion.strftime('%Y-%m-%d %H:%M:%S') if s1.FechaCreacion else None,
                    'IdReferencia': s2.IdReferencia,
                    'Descripcion': s2.Descripcion,
                    'Cantidad': float(s2.Cantidad) if s2.Cantidad is not None else None,
                    'Valor': float(s2.Valor) if s2.Valor is not None else None,
                    'Total': float(s1.total) if s1.total is not None else None
                })

        app.logger.info(f'Número de salidas encontradas: {len(resultado)}')
        
        return jsonify({
            'salidas': resultado,
            'total_salidas': len(resultado)
        })
    except Exception as e:
        app.logger.error(f'Error en get_salidas_inventario_informes: {str(e)}')
        return jsonify({'error': f'Error al obtener los datos: {str(e)}'}), 500

@app.route('/api/saldos_bodegas', methods=['GET'])
def get_saldos_bodegas():
    id_referencia = request.args.get('idReferencia')
    id_bodega = request.args.get('idBodega')
    mes_actual = datetime.now().strftime('%Y%m')

    saldo = SaldosBodega.query.filter_by(
        IdBodega=id_bodega,
        Mes=mes_actual,
        IdReferencia=id_referencia
    ).first()

    if saldo:
        return jsonify([{
            'IdReferencia': saldo.IdReferencia,
            'IdBodega': saldo.IdBodega,
            'Saldo': float(saldo.Saldo)
        }])
    else:
        return jsonify([])

@app.route('/api/licencia/<nit>', methods=['GET'])
def obtener_licencia_por_nit(nit):
    licencia = Licencia.query.filter_by(nit=nit).first()
    if licencia:
        return jsonify({
            'success': True,
            'licencia': {
                'nit': licencia.nit,
                'razonSocial': licencia.razon_social,
                'nombreComercial': licencia.nombre_comercial,
                'ubicacionComercial': licencia.ubicacion_comercial,
                'ciudad': licencia.ciudad,
                'telefono': licencia.telefono,
                'version': licencia.version,
                'numeroLicencia': licencia.numero_licencia,
                'cantidadUsuarios': licencia.cantidad_usuarios,
                'tipoLicencia': licencia.tipo_licencia,
                'fechaVencimiento': licencia.fecha_vencimiento.isoformat() if licencia.fecha_vencimiento else None
            }
        })
    else:
        return jsonify({'success': False, 'message': 'No se encontró licencia para el NIT proporcionado'}), 404

@app.route('/api/generar_imagen_licencia/<nit>', methods=['GET'])
def generar_imagen_licencia(nit):
    licencia = Licencia.query.filter_by(nit=nit).first()
    if licencia:
        try:
            img = Image.new('RGB', (800, 600), color = (255, 255, 255))
            d = ImageDraw.Draw(img)
            
            logo_path = os.path.join(app.root_path, 'static', 'img', 'Logo.png')
            logo = Image.open(logo_path)
            logo = logo.resize((100, 100))
            img.paste(logo, (10, 10), logo if logo.mode == 'RGBA' else None)
            
            firma_path = os.path.join(app.root_path, 'static', 'img', 'firma.png')
            firma = Image.open(firma_path)
            firma = firma.resize((150, 50))
            img.paste(firma, (600, 500), firma if firma.mode == 'RGBA' else None)

            font_path = os.path.join(app.root_path, 'static', 'fonts', 'arial.ttf')
            font = ImageFont.truetype(font_path, 16)

            d.text((10,120), f"www.migsistemas.com - info@migsistemas.com", font=font, fill=(0,0,0))
            d.text((10,140), f"Cel: 300 225 7898", font=font, fill=(0,0,0))
            d.text((10,180), f"Medellín, {datetime.now().strftime('%d de %B de %Y')}", font=font, fill=(0,0,0))
            d.text((10,220), f"Señores", font=font, fill=(0,0,0))
            d.text((10,240), f"{licencia.nombre_comercial}", font=font, fill=(0,0,0))
            d.text((10,260), f"{licencia.ciudad}", font=font, fill=(0,0,0))
            d.text((10,300), f"REF: Licenciamiento De Software MIG", font=font, fill=(0,0,0))
            d.text((10,340), f"NIT: {licencia.nit}", font=font, fill=(0,0,0))
            d.text((10,360), f"RAZÓN SOCIAL: {licencia.razon_social}", font=font, fill=(0,0,0))
            d.text((10,380), f"NOMBRE COMERCIAL: {licencia.nombre_comercial}", font=font, fill=(0,0,0))
            d.text((10,400), f"UBICACIÓN COMERCIAL: {licencia.ubicacion_comercial}", font=font, fill=(0,0,0))
            d.text((10,420), f"CIUDAD: {licencia.ciudad}", font=font, fill=(0,0,0))
            d.text((10,440), f"TELÉFONO: {licencia.telefono}", font=font, fill=(0,0,0))
            d.text((10,460), f"VERSIÓN: {licencia.version}", font=font, fill=(0,0,0))
            d.text((10,480), f"NUMERO DE LICENCIA: {licencia.numero_licencia}", font=font, fill=(0,0,0))
            d.text((10,500), f"CANTIDAD DE USUARIOS: {licencia.cantidad_usuarios}", font=font, fill=(0,0,0))
            d.text((10,520), f"TIPO LICENCIA: {licencia.tipo_licencia}", font=font, fill=(0,0,0))
            if licencia.fecha_vencimiento:
                d.text((10,540), f"FECHA DE VENCIMIENTO: {licencia.fecha_vencimiento}", font=font, fill=(0,0,0))

            d.text((10,580), "Lo anterior se expide para cumplimiento de requisitos exigidos por la ley,", font=font, fill=(0,0,0))
            d.text((10,600), "para legalidad y autenticidad.", font=font, fill=(0,0,0))
            d.text((10,640), "Cualquier duda con gusto la aclararemos.", font=font, fill=(0,0,0))

            d.text((600,560), "MARY PARRA G.", font=font, fill=(0,0,0))
            d.text((600,580), "SISTEMAS MIG S.A.S", font=font, fill=(0,0,0))
            d.text((600,600), "NIT: 900.275.400-8", font=font, fill=(0,0,0))

            img_io = io.BytesIO()
            img.save(img_io, 'PNG')
            img_io.seek(0)

            return send_file(img_io, mimetype='image/png')
        except Exception as e:
            logging.error(f"Error al generar la imagen de la licencia: {str(e)}")
            return jsonify({'success': False, 'message': 'Error al generar la imagen de la licencia'}), 500
    else:
        return jsonify({'success': False, 'message': 'No se encontró licencia para el NIT proporcionado'}), 404
    
@app.route('/test_email')
def test_email():
    try:
        msg = Message('Test Email desde Flask',
                    sender=app.config['MAIL_DEFAULT_SENDER'],
                    recipients=['riosjuan3053@gmail.com'])
        msg.body = "Este es un correo de prueba enviado desde la aplicación Flask."
        mail.send(msg)
        return "Correo de prueba enviado. Por favor, verifica tu bandeja de entrada y carpeta de spam."
    except Exception as e:
        return f"Error al enviar el correo de prueba: {str(e)}"

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'Recurso no encontrado'}), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'error': 'Error interno del servidor'}), 500

@app.route('/api/test', methods=['GET', 'POST'])
def test_route():
    if request.method == 'POST':
        # Manejar solicitud POST
        data = request.json
        return jsonify({"message": "POST recibido", "data": data})
    else:
        # Manejar solicitud GET
        return jsonify({"message": "Conexión exitosa"})

@app.route('/ping', methods=['GET'])
def ping():
    return "pong"

@app.route('/api/consecutivos', methods=['GET', 'POST', 'PUT'])
def manejar_consecutivos():
    def get_value(data, key, default=None):
        value = data.get(key)
        return value if value not in [None, "", "null", "undefined"] else default

    def obtener_iniciales(formulario):
        mapeo_formularios = {
            'Compras de Mercancía': 'CM',
            'Cotizaciones': 'COT',
            'Cuentas de Cobro': 'CC',
            'Devolución de Compras': 'DC',
            'Entradas de Inventario': 'EI',
            'Gastos': 'GAS',
            'Ordenes de Compra': 'OC',
            'Pedidos': 'PED',
            'Remisiones': 'REM',
            'Salidas': 'SAL',
            'Solicitud de Materiales': 'SM',
            'Traslados de Bodega': 'TB',
            'Inventario Físico': 'IF'
        }
        return mapeo_formularios.get(formulario, formulario[:3].upper())

    def obtener_nombre_completo(iniciales):
        mapeo_inverso = {
            'CM': 'Compras de Mercancía',
            'COT': 'Cotizaciones',
            'CC': 'Cuentas de Cobro',
            'DC': 'Devolución de Compras',
            'EI': 'Entradas de Inventario',
            'GAS': 'Gastos',
            'OC': 'Ordenes de Compra',
            'PED': 'Pedidos',
            'REM': 'Remisiones',
            'SAL': 'Salidas',
            'SM': 'Solicitud de Materiales',
            'TB': 'Traslados de Bodega',
            'IF': 'Inventario Físico'
        }
        return mapeo_inverso.get(iniciales, iniciales)

    if request.method in ['POST', 'PUT']:
        data = request.json
        print("Datos recibidos:", data)  # Log para depuración

        consecutivo_data = {
            'IdConsecutivo': int(get_value(data, 'IdConsecutivo')),
            'Consecutivo': get_value(data, 'Consecutivo'),  # Este es el campo 'Descripción'
            'Formulario': obtener_iniciales(get_value(data, 'Formulario')),
            'Prefijo': get_value(data, 'Prefijo'),
            'Desde': get_value(data, 'Desde'),
            'Hasta': get_value(data, 'Hasta'),
            'Actual': get_value(data, 'Actual'),
            'Resolucion': get_value(data, 'Resolucion'),
            'FechaResolucion': datetime.strptime(get_value(data, 'FechaInicioResolucion'), '%Y-%m-%d').date() if get_value(data, 'FechaInicioResolucion') else None,
            'ObservacionesResolucion': get_value(data, 'Observaciones'),
            'Estado': get_value(data, 'Activo', True),
            'Comprobante': get_value(data, 'TipoDocumentoFactura'),
            'fechafinresolucion': get_value(data, 'FechaFinResolucion'),
            'tiporesolucion': get_value(data, 'Tipo')
        }

        print("Datos procesados:", consecutivo_data)  # Log para depuración

        if request.method == 'POST':
            nuevo_consecutivo = Consecutivos(**consecutivo_data)
            db.session.add(nuevo_consecutivo)
        else:  # PUT
            consecutivo = Consecutivos.query.get(consecutivo_data['IdConsecutivo'])
            if consecutivo:
                for key, value in consecutivo_data.items():
                    setattr(consecutivo, key, value)
            else:
                return jsonify({'message': 'Consecutivo no encontrado'}), 404

        try:
            db.session.commit()
            return jsonify({'message': f'Consecutivo {"creado" if request.method == "POST" else "actualizado"} exitosamente'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': f'Error al {"crear" if request.method == "POST" else "actualizar"} el consecutivo: {str(e)}'}), 500

    if request.method == 'GET':
        consecutivos = Consecutivos.query.all()
        return jsonify([{
            'IdConsecutivo': c.IdConsecutivo,
            'Consecutivo': c.Consecutivo,
            'Formulario': obtener_nombre_completo(c.Formulario),
            'Prefijo': c.Prefijo,
            'Desde': c.Desde,
            'Hasta': c.Hasta,
            'Actual': c.Actual,
            'Resolucion': c.Resolucion,
            'FechaResolucion': c.FechaResolucion.strftime('%Y-%m-%d') if c.FechaResolucion else None,
            'ObservacionesResolucion': c.ObservacionesResolucion,
            'Estado': c.Estado,
            'Comprobante': c.Comprobante,
            'fechafinresolucion': c.fechafinresolucion,
            'tiporesolucion': c.tiporesolucion
        } for c in consecutivos])

@app.route('/api/consecutivos/<int:id>', methods=['GET', 'DELETE'])
def manejar_consecutivo_individual(id):
    consecutivo = Consecutivos.query.get_or_404(id)
    if request.method == 'GET':
        return jsonify({
            'IdConsecutivo': consecutivo.IdConsecutivo,
            'Consecutivo': consecutivo.Consecutivo,
            'Descripcion': consecutivo.Descripcion,
            'Formulario': consecutivo.Formulario,
            'Prefijo': consecutivo.Prefijo,
            'Desde': consecutivo.Desde,
            'Hasta': consecutivo.Hasta,
            'Actual': consecutivo.Actual,
            'Resolucion': consecutivo.Resolucion,
            'FechaInicioResolucion': consecutivo.FechaInicioResolucion.isoformat() if consecutivo.FechaInicioResolucion else None,
            'FechaFinResolucion': consecutivo.FechaFinResolucion.isoformat() if consecutivo.FechaFinResolucion else None,
            'TipoDocumentoFactura': consecutivo.TipoDocumentoFactura,
            'Observaciones': consecutivo.Observaciones,
            'Tipo': consecutivo.Tipo,
            'Estado': consecutivo.Estado
        })
    elif request.method == 'DELETE':
        try:
            db.session.delete(consecutivo)
            db.session.commit()
            return jsonify({'message': 'Consecutivo eliminado exitosamente'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': f'Error al eliminar el consecutivo: {str(e)}'}), 500
        
@app.route('/api/consecutivo_entradas_inventario', methods=['GET'])
def obtener_consecutivo_entradas_inventario():
    consecutivo = Consecutivos.query.filter_by(Formulario='EI').first()
    if consecutivo:
        return jsonify({
            'IdConsecutivo': consecutivo.IdConsecutivo,
            'Consecutivo': consecutivo.Consecutivo,
            'Prefijo': consecutivo.Prefijo,
            'Actual': consecutivo.Actual
        })
    else:
        return jsonify({'error': 'No se encontró el consecutivo para Entradas de Inventario'}), 404

@app.route('/api/actualizar_consecutivo_entradas', methods=['POST'])
def actualizar_consecutivo_entradas():
    try:
        consecutivo = Consecutivos.query.filter_by(Formulario='EI').first()
        if consecutivo:
            actual = int(consecutivo.Actual)
            consecutivo.Actual = str(actual + 1).zfill(2)  # Usamos zfill(2) para tener siempre 2 dígitos
            db.session.commit()
            nuevo_consecutivo = f"{consecutivo.Prefijo}{consecutivo.Actual}"
            return jsonify({'success': True, 'nuevoConsecutivo': nuevo_consecutivo})
        else:
            return jsonify({'success': False, 'message': 'No se encontró el consecutivo para Entradas de Inventario'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})
    
@app.route('/api/verificar_inventario', methods=['GET'])
def verificar_inventario():
    id_referencia = request.args.get('idReferencia')
    id_bodega = request.args.get('idBodega')
    mes_actual = datetime.now().strftime('%Y%m')

    saldo = SaldosBodega.query.filter_by(
        IdBodega=id_bodega,
        Mes=mes_actual,
        IdReferencia=id_referencia
    ).first()

    if saldo:
        saldo_disponible = saldo.SaldoInicial + saldo.Entradas + saldo.Compras - saldo.Salidas - saldo.Ventas
    else:
        saldo_disponible = 0

    return jsonify({
        'disponible': saldo_disponible > 0,
        'saldoDisponible': float(saldo_disponible)
    })
    
@app.route('/api/referencias', methods=['POST', 'PUT'])
def manejar_referencias():
    data = request.json
    
    # Calcular el precio con IVA
    precio_sin_iva = data.get('precioVenta1')
    iva_porcentaje = data.get('iva', 0)
    if precio_sin_iva is not None and iva_porcentaje is not None:
        precio_sin_iva = float(precio_sin_iva)
        iva_porcentaje = float(iva_porcentaje)
        precio_con_iva = precio_sin_iva * (1 + (iva_porcentaje / 100))
    else:
        precio_con_iva = None
    
    referencia_data = {
        'IdReferencia': data.get('codigo'),
        'Referencia': data.get('descripcion'),
        'IdGrupo': data.get('grupo'),
        'IdUnidad': data.get('unidad'),
        'Ubicacion': data.get('ubicacion') or None,
        'Costo': data.get('costo') or None,
        'PrecioVenta1': precio_con_iva,
        'IVA': iva_porcentaje,
        'Marca': data.get('marca') or None,
        'EstadoProducto': data.get('estadoProducto') or None,
        'Estado': data.get('activo', True),
        'Tipo': data.get('esServicio', False),
        'ManejaInventario': not data.get('esServicio', False),
        'productoagotado': data.get('agotado', False),
        'modificaprecio': data.get('modificaPrecio', False),
        'idsubgrupo': data.get('subgrupo') or None,
        'idsubcategoria': data.get('subcategoria') or None,
        'idbodega': data.get('bodega') or None
    }

    try:
        referencia = Referencia.query.get(referencia_data['IdReferencia'])
        if referencia:
            # Si la referencia existe, actualizar sus campos
            for key, value in referencia_data.items():
                setattr(referencia, key, value)
            mensaje = 'Referencia actualizada exitosamente'
        else:
            # Si la referencia no existe, crear una nueva
            nueva_referencia = Referencia(**referencia_data)
            db.session.add(nueva_referencia)
            mensaje = 'Referencia creada exitosamente'

        db.session.commit()
        return jsonify({'message': mensaje}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': f'Error en la base de datos: {str(e)}'}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error inesperado: {str(e)}'}), 500

@app.route('/api/referencias', methods=['GET'])
def obtener_referencias():
    filtro = request.args.get('filtro', '')
    id_bodega = request.args.get('idBodega', '')
    mes_actual = datetime.now().strftime('%Y%m')

    query = text("""
        SELECT 
            r."IdReferencia", 
            r."Referencia", 
            r."PrecioVenta1", 
            r."IVA", 
            r."Ubicacion", 
            r."idbodega", 
            r."IdUnidad", 
            COALESCE(s."Saldo", 0) as Saldo
        FROM 
            referencias r
        LEFT JOIN 
            "SaldosBodega" s
        ON 
            r."IdReferencia" = s."IdReferencia"
            AND s."IdBodega" = :id_bodega
            AND s."Mes" = :mes_actual
        WHERE 
            (r."IdReferencia" ILIKE :filtro OR r."Referencia" ILIKE :filtro)
            AND r."Estado" = True
    """)

    try:
        result = db.session.execute(query, {
            'filtro': f'%{filtro}%',
            'id_bodega': id_bodega,
            'mes_actual': mes_actual
        })
        
        referencias = [{
            'IdReferencia': row.IdReferencia,
            'Referencia': row.Referencia,
            'PrecioVenta1': str(row.PrecioVenta1),
            'IVA': str(row.IVA),
            'Ubicacion': row.Ubicacion,
            'idbodega': row.idbodega,
            'IdUnidad': row.IdUnidad,
            'Saldo': str(row.Saldo)
        } for row in result]

        return jsonify(referencias)
    except Exception as e:
        print(f"Error al obtener referencias: {str(e)}")
        return jsonify({'error': 'Error al obtener referencias'}), 500

@app.route('/api/salidas_inventario', methods=['POST'])
def crear_salida_inventario():
    data = request.json
    
    nueva_salida = Salidas1(
        Numero=data['Numero'],
        Mes=data['Mes'],
        IdBodega=data['IdBodega'],
        Observaciones=data['Observaciones'],
        FechaCreacion=datetime.now(),
        IdUsuario=data['IdUsuario'],
        IdConsecutivo=data['IdConsecutivo'],
        Total=data['Total']
    )
    db.session.add(nueva_salida)
    
    for detalle in data['detalles']:
        nuevo_detalle = Salidas2(
            ID=f"{data['Numero']}_{detalle['IdReferencia']}",
            Numero=data['Numero'],
            IdReferencia=detalle['IdReferencia'],
            Descripcion=detalle['Descripcion'],
            Cantidad=detalle['Cantidad'],
            Valor=detalle['Valor'],
            Subtotal=detalle['Subtotal'],
            Idunidad=detalle['Idunidad']
        )
        db.session.add(nuevo_detalle)
    
    db.session.commit()
    return jsonify({'success': True, 'message': 'Salida de inventario creada exitosamente'}), 201

@app.route('/api/guardar_salida', methods=['POST'])
def guardar_salida():
    data = request.json
    salida1_data = data.get('salida1', {})
    salidas2_data = data.get('salidas2', [])

    try:
        # Asegurarse de que el usuario 'MIG' existe
        get_or_create_mig_user()

        # Crear instancia de Salidas1
        nueva_salida1 = Salidas1(
            Numero=salida1_data['Numero'],
            Mes=salida1_data['Mes'],
            Anulado=salida1_data['Anulado'],
            IdBodega=salida1_data['IdBodega'],
            CuentaDebito=salida1_data.get('CuentaDebito'),
            CuentaCredito=salida1_data.get('CuentaCredito'),
            Observaciones=salida1_data.get('Observaciones'),
            FechaCreacion=datetime.fromisoformat(salida1_data['FechaCreacion']),
            IdUsuario='MIG',
            Recibe=salida1_data.get('Recibe'),
            idproyecto=salida1_data.get('idproyecto'),
            fechamodificacion=datetime.fromisoformat(salida1_data['fechamodificacion']) if salida1_data.get('fechamodificacion') else None,
            IdConsecutivo=salida1_data['IdConsecutivo'],
            op=salida1_data.get('op'),
            fecha=datetime.fromisoformat(salida1_data['fecha']),
            subtotal=Decimal(str(salida1_data.get('subtotal', '0'))),
            total_iva=Decimal(str(salida1_data.get('total_iva', '0'))),
            total_impoconsumo=Decimal(str(salida1_data.get('total_impoconsumo', '0'))),
            total_ipc=Decimal(str(salida1_data.get('total_ipc', '0'))),
            total_ibua=Decimal(str(salida1_data.get('total_ibua', '0'))),
            total_icui=Decimal(str(salida1_data.get('total_icui', '0'))),
            total=Decimal(str(salida1_data.get('total', '0')))
        )
        db.session.add(nueva_salida1)

        # Guardar en Salidas2 y actualizar SaldosBodega
        mes_actual = datetime.now().strftime('%Y%m')
        for salida2 in salidas2_data:
            if not salida2['IdReferencia']:
                continue  # Saltar referencias vacías

            # Verificar si la referencia existe
            referencia = Referencia.query.get(salida2['IdReferencia'])
            if not referencia:
                return jsonify({'success': False, 'message': f'La referencia {salida2["IdReferencia"]} no existe'}), 400

            nueva_salida2 = Salidas2(
                ID=salida2['ID'],
                Numero=salida2['Numero'],
                IdReferencia=salida2['IdReferencia'],
                Descripcion=salida2['Descripcion'],
                Cantidad=Decimal(str(salida2['Cantidad'])),
                Valor=Decimal(str(salida2['Valor'])),
                IVA=Decimal(str(salida2.get('IVA', '0'))),
                Descuento=Decimal('0'),
                lote=salida2.get('lote', ''),
                idunidad=salida2['idunidad'],
                impoconsumo=Decimal(str(salida2.get('impoconsumo', '0'))),
                ipc=Decimal(str(salida2.get('ipc', '0'))),
                imp_ibua=Decimal(str(salida2.get('imp_ibua', '0'))),
                imp_icui=Decimal(str(salida2.get('imp_icui', '0')))
            )
            db.session.add(nueva_salida2)

            # Actualizar SaldosBodega
            saldo = SaldosBodega.query.filter_by(
                IdBodega=salida1_data['IdBodega'],
                Mes=mes_actual,
                IdReferencia=salida2['IdReferencia']
            ).first()

            if saldo:
                saldo.Salidas += Decimal(str(salida2['Cantidad']))
                saldo.Saldo -= Decimal(str(salida2['Cantidad']))
            else:
                nuevo_saldo = SaldosBodega(
                    IdBodega=salida1_data['IdBodega'],
                    Mes=mes_actual,
                    IdReferencia=salida2['IdReferencia'],
                    Salidas=Decimal(str(salida2['Cantidad'])),
                    Saldo=-Decimal(str(salida2['Cantidad'])),
                    SaldoInicial=Decimal('0'),
                    Entradas=Decimal('0'),
                    Compras=Decimal('0'),
                    Ventas=Decimal('0')
                )
                db.session.add(nuevo_saldo)

        db.session.commit()
        return jsonify({'success': True, 'message': 'Salida guardada y saldo actualizado con éxito'})
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error al guardar la salida: {str(e)}")
        return jsonify({'success': False, 'message': f'Error al guardar la salida: {str(e)}'}), 500

@app.route('/api/salidas_inventario/<numero>', methods=['PUT'])
def actualizar_salida_inventario(numero):
    data = request.json
    
    salida = Salidas1.query.filter_by(Numero=numero).first()
    if not salida:
        return jsonify({'success': False, 'message': 'Salida no encontrada'}), 404
    
    salida.Total = data['Total']
    salida.Observaciones = data['Observaciones']
    
    Salidas2.query.filter_by(Numero=numero).delete()
    
    for detalle in data['detalles']:
        nuevo_detalle = Salidas2(
            ID=f"{numero}_{detalle['IdReferencia']}",
            Numero=numero,
            IdReferencia=detalle['IdReferencia'],
            Descripcion=detalle['Descripcion'],
            Cantidad=detalle['Cantidad'],
            Valor=detalle['Valor'],
            Subtotal=detalle['Subtotal'],
            Idunidad=detalle['Idunidad']
        )
        db.session.add(nuevo_detalle)
    
    db.session.commit()
    return jsonify({'success': True, 'message': 'Salida de inventario actualizada exitosamente'})

# Función auxiliar para crear o obtener el usuario 'MIG'
def get_or_create_mig_user():
    mig_user = Usuarios.query.get('MIG')
    if not mig_user:
        mig_user = Usuarios(
            IdUsuario='MIG',
            Contraseña='temp_pwd',
            Descripcion='Usuario default',
            Estado=True
        )
        db.session.add(mig_user)
        db.session.flush()
    return mig_user

@app.route('/api/entradas_informes')
@cross_origin()
def get_entradas_informes():
    app.logger.info('Función get_entradas_informes llamada')
    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin = request.args.get('fecha_fin')
    
    app.logger.info(f'Fechas recibidas: inicio={fecha_inicio}, fin={fecha_fin}')

    if not fecha_inicio or not fecha_fin:
        return jsonify({'error': 'Se requieren fechas de inicio y fin'}), 400

    try:
        fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
        fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Formato de fecha inválido'}), 400

    try:
        # Primero, obtenemos los datos de Entradas1
        entradas1 = Entradas1.query.filter(Entradas1.fecha.between(fecha_inicio, fecha_fin)).all()
        
        resultado = []
        for e1 in entradas1:
            # Luego, para cada entrada en Entradas1, buscamos las correspondientes en Entradas2
            entradas2 = Entradas2.query.filter_by(Numero=e1.Numero).all()
            for e2 in entradas2:
                resultado.append({
                    'Numero': e1.Numero,
                    'Fecha': e1.FechaCreacion.strftime('%Y-%m-%d %H:%M:%S') if e1.FechaCreacion else None,
                    'IdReferencia': e2.IdReferencia,
                    'Descripcion': e2.Descripcion,
                    'Cantidad': float(e2.Cantidad) if e2.Cantidad is not None else None,
                    'Valor': float(e2.Valor) if e2.Valor is not None else None,
                    'Total': float(e1.total) if e1.total is not None else None
                })

        app.logger.info(f'Número de entradas encontradas: {len(resultado)}')
        
        return jsonify({
            'entradas': resultado,
            'total_entradas': len(resultado)
        })
    except Exception as e:
        app.logger.error(f'Error en get_entradas_informes: {str(e)}')
        return jsonify({'error': f'Error al obtener los datos: {str(e)}'}), 500

@app.route('/api/actualizar_consecutivo_salidas_inventario', methods=['POST'])
def actualizar_consecutivo_salidas_inventario():
    try:
        consecutivo = Consecutivos.query.filter_by(Formulario='SAL').first()
        if consecutivo:
            # Incrementar el consecutivo
            actual = int(consecutivo.Actual)
            actual += 1
            # Formatear el nuevo consecutivo con solo dos dígitos
            consecutivo.Actual = f"{actual:02d}"
            db.session.commit()
            
            nuevo_consecutivo = f"{consecutivo.Prefijo}{consecutivo.Actual}"
            return jsonify({'success': True, 'nuevoConsecutivo': nuevo_consecutivo})
        else:
            return jsonify({'success': False, 'message': 'No se encontró el consecutivo para Salidas de Inventario'}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500
    
@app.route('/api/referencias', methods=['POST'])
def crear_referencia():
    data = request.json
    logging.debug(f"Datos recibidos: {data}")
    
    try:
        # Usar el código generado como IdReferencia
        nuevo_id = data.get('codigo')
        if not nuevo_id:
            return jsonify({'error': 'El código del producto es requerido'}), 400

        nueva_referencia = Referencia(
            IdReferencia=nuevo_id,
            Referencia=data['descripcion'],
            IdGrupo=data['grupo'],
            IdUnidad=data['unidad'],
            Costo=data.get('costo', 0),
            PrecioVenta1=data.get('precioVenta1', 0),
            IVA=data.get('iva', 0),
            Ubicacion=data.get('ubicacion'),
            Marca=data.get('marca'),
            EstadoProducto=data.get('estadoProducto', 'Bueno'),
            Estado=data.get('activo', True),
            Tipo=data.get('esServicio', False),
            ManejaInventario=not data.get('esServicio', False),
            productoagotado=data.get('agotado', False),
            idsubgrupo=data.get('subgrupo'),
            idsubcategoria=data.get('subcategoria'),
            idbodega=data.get('bodega'),
            FechaCreacion=datetime.utcnow(),
            StockMinimo=0,
            StockMaximo=0,
            SaldoAntesInv=0,
            Insumo=False,
            costoreal=0
        )
        
        logging.debug(f"Nueva referencia creada: {nueva_referencia.__dict__}")
        
        db.session.add(nueva_referencia)
        db.session.commit()
        
        logging.info(f"Referencia creada exitosamente con código: {nuevo_id}")
        return jsonify({
            'message': 'Referencia creada exitosamente',
            'codigo': nuevo_id
        }), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        logging.error(f"Error de SQLAlchemy: {str(e)}")
        logging.error(f"Detalles del error: {e.__dict__}")
        return jsonify({'error': f'Error de base de datos: {str(e)}'}), 400
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error inesperado: {str(e)}")
        logging.error(f"Detalles del error: {traceback.format_exc()}")
        return jsonify({'error': f'Error inesperado: {str(e)}'}), 500

@app.route('/api/grupos/<string:id_grupo>/siguiente-codigo', methods=['POST'])
def obtener_siguiente_codigo(id_grupo):
    try:
        grupo = Grupo.query.get(id_grupo)
        if not grupo:
            return jsonify({'error': 'Grupo no encontrado'}), 404

        # Incrementar el último código
        if grupo.ultimoCodigo is None:
            grupo.ultimoCodigo = 0
        grupo.ultimoCodigo += 1

        # Generar el nuevo código
        nuevo_codigo = f"{id_grupo}{grupo.ultimoCodigo:02d}"

        # Guardar los cambios
        db.session.commit()

        return jsonify({'nuevoCodigo': nuevo_codigo}), 200
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error al generar siguiente código: {str(e)}")
        return jsonify({'error': 'Error al generar el código'}), 500

if __name__ == '__main__':
    # Configuración para desarrollo local
    app.run(host='0.0.0.0', port=5000, debug=True)
else:
    # Configuración para producción
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', default=5000)))