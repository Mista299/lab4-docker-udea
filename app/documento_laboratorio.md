# Laboratorio 4 — Contenedores y Despliegue con Docker

**Universidad de Antioquia — Cloud Computing — 2026-II**

## Descripción técnica

El laboratorio consistió en contenerizar una aplicación web sencilla
desarrollada en **Python 3.12 con Flask**, empaquetarla como imagen Docker,
ejecutarla localmente y publicarla en **Docker Hub** para validar su
portabilidad.

La aplicación expone tres endpoints HTTP en el puerto `3000`:

- `GET /`        — devuelve información del servicio y los endpoints
  disponibles en formato JSON.
- `GET /sumar?a=<n>&b=<n>` — recibe dos números como parámetros de consulta
  y retorna su suma en JSON (`{"operacion":"suma","a":..,"b":..,"resultado":..}`).
- `GET /health`  — endpoint de healthcheck que responde `{"status":"ok"}`.

El proceso de despliegue siguió los pasos definidos en la guía del
laboratorio:

1. **Creación del proyecto**: archivo `app.py` con la lógica de Flask y
   `requirements.txt` con la dependencia `flask==3.0.3`.
2. **Creación del Dockerfile** usando la imagen base oficial
   `python:3.12-slim` (variante ligera de Debian). El Dockerfile define:
   - `WORKDIR /app` como directorio de trabajo;
   - copia e instalación de dependencias antes que el código, para
     aprovechar la caché de capas de Docker;
   - `EXPOSE 3000` para documentar el puerto;
   - `CMD ["python","app.py"]` como proceso principal.
3. **Construcción de la imagen**: `docker build -t miapp-docker:v1 .`
4. **Ejecución del contenedor**: `docker run -d -p 3000:3000 miapp-docker:v1`,
   mapeando el puerto `3000` del host al puerto `3000` del contenedor.
5. **Verificación**: pruebas con `curl` y el navegador
   (`http://localhost:3000/sumar?a=10&b=25` → `resultado: 35`).
6. **Publicación**: `docker tag` + `docker login` + `docker push USUARIO/miapp-docker:v1`.

## ¿Cómo mejora Docker la arquitectura de despliegue?

Docker introduce un nivel de abstracción sobre el sistema operativo
mediante **contenedores**, que son procesos aislados que comparten el
kernel del host pero cuentan con su propio sistema de archivos,
redes y variables de entorno. Esta característica impacta la arquitectura
de despliegue en cuatro dimensiones clave:

1. **Portabilidad**: una imagen Docker es ejecutable en cualquier host
   que disponga del daemon de Docker (Linux, macOS, Windows, servidores
   on-premise, instancias EC2, máquinas de GCP, clústeres Kubernetes).
   Se elimina el clásico problema de *"en mi máquina sí funciona"*: el
   binario, las dependencias del sistema, la versión del lenguaje y las
   librerías viajan dentro de la imagen.

2. **Aislamiento**: cada contenedor posee su propio filesystem, espacio
   de procesos y stack de red, de modo que múltiples aplicaciones o
   versiones de la misma aplicación pueden coexistir en un mismo host
   sin colisionar por puertos, dependencias o variables de entorno. Esto
   reduce la superficie de error y facilita pruebas limpias.

3. **Escalabilidad**: gracias al bajo overhead de los contenedores
   (segundos, no minutos) y a su inmutabilidad, las imágenes son la
   unidad natural de escalado. Orquestadores como **Kubernetes** o
   **Docker Swarm** replican contenedores horizontalmente ante picos de
   carga y los retiran cuando la demanda baja, sin intervención humana.

4. **Reproducibilidad y versionado**: el `Dockerfile` es código fuente
   declarativo, versionable en Git. Cada cambio produce una nueva
   *tag* de imagen (`v1`, `v2`, …), lo que permite rollback inmediato,
   auditoría y pipelines de **CI/CD** consistentes (build → test →
   push → deploy) sin intervención manual sobre los servidores.

En conjunto, Docker desplaza la frontera del despliegue desde
*"configurar servidores"* hacia *"definir imágenes inmutables y
orquestarlas"*, alineando desarrollo y operaciones bajo un mismo
contrato reproducible.

---

**Fecha de entrega:** 12 de octubre de 2026 — 11:59 PM