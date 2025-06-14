CREATE TRIGGER TRG_CLIENTE_INSERT
AFTER INSERT ON CLIENTE
FOR EACH ROW
INSERT INTO AUDITORIA (
    USUARIO, FECHA_HORA, NOMBRE_TABLA, OPERACION, LLAVE_PRIMARIA, DETALLE
)
VALUES (
    SUBSTRING_INDEX(USER(), '@', 1), NOW(), 'CLIENTE', 'INSERT', NEW.COD_CLI,
    CONCAT('Nuevo registro: ',
        NEW.RSO_CLI , ', ', NEW.DIR_CLI)
);

CREATE TRIGGER TRG_CLIENTE_UPDATE
AFTER UPDATE ON CLIENTE
FOR EACH ROW
INSERT INTO AUDITORIA (
    USUARIO, FECHA_HORA, NOMBRE_TABLA, OPERACION, LLAVE_PRIMARIA, DETALLE
)
VALUES (
    SUBSTRING_INDEX(USER(), '@', 1), NOW(), 'CLIENTE', 'UPDATE', OLD.COD_CLI,
    CONCAT('Registro actualizado: ',
        'Antes: ', OLD.RSO_CLI, ' / Después: ', NEW.RSO_CLI , ', ', 'Antes: ', OLD.DIR_CLI, ' / Después: ', NEW.DIR_CLI)
);

CREATE TRIGGER TRG_CLIENTE_DELETE
AFTER DELETE ON CLIENTE
FOR EACH ROW
INSERT INTO AUDITORIA (
    USUARIO, FECHA_HORA, NOMBRE_TABLA, OPERACION, LLAVE_PRIMARIA, DETALLE
)
VALUES (
    SUBSTRING_INDEX(USER(), '@', 1), NOW(), 'CLIENTE', 'DELETE', OLD.COD_CLI,
    CONCAT('Registro eliminado: ',
        OLD.RSO_CLI , ', ', OLD.DIR_CLI)
);

CREATE TRIGGER TRG_DISTRITO_INSERT
AFTER INSERT ON DISTRITO
FOR EACH ROW
INSERT INTO AUDITORIA (
    USUARIO, FECHA_HORA, NOMBRE_TABLA, OPERACION, LLAVE_PRIMARIA, DETALLE
)
VALUES (
    SUBSTRING_INDEX(USER(), '@', 1), NOW(), 'DISTRITO', 'INSERT', NEW.COD_DIS,
    CONCAT('Nuevo registro: ',
        NEW.NOM_DIS)
);

CREATE TRIGGER TRG_DISTRITO_UPDATE
AFTER UPDATE ON DISTRITO
FOR EACH ROW
INSERT INTO AUDITORIA (
    USUARIO, FECHA_HORA, NOMBRE_TABLA, OPERACION, LLAVE_PRIMARIA, DETALLE
)
VALUES (
    SUBSTRING_INDEX(USER(), '@', 1), NOW(), 'DISTRITO', 'UPDATE', OLD.COD_DIS,
    CONCAT('Registro actualizado: ',
        'Antes: ', OLD.NOM_DIS, ' / Después: ', NEW.NOM_DIS)
);

CREATE TRIGGER TRG_DISTRITO_DELETE
AFTER DELETE ON DISTRITO
FOR EACH ROW
INSERT INTO AUDITORIA (
    USUARIO, FECHA_HORA, NOMBRE_TABLA, OPERACION, LLAVE_PRIMARIA, DETALLE
)
VALUES (
    SUBSTRING_INDEX(USER(), '@', 1), NOW(), 'DISTRITO', 'DELETE', OLD.COD_DIS,
    CONCAT('Registro eliminado: ',
        OLD.NOM_DIS)
);

CREATE TRIGGER TRG_VENDEDOR_INSERT
AFTER INSERT ON VENDEDOR
FOR EACH ROW
INSERT INTO AUDITORIA (
    USUARIO, FECHA_HORA, NOMBRE_TABLA, OPERACION, LLAVE_PRIMARIA, DETALLE
)
VALUES (
    SUBSTRING_INDEX(USER(), '@', 1), NOW(), 'VENDEDOR', 'INSERT', NEW.COD_VEN,
    CONCAT('Nuevo registro: ',
        NEW.NOM_VEN , ', ', NEW.APE_VEN)
);

CREATE TRIGGER TRG_VENDEDOR_UPDATE
AFTER UPDATE ON VENDEDOR
FOR EACH ROW
INSERT INTO AUDITORIA (
    USUARIO, FECHA_HORA, NOMBRE_TABLA, OPERACION, LLAVE_PRIMARIA, DETALLE
)
VALUES (
    SUBSTRING_INDEX(USER(), '@', 1), NOW(), 'VENDEDOR', 'UPDATE', OLD.COD_VEN,
    CONCAT('Registro actualizado: ',
        'Antes: ', OLD.NOM_VEN, ' / Después: ', NEW.NOM_VEN , ', ', 'Antes: ', OLD.APE_VEN, ' / Después: ', NEW.APE_VEN)
);

CREATE TRIGGER TRG_VENDEDOR_DELETE
AFTER DELETE ON VENDEDOR
FOR EACH ROW
INSERT INTO AUDITORIA (
    USUARIO, FECHA_HORA, NOMBRE_TABLA, OPERACION, LLAVE_PRIMARIA, DETALLE
)
VALUES (
    SUBSTRING_INDEX(USER(), '@', 1), NOW(), 'VENDEDOR', 'DELETE', OLD.COD_VEN,
    CONCAT('Registro eliminado: ',
        OLD.NOM_VEN , ', ', OLD.APE_VEN)
);

CREATE TRIGGER TRG_PROVEEDOR_INSERT
AFTER INSERT ON PROVEEDOR
FOR EACH ROW
INSERT INTO AUDITORIA (
    USUARIO, FECHA_HORA, NOMBRE_TABLA, OPERACION, LLAVE_PRIMARIA, DETALLE
)
VALUES (
    SUBSTRING_INDEX(USER(), '@', 1), NOW(), 'PROVEEDOR', 'INSERT', NEW.COD_PRV,
    CONCAT('Nuevo registro: ',
        NEW.RSO_PRV , ', ', NEW.DIR_PRV)
);

CREATE TRIGGER TRG_PROVEEDOR_UPDATE
AFTER UPDATE ON PROVEEDOR
FOR EACH ROW
INSERT INTO AUDITORIA (
    USUARIO, FECHA_HORA, NOMBRE_TABLA, OPERACION, LLAVE_PRIMARIA, DETALLE
)
VALUES (
    SUBSTRING_INDEX(USER(), '@', 1), NOW(), 'PROVEEDOR', 'UPDATE', OLD.COD_PRV,
    CONCAT('Registro actualizado: ',
        'Antes: ', OLD.RSO_PRV, ' / Después: ', NEW.RSO_PRV , ', ', 'Antes: ', OLD.DIR_PRV, ' / Después: ', NEW.DIR_PRV)
);

CREATE TRIGGER TRG_PROVEEDOR_DELETE
AFTER DELETE ON PROVEEDOR
FOR EACH ROW
INSERT INTO AUDITORIA (
    USUARIO, FECHA_HORA, NOMBRE_TABLA, OPERACION, LLAVE_PRIMARIA, DETALLE
)
VALUES (
    SUBSTRING_INDEX(USER(), '@', 1), NOW(), 'PROVEEDOR', 'DELETE', OLD.COD_PRV,
    CONCAT('Registro eliminado: ',
        OLD.RSO_PRV , ', ', OLD.DIR_PRV)
);

CREATE TRIGGER TRG_PRODUCTO_INSERT
AFTER INSERT ON PRODUCTO
FOR EACH ROW
INSERT INTO AUDITORIA (
    USUARIO, FECHA_HORA, NOMBRE_TABLA, OPERACION, LLAVE_PRIMARIA, DETALLE
)
VALUES (
    SUBSTRING_INDEX(USER(), '@', 1), NOW(), 'PRODUCTO', 'INSERT', NEW.COD_PRO,
    CONCAT('Nuevo registro: ',
        NEW.DES_PRO , ', ', NEW.PRE_PRO)
);

CREATE TRIGGER TRG_PRODUCTO_UPDATE
AFTER UPDATE ON PRODUCTO
FOR EACH ROW
INSERT INTO AUDITORIA (
    USUARIO, FECHA_HORA, NOMBRE_TABLA, OPERACION, LLAVE_PRIMARIA, DETALLE
)
VALUES (
    SUBSTRING_INDEX(USER(), '@', 1), NOW(), 'PRODUCTO', 'UPDATE', OLD.COD_PRO,
    CONCAT('Registro actualizado: ',
        'Antes: ', OLD.DES_PRO, ' / Después: ', NEW.DES_PRO , ', ', 'Antes: ', OLD.PRE_PRO, ' / Después: ', NEW.PRE_PRO)
);

CREATE TRIGGER TRG_PRODUCTO_DELETE
AFTER DELETE ON PRODUCTO
FOR EACH ROW
INSERT INTO AUDITORIA (
    USUARIO, FECHA_HORA, NOMBRE_TABLA, OPERACION, LLAVE_PRIMARIA, DETALLE
)
VALUES (
    SUBSTRING_INDEX(USER(), '@', 1), NOW(), 'PRODUCTO', 'DELETE', OLD.COD_PRO,
    CONCAT('Registro eliminado: ',
        OLD.DES_PRO , ', ', OLD.PRE_PRO)
);

CREATE TRIGGER TRG_FACTURA_INSERT
AFTER INSERT ON FACTURA
FOR EACH ROW
INSERT INTO AUDITORIA (
    USUARIO, FECHA_HORA, NOMBRE_TABLA, OPERACION, LLAVE_PRIMARIA, DETALLE
)
VALUES (
    SUBSTRING_INDEX(USER(), '@', 1), NOW(), 'FACTURA', 'INSERT', NEW.NUM_FAC,
    CONCAT('Nuevo registro: ',
        NEW.FEC_FAC , ', ', NEW.COD_CLI , ', ', NEW.EST_FAC)
);

CREATE TRIGGER TRG_FACTURA_UPDATE
AFTER UPDATE ON FACTURA
FOR EACH ROW
INSERT INTO AUDITORIA (
    USUARIO, FECHA_HORA, NOMBRE_TABLA, OPERACION, LLAVE_PRIMARIA, DETALLE
)
VALUES (
    SUBSTRING_INDEX(USER(), '@', 1), NOW(), 'FACTURA', 'UPDATE', OLD.NUM_FAC,
    CONCAT('Registro actualizado: ',
        'Antes: ', OLD.FEC_FAC, ' / Después: ', NEW.FEC_FAC , ', ', 'Antes: ', OLD.COD_CLI, ' / Después: ', NEW.COD_CLI , ', ', 'Antes: ', OLD.EST_FAC, ' / Después: ', NEW.EST_FAC)
);

CREATE TRIGGER TRG_FACTURA_DELETE
AFTER DELETE ON FACTURA
FOR EACH ROW
INSERT INTO AUDITORIA (
    USUARIO, FECHA_HORA, NOMBRE_TABLA, OPERACION, LLAVE_PRIMARIA, DETALLE
)
VALUES (
    SUBSTRING_INDEX(USER(), '@', 1), NOW(), 'FACTURA', 'DELETE', OLD.NUM_FAC,
    CONCAT('Registro eliminado: ',
        OLD.FEC_FAC , ', ', OLD.COD_CLI , ', ', OLD.EST_FAC)
);

CREATE TRIGGER TRG_DETALLE_FACTURA_INSERT
AFTER INSERT ON DETALLE_FACTURA
FOR EACH ROW
INSERT INTO AUDITORIA (
    USUARIO, FECHA_HORA, NOMBRE_TABLA, OPERACION, LLAVE_PRIMARIA, DETALLE
)
VALUES (
    SUBSTRING_INDEX(USER(), '@', 1), NOW(), 'DETALLE_FACTURA', 'INSERT', NEW.NUM_FAC,
    CONCAT('Nuevo registro: ',
        NEW.CAN_VEN , ', ', NEW.PRE_VEN)
);

CREATE TRIGGER TRG_DETALLE_FACTURA_UPDATE
AFTER UPDATE ON DETALLE_FACTURA
FOR EACH ROW
INSERT INTO AUDITORIA (
    USUARIO, FECHA_HORA, NOMBRE_TABLA, OPERACION, LLAVE_PRIMARIA, DETALLE
)
VALUES (
    SUBSTRING_INDEX(USER(), '@', 1), NOW(), 'DETALLE_FACTURA', 'UPDATE', OLD.NUM_FAC,
    CONCAT('Registro actualizado: ',
        'Antes: ', OLD.CAN_VEN, ' / Después: ', NEW.CAN_VEN , ', ', 'Antes: ', OLD.PRE_VEN, ' / Después: ', NEW.PRE_VEN)
);

CREATE TRIGGER TRG_DETALLE_FACTURA_DELETE
AFTER DELETE ON DETALLE_FACTURA
FOR EACH ROW
INSERT INTO AUDITORIA (
    USUARIO, FECHA_HORA, NOMBRE_TABLA, OPERACION, LLAVE_PRIMARIA, DETALLE
)
VALUES (
    SUBSTRING_INDEX(USER(), '@', 1), NOW(), 'DETALLE_FACTURA', 'DELETE', OLD.NUM_FAC,
    CONCAT('Registro eliminado: ',
        OLD.CAN_VEN , ', ', OLD.PRE_VEN)
);

CREATE TRIGGER TRG_ORDEN_COMPRA_INSERT
AFTER INSERT ON ORDEN_COMPRA
FOR EACH ROW
INSERT INTO AUDITORIA (
    USUARIO, FECHA_HORA, NOMBRE_TABLA, OPERACION, LLAVE_PRIMARIA, DETALLE
)
VALUES (
    SUBSTRING_INDEX(USER(), '@', 1), NOW(), 'ORDEN_COMPRA', 'INSERT', NEW.NUM_OCO,
    CONCAT('Nuevo registro: ',
        NEW.FEC_OCO , ', ', NEW.COD_PRV , ', ', NEW.EST_OCO)
);

CREATE TRIGGER TRG_ORDEN_COMPRA_UPDATE
AFTER UPDATE ON ORDEN_COMPRA
FOR EACH ROW
INSERT INTO AUDITORIA (
    USUARIO, FECHA_HORA, NOMBRE_TABLA, OPERACION, LLAVE_PRIMARIA, DETALLE
)
VALUES (
    SUBSTRING_INDEX(USER(), '@', 1), NOW(), 'ORDEN_COMPRA', 'UPDATE', OLD.NUM_OCO,
    CONCAT('Registro actualizado: ',
        'Antes: ', OLD.FEC_OCO, ' / Después: ', NEW.FEC_OCO , ', ', 'Antes: ', OLD.COD_PRV, ' / Después: ', NEW.COD_PRV , ', ', 'Antes: ', OLD.EST_OCO, ' / Después: ', NEW.EST_OCO)
);

CREATE TRIGGER TRG_ORDEN_COMPRA_DELETE
AFTER DELETE ON ORDEN_COMPRA
FOR EACH ROW
INSERT INTO AUDITORIA (
    USUARIO, FECHA_HORA, NOMBRE_TABLA, OPERACION, LLAVE_PRIMARIA, DETALLE
)
VALUES (
    SUBSTRING_INDEX(USER(), '@', 1), NOW(), 'ORDEN_COMPRA', 'DELETE', OLD.NUM_OCO,
    CONCAT('Registro eliminado: ',
        OLD.FEC_OCO , ', ', OLD.COD_PRV , ', ', OLD.EST_OCO)
);

CREATE TRIGGER TRG_DETALLE_COMPRA_INSERT
AFTER INSERT ON DETALLE_COMPRA
FOR EACH ROW
INSERT INTO AUDITORIA (
    USUARIO, FECHA_HORA, NOMBRE_TABLA, OPERACION, LLAVE_PRIMARIA, DETALLE
)
VALUES (
    SUBSTRING_INDEX(USER(), '@', 1), NOW(), 'DETALLE_COMPRA', 'INSERT', NEW.NUM_OCO,
    CONCAT('Nuevo registro: ',
        NEW.CAN_DET)
);

CREATE TRIGGER TRG_DETALLE_COMPRA_UPDATE
AFTER UPDATE ON DETALLE_COMPRA
FOR EACH ROW
INSERT INTO AUDITORIA (
    USUARIO, FECHA_HORA, NOMBRE_TABLA, OPERACION, LLAVE_PRIMARIA, DETALLE
)
VALUES (
    SUBSTRING_INDEX(USER(), '@', 1), NOW(), 'DETALLE_COMPRA', 'UPDATE', OLD.NUM_OCO,
    CONCAT('Registro actualizado: ',
        'Antes: ', OLD.CAN_DET, ' / Después: ', NEW.CAN_DET)
);

CREATE TRIGGER TRG_DETALLE_COMPRA_DELETE
AFTER DELETE ON DETALLE_COMPRA
FOR EACH ROW
INSERT INTO AUDITORIA (
    USUARIO, FECHA_HORA, NOMBRE_TABLA, OPERACION, LLAVE_PRIMARIA, DETALLE
)
VALUES (
    SUBSTRING_INDEX(USER(), '@', 1), NOW(), 'DETALLE_COMPRA', 'DELETE', OLD.NUM_OCO,
    CONCAT('Registro eliminado: ',
        OLD.CAN_DET)
);

CREATE TRIGGER TRG_ABASTECIMIENTO_INSERT
AFTER INSERT ON ABASTECIMIENTO
FOR EACH ROW
INSERT INTO AUDITORIA (
    USUARIO, FECHA_HORA, NOMBRE_TABLA, OPERACION, LLAVE_PRIMARIA, DETALLE
)
VALUES (
    SUBSTRING_INDEX(USER(), '@', 1), NOW(), 'ABASTECIMIENTO', 'INSERT', NEW.COD_PRV,
    CONCAT('Nuevo registro: ',
        NEW.PRE_ABA)
);

CREATE TRIGGER TRG_ABASTECIMIENTO_UPDATE
AFTER UPDATE ON ABASTECIMIENTO
FOR EACH ROW
INSERT INTO AUDITORIA (
    USUARIO, FECHA_HORA, NOMBRE_TABLA, OPERACION, LLAVE_PRIMARIA, DETALLE
)
VALUES (
    SUBSTRING_INDEX(USER(), '@', 1), NOW(), 'ABASTECIMIENTO', 'UPDATE', OLD.COD_PRV,
    CONCAT('Registro actualizado: ',
        'Antes: ', OLD.PRE_ABA, ' / Después: ', NEW.PRE_ABA)
);

CREATE TRIGGER TRG_ABASTECIMIENTO_DELETE
AFTER DELETE ON ABASTECIMIENTO
FOR EACH ROW
INSERT INTO AUDITORIA (
    USUARIO, FECHA_HORA, NOMBRE_TABLA, OPERACION, LLAVE_PRIMARIA, DETALLE
)
VALUES (
    SUBSTRING_INDEX(USER(), '@', 1), NOW(), 'ABASTECIMIENTO', 'DELETE', OLD.COD_PRV,
    CONCAT('Registro eliminado: ',
        OLD.PRE_ABA)
);
