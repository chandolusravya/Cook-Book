from flask import Flask, jsonify, request,render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Sravya!234@localhost:3306/recipesdb'

db=SQLAlchemy(app)

#define recipe model
class Recipe(db.Model): #create table with this class name
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    ingridents = db.Column(db.String(255), nullable=False)
    How = db.Column(db.String(255), nullable=False)

recipes = [
    {'name': 'Chickpea Salad', 'ingridents': 'chickpeas,Tomatoes,Cucumbers,Salt,Pepper,Lemon Juice', 'How': 'Dice the vegetables. Then add salt, pepper, lemon juice and cooked beans.'},
]

# Create all tables

with app.app_context():
    db.create_all()

@app.route('/')
def main_page():
    # Get the warning message if it exists
    warning = request.args.get('warning', None)
    return render_template('main_page.html', recipes=recipes, warning=warning)

@app.route('/add_recipe', methods=['GET', 'POST'])
def add_recipe():
    if request.method == 'POST':
        name = request.form['name']
        ingridents = request.form['ingridents']
        How = request.form['How']
        if not name or not ingridents or not How:
            return render_template('add_recipe.html', warning="Please fill in all fields")
        # Create a new recipe dictionary
        # Create a new recipe object
        new_recipe = Recipe(name=name, ingridents=ingridents, How=How)
        # Add the new recipe to the database
        # Add the new recipe to the list of recipes
        
        #recipes.append(new_recipe)
        # Add the new recipe to the database
        db.session.add(new_recipe)
        db.session.commit()
        # Redirect to the home page after adding the recipe
        return redirect(url_for('main_page', warning='Successfully added!'))
    return render_template('add_recipe.html')


@app.route('/recipes', methods=['GET'])
def get_recipes():
    recipes = Recipe.query.all()
    #recipes_data = [{'name': recipe.name, 'ingridents': recipe.ingridents, 'How': recipe.How} for recipe in recipes]
    #return jsonify(recipes_data)
    if recipes is not None:
        recipes_data = [{'id': recipe.id, 'name': recipe.name, 'ingridents': recipe.ingridents, 'How': recipe.How} for recipe in recipes if recipe is not None]
        return jsonify(recipes_data)
    else:
        return jsonify({'message': 'No recipes found'})
    

@app.route('/recipes/<int:recipe_id>', methods=['GET'])
def get_recipe(recipe_id):
    recipe = Recipe.query.get(recipe_id)
    if recipe:
        recipe_data = {'id': recipe.id, 'name': recipe.name, 'ingridents': recipe.ingridents, 'How': recipe.How}
        return jsonify(recipe_data)
        #return render_template('recipe_details.html', recipe=recipe)
    else:
        return jsonify({'message': 'Recipe not found'})
    

@app.route('/recipes/<int:recipe_id>', methods=['PUT','POST'])
def update_recipe(recipe_id):
    recipe = Recipe.query.get(recipe_id)
    if recipe:
            # data = request.get_json()
            recipe.name = request.form.get('name')
            recipe.ingridents = request.form.get('ingridents')
            recipe.How = request.form.get('How')
            db.session.commit()
            # return jsonify({'message': 'Recipe updated successfully'})
            return redirect(url_for("main_page"))
    else:
        # return jsonify({'message': 'Recipe not found'})
        return render_template(url_for("main_page"))

@app.route('/recipes/<int:recipe_id>', methods=['DELETE'])
def delete_recipe(recipe_id):
    recipe = Recipe.query.get(recipe_id)
    if recipe:
        db.session.delete(recipe)
        db.session.commit()
        return jsonify({'message': 'Recipe deleted successfully'})
    else:
        return jsonify({'message': 'Recipe not found'})





if __name__ == '__main__':
    app.run(debug=True)


