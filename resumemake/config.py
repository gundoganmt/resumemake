import psycopg2, os

class Config:
    SECRET_KEY = '7c6b7967-dcba-4796-a261-f36b028144e3'
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres:WulIgtM5zk@localhost/resumemake"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = "smtp.zoho.com"
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = "admin@webpaget.com"
    MAIL_PASSWORD = "UpG6v6Z1Cj23"
