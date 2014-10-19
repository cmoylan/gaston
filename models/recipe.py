import json

from database import get_db
# TODO: abstract db stuff

#recipes = get_db().collection('recipes')
#if not recipes.exists():
#    with db.transaction():
#        recipes.create()
#
def collection():
    return get_db().collection('recipes')


class Recipe:

    id = None
    _fields = ['name', 'ingredients', 'steps', '__id']
    _setters = {'ingredients': 'parse_ingredients',
                'steps': 'parse_steps'}


    def  __init__(self, attrs={}):
        self.id = None
        self._set_attrs(attrs)


    @classmethod
    def find(cls, id):
        recipe = collection().fetch(id)
        return cls(recipe)


    @classmethod
    def find_by_name(cls, name):
        #results = recipes.all() or []
        recipes = collection().filter(lambda obj: name in obj['name'])
        return [cls(recipe) for recipe in recipes]


    @classmethod
    def create(cls, attrs):
        with get_db().transaction():
            collection().store(attrs)
        return cls(attrs)


    @classmethod
    def all(cls):
        recipes = collection().all()
        return [cls(recipe) for recipe in recipes]


    @classmethod
    def delete(*ids):
        with get_db().transaction():
            for id in ids:
                collection().delete(id)


    def save(self):
        # return false if not valid
        # build a hash from the _fields
        attrs = self._get_attrs()
        with get_db().transaction():
            # send to database
            collection().store(attrs)

        if self.id is not None:
            # delete old record
            #collection().delete(self.id)
            pass

        self.id = handle.last_record_id()
            #print "id is {0}".format(self.__id)
        return True


    def update(self, attrs):
        # find, update
        self._set_attrs(attrs)
        self.save()


    def _set_attrs(self, attrs):
        """ Set whitelisted fields from a hash """
        self._set_id(attrs)

        for field in self._fields:
            if field in attrs.keys():
                # if there is a setter, use it
                if field in self._setters.keys():
                    value = getattr(Recipe, self._setters[field])(attrs[field])
                    setattr(self, field, value)
                else:
                    setattr(self, field, attrs[field])
            else:
                setattr(self, field, None)


    def _get_attrs(self):
        record = {}
        for field in self._fields:
            record[field] = getattr(self, field)
        return record


    def _attrs_to_json(self):
        return json.dumps(self._get_attrs())


    def _set_id(self, attrs):
        if '__id' in attrs.keys():
            self.id = attrs['__id']


    def print_ingredients(self):
        s = ''
        if not hasattr(self.ingredients, '__iter__'):
            return s

        for i in self.ingredients:
            s += '{0} {1} {2}\n'.format(i['quantity'], i['unit'], i['name'])
        return s


    def print_steps(self):
        s = ''
        if not hasattr(self.steps, '__iter__'):
            return s

        for step in self.steps:
            s += '{0}\n'.format(step['step'])
        return s


    @staticmethod
    def parse_ingredients(s):
        if not isinstance(s, str):
            return s

        ingredients = []

        for line in s.split('\n'):
            parts = line.split()
            if len(parts) < 3: continue

            ingredients.append({
                'quantity': parts[0],
                'unit'    : parts[1],
                'name'    : ' '.join(parts[2:]) })

        return ingredients


    @staticmethod
    def parse_steps(s):
        if not isinstance(s, str):
            return s

        steps = []

        for line in s.split('\n'):
            steps.append({'step': line})

        return steps
