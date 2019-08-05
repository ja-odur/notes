
class ModelOperation:

    @classmethod
    def find_first(cls, keywords):
        return cls.objects.filter(**keywords).first()
