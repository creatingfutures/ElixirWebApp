from import_export import resources
from user_student.models import scores

class scoresResource(resources.ModelResource):
    class Meta:
        model = scores
        fields = ('id','student_id','batch_id','level_id','date_time','user_score','total_score','question_content_id','assessment_type_id','updated_date')
        skip_unchanged = False

