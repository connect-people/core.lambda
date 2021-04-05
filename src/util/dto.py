from flask_restplus import Namespace, fields


class NoticeDto:
    api = Namespace('notice', description='공지사항')
    pagination = api.model('pagination', {
        'page': fields.Integer(description='Number of this page of results'),
        'pages': fields.Integer(description='Total number of pages of results'),
        'per_page': fields.Integer(description='Number of items per page of results'),
        'total': fields.Integer(description='Total number of results'),
    })
    notice_post = api.model('notice_post', {
        'id': fields.Integer(description='id'),
        'title': fields.String(description='타이틀'),
        'content': fields.String(description='내용'),
        'member_id': fields.Integer(description='사용자 고유 번호'),
        'login_id': fields.String(description='작성자 아이디'),
        'member_name': fields.String(description='작성자 이름'),
        'created': fields.String(description='등록일')
    })
    notice = api.inherit('notice', pagination, {
        'items': fields.List(fields.Nested(notice_post))
    })

    notice_save = api.model('notice_save', {
        'title': fields.String(required=True, description='타이틀'),
        'content': fields.String(required=True, description='내용'),
        'member_id': fields.Integer(required=True, description='사용자 고유 번호'),
        'member_name': fields.String(required=True, description='사용자 이름'),
        'login_id': fields.String(required=True, description='사용자 아이디'),
    })

    notice_delete = api.model('notice_delete', {
        'id': fields.Integer(description='id')
    })


class BoardDto:
    api = Namespace('board', description='게시판')
    board = api.model('board', {
        'ID': fields.Integer(required=True, description='ID'),
        'brandName': fields.String(required=True, description='브랜드명'),
        'memberID': fields.Integer(required=True, description='회원번호'),
        'title': fields.String(required=True, description='타이틀'),
        'subTitle': fields.String(required=True, description='서브타이틀'),
        'content': fields.String(required=True, description='내용'),
        'majorCategoryID': fields.Integer(required=True, description='대카테고리 ID'),
        'created': fields.String(requried=False, description='등록일')
    })
