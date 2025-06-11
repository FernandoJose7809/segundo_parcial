from django.apps import AppConfig


class TeacherConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app.teacher'
    
    def ready(self):
        import app.teacher.signals
