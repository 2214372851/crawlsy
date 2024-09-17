"""
任务调度器
    调度任务
        负载均衡器
        任务运行
        任务结束
        任务暂停
    任务监控
"""


# TODO: 任务调度器待实现

class TaskScheduler:

    def load_balancing(self):
        """
        获取到所有节点负载 取前 number_of_tasks 个节点作为任务调度节点
            number_of_tasks 任务数
        """
