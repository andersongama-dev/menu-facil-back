from database.connection import SessionLocal
from models.ai import AIORM


def get_user_history(user_id, limit=10):
    session = SessionLocal()
    try:
        interactions = (
            session.query(AIORM)
            .filter(AIORM.id_user == user_id)
            .order_by(AIORM.created_at.desc())
            .limit(limit)
            .all()
        )
        history = [ia.parsed_intent for ia in interactions]
        return history
    finally:
        session.close()