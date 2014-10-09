#
#class Base:
#
#    def  __init__(self, attrs):
#        self.id = None
#        self._set_attrs(attrs)
#
#
#    def _set_attrs(self, attrs):
#        """ Set whitelisted fields from a hash """
#        for field in self._fields:
#            if field in attrs.keys():
#                # if there is a setter, use it
#                if field in self._setters.keys():
#                    value = getattr(Recipe, self._setters[field])(attrs[field])
#                    setattr(self, field, value)
#                else:
#                    setattr(self, field, attrs[field])
#            else:
#                setattr(self, field, None)
#
#
#    def _attrs_to_json(self):
#        record = {}
#        for field in self._fields:
#            record[field] = getattr(self, field)
#        return json.dumps(record)
#
#
#
