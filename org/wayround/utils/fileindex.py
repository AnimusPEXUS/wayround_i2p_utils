
import os.path
import logging

import sqlalchemy
import sqlalchemy.orm
import sqlalchemy.ext.declarative


class FileIndexer:

    Base = sqlalchemy.ext.declarative.declarative_base()

    class File(Base):

        __tablename__ = 'file'

        name = sqlalchemy.Column(
            sqlalchemy.UnicodeText,
            nullable=False,
            primary_key=True,
            default=''
            )


    def __init__(
        self,
        config_string,
        add_commit_items_no=200,
        del_commit_items_no=200,
        ):

        self._db_engine = \
            sqlalchemy.create_engine(
            config_string,
            echo=False
            )

        self.Base.metadata.bind = self._db_engine

        self.Base.metadata.create_all()


        self.add_commit_items_no = add_commit_items_no
        self.add_commit_counter = 0

        self.del_commit_items_no = del_commit_items_no
        self.del_commit_counter = 0


        try:
            self.sess = sqlalchemy.orm.Session(bind=self._db_engine)
        except:
            self.sess = None
            raise

        self.added_count = 0
        self.exists_count = 0
        self.deleted_count = 0

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


    def is_name_exists(self, name):
        c = self.sess.query(self.File).filter_by(name=name).count()
        return c != 0


    def delete(self, name):
        self.sess.query(self.File).filter_by(name=name).delete()
        return

    def delete_missing(self, basedir):
        names = self.sess.query(self.File).all()

        logging.info("Searching for missing files")

        for i in names:
            full_name = os.path.abspath(basedir + os.path.sep + i.name)
            if not os.path.exists(full_name):

                logging.debug("`{}' not found -- deleting".format(full_name))

                self.sess.delete(i)

                self.del_commit_counter += 1
                self.deleted_count += 1

                if self.del_commit_counter >= self.del_commit_items_no:
                    self.sess.commit()
                    self.del_commit_counter = 0


    def add(self, name):

        if not self.is_name_exists(name):

            f = self.File()
            f.name = name

            self.sess.add(f)

            self.add_commit_counter += 1
            self.added_count += 1

            if self.add_commit_counter >= self.add_commit_items_no:
                self.sess.commit()
                self.add_commit_counter = 0

        else:
            self.exists_count += 1

        return

    def reset_counters(self):
        self.exists_count = 0
        self.added_count = 0

    def get_size(self):
        return self.sess.query(self.File).count()

    def get_files(self):
        q = self.sess.query(self.File).all()
        ret = []
        for i in q:
            ret.append(i.name)
        return ret