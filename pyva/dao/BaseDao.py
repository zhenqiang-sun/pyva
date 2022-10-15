from sqlalchemy.orm import Session


class BaseDao:
    """
    Base(基础)Dao，用于被继承.

    CRUD基础Dao类，拥有基本方法，可直接继承使用
    """

    db: Session = None

    def __init__(self, db: Session):
        self.db = db

    def insert(self, entity):
        """
        创建一条数据
        :param entity: 数据模型实例
        """
        self.db.add(entity)
        self.db.flush()

    def read(self, Entity, id: int):
        """
        读取一条数据
        :param Entity: 对象
        :param id: 数据id
        :return: 数据模型实例
        """

        return self.db.query(Entity).get(id)

    def update(self, entity):
        """
        更新一条数据
        :param entity: 数据模型实例
        :return:
        """
        self.db.add(entity)
        self.db.flush()

    def delete(self, entity):
        """
        删除一条数据
        :param entity: 数据模型实体
        """
        self.db.delete(entity)
        self.db.flush()
