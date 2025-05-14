from sqlalchemy import Column, Integer, String
from app.database import Base, engine

class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=True)

def init_db():
    Base.metadata.create_all(bind=engine)
    print("Tabelas criadas com sucesso.")