from sqlalchemy import ForeignKey, Column, Integer, String, inspect
from sqlalchemy.orm import relationship, backref

from database import Base, db_session


class GastonBase():

    @classmethod
    def find(cls, id):
        """Find the model by id"""
        # TODO: handle not found
        return cls.query.filter(cls.id == id).first()


    @classmethod
    def all(cls):
        """Return all instances of a model"""
        return cls.query.all()


    def destroy(self):
        """Delete the record"""
        db_session.delete(self)
        return db_session.commit()


    def save(self):
        """Persists the model to the database"""
        db_session.add(self)
        return db_session.commit()


    def persisted(self):
        return inspect(self).persistent


    def _set_attrs(self, attrs):
        """Set whitelisted fields from a dict"""
        #import pdb; pdb.set_trace()

        for field in self._fields:
            if field in attrs.keys():
                # NOTE: doing this explicitly in the constructor for now
                # If there is a custom setter, use it
                #if field in self._setters.keys():
                #    getattr(self.__class__, self._setters[field])(self, attrs[field])
                # Otherwise just set the field
                #else:
                setattr(self, field, attrs[field])
            else:
                # TODO: set to blank
                pass


class Ingredient(Base, GastonBase):
    """Ingredient model"""
    __tablename__ = 'ingredients'

    quantity = Column(Integer)
    unit = Column(String(50))
    name = Column(String)
    number = Column(Integer, primary_key=True)
    recipe_id = Column(Integer, ForeignKey('recipes.id'), primary_key=True)

    _fields = ['quantity', 'unit', 'name', 'number']
    _setters = {}


    def  __init__(self, attrs={}):
        self._set_attrs(attrs)


    def display(self):
        return '{} {} {}'.format(self.quantity, self.unit, self.name)


class Step(Base, GastonBase):
    """Step model"""
    __tablename__ = 'steps'

    number = Column(Integer, primary_key=True)
    description = Column(String)
    recipe_id = Column(Integer, ForeignKey('recipes.id'), primary_key=True)

    _fields = ['number', 'description']
    _setters = {}


    def __init__(self, attrs={}):
        self._set_attrs(attrs)


    def display(self):
        return '{} {}'.format(self.number, self.description)


class Recipe(Base, GastonBase):
    """Recipe model"""
    __tablename__ = 'recipes'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    ingredients = relationship('Ingredient',
                               order_by='asc(Ingredient.number)',
                               primaryjoin='Ingredient.recipe_id==Recipe.id',
                               cascade='all, delete, delete-orphan')
    steps       = relationship('Step',
                               order_by='asc(Step.number)',
                               primaryjoin='Step.recipe_id==Recipe.id',
                               cascade='all, delete, delete-orphan')

    _fields = ['name']
    #_setters = {'ingredients': '_set_ingredients'}


    def  __init__(self, attrs={}):
        if 'ingredients' in attrs.keys():
            self._set_ingredients(attrs.get('ingredients'))

        if 'steps' in attrs.keys():
            self._set_steps(attrs.get('steps'))

        self._set_attrs(attrs)


    # TODO: duplication
    def update(self, attrs={}):
        if 'ingredients' in attrs.keys():
            self._set_ingredients(attrs.get('ingredients'))

        if 'steps' in attrs.keys():
            self._set_steps(attrs.get('steps'))

        self._set_attrs(attrs)


    # TODO: meta this?
    def _set_ingredients(self, attrs):
        ingredients = []
        for ingredient_attrs in self.parse_ingredients(attrs):
            ingredients.append(Ingredient(ingredient_attrs))

        self.ingredients = ingredients


    # TODO: meta this?
    def _set_steps(self, attrs):
        steps = []
        for step_attrs in self.parse_steps(attrs):
            steps.append(Step(step_attrs))

        self.steps = steps


    @staticmethod
    def parse_ingredients(s):
        #if not isinstance(s, str):
        #    return s
        ingredients = []
        # TODO: this sucks, make it more elegant
        count = 1

        for line in s.split('\n'):
            parts = line.split()
            if len(parts) < 3: continue

            ingredients.append({
                'number'  : count,
                'quantity': parts[0],
                'unit'    : parts[1],
                'name'    : ' '.join(parts[2:]) })
            count += 1

        return ingredients


    @staticmethod
    def parse_steps(s):
        steps = []
        count = 1

        for line in s.split('\n'):
            steps.append({
                'number': count,
                'description': line })
            count += 1

        return steps

