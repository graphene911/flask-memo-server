from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api
from config import Config
from resources.follow import FollowListResource, FollowResource
from resources.memo import MemoListResource
from resources.memo_update import MemoUpdateResource
from resources.user import UserLoginResource, UserLogoutResource, UserRegisterResource, jwt_blacklist

print('1')
app = Flask(__name__)
print('2')

# 환경변수 셋팅
app.config.from_object(Config)
print('3')
# JWT Token Library 만들기
jwt = JWTManager(app)
print('4')

# 로그아웃 된 토큰이 들어있는 set을 jwt에 알려준다.
@jwt.token_in_blocklist_loader
def check_if_otken_is_revoked(jwt_header, jwt_payload) :
    jti = jwt_payload['jti']
    return jti in jwt_blacklist
print('5')
api = Api(app)
print('6')
# 경로와 resource(API 코드)를 연결한다.
api.add_resource(UserRegisterResource, '/users/register')
print('7')
api.add_resource(UserLoginResource, '/users/login')
print('8')
api.add_resource(UserLogoutResource, '/users/logout')
print('9')
api.add_resource(MemoListResource, '/memo')
print('10')
api.add_resource(MemoUpdateResource, '/memo/<int:memo_id>')
print('11')
api.add_resource(FollowResource, '/follow/<int:follow_id>')
print('12')
api.add_resource(FollowListResource, '/follow')
print('13')
if __name__ == '__main__' :
    app.run()
print('14')