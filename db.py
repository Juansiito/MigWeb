from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.dialects.postgresql import NUMERIC
from sqlalchemy.sql import func
from sqlalchemy import Column, String, Numeric, Text, ForeignKey, Boolean, Integer, DateTime, Float
from sqlalchemy.orm import relationship
import uuid
from sqlalchemy.dialects.postgresql import UUID

db = SQLAlchemy()

def init_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost/INVENTARIO'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

class Bodegas(db.Model):
    __tablename__ = 'Bodegas'
    IdBodega = Column(String(20), primary_key=True)
    Descripcion = Column(String(500), nullable=False)
    Estado = Column(Boolean, nullable=False)
    Email = Column(String(50))
    nombrepunto = Column(String(100))
    direccionpunto = Column(String(100))
    telefonopunto = Column(String(100))
    saldos = relationship('SaldosBodega', back_populates='bodega')

class Licencia(db.Model):
    __tablename__ = 'licencia'
    id = Column(Text, primary_key=True)
    razonsocial = Column(Text, nullable=False)
    nombrecomercial = Column(Text, nullable=False)
    fecha = Column(DateTime, default=func.now())
    ubicacioncomercial = Column(Text, nullable=False)
    ciudad = Column(Text, nullable=False)
    telefono = Column(Text, nullable=False)
    version = Column(Text, nullable=False)
    numerolicencia = Column(Text, nullable=False, unique=True)
    cantidadusuario = Column(Integer, nullable=False)
    numerofacturacompra = Column(Text)
    fechacompra = Column(DateTime)
    fechavencimiento = Column(DateTime)
    nit = Column(Text, nullable=False)
    tipolicencia = Column(Text, nullable=False)

class Consecutivos(db.Model):
    __tablename__ = 'consecutivos'
    IdConsecutivo = Column(Integer, primary_key=True, autoincrement=False)
    Consecutivo = Column(String(50), nullable=False)
    Formulario = Column(String(3), nullable=False)
    Prefijo = Column(String(5), nullable=False)
    Desde = Column(String(10), nullable=False)
    Hasta = Column(String(10), nullable=False)
    Actual = Column(String(10), nullable=False)
    Resolucion = Column(String(15))
    FechaResolucion = Column(DateTime)
    ObservacionesResolucion = Column(Text)
    Estado = Column(Boolean, nullable=False, default=True)
    Comprobante = Column(String(20))
    Predeterminado = Column(Integer)
    fechafinresolucion = Column(Text)
    tiporesolucion = Column(String(20))

class Entradas1(db.Model):
    __tablename__ = 'entradas1'
    Numero = Column(String(15), primary_key=True)
    Mes = Column(String(6), nullable=False)
    Anulado = Column(Boolean, nullable=False, default=False)
    IdBodega = Column(String(20), ForeignKey('Bodegas.IdBodega'), nullable=False)
    CuentaDebito = Column(String(50))
    CuentaCredito = Column(String(50))
    Observaciones = Column(String(500))
    FechaCreacion = Column(DateTime, nullable=False)
    IdUsuario = Column(String(15), ForeignKey('Usuarios.IdUsuario'), nullable=False)
    Recibe = Column(String(50))
    IdProyecto = Column(String(50))
    fechamodificacion = Column(DateTime)
    IdConsecutivo = Column(Integer, nullable=False, default=15)
    op = Column(String(10))
    fecha = Column(DateTime)
    idcliente = Column(String(50))
    transmitido = Column(Boolean)
    subtotal = Column(Numeric(14, 2), default=0)
    total_iva = Column(Numeric(14, 2), default=0)
    total_impoconsumo = Column(Numeric(14, 2), default=0)
    total_ipc = Column(Numeric(14, 2), default=0)
    total_ibua = Column(Numeric(14, 2), default=0)
    total_icui = Column(Numeric(14, 2), default=0)
    total = Column(Numeric(14, 2), default=0)

    bodega = relationship('Bodegas', backref='entradas1')
    usuario = relationship('Usuarios', backref='entradas1')

class Entradas2(db.Model):
    __tablename__ = 'entradas2'
    ID = Column(String(50), primary_key=True)
    Numero = Column(String(15), ForeignKey('entradas1.Numero'), nullable=False)
    IdReferencia = Column(String(50), ForeignKey('referencias.IdReferencia'), nullable=False)
    Descripcion = Column(String(500), nullable=False)
    Cantidad = Column(Numeric(14, 2), nullable=False, default=0)
    Valor = Column(Numeric(14, 2), nullable=False)
    IVA = Column(Numeric(8, 2), nullable=False, default=0)
    Descuento = Column(Numeric(14, 2), nullable=False, default=0)
    remision = Column(String(15))
    idfuente = Column(String(30))
    lote = Column(Text)
    idunidad = Column(Text)
    impoconsumo = Column(Numeric(14, 2), default=0)
    ipc = Column(Numeric(14, 2), default=0)
    imp_ibua = Column(Numeric(14, 2), default=0)
    imp_icui = Column(Numeric(14, 2), default=0)

    entrada1 = relationship('Entradas1', backref='entradas2')
    referencia = relationship('Referencia', backref='entradas2')

class Salidas1(db.Model):
    __tablename__ = 'Salidas1'
    Numero = Column(String(15), primary_key=True)
    Mes = Column(String(6), nullable=True)
    Anulado = Column(Boolean, nullable=True)
    IdBodega = Column(String(20), ForeignKey('Bodegas.IdBodega'), nullable=True)
    CuentaDebito = Column(String(50), nullable=True)
    CuentaCredito = Column(String(50), nullable=True)
    Observaciones = Column(String(500))
    FechaCreacion = Column(DateTime, nullable=False, default=datetime.utcnow)
    IdUsuario = Column(String(15), ForeignKey('Usuarios.IdUsuario'), nullable=True)
    Recibe = Column(Text)
    idproyecto = Column(String(50))
    fechamodificacion = Column(DateTime)
    IdConsecutivo = Column(Integer, nullable=True, default=14)
    op = Column(String(10))
    fecha = Column(DateTime)
    subtotal = Column(NUMERIC(14, 2), default=0)
    total = Column(NUMERIC(14, 2), default=0)
    total_iva = db.Column(db.Numeric(14, 2), default=0)
    total_impoconsumo = db.Column(db.Numeric(14, 2), default=0)
    total_ipc = db.Column(db.Numeric(14, 2), default=0)
    total_ibua = db.Column(db.Numeric(14, 2), default=0)
    total_icui = db.Column(db.Numeric(14, 2), default=0)

    bodega = relationship('Bodegas', backref='salidas1')
    usuario = relationship('Usuarios', backref='salidas1')

class Salidas2(db.Model):
    __tablename__ = 'Salidas2'
    ID = Column(String(50), primary_key=True)
    Numero = Column(String(15), ForeignKey('Salidas1.Numero'), nullable=False)
    IdReferencia = Column(String(50), ForeignKey('referencias.IdReferencia'), nullable=False)
    Descripcion = Column(String(500), nullable=False)
    Cantidad = Column(NUMERIC(14, 2), nullable=False)
    Valor = Column(NUMERIC(14, 2), nullable=False)
    lote = Column(Text)
    idunidad = Column(Text)
    IVA = db.Column(db.Numeric(14, 2), default=0)  # Añadido campo IVA
    Descuento = db.Column(db.Numeric(14, 2), default=0)
    impoconsumo = db.Column(db.Numeric(14, 2), default=0)
    ipc = db.Column(db.Numeric(14, 2), default=0)
    imp_ibua = db.Column(db.Numeric(14, 2), default=0)
    imp_icui = db.Column(db.Numeric(14, 2), default=0)

    salida1 = relationship('Salidas1', backref='salidas2')
    referencia = relationship('Referencia', backref='salidas2')

class Traslados1(db.Model):
    __tablename__ = 'Traslados1'
    Numero = Column(String(15), primary_key=True)
    Mes = Column(String(6), nullable=False)
    Anulado = Column(Boolean, nullable=False)
    IdBodegaOrigen = Column(String(20), ForeignKey('Bodegas.IdBodega'), nullable=False)
    IdBodegaDestino = Column(String(20), ForeignKey('Bodegas.IdBodega'), nullable=False)
    CuentaDebito = Column(String(50))
    CuentaCredito = Column(String(50))
    Observaciones = Column(String(500))
    FechaCreacion = Column(DateTime, nullable=False)
    IdUsuario = Column(String(15), ForeignKey('Usuarios.IdUsuario'), nullable=False)
    fechamodificacion = Column(DateTime)
    IdCentroCosto = Column(String(10))
    IdConsecutivo = Column(Integer, nullable=False, default=17)
    fecha = Column(DateTime)
    subtotal = Column(Numeric(14, 2), default=0)
    total_iva = Column(Numeric(14, 2), default=0)
    total_impoconsumo = Column(Numeric(14, 2), default=0)
    total_ipc = Column(Numeric(14, 2), default=0)
    total_ibua = Column(Numeric(14, 2), default=0)
    total_icui = Column(Numeric(14, 2), default=0)
    total = Column(Numeric(14, 2), default=0)

    bodega_origen = relationship('Bodegas', foreign_keys=[IdBodegaOrigen])
    bodega_destino = relationship('Bodegas', foreign_keys=[IdBodegaDestino])
    usuario = relationship('Usuarios', backref='traslados1')

class Traslados2(db.Model):
    __tablename__ = 'Traslados2'
    ID = Column(String(25), primary_key=True)
    Numero = Column(String(15), ForeignKey('Traslados1.Numero'), nullable=False)
    IdReferencia = Column(String(50), ForeignKey('referencias.IdReferencia'), nullable=False)
    Descripcion = Column(String(500), nullable=False)
    Cantidad = Column(Numeric(14, 2), nullable=False)
    Valor = Column(Numeric(14, 2), default=0)
    IVA = Column(Numeric(8, 2), nullable=False, default=0)
    Descuento = Column(Numeric(14, 2), default=0)
    idfuente = Column(String(50))
    numerofuente = Column(String(50))
    loteorigen = Column(Text)
    lotedestino = Column(Text)
    idunidad = Column(Text)
    impoconsumo = Column(Numeric(14, 2), default=0)
    ipc = Column(Numeric(14, 2), default=0)
    imp_ibua = Column(Numeric(14, 2), default=0)
    imp_icui = Column(Numeric(14, 2), default=0)

    traslado1 = relationship('Traslados1', backref='traslados2')
    referencia = relationship('Referencia', backref='traslados2')

class SaldosBodega(db.Model):
    __tablename__ = 'SaldosBodega'
    IdBodega = Column(String(20), ForeignKey('Bodegas.IdBodega'), primary_key=True)
    Mes = Column(String(6), primary_key=True)
    IdReferencia = Column(String(50), ForeignKey('referencias.IdReferencia'), primary_key=True)
    SaldoInicial = Column(Numeric(20, 2), default=0)
    Ventas = Column(Numeric(20, 2), default=0)
    Compras = Column(Numeric(20, 2), default=0)
    Entradas = Column(Numeric(20, 2), default=0)
    Salidas = Column(Numeric(20, 2), default=0)
    Saldo = Column(Numeric(20, 2), default=0)  # Nueva columna
    costoponderado = Column(Numeric(14, 5), default=0)
    lote = Column(Text, nullable=True)  # Cambiado a nullable=True

    bodega = relationship('Bodegas', back_populates='saldos')
    referencia = relationship('Referencia', back_populates='saldos')

class Referencia(db.Model):
    __tablename__ = 'referencias'
    IdReferencia = db.Column(db.String(50), primary_key=True, nullable=False)
    Referencia = Column(String(500), nullable=False)
    IdGrupo = Column(String(10), ForeignKey('Grupos.IdGrupo'), nullable=False)
    IdUnidad = Column(String(10), ForeignKey('Unidades.IdUnidad'), nullable=False)
    StockMinimo = Column(Numeric(14, 2), default=0)
    StockMaximo = Column(Numeric(14, 2), default=0)
    Ubicacion = Column(String(30))
    IdCentroCosto = Column(String(10))
    FechaCreacion = Column(DateTime, nullable=False, default=datetime.utcnow)
    Estado = Column(Boolean, nullable=False, default=True)
    Tipo = Column(Boolean, nullable=False, default=False)
    ReferenciaProveedor = Column(String(500))
    Costo = Column(Numeric(14, 2), default=0)
    PrecioVenta1 = Column(Numeric(14, 2), default=0)
    SaldoAntesInv = Column(Numeric(20, 5), default=0)
    Insumo = Column(Boolean, nullable=False, default=False)
    IdConceptoContable = Column(String(20))
    ManejaInventario = Column(Boolean, nullable=False, default=False)
    atributada = Column(Boolean)
    idsubgrupo = Column(String(10), ForeignKey('SubGrupos.IdSubgrupo'))
    idlinea = Column(String(2))
    presentacion = Column(Boolean)
    IdUnidadpcc = Column(String(10))
    porcpreciov1 = Column(Float)
    tipocosto = Column(String(2))
    calcularprecioventa = Column(Boolean)
    Marca = Column(String(50))
    Talla = Column(String(10))
    GENERAL = Column(String(50))
    modelos = Column(String(500))
    manejaseriales = Column(Boolean)
    metalcontrolado = Column(Boolean)
    ALMACENAMIENTO = Column(String(50))
    TIPOS = Column(String(50))
    idgrupocaracteristica = Column(String(10))
    productoagotado = Column(Boolean)
    ordengrupo = Column(Integer)
    numtoques = Column(Integer)
    modificaprecio = Column(Boolean)
    costoreal = Column(Numeric(14, 2), default=0)
    fechavencimiento = Column(DateTime)
    idbodega = Column(Text)
    idsubcategoria = Column(Text, ForeignKey('subcategorias.idsubcategoria'))
    EstadoProducto = Column(String(20))
    IVA = Column(Numeric(4, 2), default=0)

    grupo = relationship('Grupo', backref='referencias')
    saldos = relationship('SaldosBodega', back_populates='referencia')
    subgrupo = relationship('SubGrupos', backref='referencias')
    subcategoria = relationship('Subcategorias', backref='referencias')
    unidad = relationship('Unidades', backref='referencias')
    EstadoProducto = Column(String(20), ForeignKey('EstadoProducto.EstadoProducto'))
    estado_producto = relationship('EstadoProducto', back_populates='referencias')

class Proveedores(db.Model):
    __tablename__ = 'Proveedores'
    Nit = Column(String(50), primary_key=True)
    RazonSocial = Column(String(100), nullable=False)
    Contacto1 = Column(String(50))
    Direccion = Column(String(100))
    Telefono1 = Column(String(50))
    IdCiudad = Column(String(10))
    Autoretenedor = Column(Boolean)
    RS = Column(Boolean)
    Actividad = Column(String(20))
    Email = Column(String(50))
    Contacto2 = Column(String(50))
    Contacto3 = Column(String(50))
    Estado = Column(Boolean, nullable=False, default=True)
    DiasCredito = Column(Integer)
    IdDepartamento = Column(String(5))
    IdTipoTercero = Column(String(5))
    CxP = Column(String(20))
    DV = Column(String(1))
    retefuente = Column(Boolean)
    clasificacion = Column(Integer)
    consignacion = Column(Boolean)
    tipo = Column(String(2))
    IdActividadEconomica = Column(String(20))
    aplicareteica = Column(Boolean)
    fechacreacion = Column(DateTime)

class Unidades(db.Model):
    __tablename__ = 'Unidades'
    IdUnidad = Column(String(10), primary_key=True)
    Unidad = Column(String(50), nullable=False)
    Estado = Column(Boolean, default=True)

class SubGrupos(db.Model):
    __tablename__ = 'SubGrupos'
    IdSubgrupo = Column(String(10), primary_key=True)
    Subgrupo = Column(String(50), nullable=False)
    IdGrupo = Column(String(10), ForeignKey('Grupos.IdGrupo'), nullable=False)
    Estado = Column(Boolean, nullable=False, default=True)

    grupo = relationship('Grupo', backref='subgrupos')

class Subcategorias(db.Model):
    __tablename__ = 'subcategorias'
    idsubcategoria = Column(Text, primary_key=True)
    categoria = Column(Text)
    idgrupo = Column(Text, ForeignKey('Grupos.IdGrupo'))
    idsubgrupo = Column(Text, ForeignKey('SubGrupos.IdSubgrupo'))
    estado = Column(Boolean)

    grupo = relationship('Grupo', backref='subcategorias')
    subgrupo = relationship('SubGrupos', backref='subcategorias')

class Grupo(db.Model):
    __tablename__ = 'Grupos'
    IdGrupo = Column(String(10), primary_key=True)
    Grupo = Column(String(50), nullable=False)
    Estado = Column(Boolean, nullable=False)
    inventario = Column(Text)
    menupos = Column(Boolean, default=None)
    ultimoCodigo = db.Column(db.Integer, default=0)  # Nuevo campo

class EstadoProducto(db.Model):
    __tablename__ = 'EstadoProducto'
    IdEstadoProducto = Column(String(10), primary_key=True)
    EstadoProducto = Column(String(50), nullable=False)
    Estado = Column(Boolean, nullable=False)

    referencias = relationship('Referencia', back_populates='estado_producto')

class Usuarios(db.Model):
    __tablename__ = 'Usuarios'
    IdUsuario = Column(String(15), primary_key=True)
    Contraseña = Column(String(255), nullable=False)  # Aumentado a 255 para hash seguro
    Descripcion = Column(String(50), nullable=False)
    Estado = Column(Boolean, nullable=False, default=True)
    Grupo = Column(Integer)
    email = Column(String(50))
    idgruporeporte = Column(Integer)
    muestracostoenconsultainventario = Column(Boolean)
    idbodega = Column(String(20), ForeignKey('Bodegas.IdBodega'))
    idvendedor = Column(String(15))
    ocultarsaldoinventario = Column(Boolean)
    apruebainventariofisico = Column(Boolean)

    bodega = relationship('Bodegas', backref='usuarios')

    def set_password(self, password):
        self.Contraseña = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.Contraseña, password)

# Añadir índices para mejorar el rendimiento
db.Index('idx_entradas1_idbodega', Entradas1.IdBodega)
db.Index('idx_entradas2_idreferencia', Entradas2.IdReferencia)
db.Index('idx_salidas1_idbodega', Salidas1.IdBodega)
db.Index('idx_salidas2_idreferencia', Salidas2.IdReferencia)
db.Index('idx_traslados1_idbodegaorigen', Traslados1.IdBodegaOrigen)
db.Index('idx_traslados1_idbodegadestino', Traslados1.IdBodegaDestino)
db.Index('idx_traslados2_idreferencia', Traslados2.IdReferencia)
db.Index('idx_saldosbodega_idreferencia', SaldosBodega.IdReferencia)
db.Index('idx_referencia_idgrupo', Referencia.IdGrupo)
db.Index('idx_subgrupos_idgrupo', SubGrupos.IdGrupo)
db.Index('idx_subcategorias_idgrupo', Subcategorias.idgrupo)
db.Index('idx_subcategorias_idsubgrupo', Subcategorias.idsubgrupo)

def init_app(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()

# Funciones auxiliares para operaciones comunes

def actualizar_saldo_bodega(id_bodega, id_referencia, cantidad, tipo_movimiento):
    """
    Actualiza el saldo de una referencia en una bodega específica.
    tipo_movimiento puede ser 'entrada', 'salida', 'venta', o 'compra'
    """
    mes_actual = datetime.now().strftime('%Y%m')
    saldo = SaldosBodega.query.filter_by(
        IdBodega=id_bodega, 
        IdReferencia=id_referencia, 
        Mes=mes_actual
    ).first()

    if not saldo:
        saldo = SaldosBodega(
            IdBodega=id_bodega,
            IdReferencia=id_referencia,
            Mes=mes_actual,
            SaldoInicial=0,
            Ventas=0,
            Compras=0,
            Entradas=0,
            Salidas=0
        )
        db.session.add(saldo)

    if tipo_movimiento == 'entrada':
        saldo.Entradas += cantidad
    elif tipo_movimiento == 'salida':
        saldo.Salidas += cantidad
    elif tipo_movimiento == 'venta':
        saldo.Ventas += cantidad
    elif tipo_movimiento == 'compra':
        saldo.Compras += cantidad

    db.session.commit()

def obtener_saldo_actual(id_bodega, id_referencia):
    """
    Obtiene el saldo actual de una referencia en una bodega específica
    """
    mes_actual = datetime.now().strftime('%Y%m')
    saldo = SaldosBodega.query.filter_by(
        IdBodega=id_bodega, 
        IdReferencia=id_referencia, 
        Mes=mes_actual
    ).first()

    if saldo:
        return (saldo.SaldoInicial + saldo.Entradas + saldo.Compras - 
                saldo.Salidas - saldo.Ventas)
    return 0

def registrar_movimiento(modelo, datos):
    """
    Registra un movimiento (entrada, salida, traslado) en la base de datos
    """
    nuevo_movimiento = modelo(**datos)
    db.session.add(nuevo_movimiento)
    db.session.commit()
    return nuevo_movimiento