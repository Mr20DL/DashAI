from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from .database import Base

class PredictionHistory(Base):
    __tablename__ = "predictions"  # <--- Este es el nombre que Postgres no encontraba

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    prediction_date = Column(DateTime, default=datetime.utcnow)
    total_sales_predicted = Column(Float)
    advice_given = Column(String)