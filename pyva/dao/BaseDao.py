from sqlalchemy.orm import Session

from pyva.Global import G


class BaseDao:
    """
    Base(基础)Dao，用于被继承.

    CRUD基础Dao类，拥有基本方法，可直接继承使用
    """

    # 数据库连接session
    db: Session = None
    # 实体对象
    Entity = None

    def __init__(self, db: Session = None):
        if db:
            self.db = db
        else:
            self.db = G.db

    def create(self, entity, commit: bool = True):
        """
        创建一条数据
        @param entity: 数据模型实例
        @param commit:
        """
        self.db.add(entity)

        if commit:
            self.db.commit()

        return entity.id

    def read(self, id: int | str):
        """
        读取一条数据
        :param id: 数据id
        :return: 数据模型实例
        """

        return self.db.query(self.Entity).get(id)

    def update(self, entity, commit: bool = True):
        """
        更新一条数据
        @param entity: 数据模型实例
        @param commit:
        :return:
        """

        self.db.add(entity)

        if commit:
            self.db.commit()

    def delete(self, entity, commit: bool = True):
        """
        删除一条数据
        @param entity: 数据模型实例
        @param commit:
        """
        self.db.delete(entity)

        if commit:
            self.db.commit()
