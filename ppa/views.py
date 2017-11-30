from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import Student, Prof, Project, Application
import datetime
from datetime import date
from django.utils import timezone
from django.core.mail import send_mail

from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.sessions.backends.db import SessionStore
# from django import request
# import json
from ldap3 import Server, Connection, ALL

IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']
# index_url = 'http://138.197.90.80/ppa/login/'
# logout_url = 'http://138.197.90.80/ppa/logout/'

dept_to_short = {
	"CSE": "Computer Science and Engineering",
    "CIVIL": "Civil Engineering",
    "EE": "Electrical Engineering",
    "ESE": "Energy Science and Engineering",
    "AERO": "Aerospace Engineering",
    "CHE": "Chemical Engineering",
    "BioSchool": "Biosciences and Bioengineering",
    "CHEM": "Chemistry",
    # "Earth Sciences",
    "HSS": "Humanities and Social Science",
    "IDC": "Industrial Design Centre",
    "MATH": "Mathematics",
    "ME": "Mechanical Engineering",
    "MET": "Metallurgical Engineering and Materials Science",
    "PHY": "Engineering Physics",
    "GEOS": "Earth Sciences",
    "SOM": "Shailesh J. Mehta School of Management",
    "IEOR": "Industrial Engineering and Operations Research",
    #to be added: applied statistics, IEOR

}

index_url = '/ppa/login/'
logout_url = '/ppa/logout/'
session = None
def home(request):

    return render(request, 'ppa/home.html')

def logout(request):
    global session
    try:
        session = SessionStore(session_key=request.session['session_key'])
    except Exception as e:
        return redirect('/ppa/')

    session.delete()
    request.session.flush()
    return redirect(index_url)
    # url = 'https://gymkhana.iitb.ac.in/sso/oauth/revoke_token/'
    # headers = {
    #     "Host": "gymkhana.iitb.ac.in",
    #     "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
    # }
    # data = {
    #     "token": "access_token",
    #     "client_id": "O17EPBeU9l5NfOWUxq1IMc9fIKZrt4WUC4GE3xYL",
    #     "client_secret": "yRwP3qGb3Y2mn8kMglQ1ZrEN7GXqB39PalThpPD4SL4az8AuUapV3vSYn5I0wazJlLZFPKQGjBKt4sRQAWRcxpoEaM271kotCo7SnNwXSjWD2UP5iUj0yIjzAnB2sZRb"
    # }
    #
    # r = requests.post(url=url, headers=headers, data=data, verify=False)



def index(request):
    global session

    session = None
    try:
        session = SessionStore(session_key=request.session['session_key'])
    except Exception as e:
        return redirect(index_url)

    if(session.exists('user_type')):
        if(session['user_type'] == 'student'):
            return redirect('/ppa/student/')
        elif(session['user_type'] == 'professor'):
            return redirect('/ppa/professor/')
        else:
            session.delete()
            request.session.flush()
            return redirect(index_url)
    else:
        session.delete()
        request.session.flush()
        return redirect(index_url)



# @csrf_exempt
# def create_user(request, key):
#     global session

#     request.session['session_key'] = key
#     session = SessionStore(session_key=request.session['session_key'])

#     #print(str(session))

#     if(session.get('user_type')!=None):

#         #set user here
#         if(session.get('user_type') == 'student'):
#             if(len(Student.objects.filter(ldap_id=session.get('ldap_id'))) == 0):
#                 s = Student(name=session['name'],
#                     department=session['department'],
#                     ldap_id=session['ldap_id'])
#                 s.save()
#                 return redirect('/ppa/my_info/')
#             else:
#                 return redirect('/ppa/student/')
#         elif(session.get('user_type') == 'professor'):
#             if(len(Prof.objects.filter(ldap_id=session.get('ldap_id'))) == 0):
#                 p = Prof(name=session['name'],
#                     department=session['department'],
#                     ldap_id=session['ldap_id'])
#                 p.save()
#                 return redirect('/ppa/professor/my_info/')
#             else:
#                 return redirect('/ppa/professor/')
#         else:
#             return HttpResponse('Invalid access1')



#         # if(session.get('user_type') == 'professor'):
#         #     return redirect('/ppa/professor/')
#         # elif(session.get('user_type') == 'student'):
#         #     return redirect('/ppa/student/')
#         # else:
#         #     return redirect(index_url)

#     else:
#         return HttpResponse("Invalid access2")

# def pretty_print_POST(req):
#     """
#     At this point it is completely built and ready
#     to be fired; it is "prepared".

#     However pay attention at the formatting used in
#     this function because it is programmed to be pretty
#     printed and may differ from the actual request.
#     """
#     print('{}\n{}\n{}\n\n{}'.format(
#         '-----------START-----------',
#         req.method + ' ' + req.url,
#         '\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
#         req.body,
#     ))

def about_page(request):

    context = {}
    return render(request, 'ppa/base_about.html', context)


def authorize(request):

	global session
	context={'checked':True}
	if(session!=None and session.exists('user_type')):
		if(session['user_type']=='student'):
			return redirect('/ppa/student/')
		elif(session[('user_type')]=='professor'):
			return redirect('/ppa/professor/')

	if(request.method == 'POST'):

		user_type = None
		uname = request.POST.get('username')
		pwd = request.POST.get('password')

		# if(request.POST.get('student-login')!=None):
        #
		# 	user_type = "student"
        #
		# elif(request.POST.get('admin-login')!=None):
        #
		# 	user_type = "admin"

		s = Server('ldap://ldap.iitb.ac.in', get_info=ALL)
		c = Connection(s, auto_bind=True)

		a = c.search('dc=iitb,dc=ac,dc=in', '(uid='+uname+')', )

		if(a):

			b = str(c.entries[0])
			# print(b)
			# start = b.index('uid')
			# end = b.index('in')
			user_dn = c.response[0]['dn']

			#to get dept of user

			context={'checked':True}
			info = b.split(',')
			user_dept = dept_to_short[info[2][3:]]
			if(info[1][3:] == "FAC"):
			    user_type="professor"
			elif(info[1][3:] == "UG"):
			    user_type = "student"
			elif(info[1][3:] == "PG"):
			    user_type = "student"
			elif(info[1][3:] == "DD"):
			    user_type = "student"
			else :
			    return render(request,'ppa/base_login_page.html',context)

			 

			#ending to get dept of user

			c1 = Connection(s, user_dn, pwd)

			if(not c1.bind()):
				return redirect('/ppa/login/')

			else:
				redir_url = ""
				session = SessionStore()
				if(user_type=="student"):
					u = Student.objects.filter(ldap_id=uname).first()
					redir_url = "/ppa/student/"
					if(u is None):
						u = Student(ldap_id=uname, department=user_dept, name="", email=uname+"@iitb.ac.in")
						redir_url = "/ppa/my_info/"
						u.save()
    				# commented out the following to allow changing of ldap passwords
    				# u = authenticate(username=uname, password=pwd)
					if(u is not None):
						session['user_type']=user_type
						session['ldap_id']=uname
						session.save()
						request.session['session_key'] = session.session_key
						return redirect(redir_url)
					else:
						return redirect('/ppa/login/')
				elif(user_type=="professor"):
					u = Prof.objects.filter(ldap_id=uname).first()
					redir_url = "/ppa/professor/"
					if(u is None):
						u = Prof(ldap_id=uname, department=user_dept, name="", email=uname+"@iitb.ac.in")
						redir_url = "/ppa/professor/my_info/"
						u.save()
    				# commented out the following to allow changing of ldap passwords
    				# u = authenticate(username=uname, password=pwd)
					if(u is not None):
						session['user_type']=user_type
						session['ldap_id']=uname
						session.save()
						request.session['session_key'] = session.session_key
						return redirect(redir_url)
					else:
						render(request,'ppa/base_login_page.html',context)
				else:
					render(request,'ppa/base_login_page.html',context)
		else:
			return render(request,'ppa/base_login_page.html',context)

# if(request.GET.get('access_token')==None):
    #context = {}
    #     return render(request, 'ppa/base_redirect_page.html', context)
    # else:
    #     access_token = request.GET.get('access_token')
    #     token_type = request.GET.get('token_type')
    #     url = 'https://gymkhana.iitb.ac.in/sso/user/api/user/?fields=first_name,last_name,type,username,email,program,mobile,roll_number'
    #     headers = {
    #         "Host":'gymkhana.iitb.ac.in',
    #         "Authorization": "Bearer " +access_token
    #     }
    #
    #     r = requests.get(url=url, headers=headers, verify=False)
    #
    #     d = r.json()
    #
    #     s = SessionStore()
    #     s['ldap_id'] = d['username']
    #
    #     if(d['type'] == 'fac'):
    #         s['user_type'] = "professor"
    #     else:
    #         s['user_type'] = "student"
    #
    #     try:
    #         s['department'] = d['program']['department_name']
    #     except Exception as e:
    #         s['department'] = "Please enter department here"
    #
    #     s['name'] = d['first_name']+" "+d['last_name']
    #     s.create()
    #
    #     request.session['session_key'] = s.session_key;
    #
    #     if(s['user_type'] == "professor"):
    #         try:
    #             pr = Prof.objects.get(ldap_id=s['ldap_id'])
    #         except Prof.DoesNotExist:
    #             pr = Prof(name=s['name'], department=s['department'], ldap_id=s['ldap_id'])
    #             pr.email = pr.ldap_id+"@iitb.ac.in"
    #             pr.save()
    #             return redirect('/ppa/professor/my_info/')
    #
    #     else:
    #         try:
    #             stu = Student.objects.get(ldap_id=s['ldap_id'])
    #         except Student.DoesNotExist:
    #             stu = Student(name=s['name'], department=s['department'], ldap_id=s['ldap_id'])
    #             stu.save()
    #             return redirect('/ppa/my_info/')
    #
    #     return redirect('/ppa/')


# @csrf_exempt
# def set_user(request):
#     global session
#     #session = SessionStore(session_key=request.session['session_key'])

#     #debug
#     # #session['ldap_id']='140040009'
#     # #session['user_type'] = 'student'
#     #end debug

#     if request.method == "POST":

#         if('ldap_id' in request.POST):
#             s = SessionStore()
#             s['ldap_id'] = request.POST['ldap_id']
#             s['user_type'] = request.POST['user_type']
#             s['department'] = request.POST['department']
#             s['password'] = request.POST['password']
#             s['name'] = request.POST['name']
#             s.create()
#             print "created session var"
#             return HttpResponse(s.session_key)

#         else:
#             return redirect(index_url)

#     else:
#         return redirect(index_url)


def test_login(request):
    global session
    context = {}
    if(request.session.get('session_key')!=None):
     	context = {}
    return render(request, 'ppa/base_login_page.html', context)


def email_page(request):
    global session

    session = None
    try:
        session = SessionStore(session_key=request.session['session_key'])
    except Exception as e:
        return redirect(index_url)

    ldap_id = session.get('ldap_id')
    sent = request.GET.get('sent')

    if sent=='True':
        sent = True
    else:
        sent = False

    context = {'ldap_id':ldap_id, 'sent':sent}

    return render(request, 'ppa/base_email_page.html', context)

def send_mail_1(request):
    global session

    session = None
    try:
        session = SessionStore(session_key=request.session['session_key'])
    except Exception as e:
        return redirect(index_url)

    if(request.method == 'POST'):

        email_id = request.POST.get('email')
        sub = "PPA: "+request.POST.get('subject')
        mes = request.POST.get('message')

        # email = EmailMessage(sub, mes, to=["viraniaman@gmail.com"])
        # email.send()

        send_mail(sub, mes, email_id, ['priyanshukumar.0309@gmail.com'], fail_silently=False)
    else:
        return HttpResponse("Error sending email. Try again")

    return redirect('/ppa/email_page?sent=True')











# ======================== STUDENT SECTION STARTS HERE ====================================

def project_detail(request, proj_id):
    global session
    session = SessionStore(session_key=request.session['session_key'])


    #debug
    #session['ldap_id']='140040009'
    #session['user_type'] = 'student'
    #end debug

    if('ldap_id' not in session):
        return HttpResponse("Login first")
    if(session['user_type'] != 'student'):
        return HttpResponse("Only students can access this page.")

    proj = Project.objects.get(id=proj_id)
    stu = Student.objects.get(ldap_id=session['ldap_id'])

    all_projs = stu.application_set.all().exclude(status = 'Rejected')

    applied=False
    selected=False
    under_review=False
    rejected=False
    waitlisted=False
    student_waiting=False
    student_rejected=False
    student_accepted=False

    app = stu.application_set.filter(project=proj)

    appl = None

    if(len(app) == 1):

        applied = True
        appl = app[0]

        if(app[0].status == 'Selected'):
            selected = True
        elif(app[0].status == 'Under Review'):
            under_review = True
        elif(app[0].status == 'Rejected'):
            rejected = True
        elif(app[0].status == 'Waitlisted'):
            waitlisted = True

        if(appl.accept_status == "Student Waiting"):
            student_waiting = True
        elif(appl.accept_status == "Student Accepted"):
            student_accepted = True
        elif(appl.accept_status == "Student Rejected"):
            student_rejected = True

    elif(len(app) == 0):
        pass

    else:
        return HttpResponse("You have made some invalid changes. Please contact the academic council to rectify it "+str(len(app)))


    context = { 'project' : proj, 'num_projects':  (len(all_projs)>=5),
                'applied':applied, 'app':appl, 'selected':selected,
                'rejected':rejected, 'under_review':under_review,
                'student_waiting': student_waiting, 'student_accepted': student_accepted,
                'student_rejected':student_rejected, 'waitlisted': waitlisted }

    return render(request, 'ppa/base_proj_detail.html', context)

def apply_for_project(request, proj_id):
    global session
    session = SessionStore(session_key=request.session['session_key'])


    #debug
    #session['ldap_id']='140040009'
    #session['user_type'] = 'student'
    #end debug

    if('ldap_id' not in session):
        return HttpResponse("Login first")
    if(session['user_type'] != 'student'):
        return HttpResponse("Only students can access this page.")

    proj = Project.objects.get(id=proj_id)
    stu = Student.objects.get(ldap_id=session['ldap_id'])

    appl_list = proj.application_set.filter(student__ldap_id=session['ldap_id'])
    all_appls = stu.application_set.all().exclude(status="Rejected")
    # all_appls2 = all_appls.filter(accept_status="Student Accepted")

    # if(len(all_appls2)==1):
    #     url = '/ppa/project_detail/'+str(proj_id)+'/'
    #     return redirect(url)

    if(len(all_appls)>=5):
        return HttpResponse("You cannot apply for more than 5 projects")

    if(len(appl_list)!=0):
        return HttpResponse("You cannot apply for one project more than once")
    if(proj.deadline_passed()):
        return HttpResponse("The deadline for applications to this project has passed!")
    else:
        appl = Application(student=stu,
            project=proj,
            status='Under Review',
            accept_status="Student Waiting",
            message_from_prof=' ',
            message_to_prof=' ',
            accept_datetime = datetime.datetime.now())
        appl.save()
        url = '/ppa/project_detail/'
        url += str(appl.project.id)
        url += '/'
        return redirect(url)
        # return redirect('/ppa/my_applications/')

def my_applications(request):
    global session
    session = SessionStore(session_key=request.session['session_key'])


    #debug
    #session['ldap_id']='140040009'
    #session['user_type'] = 'student'
    #end debug

    if('ldap_id' not in session):
        return HttpResponse("Login first")
    if(session['user_type'] != 'student'):
        return HttpResponse("Only students can access this page")

    stu = Student.objects.get(ldap_id = session['ldap_id'])
    apps = Application.objects.filter(student__ldap_id = stu.ldap_id).exclude(accept_status = "Student Removed")

    context = {'apps':apps}

    return render(request, 'ppa/base_my_applications.html', context)

# def save_answers(request, proj_id):

#     #use post data to save answers

#     #debug
#     #session['ldap_id']='140040009'
#     #session['user_type'] = 'student'
#     #end debug

#     if('ldap_id' not in session):
#         return HttpResponse("Login first")
#     if(session['user_type'] != 'student'):
#         return HttpResponse("Only students can access this page.")

#     if request.method == "POST" :
#         for key, value in request.POST.iteritems():
#             s = str(key)
#             if(s.startswith('ans')):
#                 ans_id = int(s[3:])
#                 ans = Answer.objects.get(id=ans_id)
#                 ans.text = value
#                 ans.save()
#         return redirect('/ppa/project_detail/'+str(proj_id)+'/')

#     else:
#         return HttpResponse("There was an error saving answers. Please try again")


def send_to_prof(request, app_id):
    global session
    session = SessionStore(session_key=request.session['session_key'])

    #insert redirect to project page here

    #debug
    #session['ldap_id']='140040009'
    #session['user_type'] = 'student'
    #end debug

    if('ldap_id' not in session):
        return HttpResponse("Login first")
    if(session['user_type'] != 'student'):
        return HttpResponse("Only students can access this page.")

    if request.method == "POST":
        msg = request.POST.get('msg')
        if(msg is not None):
            appl = Application.objects.get(id=app_id)
            appl.message_to_prof = msg
            appl.save()
            url = '/ppa/project_detail/'
            url += str(appl.project.id)
            url += '/'
            return redirect(url)
        else:
            return HttpResponse("Some error in sending message to prof")

    return HttpResponse("Some error in sending data from form while sending message to prof")



def update_sop(request, app_id):
    global session
    session = SessionStore(session_key=request.session['session_key'])

    #insert redirect to project page here

    #debug
    #session['ldap_id']='140040009'
    #session['user_type'] = 'student'
    #end debug

    if('ldap_id' not in session):
        return HttpResponse("Login first")
    if(session['user_type'] != 'student'):
        return HttpResponse("Only students can access this page.")

    if request.method == "POST":
        msg = request.POST.get('sop')
        if(msg is not None):
            appl = Application.objects.get(id=app_id)
            appl.sop_answer = msg
            appl.save()
            url = '/ppa/project_detail/'
            url += str(appl.project.id)
            url += '/'
            return redirect(url)
        else:
            return HttpResponse("Some error in Updating SOP")

    return HttpResponse("Some error in sending data from form while Updating SOP ")

def accept_project(request, app_id):
    global session
    session = SessionStore(session_key=request.session['session_key'])

    #insert redirect to project page here
    #insert countdown here

    #debug
    #session['ldap_id']='140040009'
    #session['user_type'] = 'student'
    #end debug

    if('ldap_id' not in session):
        return HttpResponse("Login first")
    if(session['user_type'] != 'student'):
        return HttpResponse("Only students can access this page.")

    appl = Application.objects.get(id=app_id)

    if(appl.student.ldap_id != session['ldap_id'] or appl.status != "Selected"):
        return HttpResponse("Invalid access")

    appl.accept_status = "Student Accepted"
    appl.accept_datetime = datetime.datetime.now()
    appl.save()

    # other_appls = Application.objects.all().exclude(accept_status="Student Accepted")
    # other_appls = other_appls.exclude(accept_status="Student Rejected")

    # for appl1 in other_appls:
    #     appl1.accept_status = "Student Accepted Another Project"
    #     appl1.save()

    return redirect('/ppa/my_applications/')

def reject_project(request, app_id):
    global session
    session = SessionStore(session_key=request.session['session_key'])

    #insert redirect to project page here

     #debug
    #session['ldap_id']='140040009'
    #session['user_type'] = 'student'
    #end debug

    if('ldap_id' not in session):
        return HttpResponse("Login first")
    if(session['user_type'] != 'student'):
        return HttpResponse("Only students can access this page.")

    appl = Application.objects.get(id=app_id)

    if(appl.student.ldap_id != session['ldap_id'] or appl.status != "Selected"):
        return HttpResponse("Invalid access")

    appl.accept_status = "Student Rejected"

    #shift waitlist up by 1

    waitlisted_appls = appl.project.application_set.filter(status="Waitlisted")

    for appl1 in waitlisted_appls:
        appl1.waitlist_no = appl1.waitlist_no - 1
        if(appl1.waitlist_no == 0):
            appl1.status = "Selected"
        appl1.save()

    appl.save()

    return redirect('/ppa/my_applications/')


def remove_application(request, app_id):
    global session
    session = SessionStore(session_key=request.session['session_key'])

    #insert redirect to project page here

     #debug
    #session['ldap_id']='140040009'
    #session['user_type'] = 'student'
    #end debug

    if('ldap_id' not in session):
        return HttpResponse("Login first")
    if(session['user_type'] != 'student'):
        return HttpResponse("Only students can access this page.")

    appl = Application.objects.get(id=app_id)

    if(appl.student.ldap_id != session['ldap_id'] or appl.status != "Under Review" or appl.project.deadline_passed()):
        return HttpResponse("Invalid access")

    appl.delete()

    return redirect('/ppa/my_applications/')


def my_info(request):
    global session
    session = SessionStore(session_key=request.session['session_key'])

    #debug
    #session['ldap_id']='140040009'
    #session['user_type'] = 'student'
    #end debug

    if('ldap_id' not in session):
        return HttpResponse("Login first")
    if(session['user_type'] != 'student'):
        return HttpResponse("Only students can access this page.")

    stu = Student.objects.get(ldap_id=session['ldap_id'])
    updated=request.GET.get('updated')

    if(updated=='True'):
        updated=True
    else:
        updated=False

    context = {
            'updated':updated,
            'student': stu
        }

    return render(request, 'ppa/base_my_info.html', context)

def save_my_info(request):
 global session
 session = SessionStore(session_key=request.session['session_key'])

    #debug
    #session['ldap_id']='140040009'
    #session['user_type'] = 'student'
    #end debug

 if('ldap_id' not in session):
     return HttpResponse("Login first")
 if(session['user_type'] != 'student'):
     return HttpResponse("Only students can access this page.")

 stu = Student.objects.get(ldap_id=session['ldap_id'])

 if(request.method == "POST"):
     stu.name = request.POST.get('name')
     stu.email = request.POST.get('email')
     stu.yos = request.POST.get('yos')
     stu.cpi = request.POST.get('cpi')
     stu.ph_no = request.POST.get('ph_no')
     try:
         if (request.FILES['profile_dp'] is not None):
             stu.profile_dp.delete()
             stu.profile_dp = request.FILES['profile_dp']
             stu.save()
     except Exception as e:
         stu.save()
 return redirect('/ppa/my_info?updated=True')



def student_home(request):
    global session
    session = SessionStore(session_key=request.session['session_key'])

    #debug
    #session['ldap_id']='140040009'
    #session['user_type'] = 'student'
    #end debug

    if('ldap_id' not in session):
        return HttpResponse("Login first")
    if(session['user_type'] != 'student'):
        return HttpResponse("Only students can access this page.")

    projects = Project.objects.all()
    Date = date.today()
    context = {
            'projects': projects,
            'Date': Date
        }

    return render(request, 'ppa/base_test.html', context)











# ======================== PROF SECTION STARTS HERE ====================================

def prof_my_info(request):
    global session
    session = SessionStore(session_key=request.session['session_key'])

    #debug
    if (session['ldap_id']=='kumar_priyanshu'):
        session['user_type'] = 'professor'
    #end debug

    if('ldap_id' not in session):
        return HttpResponse("Login first")
    if(session['user_type'] != 'professor'):
        return HttpResponse("Only professors can access this page.")

    prof = Prof.objects.filter(ldap_id=session.get('ldap_id')).first()
    updated = request.GET.get('updated')
    if(updated=="True"):
        updated=True
    else:
        updated=False

    context = { 'prof':prof, 'updated':updated }

    return render(request, 'ppa/base_prof_info.html', context)


def prof_home(request):
    global session
    session = SessionStore(session_key=request.session['session_key'])

    #debug
    if (session['ldap_id']=='kumar_priyanshu'):
        session['user_type'] = 'professor'
    #end debug

    if('ldap_id' not in session):
        return HttpResponse("Login first")
    if(session['user_type'] != 'professor'):
        return HttpResponse("Only professors can access this page.")

    prof = Prof.objects.get(ldap_id=session['ldap_id'])
    my_projects = prof.project_set.all()
    context = {
            'my_projects': my_projects
        }

    return render(request, 'ppa/base_my_projects.html', context)

def project_applications(request, proj_id):
    global session
    session = SessionStore(session_key=request.session['session_key'])

    #debug
    if (session['ldap_id']=='kumar_priyanshu'):
        session['user_type'] = 'professor'
    #end debug

    if('ldap_id' not in session):
        return HttpResponse("Login first")
    if(session['user_type'] != 'professor'):
        return HttpResponse("Only professors can access this page.")

    proj = Project.objects.get(id=proj_id)

    if(proj.prof.ldap_id != session['ldap_id']):
        return HttpResponse("Invalid Access")

    appls = proj.application_set.all()
    updated = request.GET.get('updated')
    if(updated == "True"):
        updated = True
    else:
        updated = False

    context = { 'proj':proj, 'appls':appls, 'updated':updated }

    return render(request, 'ppa/base_project_applications.html', context)

def update_table(request, proj_id):
    global session
    session = SessionStore(session_key=request.session['session_key'])

    #debug
    if (session['ldap_id']=='kumar_priyanshu'):
        session['user_type'] = 'professor'
    #end debug

    if('ldap_id' not in session):
        return HttpResponse("Login first")
    if(session['user_type'] != 'professor'):
        return HttpResponse("Only professors can access this page.")

    proj = Project.objects.get(id=proj_id)

    if(proj.prof.ldap_id != session['ldap_id']):
        return HttpResponse("Invalid Access")

    if(request.method == "POST"):

        print (request.POST.get('update_btn'))
        print (request.POST.get('reject_btn'))

        for key, value in request.POST.items():

            if(request.POST.get('update_btn')!=None):
                if((key).startswith('status')):
                    appl_id = int(key[7:])
                    appl = Application.objects.get(id=appl_id)
                    x=str(appl.id)
                    message_from_prof = request.POST.get(''+ x + '')
                    appl.message_from_prof = message_from_prof
                    if( appl.status == "Waitlisted" and ( value == "Under Review" or value == "Selected" or value == "Rejected" ) ):

                        appls2 = Application.objects.all().exclude(waitlist_no=0)

                        # for appl3 in appls2:
                        #     if(appl3.waitlist_no > int(request.POST.get('waitlist_'+(str(appl_id))))):
                        #         appl3.waitlist_no = appl3.waitlist_no - 1
                        #         appl3.save()

                        appl.waitlist_no = 0

                    if( value == "Selected" ):

                        appl.accept_datetime = timezone.now()

                    if(value == "Rejected"):

                        appl.accept_status = "";

                    # if( appl.status == "Selected" and ( value == "Under Review" or value == "Waitlisted" or value == "Rejected" ) ):

                    #     stu = appl.student
                    #     for appl2 in stu.application_set.all():
                    #         if(appl2.accept_status == "Student Accepted Another Project"):
                    #             appl2.accept_status = "Student Waiting"
                    #             appl2.save()

                    appl.status = value
                    appl.save()
                if(key.startswith('waitlist')):
                    appl_id = int(key[9:])
                    val1 = request.POST.get('status_'+str(appl_id))
                    if(val1 == "Waitlisted"):
                        appl = Application.objects.get(id=appl_id)
                        appl.waitlist_no = int(value)
                        appl.save()

            elif(request.POST.get('reject_btn')!=None):
                if((key).startswith('status')):

                    appl_id = int(key[7:])
                    appl = Application.objects.get(id=appl_id)

                    if((appl.status!="Selected") and (appl.status!="Waitlisted")):
                        appl.status = "Rejected"
                        appl.waitlist_no = 0
                        appl.save()


            else:
                return HttpResponse("Some error occured in updating table!")

    return redirect('/ppa/project_applications/'+str(proj_id)+'/?updated=True')

# def view_answers(request, appl_id):

#     #debug
#     #session['ldap_id']='14007009'
#     #session['user_type'] = 'professor'
#     #end debug

#     if('ldap_id' not in session):
#         return HttpResponse("Login first")
#     if(session['user_type'] != 'professor'):
#         return HttpResponse("Only professors can access this page.")

#     appl = Application.objects.get(id=appl_id)

#     if(appl.project.prof.ldap_id != session['ldap_id']):
#         return HttpResponse("Invalid Access")

#     context = { 'name':appl.student.name, 'answers':appl.answer_set.all() }

#     return render(request, 'ppa/base_view_answers.html', context)



def change_details(request, proj_id):
    global session
    session = SessionStore(session_key=request.session['session_key'])

    #debug
    #session['ldap_id']='14007009'
    #session['user_type'] = 'professor'
    #end debug
    if (session['ldap_id']=='kumar_priyanshu'):
        session['user_type'] = 'professor'

    if('ldap_id' not in session):
        return HttpResponse("Login first")
    if(session['user_type'] != 'professor'):
        return HttpResponse("Only professors can access this page.")

    proj = Project.objects.get(id=proj_id)

    if(proj.prof.ldap_id != session['ldap_id']):
        return HttpResponse("Invalid Access")

    updated=request.GET.get('updated')

    if(updated=='True'):
        updated=True
    else:
        updated=False

    context = {'proj':proj, 'updated':updated}

    return render(request, 'ppa/base_update_project.html', context)

def new_project(request):
    global session
    session = SessionStore(session_key=request.session['session_key'])

    #debug
    #session['ldap_id']='14007009'
    #session['user_type'] = 'professor'
    #end debug
    if (session['ldap_id'] == 'kumar_priyanshu'):
        session['user_type'] = 'professor'
    if('ldap_id' not in session):
        return HttpResponse("Login first")
    if(session['user_type'] != 'professor'):
        return HttpResponse("Only professors can access this page.")

    context = {}

    return render(request, 'ppa/base_new_project.html', context)

def save_new_project(request):
    global session
    session = SessionStore(session_key=request.session['session_key'])

    #debug
    #session['ldap_id']='14007009'
    #session['user_type'] = 'professor'
    #end debug
    if (session['ldap_id'] == 'kumar_priyanshu'):
        session['user_type'] = 'professor'
    if('ldap_id' not in session):
        return HttpResponse("Login first")
    if(session['user_type'] != 'professor'):
        return HttpResponse("Only professors can access this page.")

    if(request.method == "POST"):
        professor = Prof.objects.get(ldap_id=session['ldap_id'])

        date = request.POST.get('application_deadline')
        date1 = datetime.datetime.strptime(date, "%Y-%m-%d")
        date2 = request.POST.get('expected_start_date')	
        date3 = datetime.datetime.strptime(date2, "%Y-%m-%d")

        proj = Project(name=request.POST.get('name'),
            description=request.POST.get('description'),
            requirements=request.POST.get('requirements'),
            additional_comments=request.POST.get('additional_comments'),
            num_positions=request.POST.get('num_positions'),
            duration=request.POST.get('duration'),
            sop_question=request.POST.get('sop'),
            prof=professor,
            application_deadline=date1,
            expected_start_date=date3
            )
        proj.save()

        # q1 = request.POST.get('q1')
        # q2 = request.POST.get('q2')
        # q3 = request.POST.get('q3')

        # ques1 = Question(project=proj, text=q1)
        # ques1.save()
        # ques2 = Question(project=proj, text=q2)
        # ques2.save()
        # ques3 = Question(project=proj, text=q3)
        # ques3.save()

    return redirect('/ppa/professor/')

def update_project_details(request, proj_id):
    global session
    session = SessionStore(session_key=request.session['session_key'])
    if (session['ldap_id'] == 'kumar_priyanshu'):
        session['user_type'] = 'professor'
    #debug
    #session['ldap_id']='14007009'
    #session['user_type'] = 'professor'
    #end debug

    if('ldap_id' not in session):
        return HttpResponse("Login first")
    if(session['user_type'] != 'professor'):
        return HttpResponse("Only professors can access this page.")

    proj = Project.objects.get(id=proj_id)

    if(proj.prof.ldap_id != session['ldap_id']):
        return HttpResponse("Invalid Access")

    if(request.method == "POST"):

        date = request.POST.get('application_deadline')
        date1 = datetime.datetime.strptime(date, "%Y-%m-%d")
        date2 = request.POST.get('expected_start_date')
        date3 = datetime.datetime.strptime(date2, "%Y-%m-%d")

        proj.name = request.POST.get('name')
        proj.description = request.POST.get('description')
        proj.requirements = request.POST.get('requirements')
        proj.additional_comments = request.POST.get('additional_comments')
        proj.application_deadline = date1
        proj.expected_start_date = date3
        proj.num_positions = request.POST.get('num_positions')
        proj.duration = request.POST.get('duration')
        proj.sop_question = request.POST.get('sop')

        proj.save()

        # q1 = request.POST.get('q1')
        # q2 = request.POST.get('q2')
        # q3 = request.POST.get('q3')

        # new_q_set = [q1, q2, q3]
        # old_q_set = proj.question_set.all()

        # qset = zip(new_q_set, old_q_set);

        # for new_q, old_q in qset:
        #     old_q.text = new_q
        #     old_q.save()

    return redirect('/ppa/change_details/'+ proj_id +'/?updated=True')

def save_prof_info(request):
 global session
 session = SessionStore(session_key=request.session['session_key'])

    #debug
 if (session['ldap_id']=='kumar_priyanshu'):
     session['user_type'] = 'professor'
    #end debug


 if('ldap_id' not in session):
	 return HttpResponse("Login first")
 if(session['user_type'] != 'professor'):
	 return HttpResponse("Only professors can access this page.")

 prof = Prof.objects.filter(ldap_id=session.get('ldap_id')).first()

 if (prof is None):
     prof1 = Prof(name=request.POST.get('name'),
                  email = request.POST.get('email'),
                  ldap_id = session.get('ldap_id'),
                  department = request.POST.get('department')
                  )
     prof1.save()

 else:
     if(request.method=='POST'):
          prof.name = request.POST.get('name')
          prof.email = request.POST.get('email')
          prof.department = request.POST.get('department')
          try:
              if (request.FILES['profile_dp'] is not None):
                  prof.profile_dp.delete()
                  prof.profile_dp = request.FILES['profile_dp']
                  prof.save()
          except Exception as e:
                  prof.save()


 return redirect('/ppa/professor/my_info/?updated=True')





def remove_project(request,proj_id):
    global session
    session = SessionStore(session_key=request.session['session_key'])

    if (session['ldap_id'] == 'kumar_priyanshu'):
        session['user_type'] = 'professor'

    if ('ldap_id' not in session):
        return HttpResponse("Login first")
    if (session['user_type'] != 'professor'):
        return HttpResponse("Only professors can access this page.")

    proj = Project.objects.get(id=proj_id)

    if (proj.prof.ldap_id != session['ldap_id']):
        return HttpResponse("Invalid Access")

    appls = proj.application_set.all()


    appls.delete()

    proj.delete()

    return redirect('/ppa/professor/')