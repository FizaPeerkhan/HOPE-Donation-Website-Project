from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from .models import Donor_Registers, Ngo_Registers
from django.contrib.auth.hashers import check_password

class CustomAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, user_type=None):
        if user_type == 'donor':
            try:
                # Find the donor by username
                donor = Donor_Registers.objects.get(username=username)
                # Check if the password matches
                if check_password(password, donor.password):
                    return donor
            except Donor_Registers.DoesNotExist:
                return None
        elif user_type == 'ngo':
            try:
                # Find the NGO by username
                ngo = Ngo_Registers.objects.get(username=username)
                # Check if the password matches
                if check_password(password, ngo.password):
                    return ngo
            except Ngo_Registers.DoesNotExist:
                return None
        return None

    def get_user(self, user_id):
        try:
            # Attempt to retrieve the user from both Donor_Registers and Ngo_Registers
            donor = Donor_Registers.objects.get(id=user_id)
            return donor
        except Donor_Registers.DoesNotExist:
            try:
                ngo = Ngo_Registers.objects.get(id=user_id)
                return ngo
            except Ngo_Registers.DoesNotExist:
                return None
