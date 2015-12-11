from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.conf import settings

from wpadmin.utils import get_admin_site_name
from wpadmin.menu import items
from wpadmin.menu.menus import Menu

class TopMenu(Menu):

    def init_with_context(self, context):

        admin_site_name = get_admin_site_name(context)

        self.children += [
            items.MenuItem(
                title='IEDCS Server',
                icon='fa-connectdevelop',
                css_styles='font-size: 1.5em;',
            ),
        ]


class LeftMenu(Menu):
    def init_with_context(self, context):

        admin_site_name = get_admin_site_name(context)
        user = context.get('request').user

        self.children += [
            items.MenuItem(
                title='Back to home',
                url='/admin',
                icon='fa-bullseye',
                css_styles='font-size: 1.2em;',
            ),

            items.MenuItem(
                    title=_('Users'),
                    url=reverse('admin:core_user_changelist'),
                    # enabled=user.has_perm('custom_users.change_customuser'),
                    icon='fa-users'
            ),
            items.MenuItem(
                    title=_('Players'),
                    url=reverse('admin:core_player_changelist'),
                    # enabled=user.has_perm('core.change_profile'),
                    icon='fa-play'
            ),

            items.MenuItem(
                    title=_('Devices'),
                    url=reverse('admin:core_device_changelist'),
                    # enabled=user.has_perm('core.change_attribute'),
                    icon='fa-laptop'
            ),

            items.MenuItem(
                    title=_('Content'),
                    url=reverse('admin:core_content_changelist'),
                    # enabled=user.has_perm('core.change_attribute'),
                    icon='fa-database'
            ),

            items.MenuItem(
                    title=_('Purchases'),
                    url=reverse('admin:core_purchase_changelist'),
                    # enabled=user.has_perm('core.change_attribute'),
                    icon='fa-shopping-cart'
            ),

        ]
