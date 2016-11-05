import base64

from ..model.User import User



#-----  AWS ------#
from ..aws.DynamoDB import DynamoDB
from ..heroku import MemCachier


class UserController():

    fileSystem = None
#-----  AWS ------#
    dynamoDB = None
    elasticache = None

    def __init__(self):
    #-----  AWS ------#
        self.dynamoDB = DynamoDB()
        self.elasticache = MemCachier()

    def add_User(self, names, lastnames, email, password):
        user = User()
        user.set_variables_user(names, lastnames, email, password)
        data = self.dynamoDB.createUser(user)
        self.elasticache.set_variable(user.email, user.to_save())

        if data is None:
            return None
        else:
            data.email = None
            data.password = None
            return data

    def login_user(self, email, password):
        get_from_dynamo = False

        if self.elasticache.get_variable(email) is not None:
            print "Retrieving Logging from Elastic Cache"
            v_cache = self.elasticache.get_variable(email)
        else:
            print "Retrieving Logging from Dynamo"
            v_cache = self.dynamoDB.getUserByEmail(email)
            get_from_dynamo = True

        if v_cache is None:
            return None
        else:
            user = User()
            user.set_variables_db(v_cache)
            if get_from_dynamo is True:
                self.elasticache.set_variable(user.email, user.to_save())
            if user.password == base64.b64encode(password):
                return user
            else:
                return None

    def getUserFromDict(self, dictionary):
        user = User()
        user.set_variables_db(dictionary)
        return user

    def getUserContestNumber(self, user_id):
        return self.dynamoDB.getUserContestNumber(user_id)

    def getUserVideoNumber(self, user_id):
        return self.dynamoDB.getUserVideoNumber(user_id)

    def getUserId(self, user_id):
        data = self.dynamoDB.getUser(user_id)
        tmp_user = None
        if data is not None:
            tmp_user = User()
            tmp_user.set_variables_db(data)
        return tmp_user

    def getLatestUser(self):
        users = []
        for user in self.dynamoDB.getLatestUser():
            tmp_user = User()
            tmp_user.set_variables_db(user)
            users.append(tmp_user)
        return users

    def getUsers(self):
        users = []
        for user in self.dynamoDB.getUsers():
            tmp_user = User()
            tmp_user.set_variables_db(user)
            users.append(tmp_user)
        return users