from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^$index', views.index, name='index'),
    url(r'^student/$', views.student_home, name='student_home'),
    # url(r'^set_user/$', views.set_user, name='set_user'),
    url(r'^my_applications/$', views.my_applications, name='my_applications'),
    url(r'^my_info/$', views.my_info, name='my_info'),
    url(r'^save_my_info/$', views.save_my_info, name='save_my_info'),



    url(r'^project_detail/(?P<proj_id>[0-9]+)/$', views.project_detail, name='project_detail'),
    url(r'^apply_for_project/(?P<proj_id>[0-9]+)/$', views.apply_for_project, name='apply_for_project'),
    url(r'^send_to_prof/(?P<app_id>[0-9]+)/$', views.send_to_prof, name='send_to_prof'),
    url(r'^update_sop/(?P<app_id>[0-9]+)/$', views.update_sop, name='update_sop'),
    url(r'^accept_project/(?P<app_id>[0-9]+)/$', views.accept_project, name='accept_project'),
    url(r'^reject_project/(?P<app_id>[0-9]+)/$', views.reject_project, name='reject_project'),
    url(r'^remove_application/(?P<app_id>[0-9]+)/$', views.remove_application, name='remove_application'),
    # url(r'^save_answers/(?P<proj_id>[0-9]+)/$', views.save_answers, name='save_answers'),


    url(r'^email_page/$', views.email_page, name='email_page'),
    url(r'^send_mail/$', views.send_mail_1, name='send_mail_1'),

    url(r'^professor/$', views.prof_home, name='prof_home'),
    url(r'^update_table/(?P<proj_id>[0-9]+)/$', views.update_table, name='update_table'),
    # url(r'^view_answers/(?P<appl_id>[0-9]+)/$', views.view_answers, name='view_answers'),


    url(r'^project_applications/(?P<proj_id>[0-9]+)/$', views.project_applications, name='project_applications'),
    url(r'^change_details/(?P<proj_id>[0-9]+)/$', views.change_details, name='change_details'),
    url(r'^new_project/$', views.new_project, name='new_project'),
    url(r'^save_new_project/$', views.save_new_project, name='save_new_project'),
    url(r'^update_project_details/(?P<proj_id>[0-9]+)/$', views.update_project_details, name='update_project_details'),
    url(r'^professor/my_info/$', views.prof_my_info, name='prof_my_info'),
    url(r'^save_prof_info/$', views.save_prof_info, name='save_prof_info'),
    url(r'^remove_project/(?P<proj_id>[0-9]+)/$', views.remove_project, name='remove_project'),
    url(r'^logout/$', views.logout, name='logout'),
    # url(r'^create_user/(?P<key>.+)/$', views.create_user, name='create_user'),

    url(r'^login/$', views.test_login, name='test_login'),
    url(r'^authorize/$', views.authorize, name='authorize'),

    url(r'^about/$', views.about_page, name='about_page'),

]


