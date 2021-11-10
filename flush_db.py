from api.database import Base, engine

# below option flushes the db !
if __name__ == '__main__':
    Base.metadata.drop_all(bind=engine) 
    Base.metadata.create_all(bind=engine)

