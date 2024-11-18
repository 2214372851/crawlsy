from django.core.management.base import BaseCommand
from django.core.management.utils import get_random_secret_key
from django.conf import settings


class Command(BaseCommand):
    help = 'NODE SERCRET KEY 管理'

    def add_arguments(self, parser):
        parser.add_argument('method', type=str, help='lookup 获取当前密钥 | create 生成一个密钥')

    def handle(self, *args, **options):

        if options['method'] == 'create':
            node_secret_key = get_random_secret_key()
            self.stdout.write(self.style.SUCCESS(f'节点密钥生成: {node_secret_key}'))
        elif options['method'] == 'lookup':
            node_secret_key = settings.SECRET_KEY
            if node_secret_key:
                self.stdout.write(self.style.SUCCESS(f'节点密钥: {node_secret_key}'))
        else:
            self.stdout.write(self.style.ERROR('参数错误'))