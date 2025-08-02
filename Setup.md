# Ejecucion de Pruebas

Este documento describe los pasos necesarios para ejecutar las pruebas en un entorno local utilizando Docker y Docker Compose.

## Requisitos Previos

Antes de comenzar, se debe contar con los siguientes programas instalados en el sistema:

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

## Pasos para Configurar el Proyecto

1. **Clonar el Repositorio**

   Clonar el repositorio del proyecto en la máquina local:

   ```bash
   git clone https://github.com/EnriqueVilchezL/gemca-llm-code-analyzer.git
   cd gemca-llm-code-analyzer
   ```

2. **Construir los Contenedores**

   Construir las imágenes de Docker para todas las pruebas
   
    definidos en el archivo `docker-compose.yml`:

   ```bash
   docker-compose build
   ```

3. **Iniciar los Servicios**

   Ejecutar las pruebas definidos en el archivo `docker-compose.yml`:

   ```bash
   docker-compose up
   ```

## Variables de Entorno

Hay un archivo `.env` para configurar las variables de entorno necesarias. Es importante asegurarse de que dicho archivo este correctamente definidos antes de iniciar las pruebas.

## Detener las pruebas

Para detener todas las pruebas en ejecución, se debe ejecutar el siguiente comando:

```bash
docker-compose down
```

## Limpieza

En caso de que se requiera eliminar los contenedores, redes y volúmenes creados por Docker Compose, se puede utilizar:

```bash
docker-compose down --volumes
```