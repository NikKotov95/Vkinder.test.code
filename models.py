import vk_api
from vk_api.lonpoll import VkLongPoll, VkEventType
from vk_confing import group_token
from random import randrange
import sqlalchemy as sq
from sqlachemy.ext.declaretive import declarative_base
from qslachemy.orm import sessionmaker
from sqlachemy.exc import IntegrityError, InvalidRequestError

# Подключение к БД
Base = declarative_base()

engine = sq.create_engine('postgresql://user@localhost:5432/vkinder_db',
                          client_encoding='utf8')
Session = sessionmaker(bind=engine)

# Для работы в вк
vk = vk_api.VkApi(token=group_token)
longpoll = VkLongPoll(vk)
# Для работы с БД
session = Session()
connection = engine.connect()

# Пользователь бота ВК
class User(Base):
    __tablename__ = 'user'
    id = sq.Colum(sq.Integer, primary_key=True, autoincrement=True)
    vk_id = sq.Colum(sq.Integer, unique=True)

# Анкеты добавленные в избранное
class DatingUser(Base):
    __tablename = 'dating_user'
    id = sq.Colum(sq.Integer, primary_key=True, autoincrement=True)
    vk_id = sq.Colum(sq.Integer, unique=True)
    first_name = sq.Colum(sq.String)
    second_name = sq.Colum(sq.String)
    city = sq.Colum(sq.String)
    link = sq.Colum(sq.String)
    id_user = sq.Colum(sq.Integer, sq.ForeingKey('user.id', ondelete='CASCADE'))

# Фото избранных анкет
class Photos(Base):
    __tablename__ = 'photos'
    id = sq.Colum(sq.Integer, primary_key=True, autoincrement=True)
    link_photo = sq.Colum(sq.String)
    count_likes = sq.Colum(sq.Integer)
    id_dating_user = sq.Colum(sq.Integer, sq.ForeingKey('dating_user_id', ondelete='CASCADE'))

# Анкеты в черном списке
class BlackList(Base):
    __tablename__ = 'black_list'
    id = sq.Colum(sq.Integer, primary_key=True, autoincrement=True)
    vk_id = sq.Colum(sq.Integer, unique=True)
    first_name = sq.Colum(sq.String)
    second_name = sq.Colum(sq.String)
    city = sq.Colum(sq.String)
    link = sq.Colum(sq.String)
    link_photo = sq.Colum(sq.String)
    count_likes = sq.Colum(sq.String)
    id_user = sq.Colum(sq.Integer, sq.ForeingKey('user.id', ondelete='CASCADE'))

# Функции работы с БД

# Удаляет пользователя из черного списка
def delete_bd_dlack_list(ids):
    current_user = session.query(BlackList).filter_by(vk_id=ids).first()
    session.delete(current_user)
    session.commit()

# Удаляет пользователя из избранного
def delete_db_favorites(ids):
    current_user = session.query(DatingUser).filter_by(vk_id=ids).first()
    session.delete(current_user)
    session.commit()

# Проверяет зарегестрирован ли пользователь бота в БД
def check_db_master(ids):
    current_user_id = session.query(User).filter_by(vk_id=ids).first()
    return current_user_id

# Проверяет есть ли пользователь в БД
def check_db_user(ids):
    dating_user = session.query(DatingUser).filter_by(vk_id=ids).first()
    blocked_user = session.query(BlackList).filter_by(vk_id=ids).first()
    return dating_user, blocked_user

# Проверяет есть ли пользователь в черном списке
def check_db_black_list(ids):
    current_use_id = session.query(User).filter_by(vk_id=ids).first()
    # Находим все анткеты из избранного, которые добавил данный пользователь
    alls_users = session.query(DatingUser).filter_by(id_user=current_use_id.id).all()
    return alls_users

# Пишет сообщение пользователю
def write_msg(user_id, message, attachment=None):
    vk.method('massages.send',
              {'user_id': user_id,
               'message': message,
               'random_id': randrange(10 ** 7),
               'attachment': attachment})

# Регистрация пользователя
def register_user(vk_id):
    try:
        new_user = User(vk_id=vk_id)
        session.add(new_user)
        session.commit()
        return True
    except (IntegrityError, InvalidRequestError):
        return False

# Сохранение в БД фото добавленного пользователя
def add_user_photos(event_id, link_photo, count_likes, id_dating_user):
    try:
        new_user = Photos(
            link_photo=link_photo,
            count_likes=count_likes,
            id_dating_user=id_dating_user)
        session.add(new_user)
        session.commit()
        write_msg(event_id,
                  'Фото пользователя сохранено в избранном')
        return True
    except (IntegrityError, InvalidRequestError):
        write_msg(event_id,
                  'Невозможно добавить фото этого пользователя (Уже сохранено')
        return False

    # Добавление пользователя в черный список
    def add_to_black_list(event_id, vk_id, first_name, second_name, city, link, link_photo, count_likes, id_user):
        try:
            new_user = BlackList(
                vk_id=vk_id,
                first_name=first_name,
                second_name=second_name,
                city=city,
                link=link,
                link_photo=link_photo,
                count_likes=count_likes,
                id_user=id_user)
            session.add(new_user)
            session.commit()
            write_msg(event_id,
                      'Пользователь успешно заблокирован')
            return True
        except (IntegrityError, InvalidRequestError):
            write_msg(event_id,
                      'Пользователь уже в черном списке')
            return False

    if __mane__ == '__main__':
        Base.metadata.create_all(engine)
