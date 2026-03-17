from database.connection import SessionLocal
from models.user_preference import UserPreferenceORM


def get_user_preferences(user_id, limit=10):
    session = SessionLocal()
    try:
        preferences = (
            session.query(UserPreferenceORM)
            .filter(UserPreferenceORM.id_user == user_id)
            .order_by(UserPreferenceORM.confidence_score.desc())
            .limit(limit)
            .all()
        )
        result = [
            {
                "preference_type": pref.preference_type,
                "preference_value": pref.preference_value,
                "confidence_score": float(pref.confidence_score) if pref.confidence_score is not None else None
            }
            for pref in preferences
        ]
        return result
    finally:
        session.close()