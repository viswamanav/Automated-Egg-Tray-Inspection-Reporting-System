from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from api.database import Base


# Table to store each inspection
class Inspection(Base):
    __tablename__ = "inspections"

    id = Column(Integer, primary_key=True, index=True)

    image_name = Column(String)

    expected_eggs = Column(Integer)

    detected_eggs = Column(Integer)

    missing_eggs = Column(Integer)

    status = Column(String)

    model_name = Column(String)

    inference_time = Column(Float)

    # One inspection can have many detections
    detections = relationship("DetectionItem", back_populates="inspection")


# Table to store every detected egg
class DetectionItem(Base):
    __tablename__ = "detection_items"

    id = Column(Integer, primary_key=True, index=True)

    inspection_id = Column(Integer, ForeignKey("inspections.id"))

    class_name = Column(String)

    confidence = Column(Float)

    x1 = Column(Float)
    y1 = Column(Float)
    x2 = Column(Float)
    y2 = Column(Float)

    # Connect back to Inspection
    inspection = relationship("Inspection", back_populates="detections")