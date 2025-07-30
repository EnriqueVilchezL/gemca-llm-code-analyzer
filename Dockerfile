# quiero comenzar desde el contenedor con python 3.11 slim
FROM python:3.12-slim

# copiar todo al directorio de trabajo
COPY . .

# instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# crear directorios necesarios
RUN mkdir -p analysis/results/php
RUN mkdir -p analysis/results/csharp

# descomprimir los casos de prueba
RUN python3 -m zipfile -e test_data/php.zip test_data/php
RUN python3 -m zipfile -e test_data/csharp.zip test_data/csharp

# ejecutar la aplicación
CMD ["python3", "src/test_cases.py"]