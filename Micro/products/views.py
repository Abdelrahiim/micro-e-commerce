import mimetypes
from typing import Any, Dict
from django.shortcuts import render ,redirect ,get_object_or_404
from django.views import View ,generic
from Micro.products.forms import ProductForm, ProductUpdateForm
from Micro.products.models import Product , ProductAttachment
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import FileResponse , HttpResponseBadRequest


# ---------------------------------------------------------------
class ProductCreateView(LoginRequiredMixin,View):
    template_name = "products/create.html"
    form_class= ProductForm
    
    # ------------------------------
    def get(self,request,*args, **kwargs):
        return render(request=request,template_name=self.template_name,context=self.get_context_data())
    
    # ------------------------------
    def get_context_data(self, **kwargs):
        context = {}
        context["form"] = self.get_form()
        return context
    
    # ------------------------------
    def post(self,request,*args, **kwargs):
        form = self.get_form(data=request.POST)
        if form.is_valid():
            self.create_product(request.user,form)
            return redirect('product:list')
            
    # ------------------------------
    def create_product(self,user,form):
        product = form.save(commit=False)
        product.user = user
        product.save()
        
    # ------------------------------
    def get_form(self, **kwargs) :
        if kwargs:
            data = kwargs["data"]
            form = self.form_class(data)
        else:
            form = self.form_class()
        return form
    
    
# --------------------------------------------------------------- 
class ProductListView(generic.ListView):
    template_name = "products/list.html"
    queryset = Product.objects.all()
    
    
# ---------------------------------------------------------------
class ProductDetailView(LoginRequiredMixin,View):
    template_name = "products/detail.html"
    form_class = ProductUpdateForm
    
    # ------------------------------
    def get(self, request, *args, **kwargs):
        handle = kwargs["handle"]
        return render(request,self.template_name,self.get_context_data(handle=handle))
    
    # ------------------------------
    def get_context_data(self, **kwargs):
        context = {}
        context["product"] = get_object_or_404(Product,handle = kwargs['handle']) 
        is_owner = context["product"].user == self.request.user
        context['is_owner'] = is_owner
        if is_owner:
            context['form'] = self.get_form(instance=context["product"])
        return context
    
    # ------------------------------
    def get_form(self, **kwargs) :
        if kwargs.get('data') :
            form = self.form_class(data = kwargs['data'],files=kwargs['file'],instance=kwargs["instance"] )
        else:
            form = self.form_class(instance=kwargs["instance"])
        return form

    # ------------------------------
    def post(self,request,*args, **kwargs):
        product= get_object_or_404(Product,handle = kwargs['handle']) 
        
        form = self.get_form(data=request.POST,file=request.FILES, instance=product)
        
        if form.is_valid():
            
            self.update_product(request.user,form)
            return redirect('product:list')
        
    # ------------------------------
    def update_product(self,user,form):
        updated_product = form.save(commit=False)
        updated_product.user = user
        updated_product.save()
        
        
        
# ---------------------------------------------------------------
class ProductAttachmentDownLoadView(View):
    
    def get(self,request,*args, **kwargs):
        attachment = ProductAttachment.objects.all().first()
        file = attachment.file.open('rb')
        can_download = attachment.is_free or False
        if  can_download is False :
            return HttpResponseBadRequest()
        
        filename = attachment.file.name
        content_type ,_ = mimetypes.guess_type(filename)
        response = FileResponse(file)
        print(content_type)
        response['Content-type'] = content_type
        response['Content-Disposition'] = f"attachment;filename={filename}" 
        return response