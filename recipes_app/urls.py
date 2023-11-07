from django.urls import path
from . import views

urlpatterns = [
    path("", views.get_home, name="home"),
    path("recipes/", views.get_recipes, name="recipes"),
    path("user_recipes/", views.get_user_recipes, name="user_recipes"),
    path("add_recipe/", views.add_recipe, name="add_recipe"),
    path(
        "user_recipe_detail/<int:user_id>",
        views.get_recipes_from_user_id,
        name="user_recipe_detail",
    ),
    path(
        "recipe_detail/<int:item_id>",
        views.get_detail_recipe_by_id,
        name="recipe_detail",
    ),
    path("recipe_edit/<int:item_id>", views.edit_recipe_by_id, name="recipe_edit"),
    path(
        "category_edit/<int:item_id>", views.edit_category_by_id, name="category_edit"
    ),
    path(
        "recipe_delete/<int:item_id>",
        views.delete_cookbook_items_by_id,
        name="recipe_delete",
    ),
    path("users/", views.get_users, name="users"),
    path("login/", views.input, name="login"),
    path("logout/", views.output, name="logout"),
    path("register/", views.register, name="register"),
]
