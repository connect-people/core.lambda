import logging
import boto3
import os

from datetime import datetime
from werkzeug.utils import secure_filename
from sqlalchemy.sql import text
from urllib.parse import urlparse, ParseResult

from .. import db
from ..model.board import Board, BoardImage
from ..model.category import CategoryScope
from ..config import S3_HOST, S3_BUCKET


def upload_image(file):
    filename = secure_filename(file.filename)
    temp_path = f'temp/{"{:%Y%m%d}".format(datetime.now())}/{filename}'

    logging.debug(temp_path)

    s3 = boto3.client('s3')
    s3.upload_fileobj(
        file,
        S3_BUCKET,
        temp_path,
        ExtraArgs={
            'ACL': 'public-read',
            'ContentType': 'application/octet-stream',
            'ServerSideEncryption': 'AES256'
        }
    )
    return f'{S3_HOST}/{temp_path}'


def resize_image(image_path, resized_path) -> bool:
    try:
        app_env = os.environ.get('APP_ENV')
        if app_env == "local":
            import PIL
            with PIL.Image.open(image_path) as image:
                image.thumbnail(tuple(x / 2 for x in image.size), PIL.Image.ANTIALIAS)
                image.save(resized_path)
        else:
            from PIL import Image, ExifTags
            with Image.open(image_path) as image:
                image.thumbnail(tuple(x / 2 for x in image.size), Image.ANTIALIAS)
                if ExifTags.TAGS.keys():
                    for orientation in ExifTags.TAGS.keys():
                        if ExifTags.TAGS[orientation] == 'Orientation':
                            break
                    exif = image._getexif()
                    logging.debug(f'exif[orientation] : {exif[orientation]}')
                    if exif[orientation] == 3:
                        image = image.rotate(180, expand=True)
                    elif exif[orientation] == 6:
                        image = image.rotate(270, expand=True)
                    elif exif[orientation] == 8:
                        image = image.rotate(90, expand=True)

                image.save(resized_path)
                image.close()
        return True

    except Exception as e:
        logging.error(str(e))
        return False


def save_new_board(data, member_id) -> int:
    try:
        new_board = Board(
            brandName=data['brandName'],
            memberID=member_id,
            title=data['title'],
            subTitle=data['subTitle'],
            content=data['content']
        )
        save(new_board)

        if data['imageUrls']:
            s3 = boto3.client('s3')
            for i, image_url in enumerate(data['imageUrls']):
                parts = urlparse(image_url)
                filename = parts.path.split("/")[3]
                temp_key = parts.path.lstrip("/")
                download_path = f'/tmp/{filename}'
                resized_path = f'/tmp/resized-{filename}'
                upload_key = f'images/storage/board/{"{:%Y%m%d}".format(datetime.now())}/{filename}'

                s3.download_file(S3_BUCKET, temp_key, download_path)
                logging.debug(f'temp image download complete. {download_path}')
                if resize_image(download_path, resized_path) is False:
                    logging.error(f'image resizing fail. {download_path}')
                    s3.upload_file(download_path, S3_BUCKET, upload_key, ExtraArgs={'ACL': 'public-read'})
                else:
                    logging.debug(f'image resizing complete. {resized_path}')
                    s3.upload_file(resized_path, S3_BUCKET, upload_key, ExtraArgs={'ACL': 'public-read'})
                logging.debug(f's3 upload complete. {upload_key}')

                cdn = ParseResult(
                    scheme='https',
                    netloc='d1cyiajrf0e1fn.cloudfront.net',
                    path=f'/{upload_key}',
                    params='',
                    query='',
                    fragment=''
                )
                logging.debug(cdn.geturl())
                new_board_image = BoardImage(
                    boardID=new_board.ID,
                    imageNumber=i,
                    imageUrl=cdn.geturl()
                )
                save(new_board_image)

        if data['categoryIDs']:
            for i, category_id in enumerate(data['categoryIDs']):
                if category_id in [1, 2, 3, 4]:
                    board = Board.query.filter(Board.ID == new_board.ID).one()
                    board.majorCategoryID = category_id
                    save(board)
                else:
                    category_scope = CategoryScope(
                        categoryID=category_id,
                        type=1,
                        value=new_board.ID
                    )
                    save(category_scope)

        return new_board.ID

    except Exception as e:
        logging.error(str(e))
        db.session.rollback()
        return 0

    finally:
        db.session.close()


def get_all_boards(page=1, per_page=200):
    try:
        count = db.engine.execute(text(
            """
            SELECT COUNT(*) FROM Board
            """
        )).scalar()

        offset = (page - 1) * per_page

        query = db.engine.execute(text(
            """
            SELECT
                b.ID AS ID, 
                b.brandName AS brandName, 
                b.memberID AS memberID, 
                b.title AS title, 
                b.subTitle AS subTitle, 
                b.content AS content, 
                IFNULL((SELECT bi.imageUrl FROM BoardImage bi WHERE bi.boardID = b.ID AND bi.imageNumber = 0 LIMIT 1), null) AS imageUrl,
                IFNULL((SELECT c.name FROM Category AS c WHERE c.ID = b.majorCategoryID), null) AS majorCategoryName, 
                b.created AS created 
            FROM Board AS b 
            ORDER BY b.ID DESC
            LIMIT :per_page OFFSET :offset
            """), per_page=per_page, offset=offset
        )

        return {
            'items': query.all(),
            'page': page,
            'pages': (count // per_page) + (1 if (count / per_page) > 0 else 0),
            'per_page': per_page,
            'total': count
        }
    except Exception as e:
        logging.error(str(e))
    finally:
        db.session.close()


def get_by_board_id(notice_id) -> dict:
    try:
        board = Board.query.filter_by(ID=notice_id).first()

        board_images = db.engine.execute(text(
            """
            SELECT
                imageUrl AS imageUrl
            FROM BoardImage
            WHERE boardID = :board_id
            ORDER BY imageNumber ASC
            """), board_id=board.ID
        ).all()

        board.imageUrls = [bi[0] for bi in board_images]

        return board
    except Exception as e:
        logging.error(str(e))
    finally:
        db.session.close()


def get_by_member_id(member_id, page=1, per_page=20) -> Board:
    try:
        count = db.engine.execute(text(
            """
            SELECT COUNT(*) FROM Board WHERE memberID = :member_id
            """
        ), member_id=member_id).scalar()

        offset = (page - 1) * per_page

        boards = db.engine.execute(text(
            """
            SELECT
                b.ID AS ID, 
                b.brandName AS brandName, 
                b.memberID AS memberID, 
                b.title AS title, 
                b.subTitle AS subTitle, 
                b.content AS content, 
                IFNULL((SELECT bi.imageUrl FROM BoardImage bi WHERE bi.boardID = b.ID AND bi.imageNumber = 0 LIMIT 1), null) AS imageUrl,
                IFNULL((SELECT c.name FROM Category AS c WHERE c.ID = b.majorCategoryID), null) AS majorCategoryName, 
                b.created AS created 
            FROM Board AS b 
            WHERE b.memberID = :member_id
            ORDER BY b.ID DESC
            LIMIT :per_page OFFSET :offset
            """), member_id=member_id, offset=offset, per_page=per_page
        ).all()

        return {
            'items': boards,
            'page': page,
            'pages': (count // per_page) + (1 if (count / per_page) > 0 else 0),
            'per_page': per_page,
            'total': count
        }
    except Exception as e:
        logging.error(str(e))
    finally:
        db.session.close()


def get_by_brand_name(brand_name, page=1, per_page=20) -> Board:
    try:
        count = db.engine.execute(text(
            """
            SELECT COUNT(*) FROM Board WHERE brandName LIKE :brand_name
            """
        ), brand_name=f'%{brand_name}%').scalar()

        offset = (page - 1) * per_page

        boards = db.engine.execute(text(
            """
            SELECT
                b.ID AS ID, 
                b.brandName AS brandName, 
                b.memberID AS memberID, 
                b.title AS title, 
                b.subTitle AS subTitle, 
                b.content AS content, 
                IFNULL((SELECT bi.imageUrl FROM BoardImage bi WHERE bi.boardID = b.ID AND bi.imageNumber = 0 LIMIT 1), null) AS imageUrl,
                IFNULL((SELECT c.name FROM Category AS c WHERE c.ID = b.majorCategoryID), null) AS majorCategoryName, 
                b.created AS created 
            FROM Board AS b 
            WHERE b.brandName LIKE :brand_name
            ORDER BY b.ID DESC
            LIMIT :per_page OFFSET :offset
            """), brand_name=f'%{brand_name}%', offset=offset, per_page=per_page
        ).all()

        return {
            'items': boards,
            'page': page,
            'pages': (count // per_page) + (1 if (count / per_page) > 0 else 0),
            'per_page': per_page,
            'total': count
        }
    except Exception as e:
        logging.error(str(e))
    finally:
        db.session.close()


def save(data):
    db.session.add(data)
    db.session.commit()
