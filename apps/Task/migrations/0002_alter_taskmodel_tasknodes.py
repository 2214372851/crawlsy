# Generated by Django 4.2.1 on 2024-08-16 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Node', '0002_rename_node_uid_nodemodel_nodeuid_and_more'),
        ('Task', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskmodel',
            name='taskNodes',
            field=models.ManyToManyField(blank=True, null=True, to='Node.nodemodel', verbose_name='任务节点'),
        ),
    ]