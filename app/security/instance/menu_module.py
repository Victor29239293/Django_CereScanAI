from datetime import datetime
from django.contrib.auth.models import Group
from django.http import HttpRequest
from app.security.models import GroupModulePermission, User


class MenuModule:
    def __init__(self, request: HttpRequest):
        self._request = request
        self._path = self._request.path
        print(self._request)

    
    def fill(self, data):
        
        data['user'] = self._request.user
        data['date_time'] = datetime.now()
        data['date_date'] = datetime.now().date()

        if self._request.user.is_authenticated:
           
            data['group_list'] = self._request.user.groups.all().order_by('id')
            
            if 'group_id' not in self._request.session:
                
                if data['group_list'].exists():
                    self._request.session['group_id'] = data['group_list'].first().id
            
          
            group_id = self._request.GET.get('gpid', None)
            if group_id:
                self._request.session['group_id'] = group_id

         
            group_id = self._request.session.get('group_id')
            if group_id:
                group = Group.objects.get(id=group_id)

              
                data['group'] = {
                    'id': group.id,
                    'name': group.name,
                }

            
                data['menu_list'] = self.__get_menu_list(data['user'], group)


    def __get_menu_list(self, user: User, group: Group):
      
        group_module_permission_list = GroupModulePermission.get_group_module_permission_active_list(group.id).order_by('module__name')

      
        menu_unicos = group_module_permission_list.order_by('module__menu_id').distinct('module__menu_id')

     
        menu_list = [self._get_data_menu_list(x, group_module_permission_list) for x in menu_unicos]
        return menu_list

    
    def _get_data_menu_list(self, group_module_permission: GroupModulePermission, group_module_permission_list):
        group_module_permissions = group_module_permission_list.filter(module__menu_id=group_module_permission.module.menu_id)
        return {
            'menu': group_module_permission.module.menu,
            'group_module_permission_list': group_module_permissions,
        }
