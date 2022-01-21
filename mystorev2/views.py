from .models import Product, User, Warehouse
from .forms import RegistrationForm, GroupUpdateForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import(
    View,
    CreateView,
    UpdateView,
    ListView,
)
from django.contrib.messages.views import SuccessMessageMixin
# this will results in improper config
from django.contrib.auth.models import User, Permission, PermissionsMixin, PermissionManager, Group
from .models import User
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, models
from django.utils import timezone
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import AccessMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.contenttypes.models import ContentType


# Create your views here.

####################### DASHBOARD VIEWS ###########################

# Responsible for rendering the main application dashboard page
class Dashboard(ListView):
    model = Warehouse
    context_object_name = 'dashboard'
    template_name = 'dashboard.html'


####################### WAREHOUSE VIEWS ###########################

# Responsible for rendering the "create new warehouse" page
class WarehouseCreate(SuccessMessageMixin, CreateView):
    model = Warehouse
    context_object_name = 'warehouse'
    template_name = "warehouse.html"
    success_message = "Warehouse created successfully"
    success_url = '/'
    fields = '__all__'

# Responsible for rendering the "list all warehouse" page


class WarehouseList(ListView):
    model = Warehouse
    context_object_name = 'warehouse'
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(WarehouseList, self).get_context_data(**kwargs)
        context['product'] = Product.objects.all()

        return context

# Responsible for rendering the "update warehouse" page


class WarehouseUpdate(UpdateView):
    model = Warehouse
    fields = ['id', 'wh_name', 'wh_desc']
    template_name = 'e-warehouse.html'
    success_url = '/'

# Responsible for rendering the "delete warehouse" page


class WarehouseDelete(DeleteView):
    model = Warehouse
    context_object_name = 'warehouse'
    fields = ['id', 'wh_name', 'wh_desc']
    template_name = 'd-warehouse.html'
    success_url = '/'


####################### PRODUCT VIEWS ###########################

# Responsible for rendering the "create new product" page
class ProductCreate(SuccessMessageMixin, CreateView):
    model = Product
    context_object_name = 'product'
    template_name = "products.html"
    success_message = "Product created successfully"
    success_url = '/'
    fields = '__all__'

# Responsible for rendering the "list all product" page


class ProductList(ListView):
    model = Product
    context_object_name = 'product'
    template_name = 'dashboard.html'

# Responsible for rendering the "update product" page


class ProductUpdate(UpdateView):
    model = Product
    fields = ['prodkey', 'prod_name', 'prod_qty', 'prod_desc']
    template_name = 'e-product.html'
    success_url = '/'

# Responsible for rendering the "delete product" page


class ProductDelete(DeleteView):
    model = Product
    context_object_name = 'product'
    fields = ['prodkey', 'prod_name', 'prod_qty', 'prod_desc']
    template_name = 'd-product.html'
    success_url = '/'

####################### USER AUTHENTICATION & PERMISSION ###########################

# Responsible for rendering the "user registration" page


class RegistrationView(CreateView):
    model = User
    context_object_name = 'user'
    success_url = '/landing'
    template_name = 'register.html'
    form_class = RegistrationForm

# Responsible for rendering the "user registration - success (pending admin approval)" page


class LandingView(ListView):
    model = User
    context_object_name = 'landing'
    template_name = 'landing.html'


####################### ALC - USER BASED ###########################


# Responsible for rendering the ALC "user-based list all accesses" page


class AdminView(ListView):

    model = User
    context_object_name = 'allUser'
    fields = ['__all__']
    template_name = "admin-view.html"


# Responsible for rendering the ALC "user-based update access" page


class AdminUpdate(UpdateView):

    model = User
    fields = ['username',
              'is_staff',
              'group'
              ]
    context_object_name = 'differentUser'
    template_name = 'admin-approve.html'
    success_url = '/management'

    def dispatch(self, *args, **kwargs):
        return super(AdminUpdate, self).dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(AdminUpdate, self).get_context_data(*args, **kwargs)
        obj = User.objects.all()
        grp = []
        for index in obj:
            grp.append(index.group_id)
        context['group'] = grp
        return context


####################### RBAC - GROUP BASED ###########################


# Responsible for rendering the RBAC "Role-based list all accesses" page


class AdminGroupList(ListView):
    context_object_name = 'GroupList'
    success_url = '/management'
    template_name = 'admin-group-view.html'
    queryset = Group.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super(AdminGroupList, self).get_context_data(*args, **kwargs)

        # users_group_1 = User.objects.filter(group='1')
        # users_group_2 = User.objects.filter(group='2')
        # users_group_3 = User.objects.filter(group='3')
        # users_group_4 = User.objects.filter(group='4')

        # context['users_1'] = users_group_1
        # context['users_2'] = users_group_2
        # context['users_3'] = users_group_3
        # context['users_4'] = users_group_4
# -----------------------------------------------------
        context["admin"] = []
        context["tech"] = []
        context["sales"] = []
        context["marketing"] = []
        context["groupData"] = Group.objects.all()

        for group in Group.objects.all():
            group_id = group.id
            sort_user = User.objects.filter(group=group_id)

            if group_id == 1:
                context["admin"] = sort_user
            elif group_id == 2:
                context["tech"] = sort_user
            elif group_id == 3:
                context["sales"] = sort_user
            else:
                context["marketing"] = sort_user

        return context


# Responsible for rendering the RBAC "Role-based update access" page

class AdminGroupUpdate(UpdateView):
    model = User
    fields = ['is_staff', 'is_admin']
    context_object_name = 'GroupUpdate'
    template_name = 'admin-group-update.html'
    success_url = '/management'
    queryset = Group.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super(AdminGroupUpdate, self).get_context_data(
            *args, **kwargs)
        obj = User.objects.all()

        context['usergroup'] = obj

        return context


def admindb(request):
    return render(request, "mystorev2/admindb.html")
