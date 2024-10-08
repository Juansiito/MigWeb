PGDMP  3            
        |         
   INVENTARIO    16.3    16.3 G    �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            �           1262    16398 
   INVENTARIO    DATABASE     �   CREATE DATABASE "INVENTARIO" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'Spanish_Colombia.1252';
    DROP DATABASE "INVENTARIO";
                postgres    false            �            1259    32800    Bodegas    TABLE     C  CREATE TABLE public."Bodegas" (
    "IdBodega" character varying(20) NOT NULL,
    "Descripcion" character varying(500) NOT NULL,
    "Estado" boolean NOT NULL,
    "Email" character varying(50),
    nombrepunto character varying(100),
    direccionpunto character varying(100),
    telefonopunto character varying(100)
);
    DROP TABLE public."Bodegas";
       public         heap    postgres    false            �            1259    33278    Consecutivos    TABLE     �  CREATE TABLE public."Consecutivos" (
    "IdConsecutivo" integer NOT NULL,
    "Consecutivo" character varying(50) NOT NULL,
    "Formulario" character varying(3) NOT NULL,
    "Prefijo" character varying(5) NOT NULL,
    "Desde" character varying(10) NOT NULL,
    "Hasta" character varying(10) NOT NULL,
    "Actual" character varying(10) NOT NULL,
    "Resolucion" character varying(15),
    "FechaResolucion" timestamp without time zone,
    "ObservacionesResolucion" text,
    "Estado" boolean NOT NULL,
    "Comprobante" character varying(20),
    "Predeterminado" integer,
    fechafinresolucion text,
    tiporesolucion character varying(20)
);
 "   DROP TABLE public."Consecutivos";
       public         heap    postgres    false            �            1259    32916    Grupos    TABLE     �   CREATE TABLE public."Grupos" (
    "IdGrupo" character varying(10) NOT NULL,
    "Grupo" character varying(50) NOT NULL,
    "Estado" boolean NOT NULL,
    inventario text,
    menupos boolean
);
    DROP TABLE public."Grupos";
       public         heap    postgres    false            �            1259    32949    InventarioFisico1    TABLE     I  CREATE TABLE public."InventarioFisico1" (
    "Numero" character varying(15) NOT NULL,
    "IdBodega" character varying(20) DEFAULT NULL::character varying,
    "Fecha" timestamp without time zone,
    "Observaciones" character varying(200) DEFAULT NULL::character varying,
    "Aprobado" boolean NOT NULL,
    "Entrega" character varying(100) DEFAULT NULL::character varying,
    "Recibe" character varying(100) DEFAULT NULL::character varying,
    "IdUsuario" character varying(15) DEFAULT NULL::character varying,
    fechacreacion timestamp without time zone,
    fechamodificacion timestamp without time zone,
    numeroentrada character varying(50) DEFAULT NULL::character varying,
    numeroentradaajuste character varying(50) DEFAULT NULL::character varying,
    numerosalida character varying(50) DEFAULT NULL::character varying
);
 '   DROP TABLE public."InventarioFisico1";
       public         heap    postgres    false            �            1259    32964    InventarioFisico2    TABLE     �  CREATE TABLE public."InventarioFisico2" (
    "ID" character varying(50) NOT NULL,
    "Numero" character varying(15) NOT NULL,
    "IdReferencia" character varying(50) NOT NULL,
    "Referencia" character varying(500) NOT NULL,
    "Grupo" character varying(50) DEFAULT NULL::character varying,
    "Costo" numeric(14,2) DEFAULT 0 NOT NULL,
    "PrecioVenta1" numeric(14,2) DEFAULT 0 NOT NULL,
    "PrecioVenta2" numeric(14,2) DEFAULT 0 NOT NULL,
    "PrecioVenta3" numeric(14,2) DEFAULT 0 NOT NULL,
    "PrecioVenta4" numeric(14,2) DEFAULT 0 NOT NULL,
    "Ubicacion" character varying(30) DEFAULT NULL::character varying,
    "Saldo" numeric(14,2) DEFAULT NULL::numeric,
    "Cantidad" double precision DEFAULT 0 NOT NULL,
    lote text,
    idunidad text
);
 '   DROP TABLE public."InventarioFisico2";
       public         heap    postgres    false            �            1259    33269    Licencia    TABLE       CREATE TABLE public."Licencia" (
    id text NOT NULL,
    razonsocial text NOT NULL,
    nombrecomercial text NOT NULL,
    fecha timestamp without time zone,
    ubicacioncomercial text NOT NULL,
    ciudad text NOT NULL,
    telefono text NOT NULL,
    version text NOT NULL,
    numerolicencia text NOT NULL,
    cantidadusuario integer NOT NULL,
    numerofacturacompra text,
    fechacompra timestamp without time zone,
    fechavencimiento timestamp without time zone,
    nit text NOT NULL,
    tipolicencia text NOT NULL
);
    DROP TABLE public."Licencia";
       public         heap    postgres    false            �            1259    33159    Referencias    TABLE     �  CREATE TABLE public."Referencias" (
    "IdReferencia" character varying(50) NOT NULL,
    "Referencia" character varying(500) NOT NULL,
    "IdGrupo" character varying(10) NOT NULL,
    "IdUnidad" character varying(10) NOT NULL,
    "StockMinimo" numeric(14,2) DEFAULT 0,
    "StockMaximo" numeric(14,2) DEFAULT 0,
    "Ubicacion" character varying(30) DEFAULT NULL::character varying,
    "IdCentroCosto" character varying(10) DEFAULT NULL::character varying,
    "FechaCreacion" timestamp without time zone NOT NULL,
    "Estado" boolean DEFAULT true NOT NULL,
    "Tipo" boolean DEFAULT false NOT NULL,
    "ReferenciaProveedor" character varying(500) DEFAULT NULL::character varying,
    "Costo" numeric(14,2) DEFAULT 0,
    "PrecioVenta1" numeric(14,2) DEFAULT 0,
    "SaldoAntesInv" numeric(20,5) DEFAULT 0,
    "Insumo" boolean DEFAULT false NOT NULL,
    "IdConceptoContable" character varying(20) DEFAULT NULL::character varying,
    idsubgrupo character varying(10) DEFAULT NULL::character varying,
    idlinea character varying(2) DEFAULT NULL::character varying,
    presentacion boolean,
    "ATRIBUTO3" character varying(50) DEFAULT NULL::character varying,
    "IdUnidadpcc" character varying(10) DEFAULT NULL::character varying,
    porcrentabilidad integer,
    preparacion boolean,
    porcpreciov1 double precision,
    tipocosto character varying(2) DEFAULT NULL::character varying,
    calcularprecioventa boolean,
    "Marca" character varying(10) DEFAULT NULL::character varying,
    "Talla" character varying(10) DEFAULT NULL::character varying,
    "GENERAL" character varying(50) DEFAULT NULL::character varying,
    modelos character varying(500) DEFAULT NULL::character varying,
    manejaseriales boolean,
    metalcontrolado boolean,
    "ALMACENAMIENTO" character varying(50) DEFAULT NULL::character varying,
    "TIPOS" character varying(50) DEFAULT NULL::character varying,
    idgrupocaracteristica character varying(10) DEFAULT NULL::character varying,
    productoagotado boolean,
    ordengrupo integer,
    fechavencimiento timestamp without time zone,
    idbodega text,
    idsubcategoria text,
    "EstadoProducto" character varying(20),
    "IVA" numeric(4,2) DEFAULT 0
);
 !   DROP TABLE public."Referencias";
       public         heap    postgres    false            �            1259    33126    SaldosBodega    TABLE     �  CREATE TABLE public."SaldosBodega" (
    "IdBodega" character varying(20) NOT NULL,
    "Mes" character varying(6) NOT NULL,
    "IdReferencia" character varying(50) NOT NULL,
    "SaldoInicial" numeric(20,2) DEFAULT 0,
    "Ventas" numeric(20,2) DEFAULT 0,
    "Compras" numeric(20,2) DEFAULT 0,
    "Entradas" numeric(20,2),
    "Salidas" numeric(20,2) DEFAULT 0,
    costoponderado numeric(14,5) DEFAULT 0,
    lote text NOT NULL,
    "Saldo" numeric(20,2) DEFAULT 0
);
 "   DROP TABLE public."SaldosBodega";
       public         heap    postgres    false            �            1259    33192    Salidas1    TABLE     z  CREATE TABLE public."Salidas1" (
    "Numero" character varying(15) NOT NULL,
    "Mes" character varying(6) NOT NULL,
    "Anulado" boolean NOT NULL,
    "IdBodega" character varying(20) NOT NULL,
    "CuentaDebito" character varying(50) DEFAULT NULL::character varying,
    "CuentaCredito" character varying(50) DEFAULT NULL::character varying,
    "Observaciones" character varying(500) DEFAULT NULL::character varying,
    "FechaCreacion" timestamp without time zone NOT NULL,
    "IdUsuario" character varying(15) NOT NULL,
    "Recibe" text,
    idproyecto character varying(50) DEFAULT NULL::character varying,
    fechamodificacion timestamp without time zone,
    "IdConsecutivo" integer DEFAULT 14 NOT NULL,
    op character varying(10) DEFAULT NULL::character varying,
    fecha timestamp without time zone,
    transmitido boolean,
    numtraslado text,
    subtotal numeric(14,2) DEFAULT 0,
    total_iva numeric(14,2) DEFAULT 0,
    total_impoconsumo numeric(14,2) DEFAULT 0,
    total_ipc numeric(14,2) DEFAULT 0,
    total_ibua numeric(14,2) DEFAULT 0,
    total_icui numeric(14,2) DEFAULT 0,
    total numeric(14,2) DEFAULT 0
);
    DROP TABLE public."Salidas1";
       public         heap    postgres    false            �            1259    33248    Salidas2    TABLE     +  CREATE TABLE public."Salidas2" (
    "ID" character varying(50) NOT NULL,
    "Numero" character varying(15) NOT NULL,
    "IdReferencia" character varying(50) NOT NULL,
    "Descripcion" character varying(500) NOT NULL,
    "Cantidad" numeric(14,2) NOT NULL,
    "Valor" numeric(14,2) NOT NULL,
    "IVA" numeric(8,2) NOT NULL,
    "Descuento" numeric(14,2) NOT NULL,
    lote text,
    idunidad text,
    impoconsumo numeric(14,2) DEFAULT 0,
    ipc numeric(14,2) DEFAULT 0,
    imp_ibua numeric(14,2) DEFAULT 0,
    imp_icui numeric(14,2) DEFAULT 0
);
    DROP TABLE public."Salidas2";
       public         heap    postgres    false            �            1259    33013 
   Traslados1    TABLE     �  CREATE TABLE public."Traslados1" (
    "Numero" character varying(15) NOT NULL,
    "Mes" character varying(6) NOT NULL,
    "Anulado" boolean NOT NULL,
    "IdBodegaOrigen" character varying(20) NOT NULL,
    "IdBodegaDestino" character varying(20) NOT NULL,
    "CuentaDebito" character varying(50),
    "CuentaCredito" character varying(50),
    "Observaciones" character varying(500),
    "FechaCreacion" timestamp without time zone NOT NULL,
    "IdUsuario" character varying(15) NOT NULL,
    fechamodificacion timestamp without time zone,
    "IdCentroCosto" character varying(10),
    "IdConsecutivo" integer DEFAULT 17 NOT NULL,
    fecha timestamp without time zone,
    subtotal numeric(14,2) DEFAULT 0,
    total_iva numeric(14,2) DEFAULT 0,
    total_impoconsumo numeric(14,2) DEFAULT 0,
    total_ipc numeric(14,2) DEFAULT 0,
    total_ibua numeric(14,2) DEFAULT 0,
    total_icui numeric(14,2) DEFAULT 0,
    total numeric(14,2) DEFAULT 0
);
     DROP TABLE public."Traslados1";
       public         heap    postgres    false            �            1259    33043 
   Traslados2    TABLE     �  CREATE TABLE public."Traslados2" (
    "ID" character varying(25) NOT NULL,
    "Numero" character varying(15) NOT NULL,
    "IdReferencia" character varying(50) NOT NULL,
    "Descripcion" character varying(500) NOT NULL,
    "Cantidad" numeric(14,2) NOT NULL,
    "Valor" numeric(14,2) DEFAULT 0,
    "IVA" numeric(8,2) DEFAULT 0 NOT NULL,
    "Descuento" numeric(14,2) DEFAULT 0,
    idfuente character varying(50),
    numerofuente character varying(50),
    loteorigen text,
    lotedestino text,
    idunidad text,
    impoconsumo numeric(14,2) DEFAULT 0,
    ipc numeric(14,2) DEFAULT 0,
    imp_ibua numeric(14,2) DEFAULT 0,
    imp_icui numeric(14,2) DEFAULT 0
);
     DROP TABLE public."Traslados2";
       public         heap    postgres    false            �            1259    32928    Usuarios    TABLE     W  CREATE TABLE public."Usuarios" (
    "IdUsuario" character varying(15) NOT NULL,
    "Contraseña" character varying(255) NOT NULL,
    "Descripcion" character varying(50) NOT NULL,
    "Estado" boolean DEFAULT true NOT NULL,
    "Grupo" integer,
    email character varying(50) DEFAULT NULL::character varying,
    idgruporeporte integer,
    muestracostoenconsultainventario boolean,
    idbodega character varying(20) DEFAULT NULL::character varying,
    idvendedor character varying(15) DEFAULT NULL::character varying,
    ocultarsaldoinventario boolean,
    apruebainventariofisico boolean
);
    DROP TABLE public."Usuarios";
       public         heap    postgres    false            �            1259    32790    consecutivos    TABLE     �  CREATE TABLE public.consecutivos (
    "IdConsecutivo" integer NOT NULL,
    "Consecutivo" character varying(50) NOT NULL,
    "Formulario" character varying(20) NOT NULL,
    "Prefijo" character varying(5) NOT NULL,
    "Desde" character varying(10) NOT NULL,
    "Hasta" character varying(10) NOT NULL,
    "Actual" character varying(10) NOT NULL,
    "Resolucion" character varying(15) DEFAULT NULL::character varying,
    "FechaResolucion" timestamp without time zone,
    "ObservacionesResolucion" text,
    "Estado" boolean DEFAULT true NOT NULL,
    "Comprobante" character varying(20) DEFAULT NULL::character varying,
    "Predeterminado" integer,
    fechafinresolucion text,
    tiporesolucion text
);
     DROP TABLE public.consecutivos;
       public         heap    postgres    false            �            1259    24743 	   entradas1    TABLE     �  CREATE TABLE public.entradas1 (
    "Numero" character varying(15) NOT NULL,
    "Mes" character varying(6) NOT NULL,
    "Anulado" boolean DEFAULT false NOT NULL,
    "IdBodega" character varying(20) NOT NULL,
    "CuentaDebito" character varying(50) DEFAULT NULL::character varying,
    "CuentaCredito" character varying(50) DEFAULT NULL::character varying,
    "Observaciones" character varying(500) DEFAULT NULL::character varying,
    "FechaCreacion" timestamp without time zone NOT NULL,
    "IdUsuario" character varying(15) NOT NULL,
    "Recibe" character varying(50) DEFAULT NULL::character varying,
    "IdProyecto" character varying(50) DEFAULT NULL::character varying,
    fechamodificacion timestamp without time zone,
    "IdConsecutivo" integer DEFAULT 15 NOT NULL,
    op character varying(10) DEFAULT NULL::character varying,
    fecha timestamp without time zone,
    idcliente character varying(50) DEFAULT NULL::character varying,
    transmitido boolean,
    subtotal numeric(14,2) DEFAULT 0,
    total_iva numeric(14,2) DEFAULT 0,
    total_impoconsumo numeric(14,2) DEFAULT 0,
    total_ipc numeric(14,2) DEFAULT 0,
    total_ibua numeric(14,2) DEFAULT 0,
    total_icui numeric(14,2) DEFAULT 0,
    total numeric(14,2) DEFAULT 0
);
    DROP TABLE public.entradas1;
       public         heap    postgres    false            �            1259    24782 	   entradas2    TABLE     �  CREATE TABLE public.entradas2 (
    "ID" character varying(50) NOT NULL,
    "Numero" character varying(15) NOT NULL,
    "IdReferencia" character varying(50) NOT NULL,
    "Descripcion" character varying(200) NOT NULL,
    "Cantidad" numeric(14,2) DEFAULT 0 NOT NULL,
    "Valor" numeric(14,2) NOT NULL,
    "IVA" numeric(8,2) DEFAULT 0 NOT NULL,
    "Descuento" numeric(14,2) DEFAULT 0 NOT NULL,
    remision character varying(15) DEFAULT NULL::character varying,
    idfuente character varying(30) DEFAULT NULL::character varying,
    lote text,
    idunidad text,
    impoconsumo numeric(14,2) DEFAULT 0,
    ipc numeric(14,2) DEFAULT 0,
    imp_ibua numeric(14,2) DEFAULT 0,
    imp_icui numeric(14,2) DEFAULT 0
);
    DROP TABLE public.entradas2;
       public         heap    postgres    false            �            1259    32923    licencia    TABLE     �  CREATE TABLE public.licencia (
    id text,
    razonsocial text,
    nombrecomercial text,
    fecha timestamp without time zone,
    ubicacioncomercial text,
    ciudad text,
    telefono text,
    version text,
    numerolicencia text,
    cantidadusuario integer,
    numerofacturacompra text,
    fechacompra timestamp without time zone,
    fechavencimiento timestamp without time zone,
    nit text,
    tipolicencia text
);
    DROP TABLE public.licencia;
       public         heap    postgres    false            �            1259    32826    referencias    TABLE     �  CREATE TABLE public.referencias (
    "IdReferencia" character varying(50) NOT NULL,
    "Referencia" character varying(500) NOT NULL,
    "IdGrupo" character varying(10) NOT NULL,
    "IdUnidad" character varying(10) NOT NULL,
    "StockMinimo" numeric(14,2) DEFAULT 0,
    "StockMaximo" numeric(14,2) DEFAULT 0,
    "Ubicacion" character varying(30) DEFAULT NULL::character varying,
    "IdCentroCosto" character varying(10) DEFAULT NULL::character varying,
    "FechaCreacion" timestamp without time zone NOT NULL,
    "Estado" boolean DEFAULT true NOT NULL,
    "Tipo" boolean DEFAULT false NOT NULL,
    "ReferenciaProveedor" character varying(500) DEFAULT NULL::character varying,
    "Costo" numeric(14,2) DEFAULT 0,
    "PrecioVenta1" numeric(14,2) DEFAULT 0,
    "SaldoAntesInv" numeric(20,5) DEFAULT 0,
    "Insumo" boolean DEFAULT false NOT NULL,
    "IdConceptoContable" character varying(20) DEFAULT NULL::character varying,
    "ManejaInventario" boolean DEFAULT false NOT NULL,
    atributada boolean,
    idsubgrupo character varying(10) DEFAULT NULL::character varying,
    idlinea character varying(2) DEFAULT NULL::character varying,
    presentacion boolean,
    "IdUnidadpcc" character varying(10) DEFAULT NULL::character varying,
    porcpreciov1 double precision,
    tipocosto character varying(2) DEFAULT NULL::character varying,
    calcularprecioventa boolean,
    "Marca" character varying(50) DEFAULT NULL::character varying,
    "Talla" character varying(10) DEFAULT NULL::character varying,
    "GENERAL" character varying(50) DEFAULT NULL::character varying,
    modelos character varying(500) DEFAULT NULL::character varying,
    manejaseriales boolean,
    metalcontrolado boolean,
    "ALMACENAMIENTO" character varying(50) DEFAULT NULL::character varying,
    "TIPOS" character varying(50) DEFAULT NULL::character varying,
    idgrupocaracteristica character varying(10) DEFAULT NULL::character varying,
    productoagotado boolean,
    ordengrupo integer,
    numtoques integer,
    modificaprecio boolean,
    costoreal numeric(14,2) DEFAULT 0,
    fechavencimiento timestamp without time zone,
    idbodega text,
    idsubcategoria text,
    "EstadoProducto" character varying(20),
    "IVA" numeric(4,2) DEFAULT 0
);
    DROP TABLE public.referencias;
       public         heap    postgres    false            �          0    32800    Bodegas 
   TABLE DATA           }   COPY public."Bodegas" ("IdBodega", "Descripcion", "Estado", "Email", nombrepunto, direccionpunto, telefonopunto) FROM stdin;
    public          postgres    false    218   D�       �          0    33278    Consecutivos 
   TABLE DATA             COPY public."Consecutivos" ("IdConsecutivo", "Consecutivo", "Formulario", "Prefijo", "Desde", "Hasta", "Actual", "Resolucion", "FechaResolucion", "ObservacionesResolucion", "Estado", "Comprobante", "Predeterminado", fechafinresolucion, tiporesolucion) FROM stdin;
    public          postgres    false    232   ӕ       �          0    32916    Grupos 
   TABLE DATA           U   COPY public."Grupos" ("IdGrupo", "Grupo", "Estado", inventario, menupos) FROM stdin;
    public          postgres    false    220   �       �          0    32949    InventarioFisico1 
   TABLE DATA           �   COPY public."InventarioFisico1" ("Numero", "IdBodega", "Fecha", "Observaciones", "Aprobado", "Entrega", "Recibe", "IdUsuario", fechacreacion, fechamodificacion, numeroentrada, numeroentradaajuste, numerosalida) FROM stdin;
    public          postgres    false    223   5�       �          0    32964    InventarioFisico2 
   TABLE DATA           �   COPY public."InventarioFisico2" ("ID", "Numero", "IdReferencia", "Referencia", "Grupo", "Costo", "PrecioVenta1", "PrecioVenta2", "PrecioVenta3", "PrecioVenta4", "Ubicacion", "Saldo", "Cantidad", lote, idunidad) FROM stdin;
    public          postgres    false    224   R�       �          0    33269    Licencia 
   TABLE DATA           �   COPY public."Licencia" (id, razonsocial, nombrecomercial, fecha, ubicacioncomercial, ciudad, telefono, version, numerolicencia, cantidadusuario, numerofacturacompra, fechacompra, fechavencimiento, nit, tipolicencia) FROM stdin;
    public          postgres    false    231   o�       �          0    33159    Referencias 
   TABLE DATA           �  COPY public."Referencias" ("IdReferencia", "Referencia", "IdGrupo", "IdUnidad", "StockMinimo", "StockMaximo", "Ubicacion", "IdCentroCosto", "FechaCreacion", "Estado", "Tipo", "ReferenciaProveedor", "Costo", "PrecioVenta1", "SaldoAntesInv", "Insumo", "IdConceptoContable", idsubgrupo, idlinea, presentacion, "ATRIBUTO3", "IdUnidadpcc", porcrentabilidad, preparacion, porcpreciov1, tipocosto, calcularprecioventa, "Marca", "Talla", "GENERAL", modelos, manejaseriales, metalcontrolado, "ALMACENAMIENTO", "TIPOS", idgrupocaracteristica, productoagotado, ordengrupo, fechavencimiento, idbodega, idsubcategoria, "EstadoProducto", "IVA") FROM stdin;
    public          postgres    false    228   ��       �          0    33126    SaldosBodega 
   TABLE DATA           �   COPY public."SaldosBodega" ("IdBodega", "Mes", "IdReferencia", "SaldoInicial", "Ventas", "Compras", "Entradas", "Salidas", costoponderado, lote, "Saldo") FROM stdin;
    public          postgres    false    227   ��       �          0    33192    Salidas1 
   TABLE DATA           M  COPY public."Salidas1" ("Numero", "Mes", "Anulado", "IdBodega", "CuentaDebito", "CuentaCredito", "Observaciones", "FechaCreacion", "IdUsuario", "Recibe", idproyecto, fechamodificacion, "IdConsecutivo", op, fecha, transmitido, numtraslado, subtotal, total_iva, total_impoconsumo, total_ipc, total_ibua, total_icui, total) FROM stdin;
    public          postgres    false    229   ��       �          0    33248    Salidas2 
   TABLE DATA           �   COPY public."Salidas2" ("ID", "Numero", "IdReferencia", "Descripcion", "Cantidad", "Valor", "IVA", "Descuento", lote, idunidad, impoconsumo, ipc, imp_ibua, imp_icui) FROM stdin;
    public          postgres    false    230   a�       �          0    33013 
   Traslados1 
   TABLE DATA           E  COPY public."Traslados1" ("Numero", "Mes", "Anulado", "IdBodegaOrigen", "IdBodegaDestino", "CuentaDebito", "CuentaCredito", "Observaciones", "FechaCreacion", "IdUsuario", fechamodificacion, "IdCentroCosto", "IdConsecutivo", fecha, subtotal, total_iva, total_impoconsumo, total_ipc, total_ibua, total_icui, total) FROM stdin;
    public          postgres    false    225   ��       �          0    33043 
   Traslados2 
   TABLE DATA           �   COPY public."Traslados2" ("ID", "Numero", "IdReferencia", "Descripcion", "Cantidad", "Valor", "IVA", "Descuento", idfuente, numerofuente, loteorigen, lotedestino, idunidad, impoconsumo, ipc, imp_ibua, imp_icui) FROM stdin;
    public          postgres    false    226   ӗ       �          0    32928    Usuarios 
   TABLE DATA           �   COPY public."Usuarios" ("IdUsuario", "Contraseña", "Descripcion", "Estado", "Grupo", email, idgruporeporte, muestracostoenconsultainventario, idbodega, idvendedor, ocultarsaldoinventario, apruebainventariofisico) FROM stdin;
    public          postgres    false    222   �       �          0    32790    consecutivos 
   TABLE DATA             COPY public.consecutivos ("IdConsecutivo", "Consecutivo", "Formulario", "Prefijo", "Desde", "Hasta", "Actual", "Resolucion", "FechaResolucion", "ObservacionesResolucion", "Estado", "Comprobante", "Predeterminado", fechafinresolucion, tiporesolucion) FROM stdin;
    public          postgres    false    217   s�       �          0    24743 	   entradas1 
   TABLE DATA           L  COPY public.entradas1 ("Numero", "Mes", "Anulado", "IdBodega", "CuentaDebito", "CuentaCredito", "Observaciones", "FechaCreacion", "IdUsuario", "Recibe", "IdProyecto", fechamodificacion, "IdConsecutivo", op, fecha, idcliente, transmitido, subtotal, total_iva, total_impoconsumo, total_ipc, total_ibua, total_icui, total) FROM stdin;
    public          postgres    false    215   8�       �          0    24782 	   entradas2 
   TABLE DATA           �   COPY public.entradas2 ("ID", "Numero", "IdReferencia", "Descripcion", "Cantidad", "Valor", "IVA", "Descuento", remision, idfuente, lote, idunidad, impoconsumo, ipc, imp_ibua, imp_icui) FROM stdin;
    public          postgres    false    216   ;�       �          0    32923    licencia 
   TABLE DATA           �   COPY public.licencia (id, razonsocial, nombrecomercial, fecha, ubicacioncomercial, ciudad, telefono, version, numerolicencia, cantidadusuario, numerofacturacompra, fechacompra, fechavencimiento, nit, tipolicencia) FROM stdin;
    public          postgres    false    221   �       �          0    32826    referencias 
   TABLE DATA           �  COPY public.referencias ("IdReferencia", "Referencia", "IdGrupo", "IdUnidad", "StockMinimo", "StockMaximo", "Ubicacion", "IdCentroCosto", "FechaCreacion", "Estado", "Tipo", "ReferenciaProveedor", "Costo", "PrecioVenta1", "SaldoAntesInv", "Insumo", "IdConceptoContable", "ManejaInventario", atributada, idsubgrupo, idlinea, presentacion, "IdUnidadpcc", porcpreciov1, tipocosto, calcularprecioventa, "Marca", "Talla", "GENERAL", modelos, manejaseriales, metalcontrolado, "ALMACENAMIENTO", "TIPOS", idgrupocaracteristica, productoagotado, ordengrupo, numtoques, modificaprecio, costoreal, fechavencimiento, idbodega, idsubcategoria, "EstadoProducto", "IVA") FROM stdin;
    public          postgres    false    219   ��       $           2606    32806    Bodegas Bodegas_pkey 
   CONSTRAINT     ^   ALTER TABLE ONLY public."Bodegas"
    ADD CONSTRAINT "Bodegas_pkey" PRIMARY KEY ("IdBodega");
 B   ALTER TABLE ONLY public."Bodegas" DROP CONSTRAINT "Bodegas_pkey";
       public            postgres    false    218            @           2606    33284    Consecutivos Consecutivos_pkey 
   CONSTRAINT     m   ALTER TABLE ONLY public."Consecutivos"
    ADD CONSTRAINT "Consecutivos_pkey" PRIMARY KEY ("IdConsecutivo");
 L   ALTER TABLE ONLY public."Consecutivos" DROP CONSTRAINT "Consecutivos_pkey";
       public            postgres    false    232            (           2606    32922    Grupos Grupos_pkey 
   CONSTRAINT     [   ALTER TABLE ONLY public."Grupos"
    ADD CONSTRAINT "Grupos_pkey" PRIMARY KEY ("IdGrupo");
 @   ALTER TABLE ONLY public."Grupos" DROP CONSTRAINT "Grupos_pkey";
       public            postgres    false    220            ,           2606    32963 (   InventarioFisico1 InventarioFisico1_pkey 
   CONSTRAINT     p   ALTER TABLE ONLY public."InventarioFisico1"
    ADD CONSTRAINT "InventarioFisico1_pkey" PRIMARY KEY ("Numero");
 V   ALTER TABLE ONLY public."InventarioFisico1" DROP CONSTRAINT "InventarioFisico1_pkey";
       public            postgres    false    223            .           2606    32979 (   InventarioFisico2 InventarioFisico2_pkey 
   CONSTRAINT     l   ALTER TABLE ONLY public."InventarioFisico2"
    ADD CONSTRAINT "InventarioFisico2_pkey" PRIMARY KEY ("ID");
 V   ALTER TABLE ONLY public."InventarioFisico2" DROP CONSTRAINT "InventarioFisico2_pkey";
       public            postgres    false    224            <           2606    33277 $   Licencia Licencia_numerolicencia_key 
   CONSTRAINT     m   ALTER TABLE ONLY public."Licencia"
    ADD CONSTRAINT "Licencia_numerolicencia_key" UNIQUE (numerolicencia);
 R   ALTER TABLE ONLY public."Licencia" DROP CONSTRAINT "Licencia_numerolicencia_key";
       public            postgres    false    231            >           2606    33275    Licencia Licencia_pkey 
   CONSTRAINT     X   ALTER TABLE ONLY public."Licencia"
    ADD CONSTRAINT "Licencia_pkey" PRIMARY KEY (id);
 D   ALTER TABLE ONLY public."Licencia" DROP CONSTRAINT "Licencia_pkey";
       public            postgres    false    231            6           2606    33189    Referencias Referencias_pkey 
   CONSTRAINT     j   ALTER TABLE ONLY public."Referencias"
    ADD CONSTRAINT "Referencias_pkey" PRIMARY KEY ("IdReferencia");
 J   ALTER TABLE ONLY public."Referencias" DROP CONSTRAINT "Referencias_pkey";
       public            postgres    false    228            4           2606    33137    SaldosBodega SaldosBodega_pkey 
   CONSTRAINT     �   ALTER TABLE ONLY public."SaldosBodega"
    ADD CONSTRAINT "SaldosBodega_pkey" PRIMARY KEY ("IdBodega", "Mes", "IdReferencia", lote);
 L   ALTER TABLE ONLY public."SaldosBodega" DROP CONSTRAINT "SaldosBodega_pkey";
       public            postgres    false    227    227    227    227            8           2606    33211    Salidas1 Salidas1_pkey 
   CONSTRAINT     ^   ALTER TABLE ONLY public."Salidas1"
    ADD CONSTRAINT "Salidas1_pkey" PRIMARY KEY ("Numero");
 D   ALTER TABLE ONLY public."Salidas1" DROP CONSTRAINT "Salidas1_pkey";
       public            postgres    false    229            :           2606    33258    Salidas2 Salidas2_pkey 
   CONSTRAINT     Z   ALTER TABLE ONLY public."Salidas2"
    ADD CONSTRAINT "Salidas2_pkey" PRIMARY KEY ("ID");
 D   ALTER TABLE ONLY public."Salidas2" DROP CONSTRAINT "Salidas2_pkey";
       public            postgres    false    230            0           2606    33027    Traslados1 Traslados1_pkey 
   CONSTRAINT     b   ALTER TABLE ONLY public."Traslados1"
    ADD CONSTRAINT "Traslados1_pkey" PRIMARY KEY ("Numero");
 H   ALTER TABLE ONLY public."Traslados1" DROP CONSTRAINT "Traslados1_pkey";
       public            postgres    false    225            2           2606    33056    Traslados2 Traslados2_pkey 
   CONSTRAINT     ^   ALTER TABLE ONLY public."Traslados2"
    ADD CONSTRAINT "Traslados2_pkey" PRIMARY KEY ("ID");
 H   ALTER TABLE ONLY public."Traslados2" DROP CONSTRAINT "Traslados2_pkey";
       public            postgres    false    226            *           2606    32936    Usuarios Usuarios_pkey 
   CONSTRAINT     a   ALTER TABLE ONLY public."Usuarios"
    ADD CONSTRAINT "Usuarios_pkey" PRIMARY KEY ("IdUsuario");
 D   ALTER TABLE ONLY public."Usuarios" DROP CONSTRAINT "Usuarios_pkey";
       public            postgres    false    222            "           2606    32799    consecutivos consecutivos_pkey 
   CONSTRAINT     i   ALTER TABLE ONLY public.consecutivos
    ADD CONSTRAINT consecutivos_pkey PRIMARY KEY ("IdConsecutivo");
 H   ALTER TABLE ONLY public.consecutivos DROP CONSTRAINT consecutivos_pkey;
       public            postgres    false    217                       2606    24765    entradas1 entradas1_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.entradas1
    ADD CONSTRAINT entradas1_pkey PRIMARY KEY ("Numero");
 B   ALTER TABLE ONLY public.entradas1 DROP CONSTRAINT entradas1_pkey;
       public            postgres    false    215                        2606    24797    entradas2 entradas2_pkey 
   CONSTRAINT     X   ALTER TABLE ONLY public.entradas2
    ADD CONSTRAINT entradas2_pkey PRIMARY KEY ("ID");
 B   ALTER TABLE ONLY public.entradas2 DROP CONSTRAINT entradas2_pkey;
       public            postgres    false    216            &           2606    32857    referencias referencias_pkey 
   CONSTRAINT     f   ALTER TABLE ONLY public.referencias
    ADD CONSTRAINT referencias_pkey PRIMARY KEY ("IdReferencia");
 F   ALTER TABLE ONLY public.referencias DROP CONSTRAINT referencias_pkey;
       public            postgres    false    219            I           2606    33222    Salidas1 FK_Salidas1_Bodegas    FK CONSTRAINT     �   ALTER TABLE ONLY public."Salidas1"
    ADD CONSTRAINT "FK_Salidas1_Bodegas" FOREIGN KEY ("IdBodega") REFERENCES public."Bodegas"("IdBodega");
 J   ALTER TABLE ONLY public."Salidas1" DROP CONSTRAINT "FK_Salidas1_Bodegas";
       public          postgres    false    4900    229    218            J           2606    33217    Salidas1 FK_Salidas1_Bodegas1    FK CONSTRAINT     �   ALTER TABLE ONLY public."Salidas1"
    ADD CONSTRAINT "FK_Salidas1_Bodegas1" FOREIGN KEY ("IdBodega") REFERENCES public."Bodegas"("IdBodega");
 K   ALTER TABLE ONLY public."Salidas1" DROP CONSTRAINT "FK_Salidas1_Bodegas1";
       public          postgres    false    218    4900    229            L           2606    33264    Salidas2 FK_Salidas1_Salidas2    FK CONSTRAINT     �   ALTER TABLE ONLY public."Salidas2"
    ADD CONSTRAINT "FK_Salidas1_Salidas2" FOREIGN KEY ("Numero") REFERENCES public."Salidas1"("Numero");
 K   ALTER TABLE ONLY public."Salidas2" DROP CONSTRAINT "FK_Salidas1_Salidas2";
       public          postgres    false    4920    230    229            K           2606    33212    Salidas1 FK_Salidas1_Usuarios    FK CONSTRAINT     �   ALTER TABLE ONLY public."Salidas1"
    ADD CONSTRAINT "FK_Salidas1_Usuarios" FOREIGN KEY ("IdUsuario") REFERENCES public."Usuarios"("IdUsuario");
 K   ALTER TABLE ONLY public."Salidas1" DROP CONSTRAINT "FK_Salidas1_Usuarios";
       public          postgres    false    229    4906    222            M           2606    33259     Salidas2 FK_Salidas2_referencias    FK CONSTRAINT     �   ALTER TABLE ONLY public."Salidas2"
    ADD CONSTRAINT "FK_Salidas2_referencias" FOREIGN KEY ("IdReferencia") REFERENCES public.referencias("IdReferencia");
 N   ALTER TABLE ONLY public."Salidas2" DROP CONSTRAINT "FK_Salidas2_referencias";
       public          postgres    false    230    4902    219            A           2606    24798     entradas2 FK_entradas1_entradas2    FK CONSTRAINT     �   ALTER TABLE ONLY public.entradas2
    ADD CONSTRAINT "FK_entradas1_entradas2" FOREIGN KEY ("Numero") REFERENCES public.entradas1("Numero");
 L   ALTER TABLE ONLY public.entradas2 DROP CONSTRAINT "FK_entradas1_entradas2";
       public          postgres    false    216    4894    215            B           2606    32980 /   InventarioFisico2 InventarioFisico2_Numero_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."InventarioFisico2"
    ADD CONSTRAINT "InventarioFisico2_Numero_fkey" FOREIGN KEY ("Numero") REFERENCES public."InventarioFisico1"("Numero");
 ]   ALTER TABLE ONLY public."InventarioFisico2" DROP CONSTRAINT "InventarioFisico2_Numero_fkey";
       public          postgres    false    4908    223    224            G           2606    33138 '   SaldosBodega SaldosBodega_IdBodega_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."SaldosBodega"
    ADD CONSTRAINT "SaldosBodega_IdBodega_fkey" FOREIGN KEY ("IdBodega") REFERENCES public."Bodegas"("IdBodega");
 U   ALTER TABLE ONLY public."SaldosBodega" DROP CONSTRAINT "SaldosBodega_IdBodega_fkey";
       public          postgres    false    218    4900    227            H           2606    33143 +   SaldosBodega SaldosBodega_IdReferencia_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."SaldosBodega"
    ADD CONSTRAINT "SaldosBodega_IdReferencia_fkey" FOREIGN KEY ("IdReferencia") REFERENCES public.referencias("IdReferencia");
 Y   ALTER TABLE ONLY public."SaldosBodega" DROP CONSTRAINT "SaldosBodega_IdReferencia_fkey";
       public          postgres    false    227    219    4902            C           2606    33038 *   Traslados1 Traslados1_IdBodegaDestino_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."Traslados1"
    ADD CONSTRAINT "Traslados1_IdBodegaDestino_fkey" FOREIGN KEY ("IdBodegaDestino") REFERENCES public."Bodegas"("IdBodega");
 X   ALTER TABLE ONLY public."Traslados1" DROP CONSTRAINT "Traslados1_IdBodegaDestino_fkey";
       public          postgres    false    4900    218    225            D           2606    33033 )   Traslados1 Traslados1_IdBodegaOrigen_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."Traslados1"
    ADD CONSTRAINT "Traslados1_IdBodegaOrigen_fkey" FOREIGN KEY ("IdBodegaOrigen") REFERENCES public."Bodegas"("IdBodega");
 W   ALTER TABLE ONLY public."Traslados1" DROP CONSTRAINT "Traslados1_IdBodegaOrigen_fkey";
       public          postgres    false    4900    218    225            E           2606    33028 $   Traslados1 Traslados1_IdUsuario_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."Traslados1"
    ADD CONSTRAINT "Traslados1_IdUsuario_fkey" FOREIGN KEY ("IdUsuario") REFERENCES public."Usuarios"("IdUsuario");
 R   ALTER TABLE ONLY public."Traslados1" DROP CONSTRAINT "Traslados1_IdUsuario_fkey";
       public          postgres    false    222    225    4906            F           2606    33057 !   Traslados2 Traslados2_Numero_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."Traslados2"
    ADD CONSTRAINT "Traslados2_Numero_fkey" FOREIGN KEY ("Numero") REFERENCES public."Traslados1"("Numero");
 O   ALTER TABLE ONLY public."Traslados2" DROP CONSTRAINT "Traslados2_Numero_fkey";
       public          postgres    false    225    4912    226            �      x�30�t�wquwT��s�p��,�,��/�*M�3605vH�M���K�����t�trT03PP61�5��462072�44��20���������ۨ`��W_�`<����w�t��\1z\\\ 9m-      �      x������ � �      �   5   x�����q�u�,���,�24�tw"���g@P����L$F��� �]2      �      x������ � �      �      x������ � �      �      x������ � �      �      x������ � �      �   D   x�30�42021�ഴ40�4�30@"�@�)����@��6Ctmf��̌Q�`��i]� D-2      �   T   x��40�42021��L�40�W��B��R��������D��؜�����1��"+0��!S= 'U����� �a�      �   E   x��40�700�289��]B�C��B]�9M�@2 Ap��y�8�p�	��=... g�a      �      x������ � �      �      x������ � �      �   s   x��404�42���4�-)�����-.M,��W(H,JTpvvQ��sw��t�tT�Tp��	
uv���sV�s��,��Ê�|=�9KRs��S�&���%�������� Ú+L      �   �   x�u��
�0@��W���1ر�e+H+;yɦ�����n2t!�����0�:ϸ��
I���O����?��8�(��n��D`��%����j��q��O�(||8Ds�m���tvh�;�ېw+��lm�HB�Vk�	�	�Wc���{�`.RC�T�3�<��_q��{U��\�!/b@      �   �   x���Aj1е��@��%۲��tѬ�̺�?Bm7�Ц�	a@��!�O�OIc_�%\�=�Ց��� ��B�>�߮-F�]!sqK���E	���GR)=���$o���L��)��<��줏!���M���vIY�ho�m9��Ki%��`Ҭ;Sd�2��S�:EڿRHKz���X����Щ�+�Z��g�����7�g+ӧ��!`~��n-׊�SG��
i㘮���в,�JQn      �   �   x����
�  �>E��$�]�c7=�c�����-F�p��
C �!⌗7 � �a4�g�� � �a�Y�.q?9���b�p��C����Xw`V���LPF��.L
S�u���柠N�N\���O�c _Ϳڽڽ(2s��6����_,���氓      �   �   x�}�=
�0@���/&��JmR�

�VE����b�� ���{\\ͭ>+wy9�H�6��v�Qm�s5n�oBۤ��=v1�1m�kch2Υ-�0A@0�ꊱ��@i�F.Y���+!�'T�~>���|�Fr.$�FƘ,��)�)|0@���c?$[LeQ/ԑ87      �     x��R�N�0=�_�Xd��6疵 zh;��i�J�Ę���I2b�ā$z�b�yO/̘��n�f6ΪHB[�� �R�XX� Q�N݊ij�$A2�������ÍS��l|2������~�޼����<Ξ��p1���`�b����+#��Z3�EcA��_�:����X=�����e�o4t���V]����y%3\Awn��$�(-��?z���[�%���<���*k�E�U�T�y����a�d�� ��{�~י�������/     