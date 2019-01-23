from django.conf.urls import url

from areas import views

urlpatterns = [
    # 获取所有的省份
    url(r'^areas/$',views.AreaProvinceView.as_view()),
    url(r'^areas/(?P<pk>\d+)/$',views.SubAreaView.as_view()),

]