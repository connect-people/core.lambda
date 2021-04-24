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
    result = api.model('result', {
        'code': fields.Integer(description='code'),
        'message': fields.String(description='message'),
    })
    pagination = api.model('pagination', {
        'page': fields.Integer(description='Number of this page of results'),
        'pages': fields.Integer(description='Total number of pages of results'),
        'per_page': fields.Integer(description='Number of items per page of results'),
        'total': fields.Integer(description='Total number of results'),
    })
    board_data = api.model('board_data', {
        'ID': fields.Integer(required=True, description='ID'),
        'brandName': fields.String(required=True, description='브랜드명'),
        'memberID': fields.Integer(required=True, description='회원번호'),
        'title': fields.String(required=True, description='타이틀'),
        'subTitle': fields.String(required=True, description='서브타이틀'),
        'content': fields.String(required=True, description='내용'),
        'majorCategoryName': fields.String(required=True, description='대카테고리명'),
        'imageUrl': fields.String(required=True, description='이미지 URL'),
        'created': fields.String(requried=False, description='등록일')
    })
    # board_detail_data = api.model('board_detail_data', {
    #     'ID': fields.Integer(required=True, description='ID'),
    #     'brandName': fields.String(required=True, description='브랜드명'),
    #     'memberID': fields.Integer(required=True, description='회원번호'),
    #     'title': fields.String(required=True, description='타이틀'),
    #     'subTitle': fields.String(required=True, description='서브타이틀'),
    #     'content': fields.String(required=True, description='내용'),
    #     'imageUrls': fields.List(fields.String),
    #     'created': fields.String(requried=False, description='등록일')
    # })
    board_save = api.model('board_save', {
        'brandName': fields.String(required=True, description='브랜드명'),
        'title': fields.String(required=True, description='타이틀'),
        'subTitle': fields.String(required=True, description='서브타이틀'),
        'content': fields.String(required=True, description='내용'),
        'imageUrls': fields.List(fields.String),
        'categoryIDs': fields.List(fields.Integer),
    })
    board = api.inherit('board', pagination, {
        'items': fields.List(fields.Nested(board_data))
    })
    board_detail = api.model('board_detail', {
        'data': fields.Nested(
            api.model('board_detail_data', {
                'ID': fields.Integer(required=True, description='ID'),
                'brandName': fields.String(required=True, description='브랜드명'),
                'memberID': fields.Integer(required=True, description='회원번호'),
                'title': fields.String(required=True, description='타이틀'),
                'subTitle': fields.String(required=True, description='서브타이틀'),
                'content': fields.String(required=True, description='내용'),
                'imageUrls': fields.List(fields.String),
                'created': fields.String(requried=False, description='등록일')
            })
        )
    })
    board_search = api.model('board_search', {
        'result': fields.Nested(result),
        'paging': fields.Nested(pagination),
        'data': fields.List(fields.Nested(board_data))
    })
    board_list = api.model('board_list', {
        'result': fields.Nested(result),
        'paging': fields.Nested(pagination),
        'data': fields.List(fields.Nested(board_data))
    })


class MemberDto:
    api = Namespace('member', description='사용자')
    member_signup = api.model('member_signup', {
        'login_id': fields.String(required=True, description='로그인아이디'),
        'password': fields.String(required=True, description='패스워드'),
        'name': fields.String(required=True, description='이름'),
        'phone': fields.String(required=False, description='휴대폰번호'),
        'is_auth': fields.Integer(required=False, description='휴대폰 인증여부'),
        'created': fields.String(requried=False, description='등록일')
    })
    member_signin = api.model('member_signin', {
        'login_id': fields.String(required=True, description='로그인아이디'),
        'password': fields.String(required=True, description='패스워드')
    })
    result = api.model('result', {
        'code': fields.Integer(description='code'),
        'message': fields.String(description='message'),
    })
    data = api.model('data', {
        'id': fields.Integer(required=False, description='사용자 고유 번호'),
        'login_id': fields.String(required=False, description='로그인아이디'),
        'password': fields.String(required=False, description='패스워드'),
        'name': fields.String(required=False, description='이름'),
        'phone': fields.String(required=False, description='휴대폰번호'),
        'is_auth': fields.Integer(required=False, description='휴대폰 인증여부'),
        'created': fields.String(requried=False, description='등록일')
    })
    me = api.model('me', {
        'result': fields.Nested(result),
        'data': fields.Nested(data)
    })


class CategoryDto:
    api = Namespace('category', description='카테고리')
    result = api.model('result', {
        'code': fields.Integer(description='code'),
        'message': fields.String(description='message'),
    })
    major_category = api.model('major_category', {
        'result': fields.Nested(result),
        'data': fields.List(fields.Nested(
            api.model('major', {
                'major_id': fields.Integer(required=True, description='id'),
                'major_label': fields.String(required=True, description='대 카테고리명'),
            })
        ))
    })
    minor_category = api.model('minor', {
        'id': fields.Integer(required=True, description='id'),
        'label': fields.String(required=True, description='중 카테고리명')
    })
    medium_category_data = api.model('medium_category_data', {
        'id': fields.Integer(required=True, description='id'),
        'label': fields.String(required=True, description='중 카테고리명'),
        'minor': fields.List(fields.Nested(minor_category))
    })
    medium_category = api.model('medium1', {
        'medium': fields.List(fields.Nested(medium_category_data))
    })
    category = api.model('medium_category', {
        'result': fields.Nested(result),
        'data': fields.Nested(medium_category)
    })
