from flask import request
from flask_restplus import Resource, reqparse

from ..util.dto import NoticeDto
from ..service.notice_service import (
    save_new_notice,
    get_all_notices,
    get_by_notice_id,
    delete_by_notice_id
)

api = NoticeDto.api
_notice_load = NoticeDto.notice
_notice_save = NoticeDto.notice_save
_notice_delete = NoticeDto.notice_delete

arguments = reqparse.RequestParser()
arguments.add_argument('page', type=int, required=False, default=1, help='현재 페이지')
arguments.add_argument('per_page', type=int, required=False, default=20, help='한 페이지에 보여질 갯수')


@api.route('/')
class NoticeList(Resource):
    @api.doc('공지사항 리스트')
    @api.expect(arguments)
    @api.marshal_with(_notice_load)
    def get(self):
        """공지사항 전체 리스트"""
        args = arguments.parse_args(request)
        page = args.get('page', 1)
        per_page = args.get('per_page', 20)
        return get_all_notices(page, per_page)

    @api.response(200, 'ok')
    @api.doc('공지사항 등록')
    @api.expect(_notice_save, validate=True)
    def post(self):
        """공지사항 등록"""
        data = request.json
        return save_new_notice(data=data)


@api.route('/<int:notice_id>')
@api.param('notice_id', 'notice_id')
@api.response(404, 'notice not found')
class Notice(Resource):
    @api.doc('공지사항 상세')
    @api.marshal_with(_notice_load)
    def get(self, notice_id) -> dict:
        """공지사항 상세"""
        notice = get_by_notice_id(notice_id)
        if not notice:
            api.abort(404)
        else:
            return notice

    @api.doc('공지사항 삭제')
    @api.marshal_with(_notice_delete)
    def delete(self, notice_id):
        """공지사항 삭제"""
        return delete_by_notice_id(notice_id)

