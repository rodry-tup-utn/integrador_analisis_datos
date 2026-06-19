# Informe de Gestión — Cadena Comercial

**Trabajo Integrador - Análisis de Datos con Python**  
**Tecnicatura Universitaria en Programación - UTN FRM**  
**Integrantes:** Mercado, Leandro — Ramirez, Rodrigo  
**Fecha:** 26/06/2026

---

## 1. Resumen Ejecutivo

El presente informe analiza un dataset de 15.000 transacciones comerciales de una cadena de comercios en Argentina, Chile y Perú, durante el período enero 2023 — marzo 2024. Luego de dos iteraciones de limpieza y transformación de datos, se construyó un dashboard interactivo en Streamlit y se respondieron cuatro preguntas de negocio clave. El análisis revela que la rentabilidad es homogénea entre países y ciudades, el método de pago no influye en el monto gastado, y que existe una oportunidad clara de mejora en la segmentación y fidelización de clientes.

---

## 2. Contexto del Dataset

- **Registros originales:** 15.000 transacciones
- **Registros finales (tras limpieza):** 12.226
- **Países:** Argentina, Chile, Perú
- **Periodo:** Enero 2023 — Marzo 2024
- **Columnas principales:** ID_Transaccion, Fecha, ID_Cliente, Pais, Ciudad, Categoria, Subcategoria, Producto, Cantidad, Precio_Unitario, Costo_Unitario, Venta_Total, Costo_Total, Metodo_Pago, Ganancia_Bruta, mes_texto, Total_Compras, Indice_Constancia

---

## 3. Proceso de ETL y Feature Engineering

### 3.1 Primera limpieza (`integrador.ipynb`)

- Conversión de columnas numéricas y eliminación de filas con valores inválidos
- Normalización de texto con `.str.strip().str.title()`
- Imputación de nulos en Ciudad, Metodo_Pago y Categoria
- Eliminación de duplicados
- Creación de columnas derivadas:
  - `Ganancia_Bruta = Venta_Total - Costo_Total`
  - `mes_texto`: nombre del mes en español
  - `Total_Compras`: frecuencia de compras por cliente
  - `Indice_Constancia`: segmentación en Fiel (VIP), Regular y Ocasional
- Eliminación de outliers sobre Venta_Total (método IQR, 1.5x)
- Redondeo de columnas monetarias a 2 decimales

### 3.2 Segunda limpieza (`hito_3.ipynb`)

- Normalización de nombres de país: unificación de variantes (Arg, ARG, Chl, CHL, Peru, PERU, etc.)
- Corrección de categoría "Nan" literal (242 registros) usando mapeo por subcategoría
- Corrección de "Electronica" → "Electrónica"
- Normalización de métodos de pago (Debito → Débito, Credito → Crédito, Efect → Efectivo, Transf → Transferencia)
- Limpieza de ciudad "Nan" → "Sin Especificar"

---

## 4. Dashboard Interactivo

Se desarrolló una aplicación web con **Streamlit** y **Plotly** que permite explorar los datos de forma dinámica.

**Filtros disponibles:** rango de fechas, país, categoría, método de pago e índice de constancia.

**Indicadores (KPIs):**
- Venta Total
- Ganancia Bruta
- Cantidad de Transacciones
- Ticket Promedio

**Visualizaciones:**
1. Evolución de ventas por mes (línea)
2. Ventas por categoría (barras)
3. Top 10 productos más vendidos (barras horizontales)
4. Ventas por país (barras)
5. Distribución por método de pago (pie)
6. Ventas por tipo de cliente (barras)

---

## 5. Respuestas a las Preguntas de Negocio

### 5.1 ¿Qué categorías de productos dejan mayor margen de ganancia por país?

**Hallazgo:** No se observan diferencias significativas entre países. Las diferencias de margen por categoría son mínimas:

- **Argentina:** margen bajo en Hogar
- **Chile:** Electrónica y Ropa con margen similar y levemente superior
- **Perú:** Ropa presenta un margen ligeramente mayor

**Conclusión:** La rentabilidad por categoría es homogénea entre los tres países. No hay una categoría que se destaque marcadamente en ningún país en particular.

---

### 5.2 ¿El método de pago influye en la cantidad total de productos comprados y el total gastado?

**Hallazgo:** Los boxplots y estadísticas descriptivas muestran que las medianas de cantidad y venta total son prácticamente iguales entre los cuatro métodos de pago (Crédito, Débito, Efectivo, Transferencia). Los rangos intercuartílicos también se superponen casi por completo.

**Conclusión:** El método de pago **no tiene una influencia relevante** ni en la cantidad de productos comprados ni en el total gastado por transacción.

---

### 5.3 ¿Cuál es el método de pago que domina las transacciones de alto valor en cada país y cómo influye esto en la venta total mensual?

**Hallazgo:**  
- Se definió "alto valor" como transacciones superiores al percentil 85 (≈$478).  
- **Débito** es el método más frecuente en las transacciones de alto valor a nivel general, aunque solo representa el 24% de la venta total mensual.  
- Débito se mantiene estable incluso en los meses de mayor volumen (enero a marzo).  

Por país:
- **Argentina:** Transferencia domina en altas transacciones
- **Chile:** Distribución relativamente uniforme entre métodos
- **Perú:** Mayoría en Crédito y Débito

**Conclusión:** Débito es el método preferido en transacciones de alto valor, pero su participación en el total es minoritaria, lo que sugiere oportunidades para incentivar su uso.

---

### 5.4 ¿Hay ciudades en cada país donde la diferencia entre el costo de los productos y el precio de venta sea significativamente menor?

**Hallazgo:** No se identificaron ciudades con rentabilidad significativamente menor al promedio de su país. Todas las ciudades analizadas presentan márgenes unitarios muy cercanos al promedio nacional.

**Conclusión:** La rentabilidad es uniforme a nivel geográfico. No existe concentración de baja rentabilidad en ninguna ciudad específica que requiera intervención localizada.

---

## 6. Diagnóstico General

| Aspecto | Diagnóstico |
|---|---|
| **Rentabilidad** | Homogénea entre países, categorías y ciudades. El negocio opera con márgenes estables y predecibles. |
| **Métodos de pago** | No impactan en el monto gastado. Débito lidera en transacciones altas pero con baja participación relativa. |
| **Clientes** | Segmento Ocasional es mayoritario. El segmento Fiel VIP es el de mayor valor pero con menor cantidad de clientes. |
| **Estacionalidad** | Fuerte concentración de ventas en el primer trimestre del año (enero-marzo). |

---

## 7. Propuestas de Mejora

### Propuesta 1: Programa de fidelización segmentado

**Problema detectado:** El 77% de los clientes pertenecen a los segmentos Ocasional y Regular, mientras que el segmento Fiel VIP (el de mayor valor) concentra apenas el 23%. Esto representa una oportunidad de mejorar la recurrencia y el ticket promedio.

**Propuesta:** Implementar un programa de beneficios escalonados según el `Indice_Constancia`:

- **Fiel VIP (10+ compras):** Descuentos exclusivos, acceso anticipado a promociones y envío gratis.
- **Regular (4-9 compras):** Beneficios intermedios con incentivos para alcanzar la categoría VIP (ej. "Te faltan 2 compras para obtener beneficios VIP").
- **Ocasional (1-3 compras):** Campañas de re-engagement con descuentos en la próxima compra.

**Justificación:** Los datos muestran que el segmento Fiel VIP genera un volumen de ventas desproporcionadamente alto en relación a su cantidad de clientes. Mover aunque sea un 5% de los clientes Ocasionales a la categoría Regular, y de Regulares a Fiel VIP, incrementaría la recurrencia de compras y el ticket promedio a largo plazo.

---

### Propuesta 2: Campañas estacionales para reducir la estacionalidad

**Problema detectado:** Las ventas se concentran fuertemente en el primer trimestre del año (enero-marzo). El resto del año el volumen disminuye, lo que genera ineficiencias en inventario, logística y personal.

**Propuesta:** Diseñar campañas promocionales específicas para los meses de menor actividad:

- **Combos cruzados:** Ofertas que combinen productos de distintas categorías (ej. "Llevá un producto de Hogar + uno de Electrónica con 15% de descuento").
- **Promociones por método de pago:** Descuentos adicionales por usar Débito en meses valle, aprovechando que es el método más estable y con mejor performance en transacciones altas.
- **Eventos temáticos:** "Mes del Hogar", "Semana de la Tecnología", etc., para distribuir la demanda a lo largo del año.

**Justificación:** La estacionalidad marcada implica picos de demanda que presionan la cadena de suministro y periodos de capacidad ociosa. Suavizar la curva de ventas permite optimizar inventarios, reducir costos operativos y mejorar la rentabilidad anual sin necesidad de aumentar el volumen total.

---

## 8. Conclusiones

El análisis de los datos de ventas de la cadena comercial permitió:

1. Validar que la rentabilidad es uniforme en toda la operación, sin focos de baja performance que requieran intervención urgente.
2. Determinar que el método de pago no condiciona el comportamiento de gasto de los clientes.
3. Identificar al Débito como el método de pago dominante en transacciones de alto valor, aunque con baja participación relativa.
4. Caracterizar la base de clientes en tres segmentos claramente diferenciados por su frecuencia de compra.
5. Detectar una fuerte estacionalidad de ventas concentrada en el primer trimestre del año.

Sobre esta base, se proponen dos líneas de acción: un programa de fidelización segmentado para retener y hacer crecer a los clientes de mayor valor, y campañas estacionales para distribuir la demanda de manera más uniforme a lo largo del año.
