from django.contrib import admin
from eventex.core.models import Speaker, Contact, Talk, CourseOld


class ContactInline(admin.TabularInline):
    """Tabela para vários contatos."""
    model = Contact
    extra = 1

class SpeakerModelAdmin(admin.ModelAdmin):
    inlines = [ContactInline]
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name', 'photo_img', 'website_link', 'email', 'phone']


    def website_link(self, obj):
        """Creates a link for website field"""
        return '<a href="{0}">{0}</a>'.format(obj.website)

    website_link.allow_tags = True
    website_link.short_description = 'website'

    def photo_img(self, obj):
        """Creates a link for photo field."""
        return '<img width =32px src="{}" />'.format(obj.photo)

    def email(self, obj):
        """Returns first contact email."""
        #return Contact.objects.filter(kind=Contact.EMAIL, speakers=obj) - Se espalhar e mudar a estrutura
        #do modelo. O ideal é encapsular em um manager.

        return obj.emails.first()

    def phone(self, obj):
        """Return first contact phone."""
        return obj.phones.first()

    email.short_description = 'email'
    phone.short_description = 'phone'

    photo_img.allow_tags = True
    photo_img.short_description = 'foto'


admin.site.register(Speaker, SpeakerModelAdmin)
admin.site.register(Talk)
admin.site.register(CourseOld)