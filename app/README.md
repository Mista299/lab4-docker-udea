# Laboratorio 4 — Contenedores y Despliegue con Docker

Aplicación web simple en **Python Flask** contenerizada con Docker.
Expone un endpoint `GET /sumar?a=<n>&b=<n>` que realiza la suma de dos números.

## Estructura

```
app/
├── app.py             # Aplicación Flask con los endpoints
├── requirements.txt   # Dependencias (Flask)
├── Dockerfile         # Receta para construir la imagen
└── .dockerignore      # Archivos excluidos del contexto de build
```

## Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/` | Información del servicio |
| GET | `/sumar?a=5&b=3` | Suma dos números |
| GET | `/health` | Estado del servicio |

## Pruebas rápidas (sin Docker)

```bash
cd app
pip install -r requirements.txt
python app.py
```

Abrir en el navegador o con curl:
```
http://localhost:3000/
http://localhost:3000/sumar?a=5&b=3
http://localhost:3000/health
```

---

## Comandos Docker (los ejecutas tú y tomas pantallazos)

> ⚠️ Todos los comandos se ejecutan dentro de la carpeta `app/`.

### 1. Verificar instalación de Docker
```bash
docker --version
docker info
```

### 2. Construir la imagen
```bash
docker build -t miapp-docker:v1 .
```

### 3. Listar imágenes
```bash
docker images
```

### 4. Ejecutar el contenedor (modo daemon)
```bash
docker run -d -p 3000:3000 --name miapp-contenedor miapp-docker:v1
```

### 5. Verificar contenedor en ejecución
```bash
docker ps
```

### 6. Probar el servicio
Abre en el navegador:
```
http://localhost:3000/
http://localhost:3000/sumar?a=10&b=25
http://localhost:3000/health
```
O con curl:
```bash
curl http://localhost:3000/
curl "http://localhost:3000/sumar?a=10&b=25"
```

### 7. Ver logs del contenedor
```bash
docker logs miapp-contenedor
```

### 8. Detener y eliminar el contenedor
```bash
docker stop miapp-contenedor
docker rm miapp-contenedor
```

### 9. Publicar en Docker Hub

Reemplaza `USUARIO` por tu usuario real de Docker Hub:
```bash
docker tag miapp-docker:v1 USUARIO/miapp-docker:v1
docker login
docker push USUARIO/miapp-docker:v1
```

### 10. (Opcional) Probar la imagen en otro entorno
```bash
docker pull USUARIO/miapp-docker:v1
docker run -d -p 3000:3000 USUARIO/miapp-docker:v1
```

---

## Capturas sugeridas para la entrega

- `docker --version` y `docker info`
- Contenido del Dockerfile en el editor
- `docker build` mostrando las capas construyéndose
- `docker images` con la imagen creada
- `docker run` + `docker ps`
- Navegador con `http://localhost:3000/sumar?a=10&b=25`
- `docker push` exitoso
- Repositorio público en Docker Hub