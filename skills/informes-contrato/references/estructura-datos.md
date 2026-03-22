# Estructura de Datos — Excel de Contratos Condugas

## Modelo de datos aprendido del OYMA (O&M Aguas)

### PRODUCCION (hoja resumen mensual)
```
MES              | date     | Primer día del mes
PRODUCCION       | numeric  | Ingresos facturados al cliente (COP)
ANHO             | int      | Año
ADMINISTRACION   | numeric  | Costos de administración central asignados
COSTO DIRECTO    | numeric  | = PRODUCCION (en este contrato son iguales, verificar)
COSTOS TOTALES   | numeric  | Suma de todos los costos del mes
UAI              | numeric  | Utilidad Antes de Impuestos = PRODUCCION - COSTOS TOTALES
```

**Observaciones:**
- ADMINISTRACION = 0 en todos los meses (¿no se asigna admin central a OYMA?)
- COSTO DIRECTO = PRODUCCION (parece ser la facturación, no el costo real)
- Datos desde abr-2023 hasta ene-2026
- Producción pico: ~$2,700M (abr-may 2024), luego cae a ~$1,400-1,600M

### BASE AD (asientos contables detalle)
```
Cuenta            | char    | Código PUC colombiano (4xxx, 5xxx, 6xxx)
Nombre Cuenta     | char    | Descripción de la cuenta
Nit               | char    | NIT del tercero
Nombre Nit        | char    | Nombre del proveedor/empleado
Documento Ref.    | char    | Referencia del documento
Fecha             | date    | Fecha del asiento
Nro Registro      | char    | Número secuencial
Comprobante       | char    | Tipo de comprobante
Procedencia       | char    | Origen del documento
Documento         | char    | Número de documento
Detalle           | char    | Descripción libre del movimiento
Centro De Costos  | char    | 7001 (Admin), 7002 (Operativo), otros
Debito            | numeric | Monto débito
Credito           | numeric | Monto crédito
Saldo             | numeric | Saldo del movimiento
Tipo              | char    | Tipo de cuenta
Naturaleza        | char    | Naturaleza contable
```

**Observaciones:**
- 132,860 registros en BASE AD
- Cuentas principales vistas: 421020 (Dif. Cambio), 421040 (Descuentos), 425050 (Reintegros)
- Centro De Costos 7001 y 7002 son los principales
- Terceros incluyen: DIAN, proveedores (La Casa del Topógrafo), cruces intercompany (Condugas Comercial, Urabá, Mantenimiento Z3)
- Hay nómina (pagos quincenales), deducciones (celulares, materiales), traslados de inventario

### PBI (Power BI)
- Modelo: OYMA_R1_1
- Filtros: Centro De Costos, Año (2025-2026)
- Fuente de datos: mismo Excel
- Entidades: BASE AD (2), PRODUCCION OYMA (2)
- Tema visual: Condugas personalizado
