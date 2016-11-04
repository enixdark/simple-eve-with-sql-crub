from eve_sqlalchemy.decorators import registerSchema
from schema import User
from eve.utils import config
registerSchema('user')(User)

DEBUG=True
SQLALCHEMY_DATABASE_URI = 'sqlite://'
SQLALCHEMY_TRACK_MODIFICATIONS = True
IF_MATCH = False

DOMAIN = {
    'user': User._eve_schema['user']
}
DOMAIN['user'].update({
    'item_lookup_field': 'id',
    'item_title': 'user',
    'additional_lookup': {
        'url': '<regex("[\w]+"):id>',
        'field': 'id'
    },
    'cache_control': 'max-age=10,must-revalidate',
    'cache_expires': 10,
    'resource_methods': ['GET', 'POST'],
    'item_methods': ['GET', 'PUT','DELETE']

  })

ID_FIELD = 'id'
ITEM_LOOKUP_FIELD = ID_FIELD
config.ID_FIELD = ID_FIELD
config.ITEM_LOOKUP_FIELD = ID_FIELD
