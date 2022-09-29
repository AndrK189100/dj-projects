from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet
from .models import Article, Tag, Scope


class RelationshipInlineFormset(BaseInlineFormSet):
    def clean(self):
        is_main = 0
        for form in self.forms:
            # В form.cleaned_data будет словарь с данными
            # каждой отдельной формы, которые вы можете проверить
            if bool(form.cleaned_data):
                if form.cleaned_data['is_main']:
                    is_main += 1
                    if is_main > 1:
                        raise ValidationError('Основной может быть только одна тематика!!!')

        if not is_main:
            raise ValidationError('Необходимо выбрать основную тематику!!!')
            # вызовом исключения ValidationError можно указать админке о наличие ошибки
            # таким образом объект не будет сохранен,
            # а пользователю выведется соответствующее сообщение об ошибке

        return super().clean()  # вызываем базовый код переопределяемого метода


class ScopeInline(admin.TabularInline):
    model = Scope
    extra = 1
    formset = RelationshipInlineFormset
    pass


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ScopeInline]
    pass


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass
