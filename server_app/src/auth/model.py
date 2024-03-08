from server_app.database.database import Base
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from datetime import datetime
from uuid import UUID, uuid4
from sqlalchemy import String, Integer, ForeignKey, PrimaryKeyConstraint, BigInteger, LargeBinary
from sqlalchemy.orm import Mapped, mapped_column


class department(Base):
    __tablename__ = 'department'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(length=1000))

    def __repr__(self):
        return f'{self.id} {self.name}'


class post(Base):
    __tablename__ = 'post'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(length=1000))

    def __repr__(self):
        return f'{self.id}, {self.name}'


class User(SQLAlchemyBaseUserTable, Base):
    """ username: ФИО сотрудника
        registered_at: время регистрации
        email: Почта сотрудника
        fk_department_id: ФК на департамент
        fk_post_id: ФК на должность
        hashed_password: Пароль
        is_active: работает ли человек по факту
    """
    __tablename__ = "user"
    __table_args__ = {'extend_existing': True}

    id: Mapped[UUID] = mapped_column(default=uuid4(), primary_key=True, index=True)
    username: Mapped[str] = mapped_column(nullable=False)
    registered_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    email: Mapped[str] = mapped_column(
        String(length=320),
        index=True,
        nullable=False,
    )
    fk_department_id: Mapped[int] = mapped_column(Integer, ForeignKey('department.id'))
    fk_post_id: Mapped[int] = mapped_column(Integer, ForeignKey('post.id'))
    hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(default=False, nullable=False)
    is_pregnant: Mapped[bool] = mapped_column(default=False, nullable=False)
    is_pregnant_replaced: Mapped[bool] = mapped_column(default=False, nullable=False)


class zamruk(Base):
    """
    fk_user_id: ссылка на замрука
    fk_dep_id: ссылка на департамент, к которому этот замрук приписан
    """
    __tablename__ = 'dep_kurators'
    __table_args__ = (
        PrimaryKeyConstraint('fk_user_id', 'fk_dep_id'),
    )

    fk_user_id: Mapped[UUID] = mapped_column(ForeignKey('user.id'))
    fk_dep_id: Mapped[int] = mapped_column(Integer, ForeignKey('department.id'))


class staff_positions(Base):
    __tablename__ = "staff_position"

    pk_fk_dep: Mapped[int] = mapped_column(Integer, ForeignKey(department.id), primary_key=True)
    pk_fk_post: Mapped[int] = mapped_column(Integer, ForeignKey(post.id), primary_key=True)
    count: Mapped[int] = mapped_column(Integer, nullable=False)


class risk(Base):
    __tablename__ = 'risk'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(length=1000))
    fk_dep: Mapped[int] = mapped_column(Integer, ForeignKey('department.id'))


class executor_group(Base):
    __tablename__ = 'executor_group'
    __table_args__ = (
        PrimaryKeyConstraint('fk_risk_id', 'fk_post_id'),
    )
    fk_risk_id: Mapped[int] = mapped_column(Integer, ForeignKey('risk.id'))
    fk_post_id: Mapped[int] = mapped_column(Integer, ForeignKey('post.id'))


class control_group(Base):
    __tablename__ = 'control_group'
    __table_args__ = (
        PrimaryKeyConstraint('fk_risk_id', 'fk_post_id'),
    )
    fk_risk_id: Mapped[int] = mapped_column(Integer, ForeignKey('risk.id'))
    fk_post_id: Mapped[int] = mapped_column(Integer, ForeignKey('post.id'))
