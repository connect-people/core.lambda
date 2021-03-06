from flask import Blueprint
from flask_restplus import Api
from .controller.notice_controller import api as notice_ns
from .controller.board_controller import api as board_ns
from .controller.member_controller import api as member_ns
from .controller.category_controller import api as category_ns

main_blueprint = Blueprint("api", __name__)

api = Api(main_blueprint,
          title='CONNECT_PEOPLE CORE API',
          version='1.0',
          description='the connect_people for flask restful web service'
          )


api.add_namespace(notice_ns, path='/notice')      # 공지사항
api.add_namespace(board_ns, path='/board')        # 게시판
api.add_namespace(member_ns, path='/member')      # 사용자
api.add_namespace(category_ns, path='/category')  # 카테고리
