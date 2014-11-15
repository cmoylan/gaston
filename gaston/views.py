from flask import render_template, request, redirect, url_for, g, flash
from database import db_session

from gaston import app
from models import Recipe, Ingredient


@app.route('/')
def root():
    return 'do it'


@app.route('/recipes')
def recipe_index():
    recipes = Recipe.all()
    flash('Got all recipes')
    return render_template('recipes/index.html', recipes=recipes)


@app.route('/recipes/<int:id>')
def recipe_show(id):
    recipe = Recipe.find(id)
    return render_template('recipes/show.html', recipe=recipe)


# TODO: merge new and edit actions
# TODO: new/edit are essentially the same, and create/update are as well
@app.route('/recipes/new', methods=['GET'])
@app.route('/recipes', methods=['POST'])
def recipe_new():
    error = None
    if request.method == 'POST':
        recipe = Recipe(request.form)
        recipe.save()
        #if recipe.save():
        return redirect(url_for('recipe_show', id=recipe.id))
    else:
        recipe = Recipe()

    # request was GET
    g.new = True
    return render_template('recipes/edit.html', recipe=recipe, error=error)


@app.route('/recipes/<int:id>/edit', methods=['GET'])
@app.route('/recipes/<int:id>', methods=['POST'])
def recipe_edit(id):
    error = None
    recipe = Recipe.find(id)

    if request.method == 'POST':
        #if recipe.update(request.form):
        recipe.update(request.form)
        recipe.save()
        return redirect(url_for('recipe_show', id=recipe.id))

    # request was GET
    return render_template('recipes/edit.html', recipe=recipe, error=error)


# TODO: don't use GET for this
@app.route('/recipes/<int:id>/delete', methods=['POST', 'DELETE', 'GET'])
def recipe_delete(id):
    recipe = Recipe.find(id)
    if recipe is None: abort(404)

    recipe.destroy()

    return redirect(url_for('recipe_index'))



@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
