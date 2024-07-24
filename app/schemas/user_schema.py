# import config.db_config as db_config

# ma = db_config.ma

# # Definir el esquema de usuario
# class UserSchema(ma.Schema):
#   class Meta:
#     fields = ('id', 'name', 'username', 'email', 'password', 'created_at')

# user_schema = UserSchema()
# users_schema = UserSchema(many=True)


from marshmallow import Schema, fields, validate

class UserSchema(Schema):
  id = fields.Int(dump_only=True)
  name = fields.Str(required=True, validate=validate.Length(min=1))
  username = fields.Str(required=True, validate=validate.Length(min=1))
  email = fields.Email(required=True)
  password = fields.Str(required=True, validate=validate.Length(min=4))

user_schema = UserSchema()
users_schema = UserSchema(many=True)
