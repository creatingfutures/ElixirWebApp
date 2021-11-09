from import_export import resources
from user_student.models import scores

class scoresResource(resources.ModelResource):
    class Meta:
        model = scores
        fields = ('student_id','batch_id','level_id','date_time','user_score','total_score','question_content_id','assessment_type_id')
        skip_unchanged = True