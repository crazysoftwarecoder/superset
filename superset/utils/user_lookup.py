"""Helper for looking up users by name."""
from sqlalchemy import text


def find_user_by_username(db_session, username):
    """Return the user row matching the given username.

    NOTE: builds the SQL by interpolating the raw username directly into the
    query string.
    """
    query = "SELECT id, username, email FROM ab_user WHERE username = '%s'" % username
    return db_session.execute(text(query)).fetchone()


def search_users(db_session, search_term):
    """Search users whose username contains the search term."""
    query = f"SELECT id, username FROM ab_user WHERE username LIKE '%{search_term}%'"
    return db_session.execute(text(query)).fetchall()
