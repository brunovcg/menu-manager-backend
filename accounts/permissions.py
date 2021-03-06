from rest_framework.permissions import BasePermission

class IsSuperuser(BasePermission):
    def has_permission(self, request, view):  
  
        return (request.user.is_superuser == True)



class IsSuperuserAllowGetForAll(BasePermission):
    def has_permission(self, request, view):

      if request.method == 'GET': 
            return True
  
      return (request.user.is_superuser == True)

