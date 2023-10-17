import db_base as db
class Recipe():
    def __init__(self, name, ingredients, category):
        self.name = name
        self.ingredients = ingredients
        self.category = category

class RecipeManager(db.DBbase):
    def __init__(self):
        super().__init__("recipesDB.sqlite")
        # self.create_table()
        self.recipes = []

    # def create_table(self):
    #     try:
    #         sql = """ CREATE TABLE IF NOT EXISTS Recipes (
    #             id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
    #             name varchar(50) NOT NULL,
    #             ingredients TEXT NOT NULL,
    #             category TEXT NOT NULL
    #         );"""
    #         super().execute_script(sql)
    #     except Exception as e:
    #         print("An error occured.", e)

    def load_recipes_from_db(self):
        recipes = []
        try:
            recipes = super().get_cursor.execute("""SELECT * FROM Recipes;""").fetchall()
            for recipe in recipes:
                name = recipe[1]
                ingredients = [ingredient.strip() for ingredient in recipe[2].split(', ')]
                category = recipe[3]
                recipes.append(Recipe(name, ingredients, category))
        except Exception as e:
            print("An error occured.", e)
        self.recipes = recipes
    def add_recipe(self, recipe):
        try:
            super().get_cursor.execute("INSERT INTO Recipes (name, ingredients, category) VALUES (?, ?, ?)", (recipe.name, ', '.join(recipe.ingredients), recipe.category))
            super().get_connection.commit()
            print(f"Add {recipe.name} successfully.")
        except Exception as e:
            print("An error has occurred.", e)
        self.recipes.append(recipe)

    def get_recipes_by_category(self, category):
        recipes = []
        try:
            if category is not None:
                rows = super().get_cursor.execute("""SELECT * FROM Recipes WHERE category like ? ;""", (category,)).fetchall()
                for row in rows:
                    name = row[1]
                    ingredients = [ingredient.strip() for ingredient in row[2].split(',')]
                    category = row[3]
                    recipes.append(Recipe(name, ingredients, category))
        except Exception as e:
            print("An error has occurred.", e)
        return recipes

    def get_recipes_by_ingredient(self, ingredients):
        recipes = []
        try:
            if ingredients is not None:
                query = "SELECT * FROM Recipes WHERE"
                # Append '%' to each ingredient to perform a partial match.
                ingredients_list = ingredients.split(',')
                query1 = " ingredients LIKE "
                query2 = ""
                for ingredient in ingredients_list:
                    query2 = query2 + query1 + "'%" + ingredient.strip() + "%' " + 'OR'
                n = 2
                replaceStr = ";"
                query2 = query2[:-n] + replaceStr
                sql = query + " " + query2
                rows = super().get_cursor.execute(sql).fetchall()
                for row in rows:
                    name = row[1]
                    ingredients = [ingredient.strip() for ingredient in row[2].split(',')]
                    category = row[3]
                    recipes.append(Recipe(name, ingredients, category))
        except Exception as e:
            print("An error has occurred.", e)
        return recipes

    def view_recipe(self):
        recipe_name = input("Enter the recipe name you want to view: ").strip()
        recipes = []
        try:
            if recipe_name is not None:
                rows = super().get_cursor.execute("""SELECT * FROM Recipes WHERE name = ? ;""",
                                                  (recipe_name.strip(),)).fetchall()
                for row in rows:
                    name = row[1]
                    ingredients = [ingredient.strip() for ingredient in row[2].split(',')]
                    category = row[3]
                    recipes.append(Recipe(name, ingredients, category))
                if recipes:
                    print(f"---------- {recipe_name} recipe ---------- ")
                    for recipe in recipes:
                        print(f"Ingredients of {recipe_name} recipe : ")
                        print(recipe.ingredients)
                        print(f"Category of {recipe_name} recipe : ")
                        print(recipe.category)
                else:
                    print(f"{recipe_name} recipe not found!")
            else:
                print(f"{recipe_name} recipe not found!")
        except Exception as e:
            print("An error has occurred.", e)


    def view_recipe_or_continue(self):
        val = input("What to view the above recipes: (y/ n) ").strip()
        if val == 'y':
            self.view_recipe()
        else:
            print("Continuing to the main menu!")

def create_recipe():
    name = input("Enter recipe name: ").strip()
    ingredients = input("Enter ingredients (comma-separated): ").split(',')
    category = input("Enter category: ").strip()
    return Recipe(name, ingredients, category)


def main():
    recipe_manager = RecipeManager()

    while True:
        print("\nRecipe Manager Menu:")
        print("1. Create a recipe")
        print("2. View recipes by category")
        print("3. View recipes by ingredient")
        print("4. View recipes by recipe name")
        print("5. Quit")

        choice = input("Enter your choice: ").strip()

        if choice == '1':
            recipe = create_recipe()
            recipe_manager.add_recipe(recipe)
            print(f"Recipe '{recipe.name}' added successfully!")
        elif choice == '2':
            category = input("Enter category to view recipes: ").strip()
            recipes = recipe_manager.get_recipes_by_category(category.strip())
            if recipes:
                print(f"Recipes in the '{category}' category:")
                for recipe in recipes:
                    print(recipe.name)
                recipe_manager.view_recipe_or_continue()
            else:
                print(f"No recipes found in the '{category}' category.")
        elif choice == '3':
            ingredient = input("Enter ingredient to view recipes: ").strip()
            recipes = recipe_manager.get_recipes_by_ingredient(ingredient.strip())
            if recipes:
                print(f"Recipes containing '{ingredient}':")
                for recipe in recipes:
                    print(recipe.name)
                recipe_manager.view_recipe_or_continue()
            else:
                print(f"No recipes found containing '{ingredient}'.")
        elif choice == '4':
            recipe_manager.view_recipe()
        elif choice == '5':
            recipe_manager.close_db()  # Close the database connection
            print("Thank you for using the Recipe Creator and Manager Application!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
