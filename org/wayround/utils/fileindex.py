
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


    def __init__(self, config_string):

        self._db_engine = \
            sqlalchemy.create_engine(
            config_string,
            echo=True
            )

        self.Base.metadata.bind = self._db_engine

        self.Base.metadata.create_all()

    def is_name_exists(self, name):

        sess = sqlalchemy.orm.Session(bind=self._db_engine)
        c = sess.query(self.File).filter_by(name=name).count()
        sess.close()

        return c != 0


    def delete(self, name):
        sess = sqlalchemy.orm.Session(bind=self._db_engine)
        sess.query(self.File).filter_by(name=name).delete()
        sess.commit()
        sess.close()

        return

    def add(self, name):

        f = self.File()
        f.name = name

        sess = sqlalchemy.orm.Session(bind=self._db_engine)

        sess.add(f)
        sess.commit()
        sess.close()
        return
