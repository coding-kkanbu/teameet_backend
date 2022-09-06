from django.core.exceptions import ObjectDoesNotExist
from django.utils.encoding import smart_str
from django.utils.translation import gettext_lazy as _
from rest_framework.relations import RelatedField


class NameRelatedField(RelatedField):
    """
    A read-write field that represents the target of the relationship
    by a unique 'name' attribute.
    """

    default_error_messages = {
        "does_not_exist": _("{name}={value}인 category 객체가 존재하지 않습니다."),
        "invalid": _("유효하지 않은 값입니다."),
    }

    def __init__(self, name_field=None, **kwargs):
        assert name_field is not None, "The `name_field` argument is required."
        self.name_field = name_field
        super().__init__(**kwargs)

    def to_internal_value(self, data):
        queryset = self.get_queryset()
        try:
            return queryset.get(**{self.name_field: data})
        except ObjectDoesNotExist:
            self.fail("does_not_exist", name=self.name_field, value=smart_str(data))
        except (TypeError, ValueError):
            self.fail("invalid")

    def to_representation(self, obj):
        return getattr(obj, self.name_field)
