"""
Django settings for meiduo_mall project.

Generated by 'django-admin startproject' using Django 1.11.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""
#测试环境使用的配置文件
import datetime
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'xy97an=yzv@3a8@923%+hyr!ym2e*wh905^4^k8ux8!l_mw2%4'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


# 指定可以通过哪些主机(ip,域名)访问后台服务器(django应用，django视图)
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'api.meiduo.site','www.meiduo.site']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 第三包注册
    'rest_framework',        # 注册drf应用
    'corsheaders',           # 解决跨域问题的第三方包
    'ckeditor',              # 富文本编辑器
    'ckeditor_uploader',     # 富文本编辑器上传图片模块'
    'django_crontab',        # 定时任务(定时更新静态的首页: index.html)
    'django_filters',        # 商品列表过滤
    'haystack',              # 商品搜索，第三方包全文检索框架，简化开发


    # 'meiduo_mall.apps.users.apps.UsersConfig',          # 用户模块
    # 'meiduo_mall.apps.ouath.apps.OuathConfig',          # 用户模块
    # 'ouath.apps.OuathConfig',                             # 用户模块
    'users',                             # 用户模块
    'ouath',                             #qq登陆模块
    'areas',                              #省市区模块
    'goods',                              #商品模块
    'contents',                           #广告模块
    'carts',                              #购物车模块
    'orders',                              #订单模块
]
# FastDFS服务器图片地址
FDFS_URL = 'http://image.meiduo.site:8888/'

# 上传图片保存的路径，使用了FastDFS后，此路径用不到
CKEDITOR_UPLOAD_PATH = 'uploads/'

# 富文本编辑器配置: 富文本编辑器ckeditor配置
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',  # 工具条功能
        'height': 300,  # 编辑器高度
        # 'width': 300,    	# 编辑器宽
    },
}

MIDDLEWARE = [

    'corsheaders.middleware.CorsMiddleware',     # 解决跨域问题的第三方包


    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'meiduo_mall.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        #模板文件所在目录
        # /home/python/code/gz07/meiduo/meiduo_mall/meiduo_mall/settings/dev.py
        # /home/python/code/gz07/meiduo/meiduo_mall/meiduo_mall/settings
        # /home/python/code/gz07/meiduo/meiduo_mall/meiduo_mall
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'meiduo_mall.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '127.0.0.1',
        'PORT': 3306,
        'USER': 'meiduo',
        'PASSWORD': 'meiduo',
        'NAME': 'meiduo_mall'
    }
}
# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'


USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

# 指定静态文件保存在哪个目录下
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static_files'),
]




# 配置使用Redis数据库
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "session": {  # 保存session数据到redis中
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    # 保存短信验证码
    "sms_codes": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    # 保存商品浏览历史记录
    "history": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/3",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },  # 保存购物车商品
    "carts": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/4",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
}

# 保存 session数据到 Redis中，主要给django的admin后台使用
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "session"

# 日志文件配置
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,  # 是否禁用已经存在的日志器
    'formatters': {  					# 日志信息显示的格式
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(lineno)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(module)s %(lineno)d %(message)s'
        },
    },
    'filters': {
        'require_debug_true': {  	# django在debug模式下才输出日志
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {  		# 日志处理方法
        'console': {  	# 向终端中输出日志
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': { 		 # 向文件中输出日志
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            # 日志文件的位置
            'filename': os.path.join(os.path.dirname(BASE_DIR), "logs/meiduo.log"),
            'maxBytes': 300 * 1024 * 1024,      # 日志文件的最大容量
            'backupCount': 10,                  # 300M * 10
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {  	# 定义了一个名为django的日志器
            'handlers': ['console', 'file'],  	# 可以同时向终端与文件中输出日志
            'level': 'INFO',  					# 日志器接收的最低日志级别
        },
    }
}

# 建议：项目开发完成再添加进来
# DRF相关配置
REST_FRAMEWORK = {
    # 异常配置
    # 'EXCEPTION_HANDLER': 'meiduo_mall.utils.exceptions.custom_exception_handler',
 # 配置项目支持的认证方式
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',  # jwt认证
        'rest_framework.authentication.SessionAuthentication',   # 管理后台使用
        'rest_framework.authentication.BasicAuthentication',
    ),
# 分页配置
    'DEFAULT_PAGINATION_CLASS': 'meiduo_mall.utils.paginations.MyPageNumberPagination',
}

# jwt认证配置
JWT_AUTH = {    # 导包： import datetime
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=1), # 开发阶段jwt有效时间设为1天

    # 修改登录成功接口返回的响应参数， 新增 user_id 和 username两个字段
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'users.utils.jwt_response_payload_handler',
}

# 指定可以跨域访问当前服务器(127.0.0.1:8000)的白名单
CORS_ORIGIN_WHITELIST = (
    '127.0.0.1:8080',
    'localhost:8080',
    'www.meiduo.site:8080',
    'api.meiduo.site:8000'
)
# 指定在跨域访问中，后台是否支持cookie操作
CORS_ALLOW_CREDENTIALS = True

# 在项目配置文件中，指定使用自定义的用户模型类
# AUTH_USER_MODEL = 'users.models.User'     # error
AUTH_USER_MODEL = 'users.User'              # ok


# 扩展登录接口: 使用自定义的认证后台, 使之支持可以使用用户名或手机号登录
AUTHENTICATION_BACKENDS = [
    'users.utils.UsernameMobileAuthBackend',
]




# 已经审核通过的应用参数， 配置到setting文件中
QQ_CLIENT_ID = '101474184'									# APP ID
QQ_CLIENT_SECRET = 'c6ce949e04e12ecc909ae6a8b09b637c'		# APP Key
QQ_REDIRECT_URI = 'http://www.meiduo.site:8080/oauth_callback.html' # 登录成功的回调地址


# 发送邮件的配置项
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.163.com'     # 指定邮箱服务器
EMAIL_PORT = 25                 # 默认端口
# 发送邮件的邮箱
EMAIL_HOST_USER = 'xujianjunyoho@163.com'    # 美多的官方邮箱
# 在邮箱中设置的客户端授权密码 （不是邮箱密码）
EMAIL_HOST_PASSWORD = 'python123456'
# 收件人看到的发件人
EMAIL_FROM = '美多官方邮箱<xujianjunyoho@163.com>'



# drf扩展: 缓存配置, 获取省份和区县接口使用到
REST_FRAMEWORK_EXTENSIONS = {
    # 缓存时间(1小时)
    'DEFAULT_CACHE_RESPONSE_TIMEOUT': 60 * 60,
    # 缓存到哪里 (caches中配置的default)
    'DEFAULT_USE_CACHE': 'default',
}


# 指定使用自定义的文件存储类(上传图片到FastDFS服务器)
DEFAULT_FILE_STORAGE = 'meiduo_mall.utils.fastdfs.storage.FdfsStorage'

# 生成的静态html文件保存的目录
GENERATED_STATIC_HTML_FILES_DIR = os.path.join(
    	os.path.dirname(os.path.dirname(BASE_DIR)), 'front_end_pc')


# 定时任务, 定时生成静态首页index.html
CRONJOBS = [
    # 参数1：定时时间设置，表示每隔3分钟执行一次
    # 参数2：要定义执行的函数，生成静态首页函数
    ('*/10 * * * *', 'contents.crons.generate_static_index_html',
        '>> /home/python/Desktop/meiduo/meiduo_mall/logs/crontab.log'),
]
#全文检索框架配置（商品检索时）
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        # 此处为elasticsearch运行的服务器ip地址，端口号默认为9200
        'URL': 'http://192.168.126.132:9200/',
        # 指定elasticsearch建立的索引库的名称
        'INDEX_NAME': 'meiduo',
    },
}
# 当添加、修改、删除数据时，自动更新索引
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

# 阿里支付相关参数 2016091200496790
ALIPAY_APPID = "2016092200570838"  # 需要修改成自己的沙箱应用的id(项目上线改成正式应用的id)
ALIPAY_URL = "https://openapi.alipaydev.com/gateway.do"  # 测试环境
# ALIPAY_URL = "https://openapi.alipay.com/gateway.do"     # 正式环境
ALIPAY_DEBUG = True