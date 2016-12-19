import os
from django.core.urlresolvers import get_urlconf, set_urlconf, resolve, reverse #Gerencial qual é o URL conf padrão do Django
from django.conf.urls import url, include
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventex.settings')

#print('get_url_conf: ', get_urlconf()) #Ainda não foi carregado. (Django posterga ao máx as coisas - lazy).
#print('Meu ROOT_URLCONF é ' + settings.ROOT_URLCONF)

def index(request):
    pass

def auth(request):
    pass

def list_(request):
    pass

def edit(request):
    pass

def new(request):
    pass

def delete(request):
    pass

class LENDConf:

    def __init__(self, model):
        self.model = model

        self.urlpatterns = [
            url(r'^(\d+)/$', edit, name='edit'),
            url(r'^new/$', new, name='new'),
            url(r'^$', list_, name='list'),
            url(r'^delete/$', delete, name='delete'),
            ]

class MySiteUrlConf:


    urlpatterns = [
        url(r'^$', index, name='index'),
        url(r'^login/$', auth, kwargs={'action': 'login'}, name='login'), #name=Apelido da rota. Se mudar a callable, retorna o cara certo.
        url(r'^logout/$', auth, kwargs={'action': 'logout'}, name='logout'),
        url(r'^groups/', include(LENDConf('groups'), namespace='groups')),
        url(r'^users/', include(LENDConf('users'), namespace='users')),
        ]

set_urlconf(MySiteUrlConf)
#print('set_url_conf', MySiteUrlConf)

print('get_url_conf', get_urlconf() )
print()
print('index: /')
print('Resolve / :', resolve('/'))
print('Reverse: ', reverse('index'))
print('---------------------')
print()

print('auth /login')
print('Resolve: ', resolve('/login/')) #Quando rpecebe /, faz o match p/ o index.
print('Reverse: ', reverse('logout'))
print('---------------------')
print()

print('auth /logout')
print('Resolve: ', resolve('/logout/'))
print('Reverse: ', reverse('login'))
print('---------------------')
print()

print('list /groups/')
print('Resolve: ', resolve('/groups/'))
print('Reverse: ', reverse('groups:list'))
print('---------------------')
print()

print('new /groups/new')
print('Resolve: ', resolve('/groups/new/'))
print('Reverse: ', reverse('groups:new'))
print('---------------------')
print()

print('edit /groups/1/')
print('Resolve: ', resolve('/groups/1/'))
print('Reverse: ', reverse('groups:edit', args=[1]))
print('---------------------')
print()

print('delete /groups/delete/')
print('Resolve: ', resolve('/groups/delete/'))
print('Reverse: ', reverse('groups:delete'))
print('---------------------')
print()