"""
Database models for university rankings
"""
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class University(Base):
    __tablename__ = 'universities'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    country = Column(String(100))

    # QS Ranking
    qs_rank = Column(Integer)
    qs_score = Column(Float)

    # THE Ranking
    the_rank = Column(Integer)
    the_score = Column(Float)

    # US News Ranking
    usnews_rank = Column(Integer)
    usnews_score = Column(Float)

    # ARWU (Shanghai Ranking/软科)
    arwu_rank = Column(Integer)
    arwu_score = Column(Float)

    # CS Rankings
    cs_rank = Column(Integer)
    cs_score = Column(Float)

    # Metadata
    last_updated = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'country': self.country,
            'rankings': {
                'qs': {'rank': self.qs_rank, 'score': self.qs_score},
                'the': {'rank': self.the_rank, 'score': self.the_score},
                'usnews': {'rank': self.usnews_rank, 'score': self.usnews_score},
                'arwu': {'rank': self.arwu_rank, 'score': self.arwu_score},
                'cs': {'rank': self.cs_rank, 'score': self.cs_score}
            },
            'last_updated': self.last_updated.isoformat() if self.last_updated else None
        }

class Database:
    def __init__(self, db_path='rankings.db'):
        self.engine = create_engine(f'sqlite:///{db_path}')
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def add_or_update_university(self, name, **kwargs):
        """Add or update a university record"""
        university = self.session.query(University).filter_by(name=name).first()

        if university:
            # Update existing record
            for key, value in kwargs.items():
                if hasattr(university, key):
                    setattr(university, key, value)
            university.last_updated = datetime.utcnow()
        else:
            # Create new record
            university = University(name=name, **kwargs)
            self.session.add(university)

        self.session.commit()
        return university

    def search_universities(self, query):
        """Search universities by name"""
        return self.session.query(University).filter(
            University.name.ilike(f'%{query}%')
        ).all()

    def get_all_universities(self):
        """Get all universities"""
        return self.session.query(University).all()

    def close(self):
        """Close database session"""
        self.session.close()
