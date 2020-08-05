from dataclasses import dataclass

from sqlalchemy import Integer, String, Column, LargeBinary

from chromesy.dal.models.Base import Base


@dataclass
class Login(Base):
    __tablename__ = 'logins'
    origin_url = Column(String)
    action_url = Column(String)
    username_element = Column(String)
    password_element = Column(String)
    password_value = Column(LargeBinary)
    submit_element = Column(String)
    signon_realm = Column(String)
    preferred = Column(Integer)
    date_created = Column(Integer)
    blacklisted_by_user = Column(Integer)
    scheme = Column(Integer)
    password_type = Column(Integer)
    times_used = Column(Integer)
    form_data = Column(LargeBinary)
    date_synced = Column(Integer)
    display_name = Column(String)
    icon_url = Column(String)
    federation_url = Column(String)
    skip_zero_click = Column(Integer)
    generation_upload_status = Column(Integer)
    possible_username_pairs = Column(LargeBinary)
    id = Column(Integer, primary_key=True)
    date_last_used = Column(Integer)