from django.contrib.auth.models import Group, Permission
from django.core.management import BaseCommand
from users.groups import GROUPS


class Command(BaseCommand):
    args = "No args required"
    help = "Creates all pre-defined User groups"

    def handle(self, *args, **kwargs):
        for group_name in GROUPS.as_list():
            group, created = Group.objects.get_or_create(name=group_name)
            self.stdout.write(f"Group {group.name} {'created' if created else 'already exists'}")

            group_permissions = GROUPS.get_group_permission_codenames(group.name)
            group.permissions.set(Permission.objects.filter(codename__in=group_permissions))
            group.save()
            self.stdout.write(f"Added permissions to group {group.name}: {', '.join(group_permissions)}")
