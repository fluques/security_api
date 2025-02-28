from marshmallow import Schema, fields


class PlainUserSchema(Schema):
    id = fields.Int(dump_only=True)
    user_name = fields.Str(required=True)
    password = fields.Str(required=True,load_only=True)
    email = fields.Str(required=True)
    is_active = fields.Bool(required=True)

class PlainGroupSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)   

class UserUpdateSchema(Schema):
    user_name = fields.Str()
    password = fields.Str()
    email=fields.Str()
    is_active=fields.Bool()

class GroupUpdateSchema(Schema):
    name = fields.Str(required=True)


class UserSchema(PlainUserSchema):
    groups = fields.List(fields.Nested(PlainGroupSchema()), dump_only=True)


class GroupSchema(PlainGroupSchema):
    users = fields.List(fields.Nested(PlainUserSchema()), dump_only=True)


class UsersAndGroupsSchema(Schema):
    id = fields.Int()
    user = fields.Nested(UserSchema)
    group = fields.Nested(GroupSchema)
