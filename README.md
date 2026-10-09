# Laboratorio 4 — Contenedores y Despliegue con Docker

**Cloud Computing — Universidad de Antioquia — 2026-II**

Aplicación web sencilla en **Python Flask** contenerizada con Docker.
Expone un endpoint `GET /sumar?a=<n>&b=<n>` que realiza la suma de dos números.

## Estructura del repositorio

```
.
├── app/
│   ├── app.py             # Aplicación Flask con los endpoints
│   ├── requirements.txt   # Dependencias (Flask)
│   ├── Dockerfile         # Receta para construir la imagen
│   └── .dockerignore      # Archivos excluidos del contexto de build
├── screenshots/           # Capturas del contenedor y Docker Hub
├── .gitignore
└── README.md
```

## Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/` | Vista HTML con formulario (interfaz web) |
| GET | `/sumar?a=5&b=3` | Suma dos números y devuelve JSON |
| GET | `/health` | Healthcheck — responde `{"status":"ok"}` |

## Ejecución local con Docker

```bash
cd app
docker build -t miapp-docker:v1 .
docker run -d -p 3000:3000 --name miapp-contenedor miapp-docker:v1
```

Abrir en el navegador: <http://localhost:3000>

## Publicación en Docker Hub

```bash
docker tag miapp-docker:v1 TU_USUARIO/miapp-docker:v1
docker login
docker push TU_USUARIO/miapp-docker:v1
```

## Autor

**Michael Stiven Tabares Tobón** — `michael.tabares@udea.edu.co`
Profesor: Juan Pablo Arango Vásquez
Medellín, 2026
