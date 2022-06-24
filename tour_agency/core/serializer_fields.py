from rest_framework.fields import MultipleChoiceField


# human-readable choice array field
class ChoiceArrayField(MultipleChoiceField):
    def to_representation(self, value):
        return {self.choices.get(str(item), item) for item in value}
