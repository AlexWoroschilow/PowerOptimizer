import inject


class Db(object): pass


class RedisDb(object):
    def __init__(self, data):
        pass

    def test(self):
        return "test"


inject.configure(lambda binder: binder.bind('database', RedisDb('localhost:1234')))

db = inject.get_injector().get_instance('database')
print(db.test())
