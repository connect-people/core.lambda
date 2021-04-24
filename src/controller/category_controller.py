import logging

from flask import request
from flask_restplus import Resource, reqparse

from ..util.dto import CategoryDto

api = CategoryDto.api
_major_category = CategoryDto.major_category
_category = CategoryDto.category


@api.route('/major')
class CategoryMajor(Resource):
    @api.doc('대 카테고리')
    @api.marshal_list_with(_major_category)
    def get(self):
        """대 카테고리"""
        major_categories = [
            {
                'major_id': 1,
                'major_label': '구매자',
            },
            {
                'major_id': 2,
                'major_label': '판매자',
            },
            {
                'major_id': 3,
                'major_label': '제조사',
            },
            {
                'major_id': 4,
                'major_label': '광고/판촉/제품소개서',
            },
            {
                'major_id': 5,
                'major_label': '기타(운송/수송) 등',
            },
        ]
        return {
            'result': {
                'code': 1,
                'message': 'ok'
            },
            'data': major_categories,
        }, 200


@api.route('/<int:major_id>/minor')
@api.param('major_id', 'major_id')
class CategoryMinor(Resource):
    @api.doc('중소 카테고리')
    @api.marshal_list_with(_category)
    def get(self, major_id):
        """중소 카테고리"""
        category = {'medium': [
            {
                'id': 1,
                'label': '패션',
                'minor': [
                    {'id': 1, 'label': '남성패션'},
                    {'id': 2, 'label': '여성패션'},
                    {'id': 3, 'label': '해외패션'},
                    {'id': 4, 'label': '아동패션'},
                    {'id': 5, 'label': '레포츠류'},
                ]
            },
            {
                'id': 2,
                'label': '부띠끄',
                'minor': [
                    {'id': 6, 'label': '화장품/향수'},
                    {'id': 7, 'label': '쥬얼리/악세사리'},
                    {'id': 8, 'label': '미용/뷰티'},
                    {'id': 9, 'label': '다이어트'},
                    {'id': 10, 'label': '건강식품'},
                    {'id': 11, 'label': '여성제품'},
                    {'id': 12, 'label': '남성제품'},
                    {'id': 13, 'label': '시계/귀금속'},
                    {'id': 14, 'label': '안경/선글라스'},
                    {'id': 15, 'label': '기타'},
                ]
            }
            ]
        }

        return {
            'result': {
                'code': 1,
                'message': 'ok'
            },
            'data': category,
        }, 200
