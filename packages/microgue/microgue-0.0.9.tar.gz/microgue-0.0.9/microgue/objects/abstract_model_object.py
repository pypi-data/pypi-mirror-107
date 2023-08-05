import uuid
from ..models.abstract_model import *
from .object import *


class RequiredAttributes(Exception):
    pass


class UniqueAttributes(Exception):
    pass


class AbstractModelObject(Object):
    """
    attributes: defined on Object
    protected_attributes: defined on Object

    required_attributes: attributes that must be include when creating a new object in the database

    unique_attributes: attributes that must be unique across all entries in the database

    _model: the instantiated model that AbstractModelObject will use to connect to the database
    """
    required_attributes = []
    unique_attributes = []
    _model = None

    def __init__(self, attributes_or_pk_value={}, sk_value=None, ):
        if type(attributes_or_pk_value) is dict:
            super().__init__(attributes_or_pk_value)
        elif type(attributes_or_pk_value) is str:
            super().__init__(self._model.get(attributes_or_pk_value, sk_value))

    def load_by_unique_attribute(self, attribute, value):
        unique_key = "{}#{}".format(attribute.upper(), value)
        reference = self._model.get(unique_key, '#UNIQUE')
        self.deserialize(self._model.get(reference.get('reference_pk'), reference.get('reference_sk')))

    def insert(self):
        # enforce required attributes
        missing_required_attributes = self._get_missing_required_attributes()
        if missing_required_attributes:
            raise RequiredAttributes('missing the following required attributes: ' + ', '.join(missing_required_attributes))

        # enforce unique attributes
        successful_unique_attributes = []

        pk = self._model.pk
        sk = self._model.sk
        pk_value = self.__dict__.get(pk)
        sk_value = self.__dict__.get(sk)

        # set the pk to a uuid value if one was not already set
        if not pk_value:
            self.__dict__[pk] = str(uuid.uuid4())
            pk_value = self.__dict__.get(pk)

        # attempt to write each unique attribute's value as an indepdendant entry in to the database
        for attribute in self.unique_attributes:
            # get the value of the unique attribute from the object
            attribute_value = self.__dict__.get(attribute)

            if attribute_value:
                # create a unique entry for each unique attribute on the object
                unique_entry = {}
                unique_entry[pk] = "{}#{}".format(attribute.upper(), attribute_value)
                unique_entry['reference_pk'] = pk_value
                if sk:
                    unique_entry[sk] = "#UNIQUE"
                    unique_entry['reference_sk'] = sk_value

                try:
                    # attempt to save the unique attribute to the table
                    self._model.insert(unique_entry)
                except ItemAlreadyExists:
                    # if the unique attribute already exists, delete the previously accepted unique attributes for this object
                    for successful_unique_attribute in successful_unique_attributes:
                        try:
                            self._model.delete("{}#{}".format(successful_unique_attribute.upper(), self.__dict__.get(successful_unique_attribute), "#UNIQUE"))
                        except:
                            pass
                    raise UniqueAttributes("{} already exists".format(attribute))
                successful_unique_attributes.append(attribute)

        self.deserialize(self._model.insert(self.serialize(hide_protected_attributes=False)))

    def update(self):
        # track unique attributes that were successfully added
        successful_unique_attributes = []

        pk = self._model.pk
        sk = self._model.sk
        pk_value = self.__dict__.get(pk)
        sk_value = self.__dict__.get(sk)

        # only pull the previous object if necessary of uniqueness
        object_previous_state = None

        # attempt to write each unique attribute's value as an indepdendant entry in to the database
        for attribute in self.unique_attributes:
            # check if the unique attribute is set
            attribute_value = self.__dict__.get(attribute)

            # pull the object before state before the update to be used to verify uniqueness
            if attribute_value and object_previous_state is None:
                object_previous_state = self._model.get(pk_value, sk_value)

            if attribute_value and attribute_value != object_previous_state.get(attribute):
                # create a unique entry that references the original object
                unique_entry = {}
                unique_entry[pk] = "{}#{}".format(attribute.upper(), attribute_value)
                unique_entry['reference_pk'] = pk_value
                if sk:
                    unique_entry[sk] = "#UNIQUE"
                    unique_entry['reference_sk'] = sk_value

                try:
                    # attempt to insert the unique attribute's value to the table
                    self._model.insert(unique_entry)
                except ItemAlreadyExists:
                    # if the unique attribute already exists, delete the previously accepted unique attributes for this object
                    for successful_unique_attribute in successful_unique_attributes:
                        try:
                            self._model.delete("{}#{}".format(successful_unique_attribute.upper(), self.__dict__.get(successful_unique_attribute), "#UNIQUE"))
                        except:
                            pass
                    raise UniqueAttributes("{} already exists".format(attribute))
                successful_unique_attributes.append(attribute)

        # remove previously used unique attribute values
        if object_previous_state:
            for successful_unique_attribute in successful_unique_attributes:
                try:
                    self._model.delete("{}#{}".format(successful_unique_attribute.upper(), object_previous_state.get(successful_unique_attribute), "#UNIQUE"))
                except:
                    pass

        self.deserialize(self._model.update(self.serialize(hide_protected_attributes=False)))

    def save(self):
        # get pk and sk
        pk = self.__dict__.get(self._model.pk)
        sk = self.__dict__.get(self._model.sk)

        # check if the record exists
        if pk:
            try:
                record_exists = bool(self._model.get(pk, sk))
            except:
                record_exists = False

        # call update or insert accordingly
        if pk and record_exists:
            self.update()
        else:
            self.insert()

    def delete(self):
        # get pk and sk
        pk = self.__dict__.get(self._model.pk)
        sk = self.__dict__.get(self._model.pk)

        try:
            return self._model.delete(pk, sk)
        except Exception as e:
            raise DeleteFailed(str(e))

    def _get_missing_required_attributes(self):
        missing_required_attributes = []
        for required_attribute in self.required_attributes:
            if self.__dict__.get(required_attribute) is None:
                missing_required_attributes.append(required_attribute)
        return missing_required_attributes
