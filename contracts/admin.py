from django import forms
from django.contrib import admin
import jdatetime
from .models import Contract, Clause , Presenter,Employer
from django.utils.html import format_html
from django.urls import reverse

class ContractClauseForm(forms.ModelForm):
    class Meta:
        model = Contract
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        content = cleaned_data.get("clauses", "")
        duration = cleaned_data.get("duration_days")
        if "مدت زمان قرارداد" in [con.title for con in content] and not duration:
            raise forms.ValidationError("لطفاً مدت زمان قرارداد را بر حسب روز کاری وارد نمایید")

        return cleaned_data
    
@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    form = ContractClauseForm

    list_display = ['employer','presenter', 'shamsi_start_date',
                    'total_amount', 'long_term', 'monthly_salary','pdf_link','pdf_link_preview']
    filter_horizontal = ('clauses',)
    
    readonly_fields = ['pdf_link','pdf_link_preview']

    def pdf_link(self, obj):
        if obj.id:
            url = reverse('admin_contract_pdf', args=[obj.id])
            return format_html(f'<a href="{url}" target="_blank">دانلود PDF</a>')
        return "-"
    
    pdf_link.short_description = 'خروجی PDF'
    
    def pdf_link_preview(self, obj):
        if obj.id:
            url = reverse('admin_contract_preview', args=[obj.id])
            return format_html(f'<a href="{url}" target="_blank">پیشنمایش</a>')
        return "-"
    
    pdf_link_preview.short_description = 'پیشنمایش'

    def shamsi_start_date(self, obj):
        if obj.created_at:
            j_date = jdatetime.datetime.fromgregorian(datetime=obj.start_date)
            return j_date.strftime('%Y/%m/%d')
        return '-'
    shamsi_start_date.short_description = "تاریخ شمسی"

@admin.register(Clause)
class ClauseAdmin(admin.ModelAdmin):
    list_display = ['title', 'order']
    list_filter = ['title']
    search_fields = ['title', 'content']


@admin.register(Presenter)
class PresenterAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent_name' ,'national_code','phone_number']
    list_filter = ['name']
    search_fields = ['name', 'parent_name','national_code']
    
    
@admin.register(Employer)
class EmployerAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent_name' ,'national_code','phone_number']
    list_filter = ['name']
    search_fields = ['name', 'parent_name','national_code']