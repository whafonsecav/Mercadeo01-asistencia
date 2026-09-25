# 📊 Dashboard de Asistencia - Mercadeo 1

[![Ver en vivo](https://img.shields.io/badge/Ver_Dashboard-En_Vivo-success?style=for-the-badge&logo=github)](https://whafonsecav.github.io/Mercadeo01-asistencia/)

Este proyecto es un tablero de métricas y control de asistencia interactivo, diseñado específicamente para la asignatura **Mercadeo 1 (Grupo 201)** del **Politécnico Grancolombiano** (Sede Bogotá, Modalidad Nocturna).

## 🚀 Enlace del Proyecto
Puedes ver el proyecto funcional y en vivo desplegado en GitHub Pages haciendo clic aquí:  
👉 **[Visitar Tablero de Asistencia en Vivo](https://whafonsecav.github.io/Mercadeo01-asistencia/)**

---

## 🎯 Características Principales

- **Visor de Listas Físicas (Carrusel Fotográfico)**: Al hacer clic en el encabezado de cualquier fecha, se abre un visor modal oscuro tipo galería que contiene la lista de asistencia original escaneada.
  - **Soporte táctil y ratón**: Permite hacer arrastre libre (Drag & Pan) y zoom (rueda del ratón o doble toque).
  - **Carrusel integrado**: Permite navegar hacia el día siguiente o anterior de manera fluida (ignora inteligentemente los días que fueron de "Trabajo Asignado" sin registro de lista física).
- **Gamificación Dinámica**: Los niveles de asistencia de cada estudiante se agrupan en una leyenda calculada automáticamente según los puntajes de la clase, presentados mediante "Caritas" con paleta de colores estilo semáforo (Verde brillante = 100%, Rojo = 0%).
- **Diseño Ultra Responsivo**: Interfaz corporativa limpia, elegante y altamente optimizada para celulares. Contiene bordes fijos y áreas separadas para un desplazamiento lateral (scroll) ergonómico.
- **Excepciones Contempladas**: Diferenciación de eventos atípicos mediante convenciones claras, como alumnos asistentes que olvidaron firmar cédula (Check amarillo) y días de no-clase presencial.

## 🛠️ Tecnologías y Fuentes

- **HTML5 & CSS3**: Interfaz estructurada sin carga de librerías de componentes complejas.
- **Vanilla JavaScript (ES6)**: Encargado de iterar la base de datos de los estudiantes en un array nativo, realizar cálculos de promedio e inyectar el DOM. Incluye lógica matemática para el centrado nativo (CSS Transforms) de las imágenes.
- **Tailwind CSS (v3 vía CDN)**: Estilos y responsividad construidos velozmente respetando el pantone oficial de la universidad (`#00205B`, `#00A5D9`, `#82B135`).
- **FontAwesome (v6)**: Iconografía general de la aplicación.

## 📂 Estructura del Proyecto

```text
📦 Mercadeo01-asistencia
 ┣ 📂 Assents
 ┃ ┣ 📂 Listas         # (Fotografías de las listas físicas por fecha)
 ┃ ┗ 📂 Logo           # (Logotipos institucionales del Politécnico)
 ┣ 📜 index.html       # Archivo principal del Dashboard Web
 ┗ 📜 README.md        # Documentación técnica
```

## 📌 Contexto de Datos
Toda la información registrada es extraída y contrastada directamente de las fotografías originales subidas al sistema, firmadas en clase y avaladas por la profesora Jennifer Florez.
