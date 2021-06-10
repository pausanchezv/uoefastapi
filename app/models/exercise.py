
from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship, declared_attr, backref

from app.core.database import Base
from app.models import UseOfEnglishActivity


class UseOfEnglishExercise(Base):
    """
    Use of English Activity
    """
    __tablename__ = "uoe_exercise"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(256), nullable=False)
    discriminator = Column(String(50))

    activity_id = Column(Integer, ForeignKey('uoe_activity.id'), nullable=False)
    activity = relationship(UseOfEnglishActivity, back_populates="exercises")

    __mapper_args__ = {
        'polymorphic_identity': 'uoe_exercise',
        'polymorphic_on': discriminator
    }


class OpenSpaceSolution(Base):

    __tablename__ = 'uoe_open_space_solution'

    id = Column(Integer, primary_key=True, index=True)
    number = Column(Integer, nullable=False)
    text = Column(String(128), nullable=False)

    exercise_id = Column(Integer, ForeignKey('uoe_open_space.id'), nullable=False)
    exercise = relationship('OpenSpace', back_populates="solutions")


class OpenSpace(UseOfEnglishExercise):

    __tablename__ = "uoe_open_space"

    id = Column(Integer, ForeignKey('uoe_exercise.id'), primary_key=True)

    solutions = relationship("OpenSpaceSolution", back_populates="exercise", cascade="all, delete")



class OpenCloze(OpenSpace):  # OpenSpace

    __tablename__ = "uoe_open_cloze"

    id = Column(Integer, ForeignKey('uoe_open_space.id', name='fk_open_cloze_id'), primary_key=True)
    text = Column(Text, doc="Open cloze docs")

    __mapper_args__ = {
        'polymorphic_identity': 'uoe_open_cloze',
    }


class WordFormation(OpenSpace):

    __tablename__ = "uoe_word_formation"

    id = Column(Integer, ForeignKey('uoe_open_space.id', name='fk_word_formation_id'), primary_key=True)
    text = Column(Text, doc="Word formation docs")

    __mapper_args__ = {
        'polymorphic_identity': 'uoe_word_formation',
    }


class KeywordTransformation(UseOfEnglishExercise):

    __tablename__ = "uoe_kw_transformation"

    id = Column(Integer, ForeignKey('uoe_exercise.id'), primary_key=True)
    phrase = Column(Text, doc="kwt docs")

    __mapper_args__ = {
        'polymorphic_identity': 'uoe_kw_transformation',
    }


