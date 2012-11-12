
import sqlalchemy.orm
import sqlalchemy.ext.declarative

class BasicDBConfigError(Exception): pass

class BasicDB:
    """
    Main package index DB handling class
    """

    Base = sqlalchemy.ext.declarative.declarative_base()

# Example Table Class. Do not remove!
#    class Info(Base):
#        """
#        Class for holding package information
#        """
#        __tablename__ = 'package_info'
#
#        name = sqlalchemy.Column(
#            sqlalchemy.UnicodeText,
#            nullable=False,
#            primary_key=True,
#            default=''
#            )
#
#        basename = sqlalchemy.Column(
#            sqlalchemy.UnicodeText,
#            nullable=False,
#            default=''
#            )
#
#        version_re = sqlalchemy.Column(
#            sqlalchemy.UnicodeText,
#            nullable=False,
#            default=''
#            )
#
#        home_page = sqlalchemy.Column(
#            sqlalchemy.UnicodeText,
#            nullable=False,
#            default=''
#            )
#
#        description = sqlalchemy.Column(
#            sqlalchemy.UnicodeText,
#            nullable=False,
#            default=''
#            )
#
#        buildscript = sqlalchemy.Column(
#            sqlalchemy.UnicodeText,
#            nullable=False,
#            default=''
#            )
#
#        installation_priority = sqlalchemy.Column(
#            sqlalchemy.Integer,
#            nullable=False,
#            default=5
#            )
#
#        removable = sqlalchemy.Column(
#            sqlalchemy.Boolean,
#            nullable=False,
#            default=True
#            )
#
#        reducible = sqlalchemy.Column(
#            sqlalchemy.Boolean,
#            nullable=False,
#            default=True
#            )
#
#        auto_newest_src = sqlalchemy.Column(
#            sqlalchemy.Boolean,
#            nullable=False,
#            default=True
#            )
#
#        auto_newest_pkg = sqlalchemy.Column(
#            sqlalchemy.Boolean,
#            nullable=False,
#            default=True
#            )

    def __init__(self, config, echo=False):

        self._db_engine = (
                sqlalchemy.create_engine(
                config,
                echo=echo
                )
            )

        self.Base.metadata.bind = self._db_engine

        self.Base.metadata.create_all()

        self.sess = sqlalchemy.orm.Session(bind=self._db_engine)

        return

    def __del__(self):
        if self:
            self.close()
        return

    def commit(self):
        if self.sess:
            self.sess.commit()

        return

    def close(self):
        if self.sess:
            self.sess.commit()
            self.sess.close()
            self.sess = None

        return
