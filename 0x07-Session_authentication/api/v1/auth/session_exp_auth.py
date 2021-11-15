#!/usr/bin/env python3
"""SessionExpAuth"""
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
from os import getenv


class SessionExpAuth(SessionAuth):
    """
    SessionExpAuth class
    """

    def __init__(self):
        """
        Constructor
        """
        try:
            self.session_duration = int(getenv('SESSION_DURATION', 0))
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """
        create_session
        """
        if user_id:
            session_id = super().create_session(user_id)
            if not session_id:
                return
            user_id = self.user_id_by_session_id.get(session_id)
            if not user_id:
                return
            session_dict = {'user_id': user_id, 'created_at': datetime.now()}
            self.user_id_by_session_id[session_id] = session_dict
            return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        user_id_for_session_id
        """
        if not session_id:
            return
        session_dict = self.user_id_by_session_id.get(session_id, None)
        if session_dict:
            user = session_dict.get('user_id', None)
            if user:
                se = self.session_duration
                if se <= 0:
                    return user
                created_at = session_dict.get('created_at', None)
                if not created_at:
                    return
                if datetime.now() > created_at + timedelta(seconds=se):
                    return
                return user
