from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
import random

# import logging
# logger = logging.getLogger(__name__)

from recipes_app.forms import (
    RecipeForm,
    LoginForm,
    UserRegistrationForm,
    CategoryForm,
    СookbookForm,
)
from recipes_app.models import Recipe, Category, Сookbook


def get_home(request):
    NUMBER = 6
    title = f"Главная страница"
    count_users = User.objects.all().count()
    count_recipes = Recipe.objects.all().count()
    cookbook_items = Сookbook.objects.all()
    cookbook_items = {
        random.choice(cookbook_items) for cookbook_items.values in range(NUMBER)
    }
    return render(
        request,
        "home.html",
        {
            "title": title,
            "count_users": count_users,
            "count_recipes": count_recipes,
            "cookbook_items": cookbook_items,
        },
    )


def get_recipes(request):
    title = f"Все рецепты"
    cookbook_items = Сookbook.objects.all()
    return render(
        request,
        "cookbook_items.html",
        {"title": title, "cookbook_items": cookbook_items},
    )


def get_recipes_from_user_id(request, user_id: int):
    cookbook_items = Сookbook.objects.get(pk=user_id)
    return render(
        request, "user_detail_cookbook_items.html", {"cookbook_items": cookbook_items}
    )


def get_detail_recipe_by_id(request, item_id: int):
    cookbook_item = Сookbook.objects.get(pk=item_id)
    title = cookbook_item.recipe.name
    return render(
        request,
        "detail_cookbook_item.html",
        {"title": title, "cookbook_items": cookbook_item},
    )


def edit_recipe_by_id(request, item_id: int):
    cookbook_item = Сookbook.objects.get(pk=item_id)
    title = f"Редактировать рецепт"
    if request.method == "GET":
        recipe_form = RecipeForm(instance=cookbook_item.recipe)
        return render(request, "add_recipe.html", {"form": recipe_form, "title": title})
    elif request.method == "POST":
        recipe_form = RecipeForm(
            request.POST, request.FILES, instance=cookbook_item.recipe
        )
        if recipe_form.is_valid():
            recipe_form.save()
            messages.success(request, f"Рецепт сохранен")
            return redirect("user_recipes")
        else:
            messages.error(request, "Что-то пошло не так.... попробуйте еще раз")
            return render(
                request, "add_recipe.html", {"form": recipe_form, "title": title}
            )


def edit_category_by_id(request, item_id: int):
    cookbook_items = Сookbook.objects.get(pk=item_id)
    title = f"Редактировать категорию"
    if request.method == "GET":
        category_form = CategoryForm(instance=cookbook_items.category)
        return render(
            request, "add_recipe.html", {"form": category_form, "title": title}
        )
    elif request.method == "POST":
        category_form = CategoryForm(request.POST, instance=cookbook_items.category)
        if category_form.is_valid():
            cookbook_items.category = Category(id=category_form.cleaned_data["name"])
            cookbook_items.save()
            messages.success(request, f"Категория сохранена")
            return redirect("user_recipes")
        else:
            messages.error(request, "Что-то пошло не так.... попробуйте еще раз")
            return render(
                request, "add_recipe.html", {"form": category_form, "title": title}
            )


def delete_cookbook_items_by_id(request, item_id: id):
    cookbook_items = Сookbook.objects.get(pk=item_id)
    if cookbook_items:
        cookbook_items.delete()
        messages.success(request, "Рецепт удален")
    else:
        messages.error(request, "Рецепт не найден")
    return redirect("user_recipes")


def get_users(request):
    title = "Список пользователей"
    users = User.objects.all()
    return render(request, "users.html", {"title": title, "users": users})


def get_user_recipes(request):
    title = "Мои рецепты"
    cookbook_items = Сookbook.objects.filter(user_id=request.user)
    if not cookbook_items:
        messages.info(request, f"У Вас пока нет ни одного рецепта")
        return redirect("/")
    return render(
        request,
        "user_cookbook_items.html",
        {
            "title": title,
            "cookbook_items": cookbook_items,
            "username": request.user.username,
        },
    )


def add_recipe(request):
    title = "Добавить рецепт"
    head_title = "Добавить рецепт: "
    cookbook_item = СookbookForm(request.POST, request.FILES)
    if request.method == "GET":
        return render(
            request,
            "add_recipe.html",
            {"form": cookbook_item, "title": title, "head_title": head_title},
        )
    elif request.method == "POST":
        if cookbook_item.is_valid():
            name = cookbook_item.cleaned_data["name"]
            category = cookbook_item.cleaned_data["category"]
            description = cookbook_item.cleaned_data["description"]
            steps = cookbook_item.cleaned_data["steps"]
            cooking_time = cookbook_item.cleaned_data["cooking_time"]
            image = cookbook_item.cleaned_data["image"]
            recipe = Recipe(
                name=name,
                description=description,
                steps=steps,
                cooking_time=cooking_time,
                image=image,
            )
            category = Category(id=category)
            recipe.save()
            сookbook_item = Сookbook(
                user=request.user, recipe=recipe, category=category
            )
            сookbook_item.save()
            messages.success(request, f"Рецепт сохранен")
            return redirect("user_recipes")
    else:
        messages.error(request, f"Не получилось сохранить рецепт")
        return render(
            request,
            "add_recipe.html",
            {"form": cookbook_item, "title": title, "head_title": head_title},
        )
    return render(
        request,
        "add_recipe.html",
        {"form": cookbook_item, "title": title, "head_title": head_title},
    )


def input(request):
    title = "Вход"
    if request.method == "GET":
        login_form = LoginForm()
        return render(
            request, "register/login.html", {"form": login_form, "title": title}
        )
    elif request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data["username"]
            password = login_form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f"Добро пожаловать, {username.title()} !")
                return redirect("home")
    messages.error(request, f"Некорректное имя пользователя или пароль")
    return render(request, "register/login.html", {"form": login_form, "title": title})


def register(request):
    title = "Регистрация"
    if request.method == "POST":
        user_reg_form = UserRegistrationForm(request.POST)
        if user_reg_form.is_valid():
            if user_reg_form["password"].value() != user_reg_form["password2"].value():
                messages.success(request, f"Пароли не совпадают")
                user_reg_form = UserRegistrationForm(request.POST)
            else:
                new_user = user_reg_form.save(commit=False)
                new_user.set_password(user_reg_form.cleaned_data["password"])
                new_user.save()
                messages.success(request, f"Пользователь успешно сохранен")
                return redirect("login")
        else:
            messages.success(request, f"Данные некорректны")
            user_reg_form = UserRegistrationForm(request.POST)
    else:
        user_reg_form = UserRegistrationForm()
    return render(
        request,
        "register/register.html",
        {"form": user_reg_form, "title": title},
    )


def output(request):
    title = "Выход"
    if request.user.is_authenticated:
        logout(request)
        # messages.success(request, f"Вы вышли, до новых встреч!")
        return render(request, "register/logout.html", {"title": title})
    else:
        return redirect("login")
