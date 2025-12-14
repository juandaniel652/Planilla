from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Asignaciones(Base):
    __tablename__ = 'asignaciones'
    id = Column(Integer, primary_key=True, index=True)
    territorio_id = Column(Integer, index=True)
    conductor_id = Column(Integer, index=True)
    fecha_asignado = Column(Date)
    fecha_completado = Column(Date)
    cantidad_abarcado = Column(String)

class Conductores(Base):
    __tablename__ = 'conductores'
    id = Column(Integer, primary_key=True, index=True)
    nombre_completo = Column(String)

class Territorios(Base):
    __tablename__ = 'territorios'
    id = Column(Integer, primary_key=True, index=True)
    numero = Column(Integer, unique=True)


def crear_asignacion(db: Session, territorio_id: int, conductor_id: int, fecha_asignado: str, fecha_completado: str, cantidad_abarcado: str):
    db_asignacion = Asignaciones(
        territorio_id=territorio_id,
        conductor_id=conductor_id,
        fecha_asignado=fecha_asignado,
        fecha_completado=fecha_completado,
        cantidad_abarcado=cantidad_abarcado
    )
    db.add(db_asignacion)
    db.commit()
    db.refresh(db_asignacion)
    return db_asignacion


