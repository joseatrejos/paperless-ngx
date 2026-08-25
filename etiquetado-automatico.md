# Etiquetado automático de documentos en Paperless-ngx

## Resumen

La funcionalidad de etiquetado automático que se solicitó **ya existe de forma nativa** en Paperless-ngx a través del sistema de **Workflows**.

---

## ¿Qué son los Workflows?

Un Workflow es una regla que se ejecuta automáticamente cuando un documento entra al sistema (por consumo, API o correo). Cada workflow tiene:

- **Triggers**: condiciones que determinan a qué documentos aplica (por nombre de archivo, ruta, contenido, etc.)
- **Actions**: lo que hace cuando las condiciones se cumplen (asignar etiquetas, tipo de documento, corresponsal, mover a carpeta, etc.)

---

## ¿Cómo cubre la necesidad pedida?

La solicitud era: *"N pares de (Etiqueta, Criterio de asignación) que se evalúen automáticamente sobre cada documento nuevo"*.

Con los Workflows nativos se puede hacer exactamente eso:

| Lo que se pidió | Equivalente en Workflows |
|---|---|
| Criterio de asignación (texto) | Campo `match` del trigger, con algoritmos fuzzy, regex, literales, etc. |
| Etiqueta a asignar | Action de tipo **Assignment** → campo "Assign tags" |
| Se activa al subir un documento | Trigger de tipo **Consumption** (consume folder, API upload, mail fetch) |
| N reglas independientes | N workflows, uno por cada par etiqueta-criterio |

---

## Ejemplo concreto

**Objetivo**: Asignar la etiqueta `Factura` a documentos que contengan la palabra "factura".

**Configuración del Workflow**:

- **Trigger**:
  - Tipo: `Document added`
  - Fuentes: `Consume folder`, `API upload`, `Mail fetch`
  - Algoritmo de matching: `Any word` (o `Fuzzy`, `Regex`, etc.)
  - Match: `factura`
- **Action**:
  - Tipo: `Assignment`
  - Assign tags: `Factura`

Paperless lo aplica automáticamente a cada documento nuevo que cumpla la condición, sin intervención manual.

---

## ¿Cuándo sí tendría sentido agregar IA?

La única diferencia real que aportaría una integración con LLM es cuando el criterio **no se puede expresar como un patrón** (keyword, regex, fuzzy). Por ejemplo:

> *"Asigna la etiqueta `Contrato` si el documento es un acuerdo legal entre dos partes, independientemente de las palabras exactas que use."*

Ese tipo de criterio semántico no puede capturarse con matching tradicional. Para los demás casos, los Workflows cubren la necesidad sin costo adicional de infraestructura de IA.

---

## Recomendación

Usar los Workflows nativos como solución inmediata. Si en el futuro se identifican casos donde el matching semántico es necesario, se puede extender el sistema con un nuevo tipo de acción de tipo "AI Labeling" (ya explorado técnicamente).
