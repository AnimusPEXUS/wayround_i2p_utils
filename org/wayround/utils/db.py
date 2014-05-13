
import sqlalchemy.orm


class BasicDBConfigError(Exception):
    pass


class BasicDB:

    """
    Main package index DB handling class
    """

    # NOTE: Example Table Class. Do not remove!
    #
    #    Base = sqlalchemy.ext.declarative.declarative_base()
    #
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

    def __init__(
        self, *args, echo=False, create_all=False, **kwargs
        ):

        self._db_engine = (
                sqlalchemy.create_engine(
                *args,
                echo=echo,
                **kwargs
                )
            )

        self.Base.metadata.bind = self._db_engine

        if create_all:
            self.Base.metadata.create_all()

        self.session = sqlalchemy.orm.Session(bind=self._db_engine)

        return

#    def __del__(self):
#        if self:
#            self.close()
#        return

    def create_all(self):
        self.Base.metadata.create_all()

    def commit(self):
        if self.session:
            self.session.commit()

        return

    def close(self):
        if self.session:
            self.session.commit()
            self.session.close()
            self.session = None

        return

    destroy = close
