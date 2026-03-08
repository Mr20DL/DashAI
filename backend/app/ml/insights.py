# backend/app/ml/insights.py
import random

def generate_business_advice(sales_summary):
    """
    Aquí es donde conectaríamos OpenAI (GPT) o Hugging Face.
    Por ahora, usaremos una 'IA basada en Reglas' para probar el flujo rápido.
    """
    
    current_sales = sales_summary['total_ventas_historicas']
    predicted_sales = sales_summary['prediccion_mes_siguiente']
    
    # Calculamos el crecimiento
    growth = ((predicted_sales - current_sales) / current_sales) * 100
    
    advice = ""
    tone = ""

    if growth > 10:
        tone = "positive"
        advice = (
            f"🚀 **Tendencia Alcista Detectada (+{round(growth, 1)}%)**: "
            "Se prevé un aumento significativo en la demanda. "
            "Recomendación: Aumenta tu inventario un 15% y prepara campañas de marketing para aprovechar el tráfico."
        )
    elif growth < -10:
        tone = "negative"
        advice = (
            f"⚠️ **Alerta de Caída (-{abs(round(growth, 1))}%)**: "
            "Las proyecciones indican una desaceleración. "
            "Recomendación: Lanza ofertas flash para rotar stock y revisa tus gastos operativos este mes."
        )
    else:
        tone = "neutral"
        advice = (
            f"⚖️ **Estabilidad (+{round(growth, 1)}%)**: "
            "El mercado se mantiene estable. "
            "Recomendación: Es buen momento para fidelizar clientes actuales mediante programas de lealtad."
        )

    return {
        "text": advice,
        "tone": tone
    }