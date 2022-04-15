from tortoise import Model, fields
from tortoise.contrib.pydantic import pydantic_model_creator

from models.user_model import User

class FriendMatch(Model):
    uuid= fields.UUIDField(pk=True)
    request_user= fields.ForeignKeyField("models.User", related_name="friends_matches")
    request_user_infos: fields.ForeignKeyRelation[User]
    main_user_uuid= fields.CharField(max_length=100, null=False)
    accepted= fields.BooleanField(default=False, null=False)
    
friend_match_pydanticIn = pydantic_model_creator(FriendMatch, name="FriendMatchIn", exclude=("uuid", "accepted"))
friend_match_pydanticOut = pydantic_model_creator(FriendMatch, name="FriendMatchOut")