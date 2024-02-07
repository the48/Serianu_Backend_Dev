class Settings:
    PROJECT_NAME:str = "Serianu Backend Assessment"
    PROJECT_VERSION: str = "2.0.0"

    POSTGRES_USER = "postgres"
    POSTGRES_PASSWORD = "postgres"
    POSTGRES_SERVER = "127.0.0.1"
    POSTGRES_PORT = 5432
    POSTGRES_DB = "TeamRas"

    API_USER = "dev"
    API_USER_PASSWORD = "$2b$12$KZ4D9rFZaxuxN.LN5maiv.Q7c8xveOHwxaxSu.UPicXcf88mMlT9e" # need this hashed
    
    JWT_KEY = "hireme4success2024andbeyondbana@HR" #openssl rand -hex 32
    JWT_ALGORITHM = "HS256"
    JWT_VALIDITY = 10

    DATABASE_STR = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"


settings = Settings()