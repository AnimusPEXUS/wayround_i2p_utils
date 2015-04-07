"""
Tag Utils
"""

import logging

import sqlalchemy.ext.declarative
import sqlalchemy.orm

import wayround_org.utils.terminal
import wayround_org.utils.db


class TagEngine(wayround_org.utils.db.BasicDB):

    def __init__(
            self,
            config_string=None,
            bind=None,
            decl_base=None,
            metadata=None,
            init_table_data='tag',
            commit_every=1000
            ):

        super().__init__(
            config_string=config_string,
            bind=bind,
            decl_base=decl_base,
            metadata=metadata,
            init_table_data=init_table_data
            )

        self.commit_every = commit_every
        self.commit_counter = 0

        # try:
        #     self.session = sqlalchemy.orm.Session(bind=self._db_engine)
        # except:
        #     self.session = None
        #     raise

        return
        
    def init_table_mappings(self, init_table_data):

        class Table(self.decl_base):

            __tablename__ = init_table_data

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

        self.table_cls = Table

        return

    def get_mapped_tag_table(self):
        ret = None
        if self.table_cls.__tablename__ in self.decl_base.metadata.tables:
            ret = self.decl_base.metadata.tables[self.table_cls.__tablename__]
        return ret

    def create_tables(self):
        self.decl_base.metadata.tables[self.get_mapped_tag_table()].create()
        return

    def set_tags(self, obj, tags=[]):

        session = sqlalchemy.orm.Session(self.decl_base.metadata.bind)

        session.query(self.table_cls).filter_by(obj=obj).delete()

        for i in tags:
            a = self.table_cls()
            a.obj = obj
            a.tag = i
            session.add(a)

        self.commit_counter += 1

        if self.commit_counter >= self.commit_every:
            logging.debug("Committing")
            session.commit()
            self.commit_counter = 0

        session.commit()
        session.close()

        return

    set_object_tags = set_tags

    def get_tags(self, obj):

        session = sqlalchemy.orm.Session(self.decl_base.metadata.bind)

        q = session.query(self.table_cls).filter_by(obj=obj).all()

        ret = set()
        for i in q:
            ret.add(i.tag)

        session.close()

        return list(ret)

    get_object_tags = get_tags

    def get_objects(self):

        session = sqlalchemy.orm.Session(self.decl_base.metadata.bind)

        q = session\
            .query(sqlalchemy.distinct(self.table_cls.obj))\
            .order_by(self.table_cls.obj)\
            .all()

        ret = list()

        for i in q:
            ret.append(i[0])

        session.close()

        return ret

    def get_objects_and_tags_dict(self):

        ret = dict()

        objs = self.get_objects()

        for i in objs:
            ret[i] = self.get_tags(i)

        return ret

    get_all_object = get_objects

    def get_all_tags(self):
        session = sqlalchemy.orm.Session(self.decl_base.metadata.bind)

        q = session.query(
            sqlalchemy.distinct(
                self.table_cls.tag
                )
            ).all()

        ret = []
        for i in q:
            ret.append(i[0])

        session.close()

        return ret

    def get_size(self):
        session = sqlalchemy.orm.Session(self.decl_base.metadata.bind)

        self.commit()

        ret = session.query(self.table_cls).count()

        session.close()

        return ret

    def get_objects_by_tag(self, tag):
        return self.get_objects_by_tags([tag])

    def get_objects_by_tags(self, tags):
        session = sqlalchemy.orm.Session(self.decl_base.metadata.bind)

        ret = set()

        q = session.query(self.table_cls)\
            .filter(self.table_cls.tag.in_(tags))\
            .all()

        for i in q:
            ret.add(i.obj)

        session.close()

        return list(ret)

    objects_by_tags = get_objects_by_tags

    def del_object_tags(self, obj, synchronize_session='evaluate'):

        session = sqlalchemy.orm.Session(self.decl_base.metadata.bind)

        if isinstance(obj, list):

            if len(obj) > 0:
                for i in range(int(len(obj) / 100) + 1):
                    session.query(self.table_cls)\
                        .filter(self.table_cls.obj.in_(
                            obj[i * 100:(i + 1) * 100]
                            )
                        )\
                        .delete(
                            synchronize_session=synchronize_session
                            )

        else:
            session.query(self.table_cls).filter_by(obj=obj).delete(
                synchronize_session=synchronize_session
                )

        session.close()

        return

    def del_objects_by_tags(self, tags):

        session = sqlalchemy.orm.Session(self.decl_base.metadata.bind)

        session.query(self.table_cls)\
            .filter(self.table_cls.tag.in_(tags))\
            .delete()

        session.close()

        return

    def remove_duplicated_objects(self, mute=True):

        session = sqlalchemy.orm.Session(self.decl_base.metadata.bind)

        logging.info("Loading...")
        objs = self.get_objects()
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
                    session.query(self.table_cls)\
                    .filter_by(obj=i)\
                    .count()

                session.query(self.table_cls)\
                    .filter_by(obj=i)\
                    .delete()

            ii += 1

            if not mute:
                wayround_org.utils.terminal.progress_write(
                    "    {} of {} ({:.2f}%, deleted {})".format(
                        ii,
                        ic,
                        100 / (float(ic / ii)),
                        removed
                        )
                    )

        if not mute:
            wayround_org.utils.terminal.progress_write_finish()

        if changed:
            session.commit()

        session.close()

        return

    def clear(self):
        self.get_mapped_tag_table().delete()
        return
