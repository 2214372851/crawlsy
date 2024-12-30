from django.core.management.base import BaseCommand
from apps.User.models import UserModel


class Command(BaseCommand):
    help = '创建管理员的账号'

    def add_arguments(self, parser):
        parser.add_argument('method', type=str, help='reload 重新设置密码 | create 创建账户')

    def handle(self, *args, **options):

        if options['method'] == 'create':
            UserModel.objects.create(
                username='管理员',
                password=UserModel.make_password('Admin@123'),
                email='admin@admin.com',
                is_root=True,
            ).save()
            self.stdout.write(self.style.ERROR('User: admin@admin.com | Password: Admin@123'))
        elif options['method'] == 'reload':
            user = UserModel.objects.filter(email='admin@admin.com')
            if user.exists():
                user.update(
                    password=UserModel.make_password('Admin@123')
                )
                self.stdout.write(self.style.ERROR('密码重置为：Admin@123'))

            else:
                self.stdout.write(self.style.ERROR('账户不存在'))

        else:
            self.stdout.write(self.style.ERROR('参数错误'))



