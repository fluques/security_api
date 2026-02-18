from marshmallow import Schema, ValidationError, fields
from sqlalchemy.types import LargeBinary
class BytesField(fields.Field):
    def _validate(self, value):
        if not isinstance(value, bytes):
            raise ValidationError('Invalid input type.')

        if value is None or value == b'':
            raise ValidationError('Invalid value')


#PLAIN SCHEMAS

class PlainCompanySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    street = fields.Str(required=True)
    zip_code = fields.Str(required=True)
    city = fields.Str(required=True)
    state = fields.Str(required=True)
    country = fields.Str(required=True)
    main_email= fields.Str(required=True)
    emails = fields.Str(required=False)
    phone = fields.Str(required=True)
    celphone = fields.Str(required=False)
    is_active=fields.Bool()


class PlainUserSchema(Schema):
    id = fields.Int(dump_only=True)
    user_name = fields.Str(required=True)
    password = fields.Str(required=True,load_only=True)
    email = fields.Str(required=True)
    is_active = fields.Bool(required=True)

class PlainGroupSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)   


class ApplicationSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.Str(required=True)

####UPDATE SCHEMAS

class CompanyUpdateSchema(Schema):
    name = fields.Str(required=True)
    street = fields.Str(required=True)
    zip_code = fields.Str(required=True)
    city = fields.Str(required=True)
    state = fields.Str(required=True)
    country = fields.Str(required=True)
    main_email= fields.Str(required=True)
    emails = fields.Str(required=False)
    phone = fields.Str(required=True)
    celphone = fields.Str(required=False)
    is_active=fields.Bool()

class ApplicationUpdateSchema(Schema):
    name = fields.Str(required=True)

class UserUpdateSchema(Schema):
    user_name = fields.Str()
    password = fields.Str()
    email=fields.Str()
    is_active=fields.Bool()

class GroupUpdateSchema(Schema):
    name = fields.Str(required=True)

class SettingsUpdateSchema(Schema):
    smtp_server = fields.Str()
    smtp_user = fields.Str()
    smtp_password = fields.Str()

class ResourceUpdateSchema(Schema):
    name = fields.Str(required=True)
    uri = fields.Str(required=True)

class ActionUpdateSchema(Schema):
    name = fields.Str(required=True)

#COMPLETE SCHEMAS
class SettingsSchema(Schema):
    id = fields.Int(dump_only=True)
    smtp_server = fields.Str()
    smtp_user = fields.Str()
    smtp_password = fields.Str()

class ActionSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)

class UserTypeSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)

class ResourceSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    uri = fields.Str(required=True)

#NESTED SCHEMAS

class PlainPermissionsSchema(Schema):
    id = fields.Int(dump_only=True)
    company_id= fields.Int()
    application_id= fields.Int()
    resource_id= fields.Int()
    action_id= fields.Int()

class PermissionsSchema(PlainPermissionsSchema):
    id = fields.Int(dump_only=True)
    company = fields.Nested(PlainCompanySchema(only=("id","name")))
    resource = fields.Nested(ResourceSchema)
    action = fields.Nested(ActionSchema)
    application = fields.Nested(ApplicationSchema)

class PermissionsUpdateSchema(PlainPermissionsSchema):
    id = fields.Int(dump_only=True)
    company = fields.Nested(PlainCompanySchema(only=("id","name")))
    resource = fields.Nested(ResourceSchema)
    action = fields.Nested(ActionSchema)
    application = fields.Nested(ApplicationSchema)


#class TypesAndUsersSchema(Schema):
#    id = fields.Int(dump_only=True)
    #type = fields.Nested(TypeSchema)
    #user = fields.Nested(PlainUserSchema)


class UsersAndPermissionsSchema(Schema):
    id = fields.Int(dump_only=True)
    permission = fields.Nested(PermissionsSchema)
    user = fields.Nested(PlainUserSchema)



class GroupsAndPermissionsSchema(Schema):
    id = fields.Int(dump_only=True)
    permission = fields.Nested(PermissionsSchema)
    group = fields.Nested(PlainGroupSchema(only=("id","name")))



class UserSchema(PlainUserSchema):
    groups = fields.List(fields.Nested(PlainGroupSchema(only=("id","name"))), dump_only=True)
    companies = fields.List(fields.Nested(PlainCompanySchema(only=("id","name"))), dump_only=True)
    permissions = fields.List(fields.Nested(PermissionsSchema), dump_only=True)
    types = fields.List(fields.Nested(UserTypeSchema(only=("id","name"))), dump_only=True)


class UserDetailSchema(PlainUserSchema):
    groups = fields.List(fields.Nested(PlainGroupSchema(only=("id","name"))), dump_only=True)
    companies = fields.List(fields.Nested(PlainCompanySchema(only=("id","name"))), dump_only=True)
    permissions = fields.List(fields.Nested(PermissionsSchema()), dump_only=True)
    types = fields.List(fields.Nested(UserTypeSchema(only=("id","name"))), dump_only=True)

class GroupSchema(PlainGroupSchema):
    users = fields.List(fields.Nested(PlainUserSchema()), dump_only=True)
    permissions = fields.List(fields.Nested(GroupsAndPermissionsSchema()), dump_only=True)


class CompanySettingsSchema(Schema):
    id = fields.Int(dump_only=True)
    hostname = fields.Str(required=True)
    #company = fields.Nested(PlainCompanySchema(), dump_only = True)

class CompanySchema(PlainCompanySchema):
    users = fields.List(fields.Nested(PlainUserSchema()), dump_only = True)
    settings = fields.Nested(CompanySettingsSchema())


# MANY TO MANY SCHEMAS
class CompaniesAndUsersSchema(Schema):
    user = fields.Nested(UserSchema)
    company = fields.Nested(CompanySchema)


class UsersAndGroupsSchema(Schema):
    user = fields.Nested(UserSchema)
    group = fields.Nested(GroupSchema)


class CompaniesAndUsersSchema(Schema):
    company = fields.Nested(CompanySchema)
    user = fields.Nested(UserSchema)


class PaginationSchema(Schema):
    page = fields.Int(required=True)
    per_page = fields.Int(required=True)