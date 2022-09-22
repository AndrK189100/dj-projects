from django.shortcuts import render
from django.http import HttpResponse

DATA = {
    'omlet': {
        'яйца, шт': 2,
        'молоко, л': 0.1,
        'соль, ч.л.': 0.5,
    },
    'pasta': {
        'макароны, г': 0.3,
        'сыр, г': 0.05,
    },
    'buter': {
        'хлеб, ломтик': 1,
        'колбаса, ломтик': 1,
        'сыр, ломтик': 1,
        'помидор, ломтик': 1,
    },
    # можете добавить свои рецепты ;)
}


def omlet_view(request):
    template_name = 'calculator/index.html'
    recipe = DATA.get('omlet')
    servings = request.GET.get('servings')

    temp_recipe = recipe.copy()
    if servings:
        servings = int(servings)
        for item in temp_recipe:
            temp_recipe[item] = temp_recipe.get(item) * servings

    context = {'recipe': temp_recipe}
    return render(request, template_name, context)


def pasta_view(request):
    template_name = 'calculator/index.html'
    recipe = DATA.get('pasta')
    servings = request.GET.get('servings')

    temp_recipe = recipe.copy()
    if servings:
        servings = int(servings)
        for item in temp_recipe:
            temp_recipe[item] = temp_recipe.get(item) * servings

    context = {'recipe': temp_recipe}
    return render(request, template_name, context)


def buter_view(request):
    template_name = 'calculator/index.html'
    recipe = DATA.get('buter')
    servings = request.GET.get('servings')

    temp_recipe = recipe.copy()
    if servings:
        servings = int(servings)
        for item in temp_recipe:
            temp_recipe[item] = temp_recipe.get(item) * servings

    context = {'recipe': temp_recipe}
    return render(request, template_name, context)


