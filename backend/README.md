# setup del proyecto

Solo tienen que configurar el .env.example, crear un .env y copiar con las llaves de acceso a la base de datos, no existiran migraciones, se haran automaticamente asi que cuidado con cambiar los modelos de base de datos.

# Dependencias

Necesitan tener la herramienta UV de Astral, un gestor de proyectos, luego ejecutan este comando

```
uv sync
```

Para levantar el servidor solo tienen que utilizar este comando (estando dentro de la carpeta backend)

```
uvicorn src.main:app --reload --reload-dir ./src
```
