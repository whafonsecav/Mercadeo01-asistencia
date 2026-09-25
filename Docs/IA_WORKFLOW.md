# Protocolo de Actualización de Asistencia para Agentes de IA

¡Hola, Agente de IA! (Antigravity, Cursor, Copilot, etc.). Si estás leyendo este documento, el usuario te ha encargado la tarea de actualizar el Dashboard de Asistencia del curso "Mercadeo 1" a partir de una o varias fotos nuevas de listas de asistencia físicas.

El Dashboard está construido con Vanilla JS puro integrado en un archivo `index.html` estático, y se despliega públicamente usando GitHub Pages. 

Por favor, sigue **rigurosamente** estos pasos para mantener la integridad del sistema.

---

## 1. Recepción, Detección y Renombrado de la Imagen
1. **Recepción**: El usuario te entregará una imagen adjunta o te indicará en qué directorio local se encuentra.
2. **Análisis de Fecha**: Inspecciona visualmente la imagen escaneada para encontrar la fecha escrita a mano (usualmente en la esquina superior derecha o en la cabecera).
3. **Renombrado**: Mueve/Copia la imagen y guárdala en el repositorio local dentro de la carpeta `Assents/Listas/`.
4. **Regla de Nomenclatura**: Debes seguir el formato secuencial exacto que ya existe:
   `[Número Secuencial]. [Mes en Inglés 3 letras] [Día] [Año].jpg`
   *Ejemplo*: Si la última lista fue `07. Sep 24 2026.jpg`, la nueva lista se llamará `08. Oct 01 2026.jpg`.

---

## 2. Lectura y Extracción de Datos (Computer Vision)
Analiza la lista fotográfica fila por fila, y cruza los nombres con la base de datos de estudiantes. Debes obedecer estas reglas históricas acordadas con el profesor:

- **Check (Chulito) o Firma Normal**: El estudiante asistió (`true`).
- **Línea Diagonal (Slash `/` o `\` cruzando la casilla)**: El estudiante NO asistió (`false`).
- **Espacio en blanco total**: El estudiante NO asistió (`false`).
- ⚠️ **Excepción (Cédula faltante)**: Si el estudiante firmó o tiene check, pero **dejó la casilla de la cédula en blanco**, el estudiante SÍ asistió (`true`), PERO debes levantar una notificación en el JSON (Explicado en el Paso 3.b) para dibujar el Check de color amarillo en el frontend.

---

## 3. Actualización de Base de Datos Estática (`index.html`)
El motor de base de datos reside en memoria directamente dentro del archivo `index.html`. Ábrelo y ubica los arreglos `sessions` y `students`.

### A) Actualizar `sessions`
Añade un nuevo objeto al final del arreglo correspondiente al nuevo día. El `id` debe continuar la secuencia.
```javascript
// Ejemplo de adición:
{ id: 8, date: "2026-10-01", label: "01 Oct", image: "Assents/Listas/08. Oct 01 2026.jpg", type: "class" }
```
*(Nota: Si el usuario te indica que hubo un día sin lista física debido a una tarea u otro evento, asígnale `type: "assignment"` y omite el campo `image`, como se hizo con el 27 de agosto).*

### B) Actualizar `students`
Itera sobre todos los objetos del arreglo `students`.
1. **Asistencia Pura**: Agrega un valor booleano (`true` o `false`) al final de su arreglo `attendance` correspondiente a la clase recién creada.
2. **Alertas de Cédula**: Si en el paso 2 detectaste que alguien olvidó poner la cédula, ubica la llave `notes` de ese estudiante y asígnale `true` utilizando el **ID numérico de la sesión** como llave.
```javascript
// Ejemplo: La estudiante olvidó la cédula en la sesión ID 8.
{"name": "VALENTINA VELANDIA RODRÍGUEZ", "attendance": [true, true, ..., true], "notes": {"2": true, "4": true, "8": true}}
```

---

## 4. Pruebas y Resiliencia del Frontend
- **No alteres la lógica CSS ni HTML**: El código de las leyendas dinámicas, el carrusel modal de imágenes y los colores del semáforo están diseñados para ajustarse en tiempo real de acuerdo a la matriz matemática de `students`. Si agregas un `true/false`, el motor calculará automáticamente la nueva escala de porcentajes sin intervención tuya.

---

## 5. Despliegue en Servidor (GitHub Pages)
Dado que el proyecto utiliza GitHub Pages, cualquier actualización guardada localmente requiere un empuje al repositorio principal. Tienes permitido ejecutar scripts en la terminal para hacerlo.

Utiliza siempre los siguientes comandos sobre el `cwd` raíz:
```powershell
git add .
git commit -m "feat(datos): Ingreso de nueva asistencia para [FECHA_DE_LA_CLASE]"
git push origin main
```
*Si tienes problemas de autenticación o el repositorio remoto de GitHub falla al hacer push, advierte de inmediato al usuario para solicitarle el token de acceso personal (PAC).*

---
**¡Fin del flujo!** Con estos 5 pasos, el dashboard web de Asistencia de Mercadeo 01 será siempre confiable, rápido y seguro.
