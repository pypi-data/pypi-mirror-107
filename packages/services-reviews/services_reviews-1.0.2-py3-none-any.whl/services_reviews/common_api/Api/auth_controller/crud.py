from services_reviews.models import User, RevokedTokenModel
from services_reviews.common_api.Api import db
    

def save_to_db(new_user: User):
    """ сохраняем пользователя в базу если его еще там нет """
    if db.session.query(User).filter(User.username==new_user.username).first() is not None:
        return None
    else:
        db.session.add(new_user)
        db.session.commit()
        return 'ok'


def add_token_to_blacklist(jti: str):
    """ добавляем токен в блэклист """
    revoked_token = RevokedTokenModel(jti = jti)
    db.session.add(revoked_token)
    db.session.commit()


def is_jti_blacklisted(jti):
    """ проверяем есть ли токен в блэклист """
    query = db.session.query(RevokedTokenModel).filter_by(jti = jti).first()
    return bool(query)

