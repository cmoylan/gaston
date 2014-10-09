import json
from flask import Flask, render_template, request, redirect, url_for

from models.recipe import Recipe


app = Flask(__name__)


@app.route('/')
def root():
    return 'Hello World!'


@app.route('/recipes')
def recipe_index():
    recipes = Recipe.all()
    return render_template('recipes/index.html', recipes=recipes)


@app.route('/recipes/<int:id>')
def recipe_show(id):
    recipe = Recipe.find(id)
    return render_template('recipes/show.html', recipe=recipe)


# TODO: merge new and edit actions
@app.route('/recipes/new', methods=['POST', 'GET'])
def recipe_new():
    error = None
    if request.method == 'POST':
        recipe = Recipe(request.form)
        if recipe.save():
            return redirect(url_for('recipe_show', id=recipe.id))
    else:
        recipe = Recipe()

    # request was GET
    return render_template('recipes/edit.html', recipe=recipe, error=error)


@app.route('/recipes/<int:id>/edit', methods=['POST', 'GET'])
def recipe_edit(id):
    error = None
    recipe = Recipe.find(id)

    if request.method == 'POST':
        recipe.update(request.form)
        if recipe.save():
            return redirect(url_for('recipes/edit.html', id=recipe.id))

    # request was GET
    return render_template('recipes/edit.html', recipe=recipe, error=error)


if __name__ == '__main__':
    app.debug = True
    app.run()
