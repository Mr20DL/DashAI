# backend/app/ml/engine.py
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
from datetime import timedelta
import io

def process_and_predict(file_content):
    # 1. Leer el archivo CSV desde la memoria (sin guardarlo en disco)
    df = pd.read_csv(io.BytesIO(file_content))
    
    # IMPORTANTE: Asumimos que el CSV tiene columnas 'fecha' y 'ventas'
    # Convertimos la fecha a formato datetime
    df['fecha'] = pd.to_datetime(df['fecha'])
    
    # 2. Preparamos datos para la IA (Scikit-learn no entiende fechas, solo números)
    # Convertimos fecha a número ordinal (ej: día 1, día 2...)
    df['fecha_num'] = df['fecha'].map(pd.Timestamp.toordinal)
    
    X = df[['fecha_num']] # Features (Fechas)
    y = df['ventas']      # Target (Ventas a predecir)
    
    # 3. Entrenar el Modelo (Regresión Lineal Simple)
    model = LinearRegression()
    model.fit(X, y)
    
    # 4. Generar Predicciones Futuras (Próximos 30 días)
    last_date = df['fecha'].max()
    future_dates = [last_date + timedelta(days=x) for x in range(1, 31)]
    
    # Convertir fechas futuras a números para que el modelo entienda
    future_dates_num = np.array([d.toordinal() for d in future_dates]).reshape(-1, 1)
    
    # Predecir
    predictions = model.predict(future_dates_num)
    
    # 5. Formatear respuesta para el Frontend
    # Combinamos fechas reales + predicciones para enviarlo todo
    result = {
        "historico": [
            {"fecha": d.strftime("%Y-%m-%d"), "ventas": v} 
            for d, v in zip(df['fecha'], df['ventas'])
        ],
        "prediccion": [
            {"fecha": d.strftime("%Y-%m-%d"), "ventas_predichas": round(p, 2)} 
            for d, p in zip(future_dates, predictions)
        ],
        "resumen": {
            "total_ventas_historicas": int(df['ventas'].sum()),
            "prediccion_mes_siguiente": int(sum(predictions))
        }
    }
    
    return result