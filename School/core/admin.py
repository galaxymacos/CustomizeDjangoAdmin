from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode

from core.models import Person, Course, Grade


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("last_name", "first_name", "show_average")
    search_fields = ("last_name__startswith", )  # Tuple
    fields = ("first_name", "last_name", "courses")

    def show_average(self, obj):  # for all people
        from django.db.models import Avg
        from django.utils.html import format_html

        grades = Grade.objects.filter(person=obj)   # get all grades of the current person
        print(type(grades))     # query set
        result = grades.aggregate(Avg("grade"))     # get aa dictionary of the aggregate
        return format_html("<b><i>{}</i></b>", result["grade__avg"])

    show_average.short_description = "Average"

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj=change, change=change, **kwargs)
        form.base_fields["first_name"].label = "First Name (Human only!)"
        return form

    class Meta:
        ordering = ("last_name", "first_name")


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("name", "year", "view_students_link")
    list_filter = ("year", )

    def view_students_link(self, obj):
        count = obj.person_set.count()
        url = (
            reverse("admin:core_person_changelist")  # admin page name convention: admin:%(app)s_%(model)s_%(page)
            + "?"
            + urlencode({"courses__id": f"{obj.id}"})
        )
        return format_html('<a href="{}">{} Students</a>', url, count)

    view_students_link.short_description = "Students"


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    pass

