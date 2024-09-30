from flask_mongoengine.db_fields import StringField


class ColorSelectField(StringField):
    """
    A field that stores a color. It is rendered as a color picker in the form.
    """

    def __init__(self, **kwargs):

        super().__init__(
            **kwargs,
            choices=[
                "Azure",
                "Blue",
                "Cyan",
                "Green",
                "Indigo",
                "Lime",
                "Orange",
                "Pink",
                "Purple",
                "Red",
                "Teal",
                "Yellow",
            ]
        )
