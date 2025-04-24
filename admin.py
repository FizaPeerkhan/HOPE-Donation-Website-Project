from django.contrib import admin
from .models import Donor_Registers
from .models import Ngo_Registers

class RegisterAdmin(admin.ModelAdmin):
    model = Donor_Registers
    # Display the fields in the order matching the form fields
    list_display = ('name', 'username',  'age', 'dob', 'contact', 'address', 'email','designation', 'pan')
    
    # Allow searching by these fields
    search_fields = ('name', 'username', 'age', 'dob', 'contact','address','email', 'designation', 'pan')
    
    # Display fields in the order they appear in the form
    fields = ('name', 'username', 'password', 'age', 'dob', 'contact', 'address', 'email', 'designation', 'pan')

admin.site.register(Donor_Registers, RegisterAdmin)


class NgoRegistersAdmin(admin.ModelAdmin):
    model = Ngo_Registers
    list_display = ('name', 'username', 'email', 'registration_date', 'certified_status', 'contact')
    search_fields = ('name', 'username', 'email', 'contact')
    list_filter = ('registration_date', 'certified_status')
    ordering = ('-registration_date',)
    fields = ('name', 'username', 'password', 'registration_date', 'certified_status', 'certificates', 'causes', 'address', 'contact', 'email', 'description', 'bank_details')

admin.site.register(Ngo_Registers, NgoRegistersAdmin)
