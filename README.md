# Metanstain – Toolkit DFIR básico para usuarios no técnicos  
**Metadatos + Frankenstein = Metanstain**  

Metanstain es un lanzador DFIR (Digital Forensics & Incident Response) diseñado para que **usuarios sin experiencia técnica** puedan analizar archivos, verificar su autenticidad y proteger su privacidad digital utilizando herramientas forenses reales, pero sin la complejidad habitual de la línea de comandos.

Es una herramienta educativa, defensiva y orientada a la alfabetización digital: permite revisar imágenes, documentos y archivos sospechosos para detectar estafas, manipulación o riesgos ocultos.

---

## ¿Por qué “Metanstain”?

El nombre surge de combinar:

- **Metadatos** → porque gran parte del análisis consiste en leer o limpiar información oculta en imágenes, documentos y archivos.  
- **Frankenstein** → porque este script une (“cose”) varias herramientas forenses open source en una sola interfaz simple y coherente.

El resultado es un pequeño “monstruo útil” que junta lo mejor de varias utilidades y lo hace accesible incluso para personas que nunca usaron la consola.

---

## Objetivo del proyecto

Metanstain está orientado a:

### 1. Usuarios novatos o no acostumbrados a la terminal  
Personas que reciben archivos por WhatsApp, email o redes sociales y necesitan saber:

- ¿Es realmente una imagen o PDF?  
- ¿Fue editado o manipulado?  
- ¿Hay metadatos que revelan ubicación o detalles privados?  
- ¿Es un archivo renombrado o potencialmente peligroso?  
- ¿Me están intentando estafar?  

### 2. Usuarios preocupados por su privacidad  
Con Metanstain podés:

- Revisar metadatos antes de compartir fotos.  
- Eliminar datos sensibles como ubicación GPS o información del dispositivo.  
- Verificar integridad mediante herramientas de hashing.  
- Analizar PDFs sospechosos sin ejecutarlos.

### 3. Emprendedores o pequeñas empresas  
Sirve como un paso previo para evitar abrir archivos potencialmente maliciosos que llegan por correo o mensajería.

---

## Herramientas integradas

Metanstain detecta si estás en Debian/Kali/Ubuntu y, si falta alguna herramienta, la instala automáticamente.  
El catálogo actual incluye:

| ID | Herramienta       | Paquete APT                 | Función principal |
|----|-------------------|-----------------------------|------------------|
| 1  | `exiftool`        | `libimage-exiftool-perl`    | Leer/eliminar metadatos EXIF, IPTC, XMP. |
| 2  | `file`            | `file`                      | Detectar tipo real de archivo (evita estafas por renombramiento). |
| 3  | `strings`         | `binutils`                  | Extraer texto oculto en binarios o documentos. |
| 4  | `xxd`             | `xxd`                       | Generar hexdumps del contenido real. |
| 5  | `binwalk`         | `binwalk`                   | Encontrar datos embebidos, compresión o secciones internas. |
| 6  | `bulk_extractor`  | `bulk-extractor`            | Extraer artefactos forenses como URLs y correos. |
| 7  | `pdfinfo`         | `poppler-utils`             | Revisar PDFs sin abrirlos. |
| 8  | `identify`        | `imagemagick`               | Mostrar información técnica de imágenes. |

---
