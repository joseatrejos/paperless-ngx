# Paperless-ngx — Guía de Capacitación


## Módulo 1 — ¿Qué es este sistema y para qué sirve?

- El sistema es un archivo digital de documentos. Subes documentos (PDF, escaneos, archivos Word, correos electrónicos) y los guarda, lee el texto y hace todo buscable.
- En lugar de buscar entre carpetas o archivos físicos, escribes una palabra y encuentras al instante todos los documentos que la contienen.
- Cada documento puede etiquetarse con tags, un corresponsal (de quién es o a quién va), un tipo de documento (factura, contrato, etc.) y campos personalizados.
- El sistema puede aprender tus hábitos de etiquetado y comenzar a etiquetar documentos de forma automática.
- Los documentos nunca salen de tu servidor — todo permanece privado.

**Conceptos clave antes de empezar:**
- **Tags** — etiquetas que adjuntas a los documentos (ej. "urgente", "impuestos-2025", "pagado")
- **Corresponsal** — la persona o empresa de quien proviene o a quien va dirigido el documento (ej. "IMSS", "CFE", "Juan Pérez")
- **Tipo de documento** — la categoría del documento (ej. Factura, Contrato, Estado de cuenta)
- **Bandeja de entrada** — los documentos recién subidos que aún no han sido revisados aparecen aquí

---

## Módulo 2 — Subir tu primer documento

**Objetivo:** Ingresar un documento al sistema.

**Opción A — Arrastrar y soltar desde el navegador:**
1. Abre la aplicación en tu navegador.
2. Arrastra cualquier PDF, imagen, Word o Excel directamente sobre cualquier página.
3. Aparece un indicador de progreso verde. Espera a que termine.
4. El documento aparecerá en tu lista en unos segundos.

**Opción B — Usar el botón de subida:**
1. Haz clic en el botón de subida (esquina superior derecha de cualquier página).
2. Selecciona un archivo desde tu computadora.
3. Espera a que el procesamiento termine.

**Opción C — Reenviar correos electrónicos:**
- Si el correo está configurado, reenviar un email con adjunto a la dirección configurada importará el adjunto automáticamente.

**¿Qué pasa después de subir?**
- El sistema lee (OCR) el texto del documento para que puedas buscarlo por contenido.
- Crea una copia con texto buscable.
- Intenta sugerir o asignar automáticamente tags, corresponsal y tipo de documento según lo que ha aprendido.

---

## Módulo 3 — Encontrar documentos

**Objetivo:** Localizar un documento específico rápidamente.

**Buscar por cualquier palabra del documento:**
1. Haz clic en la barra de búsqueda en la parte superior.
2. Escribe cualquier palabra que aparezca en el documento (ej. "IMSS", "estado de cuenta", "renovación de contrato").
3. Los resultados se actualizan mientras escribes.

**Filtrar la lista para acotar resultados:**
- Haz clic en **Filtros** en la lista de documentos.
- Filtra por: tag, corresponsal, tipo de documento, rango de fechas o campo personalizado.
- Combina múltiples filtros al mismo tiempo.

**Usar vistas guardadas para acceder rápido a búsquedas frecuentes:**
- Una vista guardada es un filtro preconfigurado que aparece en tu barra lateral o panel.
- Ejemplo: una vista llamada "Bandeja de entrada" muestra todos los documentos sin tags. Otra llamada "Facturas 2025" muestra todas las facturas de ese año.
- Para crear una: configura tus filtros y luego haz clic en **Guardar vista**.

**Encontrar documentos similares a uno que ya tienes:**
- Abre un documento y desplázate a la sección **Documentos similares**.
- El sistema muestra otros documentos con contenido relacionado.

---

## Módulo 4 — Organizar un documento (manualmente)

**Objetivo:** Agregar etiquetas a un documento para encontrarlo fácilmente después.

1. Haz clic en cualquier documento para abrirlo.
2. En el panel derecho verás los campos: **Título**, **Corresponsal**, **Tipo de documento**, **Fecha**, **Tags** y cualquier campo personalizado.
3. Edita cada campo:
   - **Título** — Dale un nombre claro (ej. "Factura CFE Marzo 2025")
   - **Corresponsal** — ¿Quién lo envió o lo recibió? (ej. "CFE")
   - **Tipo de documento** — ¿Qué tipo de documento es? (ej. "Factura")
   - **Fecha** — La fecha del documento, no la de subida
   - **Tags** — Agrega etiquetas relevantes (ej. "electricidad", "pagado", "2025")
4. Los cambios se guardan automáticamente.

**Consejos:**
- Usa nombres consistentes para los corresponsales — "CFE" y "C.F.E." crearán dos corresponsales diferentes.
- Los tags pueden anidarse: "gastos > servicios > electricidad" para mejor organización.
- El sistema aprenderá tus patrones de etiquetado y los sugerirá automáticamente con el tiempo.

---

## Módulo 5 — Crear tags, corresponsales y tipos de documento

**Objetivo:** Configurar las etiquetas que tu organización usará de forma consistente.

**Crear un tag:**
1. Ve a **Tags**.
2. Haz clic en **Agregar tag**.
3. Dale un nombre y, opcionalmente, un color.
4. Puedes anidarlo bajo un tag padre (ej. padre: "Gastos", hijo: "Servicios").

**Crear un corresponsal:**
1. Ve a **Gestionar → Corresponsales**.
2. Haz clic en **Agregar corresponsal**.
3. Ingresa el nombre exactamente como quieres que aparezca en los documentos.
4. Opcionalmente agrega reglas de coincidencia para que documentos de ese remitente se asignen automáticamente.

**Crear un tipo de documento:**
1. Ve a **Gestionar → Tipos de documento**.
2. Haz clic en **Agregar tipo de documento**.
3. Ingresa el nombre (ej. "Factura", "Contrato", "Recibo de nómina").
4. Opcionalmente agrega reglas de coincidencia.

**Agregar una regla de coincidencia (asignación automática):**
- Al crear o editar un tag/corresponsal/tipo, busca la sección **Coincidencia**.
- Configura el **Algoritmo** (ej. "Cualquier palabra") y el **Patrón** (palabras a buscar en el texto del documento).
- Ejemplo: Corresponsal "CFE" con patrón "Comisión Federal de Electricidad" — todo documento que contenga esa frase se asignará automáticamente a CFE.

---

## Módulo 6 — Configurar organización automática con flujos de trabajo

**Objetivo:** Hacer que el sistema etiquete y organice documentos automáticamente cuando llegan, sin hacerlo manualmente.

**¿Qué es un flujo de trabajo?**
Un flujo de trabajo es una regla: "Cuando X pase, hacer Y." Por ejemplo: "Cuando llegue un documento que contenga la palabra 'nómina', agregar el tag 'Nómina' y establecer el tipo como 'Recibo de nómina'."

**Crear un flujo de trabajo básico de etiquetado automático:**
1. Ve a **Gestionar → Flujos de trabajo**.
2. Haz clic en **Agregar flujo de trabajo**.
3. Dale un nombre descriptivo (ej. "Auto-etiquetar documentos de nómina").
4. Configura el **Disparador**:
   - Elige **Documento agregado** (se activa cuando un nuevo documento está completamente procesado).
   - En **Filtro**, establece condiciones — por ejemplo: **Contenido contiene** → escribe "nómina".
5. Configura la **Acción**:
   - Elige **Asignación**.
   - Completa qué asignar: tags, corresponsal, tipo de documento, ruta de almacenamiento o título.
6. Guarda el flujo de trabajo.

**Recetas comunes de flujos de trabajo:**

| Quiero… | Disparador | Filtro | Acción |
|---|---|---|---|
| Auto-etiquetar recibos de luz | Documento agregado | Contenido contiene "CFE" o "Comisión Federal" | Agregar tag "Servicios", asignar corresponsal "CFE", tipo "Factura" |
| Auto-etiquetar documentos de nómina | Documento agregado | Contenido contiene "nómina" o "IMSS" | Agregar tag "Nómina", tipo "Recibo de nómina" |
| Auto-etiquetar contratos | Documento agregado | Contenido contiene "contrato" | Agregar tag "Contratos", tipo "Contrato" |
| Notificar por correo cuando llega un documento | Documento agregado | Cualquier filtro | Acción: Correo — enviar a tu dirección |
| Mover documentos viejos a la papelera automáticamente | Programado | Documentos con más de X días y un tag específico | Acción: Mover a la papelera |

**Consejos:**
- Los flujos se procesan en orden. Número de orden menor = mayor prioridad.
- Puedes tener múltiples acciones en un solo flujo de trabajo.
- Prueba con algunos documentos antes de activar para todos.

---

## Módulo 7 — Trabajar con múltiples documentos a la vez

**Objetivo:** Aplicar cambios a muchos documentos en una sola operación.

1. En la lista de documentos, marca la casilla junto a cada documento que quieras seleccionar (o usa **Seleccionar todo**).
2. Aparece una barra de acciones masivas en la parte superior.
3. Elige qué hacer:
   - **Asignar tags / corresponsal / tipo de documento** — se aplica a todos los documentos seleccionados
   - **Descargar** — descarga todos los seleccionados como un archivo ZIP
   - **Eliminar** — mueve todos los seleccionados a la papelera
   - **Combinar** — une los documentos seleccionados en un nuevo documento único
   - **Enviar a Documenso** — envía todos los seleccionados para firma digital

---

## Módulo 8 — Compartir un documento

**Objetivo:** Dar acceso a un documento a otra persona.

**Compartir un enlace público (sin necesidad de iniciar sesión):**
1. Abre el documento.
2. Haz clic en el botón **Compartir**.
3. Haz clic en **Crear enlace para compartir**.
4. Configura una fecha de expiración opcional.
5. Copia el enlace y envíalo a quien lo necesite.

**Compartir con otro usuario del sistema:**
1. Abre el documento.
2. Ve a la pestaña **Permisos**.
3. Agrega al usuario o grupo y elige si pueden ver o también editar.

**Enviar un documento por correo electrónico:**
1. Abre el documento.
2. Haz clic en el botón **Enviar** → **Correo electrónico**.
3. Ingresa la dirección del destinatario, asunto y mensaje.
4. El documento se adjuntará y enviará.

---

## Módulo 9 — Enviar un documento para firma digital (Documenso)

**Objetivo:** Enviar un documento a Documenso para que sea firmado digitalmente.

**Antes de empezar:** Documenso debe estar configurado por tu administrador (URL y token en la configuración, y el Team Slug en la página de ajustes de la app). Si no está configurado, verás un mensaje de error con un enlace a la página de configuración.

**Desde un solo documento:**
1. Abre el documento.
2. Haz clic en el botón **Enviar** → **Firmar con Documenso**.
3. Serás redirigido a la interfaz de Documenso para configurar los campos de firma y enviar a los firmantes.

**Desde múltiples documentos a la vez:**
1. Selecciona varios documentos usando las casillas en la lista.
2. En la barra de acciones masivas, haz clic en **Enviar a Documenso**.

---

## Módulo 10 — Configurar importación de correo (IMAP)

**Objetivo:** Hacer que el sistema importe automáticamente documentos desde una bandeja de correo dedicada.

1. Ve a **Ajustes → Cuentas de correo**.
2. Para conectar por **IMAP estándar**: haz clic en **Agregar cuenta de correo**, ingresa los datos de tu servidor IMAP, guarda y verifica la conexión.
3. Para conectar por **OAuth de Gmail u Outlook** (si tu administrador lo configuró): haz clic en el botón **Conectar cuenta de Gmail** o **Conectar cuenta de Outlook** directamente en la página de Ajustes de correo. Esto te redirigirá a Google o Microsoft para autorizar el acceso — no se necesitan credenciales IMAP.

   > **Nota:** Los botones de OAuth solo aparecen si tu administrador ha configurado las credenciales de la app OAuth en el servidor. Si no los ves, usa la opción IMAP estándar.
4. Ve a **Ajustes → Reglas de correo**.
5. Haz clic en **Agregar regla de correo**.
6. Configura:
   - **Cuenta** — la cuenta que acabas de agregar
   - **Carpeta** — qué carpeta IMAP monitorear (ej. "Bandeja de entrada" o "Paperless")
   - **Filtro** — opcionalmente filtra por asunto, remitente o texto del cuerpo
   - **Acción** — qué consumir: solo el adjunto, o el correo completo como PDF
   - **Post-consumo** — qué hacer con el correo después: marcar como leído, eliminar, mover a carpeta
7. Guarda. El sistema revisará nuevos correos automáticamente cada 10 minutos.

**Consejo práctico:** Crea una dirección de correo dedicada (ej. `documentos@tuempresa.com`) y reenvía facturas, recibos y contratos ahí. Configura una regla que monitoree esa carpeta. Cada correo reenviado se importa automáticamente.

---

## Módulo 11 — Usar el panel de control

**Objetivo:** Configurar una pantalla de inicio personalizada con acceso rápido a lo más importante.

- El panel muestra **Vistas guardadas** como widgets — cada widget es una lista de documentos filtrada.
- Ejemplos de widgets: "Bandeja de entrada" (documentos sin revisar), "Facturas del mes", "Contratos por vencer".

**Agregar un widget al panel:**
1. Ve a **Gestionar → Vistas guardadas**.
2. Crea o edita una vista guardada.
3. Activa el interruptor **Mostrar en el panel**.
4. Regresa al panel — el widget aparece.

**Reorganizar el panel:**
- Arrastra y suelta los widgets para cambiar su orden.

---

## Módulo 12 — Revisar y limpiar la bandeja de entrada

**Objetivo:** Procesar los documentos recién llegados y asegurarte de que estén correctamente etiquetados.

La "Bandeja de entrada" es una vista guardada que muestra todos los documentos que aún no tienen tags (o que tienen el tag "bandeja de entrada", según la configuración).

**Flujo de trabajo diario:**
1. Abre la vista **Bandeja de entrada** desde la barra lateral o el panel.
2. Haz clic en cada documento.
3. Revisa los metadatos sugeridos automáticamente (mostrados en el panel derecho con un indicador de sugerencia).
4. Acepta o corrige: título, corresponsal, tipo de documento, fecha, tags.
5. Una vez etiquetado, el documento desaparece automáticamente de la bandeja.

**Si ves sugerencias de la IA/clasificador:**
- Aparece un pequeño ícono junto a los campos que tienen sugerencias.
- Haz clic para aceptar la sugerencia o escribe un valor diferente.

---

## Módulo 13 — Gestionar usuarios y accesos

**Objetivo:** Controlar quién puede ver y editar qué documentos.

**Agregar un nuevo usuario:**
1. Ve a **Ajustes → Usuarios y grupos**.
2. Haz clic en **Agregar usuario**.
3. Configura su nombre de usuario, correo y contraseña.
4. Asígnalo a un grupo si usas grupos para control de acceso por roles.

**Crear un grupo:**
1. Ve a **Ajustes → Usuarios y grupos → Grupos**.
2. Crea un grupo (ej. "Contabilidad", "RRHH").
3. Asigna permisos: qué tipos de objetos pueden crear, ver, editar o eliminar.

**Hacer un documento privado o compartido:**
- Por defecto, los nuevos documentos solo son visibles para quien los subió (o según la configuración de permisos predeterminada).
- Para compartir con un equipo, abre el documento → pestaña **Permisos** → agrega el grupo con acceso de Vista o Edición.

**Configurar permisos predeterminados para todo lo que subes:**
1. Ve a tu **Perfil de usuario** (haz clic en tu avatar, esquina superior derecha).
2. En **Permisos predeterminados**, configura qué usuarios/grupos obtienen acceso automáticamente a los documentos que creas.

---

## Módulo 14 — Papelera y recuperación

**Objetivo:** Eliminar documentos de forma segura y recuperarlos si es necesario.

**Eliminar un documento:**
- Abre el documento → haz clic en el botón **Eliminar**.
- El documento se mueve a la **Papelera** — NO se elimina permanentemente todavía.

**Recuperar un documento eliminado:**
1. Ve a **Papelera** en la barra lateral izquierda.
2. Encuentra el documento y haz clic en **Restaurar**.

**Eliminar permanentemente:**
- En la Papelera, haz clic en **Eliminar permanentemente** en un documento, o en **Vaciar papelera** para eliminar todo su contenido de forma definitiva.
- Después de la eliminación permanente, el documento no puede recuperarse.

---

## Módulo 15 — Búsqueda avanzada

**Objetivo:** Encontrar exactamente lo que necesitas usando técnicas de búsqueda avanzada.

| Lo que quieres | Cómo hacerlo |
|---|---|
| Documentos que contengan una frase específica | Escribe la frase exacta en la barra de búsqueda |
| Documentos de una persona específica | Filtra por **Corresponsal** |
| Todas las facturas del año pasado | Filtra por **Tipo = Factura** + **Rango de fecha = 2024** |
| Documentos con un valor específico de campo personalizado | Usa el panel de **Filtros** → **Campos personalizados** |
| Documentos similares a uno que estás viendo | Abre el documento → desplázate a **Documentos similares** |
| Documentos que aún no has revisado | Abre la vista guardada **Bandeja de entrada** |

**Consejos:**
- La búsqueda lee el texto completo de cada documento, incluyendo texto escrito a mano que fue escaneado.
- Puedes combinar texto de búsqueda con filtros para resultados precisos.
- Guarda cualquier combinación de filtros como Vista guardada para acceso con un clic.

---

## Módulo 16 — Campos personalizados

**Objetivo:** Agregar tus propios campos de datos a los documentos, más allá de los predeterminados.

Los campos personalizados te permiten almacenar información específica de tu organización. Ejemplos:
- **Número de factura** (texto)
- **Monto pagado** (monetario)
- **Fecha de vencimiento del contrato** (fecha)
- **¿Firmado?** (casilla de verificación/booleano)
- **Contrato relacionado** (enlace a otro documento)

**Crear un campo personalizado:**
1. Ve a **Gestionar → Campos personalizados**.
2. Haz clic en **Agregar campo personalizado**.
3. Nómbralo y elige su tipo (texto, número, fecha, casilla, desplegable, enlace a documento, etc.).

**Usar un campo personalizado:**
- Abre cualquier documento.
- En el panel derecho, haz clic en **Agregar campo** y elige tu campo personalizado.
- Ingresa el valor.

**Filtrar por campo personalizado:**
- En la lista de documentos, abre **Filtros → Campos personalizados** y busca por valor del campo.

---

## Módulo 17 — Preguntas frecuentes

**P: Subí un documento pero el texto está incorrecto o falta — ¿por qué?**
El documento puede ser una imagen escaneada sin texto embebido. El sistema intenta aplicar OCR automáticamente. Si la calidad del escaneo es mala (borrosa, oscura, inclinada), la extracción de texto puede ser incompleta. Intenta re-escanear a mayor resolución (300 DPI o más).

**P: Los tags/corresponsal automáticos están incorrectos — ¿cómo lo corrijo?**
Corrige los valores manualmente en el documento. El sistema aprende de tus correcciones con el tiempo. Cuanto más consistentemente etiquetes los documentos, mejores serán las sugerencias automáticas.

**P: Eliminé un documento por accidente — ¿puedo recuperarlo?**
Sí. Ve a **Papelera** en la barra lateral y haz clic en **Restaurar**. Los documentos permanecen en la papelera hasta que los elimines permanentemente o se ejecute la purga automática.

**P: ¿Pueden dos personas usar el sistema al mismo tiempo?**
Sí. Múltiples usuarios pueden estar conectados y trabajando simultáneamente.

**P: ¿Puedo ver quién hizo cambios en un documento?**
Sí, si tu administrador habilitó el registro de auditoría. Abre el documento y busca la pestaña **Historial de auditoría**.

**P: ¿Cómo cambio mi contraseña?**
Haz clic en tu avatar (esquina superior derecha) → **Perfil** → **Cambiar contraseña**.

**P: ¿Cómo activo la autenticación de dos factores (2FA)?**
Haz clic en tu avatar → **Perfil** → desplázate a la sección **Autenticación de dos factores** → sigue los pasos de configuración del código QR.

**P: ¿Puedo acceder al sistema desde mi teléfono?**
Sí. El sistema funciona en cualquier navegador móvil moderno. No hay una app móvil dedicada, pero la interfaz web se adapta a pantallas más pequeñas.
