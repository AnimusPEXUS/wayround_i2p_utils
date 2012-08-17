"""
Tag Utils
"""

import logging

import sqlalchemy
import sqlalchemy.orm
import sqlalchemy.ext.declarative


class TagEngine:

    Base = sqlalchemy.ext.declarative.declarative_base()

    class Tag(Base):

        __tablename__ = 'tag'

        tid = sqlalchemy.Column(
            sqlalchemy.Integer,
            primary_key=True,
            autoincrement=True
            )

        tag = sqlalchemy.Column(
            sqlalchemy.UnicodeText,
            nullable=False,
            default=''
            )

        obj = sqlalchemy.Column(
            sqlalchemy.UnicodeText,
            nullable=False,
            default=''
            )

    def __init__(self, config_string, commit_every=200):
        self._db_engine = \
            sqlalchemy.create_engine(
            config_string,
            echo=False
            )

        self.Base.metadata.bind = self._db_engine

        self.Base.metadata.create_all()

        self.commit_every = commit_every
        self.commit_counter = 0

        try:
            self.sess = sqlalchemy.orm.Session(bind=self._db_engine)
        except:
            self.sess = None
            raise

        return

    def __del__(self):
        self.close()
        return

    def close(self):
        if self.sess:
            self.sess.commit()
            self.sess.close()
            self.sess = None
        return

    def commit(self):
        self.sess.commit()
        return

    def set_tags(self, obj, tags=[]):
        #self.sess.query(self.Tag).filter_by(obj=obj).delete()
        self.sess.commit()

        for i in tags:
            a = self.Tag()
            a.obj = obj
            a.tag = i
            self.sess.add(a)

        self.commit_counter += 1

        if self.commit_counter >= self.commit_every:
            logging.debug("Committing")
            self.commit()
            self.commit_counter = 0

        #self.sess.commit()

        return

    def get_tags(self, obj):

        q = self.sess.query(self.Tag).filter_by(obj=obj).all()

        ret = set()
        for i in q:
            ret.add(i.tag)

        return list(ret)

    def objects_by_tags(self, tags):

        ret = set()

        for i in tags:
            q = self.sess.query(self.Tag).filter_by(tag=i).all()

            for y in q:
                ret.add(y.obj)

        return list(ret)

    def del_object_tags(self, obj):

        self.sess.query(self.Tag).filter_by(obj=obj).delete()
        #self.sess.commit()

        return

    def del_objects_by_tags(self, tags):

        for i in tags:
            self.sess.query(self.Tag).filter_by(tag=i).delete()

        #self.sess.commit()

        return

    def get_objects(self):

        q = self.sess.query(self.Tag).all()

        ret = set()
        for i in q:
            ret.add(i.obj)

        return list(ret)

    def clear(self):

        self.sess.query(self.Tag).delete()
        self.sess.commit()

        return

    def get_size(self):

        self.commit()
        lst = self.get_objects()
        return len(lst)
