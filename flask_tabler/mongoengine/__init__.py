from flask_mongoengine.wtf.orm import ModelConverter, converts
from wtforms import validators, fields


class TablerModelConverter(ModelConverter):

    def __init__(self, *kargs, **kwargs):
        super().__init__(*kargs, **kwargs)

    @converts("ColorSelectField")
    def conv_ColorSelectField(self, model, field, kwargs):
        if field.regex:
            kwargs["validators"].append(validators.Regexp(regex=field.regex))
        self._string_common(model, field, kwargs)
        return fields.StringField(**kwargs)
