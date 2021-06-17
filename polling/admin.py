from django.contrib import admin
from .models import Contact,Candidate,extenduser

admin.site.register(Contact)
# admin.site.register(Voter)
admin.site.register(Candidate)
admin.site.register(extenduser)


