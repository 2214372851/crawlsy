import json
import logging
from concurrent.futures import ThreadPoolExecutor

import redis
from celery import shared_task
from django.db.models import Q, Prefetch
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

from apps.Alerts.models import AlertRuleModel
from apps.Node.models import NodeModel
from apps.Task.models import TaskModel
from django.conf import settings
from utils.feishu import FeishuApi
from utils.node_api import NodeApi
from utils.node_stat import get_node_conn

logger = logging.getLogger('django')


@shared_task
def node_detection():
    """
    定时检测服务节点是否存活，存在数据库中状态为存活的当不存活时走webhook通知
    """
    conn = redis.StrictRedis.from_url(settings.NODE_SERVICE_URL)

    # 获取Redis中所有节点状态
    node_stats = []
    search_nodes = [key.decode('utf-8').replace('stat:', '') for key in conn.keys('stat:*')]
    for node_key in search_nodes:
        node_stats.append(json.loads(conn.get(f'stat:{node_key}')))

    # 优化查询：一次性查询出所有需要的节点及其关联的任务
    prefetch_user = Prefetch(
        'taskmodel_set',
        queryset=TaskModel.objects.filter(status=False).select_related('founder')
    )

    # 使用in条件代替exclude，避免数据库扫描
    nodes = NodeModel.objects.filter(status=True).exclude(nodeUid__in=search_nodes).prefetch_related(
        prefetch_user).all()

    # 创建Feishu API实例
    feishu_api = FeishuApi(settings.APP_ID, settings.APP_SECRET)

    # 记录哪些任务受影响的用户
    alert_users = {}
    node_name_map = {}
    for node in nodes:
        if node.nodeUid not in search_nodes and node.status:
            for task in node.taskmodel_set.all():
                feishu_id = task.founder.feishu_id
                if feishu_id not in alert_users:
                    alert_users[feishu_id] = {}
                alert_users[feishu_id][str(task.id)] = task.name
            node.status = False
            node.save()
            logger.info(f'节点 {node.name} 已离线')
        elif node.nodeUid in search_nodes and not node.status:
            node.status = True
            node.save()
            logger.info(f'节点 {node.name} 已上线')
        node_name_map[str(node.nodeUid)] = node.name

    # 发送通知给每个受影响的用户
    for feishu_id, tasks in alert_users.items():
        task_links = '\n- '.join(
            f'[{task_name}]({settings.FRONT_END_ADDRESS}task/details?id={task_id})' for task_id, task_name in tasks.items()
        )
        message = f"你的任务所在节点已经离线，受影响任务如下：\n- {task_links}"
        feishu_api.send_message(
            users_id=[feishu_id],
            msg=message,
            severity='critical',
            interval=60,
            callback_url=f'{settings.FRONT_END_ADDRESS}task',
            card_id=settings.CARD_ID,
            card_version=settings.CARD_VERSION
        )

    alert_rules = AlertRuleModel.objects.filter(status=True).filter(
        Q(target__isnull=False) | Q(feishuWebhook__isnull=False)).all()
    now = timezone.now()

    for rule in alert_rules:
        if rule.lastTriggerTime and (
                now - rule.lastTriggerTime.astimezone(timezone.utc)).total_seconds() < rule.interval:
            continue  # 如果间隔时间未到，跳过
        rule_msg = ['监控告警：']
        for node_stat in node_stats:
            num1 = node_stat.get(rule.mertric)
            if num1 is None:
                continue
            node_name = node_name_map[node_stat['node_uid']]
            num2 = rule.threshold
            if rule.condition == '>=' and num1 >= num2:
                rule_msg.append(
                    f'\n- {node_name} 节点触发阈值 {rule.mertric} [{num1} {rule.condition} {num2}] 当前值为: {num1}')
            elif rule.condition == '<=' and num1 <= num2:
                rule_msg.append(
                    f'\n- {node_name} 节点触发阈值 {rule.mertric} [{num1} {rule.condition} {num2}] 当前值为: {num1}')
            elif rule.condition == '>' and num1 > num2:
                rule_msg.append(
                    f'\n- {node_name} 节点触发阈值 {rule.mertric} [{num1} {rule.condition} {num2}] 当前值为: {num1}')
            elif rule.condition == '<' and num1 < num2:
                rule_msg.append(
                    f'\n- {node_name} 节点触发阈值 {rule.mertric} [{num1} {rule.condition} {num2}] 当前值为: {num1}')
            elif rule.condition == '=' and num1 == num2:
                rule_msg.append(
                    f'\n- {node_name} 节点触发阈值 {rule.mertric} [{num1} {rule.condition} {num2}] 当前值为: {num1}')
        if len(rule_msg) > 1:
            rule_users = [user.feishu_id for user in rule.target.all() if user.feishu_id]
            rule.lastTriggerTime = now
            rule.save()

            msg = '\n'.join(rule_msg)
            logger.info(msg)

            if rule_users:
                feishu_api.send_message(
                    users_id=rule_users,
                    msg=msg,
                    severity='warning',
                    interval=rule.interval,
                    callback_url=f'{settings.FRONT_END_ADDRESS}alert/details?id={rule.id}',
                    card_id=settings.CARD_ID,
                    card_version=settings.CARD_VERSION
                )
            if rule.feishuWebhook:
                feishu_api.send_webhook(
                    url=rule.feishuWebhook,
                    users_id=rule_users,
                    msg=msg,
                    severity='warning',
                    interval=rule.interval,
                    callback_url=f'{settings.FRONT_END_ADDRESS}alert/details?id={rule.id}',
                    card_id=settings.CARD_ID,
                    card_version=settings.CARD_VERSION
                )

    for node_stat in node_stats:
        node_uid = node_stat['node_uid']
        try:
            node = NodeModel.objects.get(nodeUid=node_uid)
            # 获取当前状态，检查是否需要更新
            current_status = node.status
            new_status = True

            if current_status != new_status:
                node.status = new_status  # 更新状态
                node.save()  # 保存到数据库
                logger.info(f'节点 {node.name} 状态已更新为: {new_status}')
        except ObjectDoesNotExist:
            logger.warning(f'节点 {node_uid} 不存在于数据库中')


@shared_task
def task_start(task_uid: str):
    task: TaskModel = TaskModel.objects.filter(taskUid=task_uid).first()
    feishu = FeishuApi(settings.APP_ID, settings.APP_SECRET)

    if not task:
        feishu.send_message(
            users_id=[task.founder.feishu_id],
            msg=f'任务 {task.name} 不存在，无法启动',
            severity='critical',
            interval=60,
            callback_url=settings.FRONT_END_ADDRESS,
            card_id=settings.CARD_ID,
            card_version=settings.CARD_VERSION
        )
        logger.warning(f'任务 {task_uid} 不存在')
        return
    if not task.isTiming: return
    nodes = task.taskNodes.all()
    if not nodes:
        feishu.send_message(
            users_id=[task.founder.feishu_id],
            msg=f'任务 {task.name} 无任务部署节点',
            severity='critical',
            interval=60,
            callback_url=f"{settings.FRONT_END_ADDRESS}/task/details?id={task.pk}",
            card_id=settings.CARD_ID,
            card_version=settings.CARD_VERSION
        )
        logger.warning(f'任务 {task_uid} 无任务部署节点')
        return
    conn = get_node_conn()
    command = task.taskSpider.command
    if not command:
        feishu.send_message(
            users_id=[task.founder.feishu_id],
            msg=f'任务 {task.name} 未配置启动命令',
            severity='critical',
            interval=60,
            callback_url=f"{settings.FRONT_END_ADDRESS}/task/details?id={task.pk}",
            card_id=settings.CARD_ID,
            card_version=settings.CARD_VERSION
        )
        logger.warning(f'任务 {task_uid} 未配置启动命令')
        return
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = {}
        for node in nodes:
            futures[node.nodeUid] = executor.submit(
                NodeApi().node_task_start, conn,
                node.nodeUid, task_uid, command
            )
        try:
            results = [i.result() for i in futures.values() if i.result()]
            for status, message, result in results:
                if not status:
                    feishu.send_message(
                        users_id=[task.founder.feishu_id],
                        msg=f'任务 {task.name} 启动失败\n错误信息如下\n{message}',
                        severity='critical',
                        interval=60,
                        callback_url=f"{settings.FRONT_END_ADDRESS}/task/details?id={task.pk}",
                        card_id=settings.CARD_ID,
                        card_version=settings.CARD_VERSION
                    )
                    logger.error(f'任务 {task.name} 启动失败\n错误信息如下\n{message}')
                    return
        except Exception as e:
            logger.error(e)
            feishu.send_message(
                users_id=[task.founder.feishu_id],
                msg=f'任务 {task.name} 启动失败\n错误信息如下\n{e}',
                severity='critical',
                interval=60,
                callback_url=f"{settings.FRONT_END_ADDRESS}/task/details?id={task.pk}",
                card_id=settings.CARD_ID,
                card_version=settings.CARD_VERSION
            )
            logger.error(f'任务 {task.name} 启动失败\n错误信息如下\n{e}', )
            return
