__author__ = 'olesya'

from DAL import *
import logging


class UserTreatment():
    def __init__(self):
        self.dal = DAL()

    def login(self, data):
        logging.info("Got login request")
        email = data["email"]
        password = data["password"]
        try:
            res = self.dal.check_user_passwd(email, password)
            logging.info("res " + str(res))
            if res:
                return 0, res
            else:
                return 3, "Wrong password"
        except UserNotExistException:
            return 2, "Error, user with this email does not exist"

    def register(self, data):
        logging.info("Got register request")
        logging.info(data)
        firstname = data["firstname"]
        lastname = data["lastname"]
        nickname = data["nickname"]
        password = data["password"]
        email = data["email"]
        try:
            self.dal.add_new_user(firstname, lastname, nickname, password, email, user_role="contributor")
            return 0, "User registered successfully"
        except UserExistException:
            return 1, "Error, user with this email is already exist"