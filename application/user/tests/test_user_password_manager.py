import unittest

from application.user.user_password_hasher import UserPasswordHasher


class TestUserPasswordManager(unittest.TestCase):
    def test_hash_and_verify(self):
        hashed_password = UserPasswordHasher.hash('1234')
        self.assertTrue(UserPasswordHasher.verify(hashed_password, '1234'))
        self.assertFalse(UserPasswordHasher.verify(hashed_password, 'wrong'))
