from sqlalchemy import create_engine,event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import Engine


#datos para la conexion a BD

dataBaseName="gestordb"
userName="root"
userPassword=""
connectionPort=3306
server="localhost"

#creando la conexion
dataBaseConnection=f"mysql+mysqlconnector://{userName}:{userPassword}@{server}:{connectionPort}/{dataBaseName}"

print(dataBaseConnection)

# Creo el motor de conexion
engine = create_engine(dataBaseConnection)

#Abrir la sesion con la baese de dato

sessionLocals = sessionmaker(autocommit=False, autoflush=False, bind=engine)
