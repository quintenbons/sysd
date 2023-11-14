broker_host = "localhost"
broker_port = 5672

celery_password = "celery_password"
celery_user = "celery_user"
celery_vhost = "celery_vhost"
celery_user_tag = "celery_tag"
celery_broker_url = f"amqp://{celery_user}:{celery_password}@{broker_host}:{broker_port}/{celery_vhost}"
celery_backend_url = "rpc://"

directory_password = "dir_password"
directory_user = "dir_user"
directory_vhost = "dir_vhost"
directory_user_tag = "dir_tag"
directory_broker_url = f"amqp://{directory_user}:{directory_password}@{broker_host}:{broker_port}/{directory_vhost}"
directory_backend_url = "rpc://"
