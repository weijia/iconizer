from iconizer.django_in_iconizer.django_starter import DjangoStarter
from iconizer.django_in_iconizer.postgresql_checker import PostgreSqlChecker


class DjangoPostgresqlStarter(DjangoStarter):
    django_main_script_name = "manage_with_conf.py"
    app_root_folder_name = "server_for_django_15_and_below"

    def get_cleanup_task_descriptors(self):
        return [{"stop_postgresql": ["scripts\\postgresql_stop.bat"]}]

    def get_frontend_task_descriptor(self):
        return {"postgresql": ["scripts\\postgresql.bat"]}

    def sync_to_main_thread(self):
        p = PostgreSqlChecker()
        p.wait_for_database_ready()
        if not p.is_django_table_created():
            # os.system("python manage_with_conf.py syncdb --noinput")
            self.init_ufs_db()
