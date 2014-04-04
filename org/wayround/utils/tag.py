"""
Tag Utils
"""

import logging

import sqlalchemy.ext.declarative
import sqlalchemy.orm

import org.wayround.utils.terminal


class TagEngine:

    Base = sqlalchemy.ext.declarative.declarative_base()

    class Tag(Base):

        __tablename__ = 'tag'

        tid = sqlalchemy.Column(
            sqlalchemy.Integer,
            primary_key=True,
            autoincrement=True
            )

        obj = sqlalchemy.Column(
            sqlalchemy.UnicodeText,
            nullable=False,
            default='',
            index=True
            )

        tag = sqlalchemy.Column(
            sqlalchemy.UnicodeText,
            nullable=False,
            default='',
            index=True
            )

    def __init__(self, config_string, commit_every=1000):

        self._db_engine = (
                sqlalchemy.create_engine(
                config_string,
                echo=False
                )
            )

        self.Base.metadata.bind = self._db_engine

        self.Base.metadata.create_all()

        self.commit_every = commit_every
        self.commit_counter = 0

        try:
            self.session = sqlalchemy.orm.Session(bind=self._db_engine)
        except:
            self.session = None
            raise

        return

    def __del__(self):
        if self:
            self.close()
        return

    def close(self):
        if self.session:
            self.session.commit()
            self.session.close()
            self.session = None
        return

    def commit(self):
        self.session.commit()
        return

    def set_tags(self, obj, tags=[], nocommit=True):
        self.session.query(self.Tag).filter_by(obj=obj).delete()
        if not nocommit:
            self.session.commit()

        for i in tags:
            a = self.Tag()
            a.obj = obj
            a.tag = i
            self.session.add(a)

        self.commit_counter += 1

        if self.commit_counter >= self.commit_every:
            logging.debug("Committing")
            self.commit()
            self.commit_counter = 0

        if not nocommit:
            self.session.commit()

        return

    set_object_tags = set_tags

    def get_tags(self, obj):

        q = self.session.query(self.Tag).filter_by(obj=obj).all()

        ret = set()
        for i in q:
            ret.add(i.tag)

        return list(ret)

    get_object_tags = get_tags

    def get_objects(self, order=None):

        if not order in [None, 'tag', 'object']:
            raise ValueError("Wrong order selected")

        q = None
        if order == None:
            q = self.session.query(self.Tag).all()
        elif order == 'tag':
            q = self.session.query(self.Tag).order_by(self.Tag.tag).all()
        elif order == 'object':
            q = self.session.query(self.Tag).order_by(self.Tag.obj).all()

        ret = list()
        for i in q:
            ret.append(i.obj)

        return ret

    def get_objects_and_tags_dict(self):

        ret = dict()

        objs = self.get_objects(order='object')

        for i in objs:
            ret[i] = self.get_tags(i)

        return ret

    get_all_object = get_objects

    def get_all_tags(self):

        q = self.session.query(sqlalchemy.distinct(self.Tag.tag)).all()

        ret = []
        for i in q:
            ret.append(i[0])

        return ret

    def get_size(self):

        self.commit()
        ret = self.session.query(self.Tag).count()

        return ret

    def get_objects_by_tag(self, tag):
        return self.get_objects_by_tags([tag])

    def get_objects_by_tags(self, tags):

        ret = set()

        q = self.session.query(self.Tag).filter(self.Tag.tag.in_(tags)).all()

        for i in q:
            ret.add(i.obj)

        return list(ret)

    objects_by_tags = get_objects_by_tags

    def del_object_tags(self, obj, synchronize_session='evaluate'):

        if isinstance(obj, list):

            for i in range(int(len(obj) / 100) + 1):
                self.session.query(self.Tag).filter(
                        self.Tag.obj.in_(
                            obj[i * 100:(i + 1) * 100])
                            ).delete(
                                synchronize_session=synchronize_session
                                )

        else:
            self.session.query(self.Tag).filter_by(obj=obj).delete(
                synchronize_session=synchronize_session
                )

        return

    def del_objects_by_tags(self, tags):

        self.session.query(self.Tag).filter(self.Tag.tag.in_(tags)).delete()

        return

    def remove_duplicated_objects(self, mute=True):

        logging.info("Loading...")
        objs = self.get_objects(order='object')
        logging.info("Cleaning...")

        changed = False
        ii = 0
        ic = len(objs)
        removed = 0
        for i in objs[:]:

            if objs.count(i) > 1:

                changed = True

                while i in objs:
                    objs.remove(i)

                removed += \
                    self.sesessionss.query(self.Tag).filter_by(obj=i).count()

                self.session.query(self.Tag).filter_by(obj=i).delete()

            ii += 1

            if not mute:
                org.wayround.utils.terminal.progress_write(
                    "    {} of {} ({:.2f}%, deleted {})".format(
                        ii,
                        ic,
                        100 / (float(ic / ii)),
                        removed
                        )
                    )

        if not mute:
            org.wayround.utils.terminal.progress_write_finish()

        if changed:
            self.session.commit()

        return

    def clear(self):

        self.session.query(self.Tag).delete()
        self.session.commit()

        return
