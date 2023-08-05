class Null:
    """
    Null: attribute's value is None
    None: attribute's value is not set
    """
    pass


class Object:
    """
    attributes: defines the attributes of the Object as well as their default values
        Null: attribute's default value is None
        None: attribute does not have a default value

    protected_attributes: attributes that should not be included when calling Object.serialize()
        Can be included by passing in hide_protected_attributes=False
    """
    attributes = {}
    protected_attributes = []

    def __init__(self, attributes={}, load_default_values=False):
        # add all attributes to the object
        for key, value in self.attributes.items():
            if load_default_values:
                # load attributes with default values
                self.__dict__[key] = value
            else:
                # load attributes as not set
                self.__dict__[key] = None

        # load object with attributes received
        self.deserialize(attributes)

    def __getattribute__(self, key):
        value = super().__getattribute__(key)
        if value is Null:
            return None
        else:
            return value

    def __setattr__(self, key, value):
        if key not in self.attributes:
            raise AttributeError("'{}' object does not have '{}' to set".format(self.__class__.__name__, key))
        if value is None:
            self.__dict__[key] = Null
        else:
            self.__dict__[key] = value

    def copy(self):
        return self.__class__(self.serialize(hide_protected_attributes=False))

    def serialize(self, hide_protected_attributes=True):
        attributes = dict()
        for key, value in self.__dict__.items():
            if value is not None:
                if value is Null:
                    attributes[key] = None
                else:
                    attributes[key] = value
        if hide_protected_attributes:
            for key in self.protected_attributes:
                attributes.pop(key, None)

        return attributes

    def deserialize(self, attributes={}):
        for key, value in attributes.items():
            if value is None:
                self.__setattr__(key, self.attributes.get(key, None))
            else:
                self.__setattr__(key, value)

    @classmethod
    def bulk_serialize(cls, objects):
        dicts = []
        for obj in objects:
            dicts.append(obj.serialize())
        return dicts

    @classmethod
    def bulk_deserialize(cls, dicts):
        objects = []
        for dic in dicts:
            objects.append(cls(dic))
        return objects
