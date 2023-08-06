from asynciorm.base.fields import (
    BaseIntegerField,
    BaseAutoIncrementField,
    BaseCharField,
    BaseTextField,
    BaseBooleanField,
    BaseDateTimeField,
    BaseDateField,
    BaseTimeField,
    BaseForeignKeyField,
    BaseFloatField,
)


class IntegerField(BaseIntegerField):
    pass


class AutoIncrementField(BaseAutoIncrementField):
    pass

    @property
    def _datatype(self):
        return ' SERIAL '


class FloatField(BaseFloatField):

    @property
    def _datatype(self):
        return ' DECIMAL '


class CharField(BaseCharField):
    pass


class TextField(BaseTextField):
    pass


class BooleanField(BaseBooleanField):

    @property
    def _datatype(self):
        return ' BOOLEAN '


class DateTimeField(BaseDateTimeField):

    @property
    def _datatype(self):
        return ' TIMESTAMP '


class TimeField(BaseTimeField):

    @property
    def _datatype(self):
        return ' TIMESTAMP '


class DateField(BaseDateField):

    @property
    def _datatype(self):
        return ' TIMESTAMP '


class ForeignKeyField(BaseForeignKeyField):

    @property
    def _datatype(self):
        return ' INTEGER '
