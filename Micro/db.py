import os
import dj_database_url
DATABASE_URL = os.getenv('PROD_DATABASE_URL')


if DATABASE_URL :
    DATABASES = {
        "default":dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True
        )
        
    }