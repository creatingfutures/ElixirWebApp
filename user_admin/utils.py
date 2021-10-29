from django.core.exceptions import PermissionDenied
from django.db import models
from django.http import HttpResponse
from user_student.models import scores
import csv


def download_csv(request, queryset):
  if not request.user.is_staff:
    raise PermissionDenied

  model = queryset.model
  model_fields = model._meta.fields + model._meta.many_to_many
  field_names = [field.name for field in model_fields]

  response = HttpResponse(content_type='text/csv')
  response['Content-Disposition'] = 'attachment; filename="export.csv"'

  # the csv writer
  writer = csv.writer(response, delimiter=";")
  # Write a first row with header information
  writer.writerow(field_names)
  # Write data rows
  for row in queryset:
      values = []
      for field in field_names:
          value = getattr(row, field)
          if callable(value):
              try:
                  value = value() or ''
              except:
                  value = 'Error retrieving value'
          if value is None:
              value = ''
          values.append(value)
      writer.writerow(values)
  return response



def save_new_scores_from_csv(file_path):
    # do try catch accordingly
    # open csv file, read lines
    from user_student.models import scores
    with open(file_path, 'r') as fp:
        csv_scores = csv.reader(fp, delimiter=',')
        row = 0
        for score in csv_scores:
            if row==0:
                headers = score
                row = row + 1
            else:
                # create a dictionary of score details
                new_score_details = {}
                for i in range(len(headers)):
                    new_score_details[headers[i]] = score[i]

                # create an instance of score model
                new_scores = scores()
                new_scores.__dict__.update(new_score_details)
                new_scores.save()
                row = row + 1
        fp.close()