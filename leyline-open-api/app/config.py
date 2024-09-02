import os

# pylint: disable-next=too-few-public-methods
class Config:
    # pylint: disable-next=line-too-long
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://user:password@db:5432/mydatabase')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
