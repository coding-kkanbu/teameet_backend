from django.contrib import admin

from kkanbu.users.models import User

# from django.contrib.auth import admin as auth_admin
# from django.utils.translation import gettext_lazy as _
# from kkanbu.users.forms import UserChangeForm, UserCreationForm

admin.site.register(User)

# @admin.register(User)
# class UserAdmin(auth_admin.UserAdmin):

#     form = UserChangeForm
#     add_form = UserCreationForm
#     fieldsets = (
#         (None, {"fields": ("username", "password")}),
#         (_("Personal info"), {"fields": ("name", "email")}),
#         (
#             _("Permissions"),
#             {
#                 "fields": (
#                     "is_active",
#                     "is_staff",
#                     "is_superuser",
#                     "groups",
#                     "user_permissions",
#                 ),
#             },
#         ),
#         (_("Important dates"), {"fields": ("last_login", "date_joined")}),
#     )
#     list_display = ["username", "name", "is_superuser"]
#     search_fields = ["name"]
