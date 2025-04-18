from django.contrib import admin
from .models import Customer, Task, Feedback, ClusteredCustomer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'item_name', 'amount', 'customer_comments', 'status', 'created_at')
    fields = ('id', 'name', 'email', 'phone', 'item_name', 'amount', 'customer_comments', 'status', 'ai_analysis')
    search_fields = ('id', 'name', 'email', 'item_name')
    list_filter = ('status', 'created_at')
    ordering = ('-created_at',)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('task_name', 'priority', 'is_completed')
    list_filter = ('is_completed', 'priority')
    search_fields = ('task_name',)
    ordering = ('priority',)


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('customer', 'feedback_text', 'sentiment', 'created_at')
    search_fields = ('customer__name', 'feedback_text')


@admin.register(ClusteredCustomer)
class ClusteredCustomerAdmin(admin.ModelAdmin):
    list_display = ('customer', 'cluster_group', 'created_at')
    list_filter = ('cluster_group',)
    search_fields = ('customer__name',)
