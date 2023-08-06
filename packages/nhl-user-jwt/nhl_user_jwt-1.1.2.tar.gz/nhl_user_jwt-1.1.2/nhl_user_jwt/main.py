# coding: utf-8
import json
from datetime import datetime, timedelta

from jose import jwt

ALGORITHM = "HS256"


class NhlUserJwt:
    def __init__(self, redis_pool, settings):
        self.redis_pool = redis_pool
        self.settings = settings
        self.invalid_jwt_cache = InvalidJWTCache(redis_pool, self)

    @staticmethod
    def _gen_jwt_sub(user_id: int, app_user_id: int, app_user_type: int):
        return f'[{user_id}, {app_user_id}, {app_user_type}]'

    def create_access_token(self, user_id: int, app_user_id: int, app_user_type: int, expires_delta: timedelta) -> str:
        expire = datetime.utcnow() + expires_delta
        to_encode = {"exp": expire, "sub": self._gen_jwt_sub(user_id, app_user_id, app_user_type)}
        encoded_jwt = jwt.encode(to_encode, self.settings['SECRET_KEY'], algorithm=ALGORITHM)
        return encoded_jwt

    def validate_access_token(self, token: str) -> dict:
        """
        jwt验签：成功后返回payload中的用户数据
        1.jwt是否能被正确解析
        2.是否在有效期
        3.用户是否被冻结或禁用

        :param token:
        :return:
        """

        # 解析payload
        try:
            payload = jwt.decode(
                token, self.settings['SECRET_KEY'], algorithms=[ALGORITHM]
            )
        except jwt.JWTError:
            return {'success': False}

        sub = json.loads(payload.get('sub'))
        exp = payload.get('exp')

        # 日期检测
        exp_datetime = datetime.fromtimestamp(float(exp))
        if exp_datetime <= datetime.utcnow():
            return {'success': False}

        # 是否被强制退出
        if self.invalid_jwt_cache.get(*sub):
            return {'success': False}
        return {'success': True, 'data': {'sub': sub}}


class InvalidJWTCache:
    """
    强制退出：
    被冻结或禁用的用户，以jwt中的sub为key在redis中做标记，在进行jwt验签时，强制退出该用户。
    用户登录在前，冻结或禁用操作在后时有效。结合用户的最后登录时间使用
    """
    def __init__(self, redis_pool, nhl_user_jwt):
        self.redis_pool = redis_pool
        self.nhl_user_jwt = nhl_user_jwt
        self.settings = nhl_user_jwt.settings

    def _gen_cache_key(self, *sub_data):
        sub = self.nhl_user_jwt._gen_jwt_sub(*sub_data)
        return self.settings['CACHE_KEY_SEPARATOR'].join([self.settings['INVALID_JWT_CACHE_KEY'], sub])

    def set(self, *sub_data):
        key = self._gen_cache_key(*sub_data)
        self.redis_pool.set(key, 1, expire=self.settings['INVALID_JWT_TTL'])

    def get(self, *sub_data) -> bool:
        key = self._gen_cache_key(*sub_data)
        val = self.redis_pool.get(key)
        return True if val else False

    def delete(self, *sub_data) -> bool:
        self.redis_pool.delete(self._gen_cache_key(*sub_data))
        return True


__all__ = ('NhlUserJwt',)
