
#创建一个celery应用对象，通常一个项目值需要创建一个celery应用就行了

#参数1：自定义名字
import os

from celery import Celery

#指定django配置文件,zai manage里,把django环境里的包导入进来用
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "meiduo_mall.settings.dev")

celery_app = Celery('meiduo',broker='redis://127.0.0.1:6379/15',
                    # backend: 后台, 保存任务执行的返回值
                    backend='redis://127.0.0.1:6379/14'
                    )
# celery_app = Celery('meiduo')
# # 加载配置文件
#celery_app.config_object('celery_tasks.config')
# 扫描指定的包下面的任务函数
celery_app.autodiscover_tasks(['celery_tasks.sms','celery_tasks.email','celery_tasks.html'])