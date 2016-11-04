import hashlib
import string
import random
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import column_property, relationship, validates
from sqlalchemy import func
from sqlalchemy import (
    Column,
    String,
    Boolean,
    Integer,
    ForeignKey,
    DateTime )

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired, BadSignature

Base = declarative_base()

class CommonColumns(Base):
    __abstract__ = True
    _created = Column(DateTime, default=func.now())
    _updated = Column(DateTime, default=func.now(), onupdate=func.now())
    _etag = Column(String(40))

class User(CommonColumns):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(80))
    password = Column(String)
    email = Column(String(255))
    delete = Column(Boolean)

    def generate_auth_token(self, expiration=24*60*60):
        s = Serializer(SECRET_KEY, expires_in=expiration)
        return s.dumps({'login': self.login })

    def isAuthorized(self, role_names):
        """Checks if user is related to given role_names.
        """
        allowed_roles = set([r.id for r in self.roles])\
            .intersection(set(role_names))
        return len(allowed_roles) > 0

    def generate_salt(self):
        return ''.join(random.sample(string.letters, 12))

    def encrypt(self, password):
        """Encrypt password using hashlib and current salt.
        """
        return str(hashlib.sha1(password + str(self.salt))\
            .hexdigest())

    @validates('password')
    def _set_password(self, key, value):
        """Using SQLAlchemy validation makes sure each
        time password is changed it will get encrypted
        before flushing to db.
        """
        self.salt = self.generate_salt()
        return self.encrypt(value)

    def check_password(self, password):
        if not self.password:
            return False
        return self.encrypt(password) == self.password

