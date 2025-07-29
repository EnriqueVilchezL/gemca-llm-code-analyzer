# quiero comenzar desde el contenedor con python 3.11 slim
FROM python:3.11-slim

# copiar todo al directorio de trabajo
COPY . .

# instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# ejecutar la aplicación
CMD ["python3", "src/test_cases.py"]