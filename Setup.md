# Configuración del Proyecto PF3882

Este documento describe los pasos necesarios para configurar y ejecutar el proyecto **PF3882** en un entorno local utilizando Docker y Docker Compose.

## Requisitos Previos

Antes de comenzar, se debe contar con los siguientes programas instalados en el sistema:

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

## Pasos para Configurar el Proyecto

1. **Clonar el Repositorio**

   Clonar el repositorio del proyecto en la máquina local:

   ```bash
   git clone https://github.com/daperez03/PF3882.git
   cd PF3882/Tarea3/
   ```

2. **Construir los Contenedores**

   Construir las imágenes de Docker para todos los microservicios definidos en el archivo `docker-compose.yml`:

   ```bash
   docker-compose build
   ```

3. **Iniciar los Servicios**

   Iniciar todos los servicios definidos en el archivo `docker-compose.yml`:

   ```bash
   docker-compose up
   ```

   Esto iniciará los siguientes microservicios:
   - **Security API** en `http://127.0.0.1:5000`
   - **Order Tracking API** en `http://127.0.0.1:5001`
   - **Route Calculation API** en `http://127.0.0.1:5002`
   - **Warehouse Management API** en `http://127.0.0.1:5003`
   - **Product Management API** en `http://127.0.0.1:5004`

4. **Verificar la Configuración**

   Es posible acceder a la documentación interactiva de cada microservicio mediante Swagger UI en las siguientes direcciones:

   - [Security API](http://127.0.0.1:5000/docs)
   - [Order Tracking API](http://127.0.0.1:5001/docs)
   - [Route Calculation API](http://127.0.0.1:5002/docs)
   - [Warehouse Management API](http://127.0.0.1:5003/docs)
   - [Product Management API](http://127.0.0.1:5004/docs)

## Variables de Entorno

Cada microservicio utiliza un archivo `.env` para configurar las variables de entorno necesarias. Es importante asegurarse de que dichos archivos estén correctamente definidos antes de iniciar los servicios.

Ejemplo de configuración para `config.env`:

```env
SECURITY_SERVICE="http://security:5000/v1"
```

## Detener los Servicios

Para detener todos los servicios en ejecución, se debe ejecutar el siguiente comando:

```bash
docker-compose down
```

## Limpieza

En caso de que se requiera eliminar los contenedores, redes y volúmenes creados por Docker Compose, se puede utilizar:

```bash
docker-compose down --volumes
```

## Notas Adicionales

- Es recomendable verificar que los puertos definidos en el archivo `docker-compose.yml` no estén siendo utilizados por otros servicios en el sistema.