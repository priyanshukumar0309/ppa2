from django.db import models
from datetime import date
import datetime


class Prof(models.Model):
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=50)
    ldap_id = models.CharField(max_length=50)
    profile_dp = models.FileField(default=None)
    email = models.EmailField(max_length=100)

    def __str__(self):
        return self.name + " " + self.ldap_id


class Student(models.Model):
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=50)
    ldap_id = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, default='dummy@email.com')
    yos = models.CharField(max_length=100,default='0')
    cpi = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    profile_dp = models.FileField(default=None)
    ph_no = models.CharField(max_length=10, default="0000000000")

    def __str__(self):
        return self.name + " " + self.ldap_id


class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    additional_comments = models.CharField(max_length=1000)
    requirements = models.CharField(max_length=1000)
    num_positions = models.IntegerField(default=0)
    prof = models.ForeignKey(Prof, on_delete=models.CASCADE)
    application_deadline = models.DateField()
    expected_start_date = models.DateField(default=datetime.datetime.max)
    duration = models.IntegerField(default=0)
    sop_question = models.CharField(max_length=100, default='')

    def deadline_passed(self):
        if date.today() > self.application_deadline:
            return True
        return False

    def __str__(self):
        return self.name + " " + str(self.prof)


class Application(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, default="Under Review")
    message_from_prof = models.CharField(max_length=500)
    message_to_prof = models.CharField(max_length=500)
    accept_status = models.CharField(max_length=50, default="Student Waiting")
    accept_datetime = models.DateTimeField()
    waitlist_no = models.IntegerField(default=0)
    sop_answer = models.CharField(max_length=300, default=' ')

    def __str__(self):
        return str(self.student) + " " + str(self.project)

# class Question(models.Model):
#     project = models.ForeignKey(Project, on_delete=models.CASCADE)
#     text = models.CharField(max_length=200)

#     def __str__(self):
#         return str(self.text)

# class Answer(models.Model):
#     application = models.ForeignKey(Application, on_delete=models.CASCADE)
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     text = models.CharField(max_length=500)














