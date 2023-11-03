import db_base as db
import csv

class Recipe:
    def __init__(self, id, name, ingredients, category):
        self.id = id
        self.name = name
        self.ingredients = ingredients
        self.category = category

class Category:
    def __init__(self, category_id, category_name, predefined):
        self.category_id = category_id
        self.category_name = category_name
        self.predefined = predefined

class RecipeManager(db.DBbase):
    def __init__(self, db_name):
        super().__init__(db_name)
        self.recipes = []
        self.category_options = []

    def reset_or_create_db(self):
        try:
            super().execute_script(""" 
            DROP TABLE IF EXISTS Recipes;
            CREATE TABLE IF NOT EXISTS Recipes (
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                name varchar(50) NOT NULL,
                ingredients TEXT NOT NULL,
                category TEXT NOT NULL
            );
            DROP TABLE IF EXISTS Categories;
                        CREATE TABLE IF NOT EXISTS Categories (
                            category_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                            category_name varchar(50) NOT NULL,
                            predefined TEXT
                        );
            INSERT INTO Categories (category_name, predefined) VALUES ('Dessert', 'Y'); 
            INSERT INTO Categories (category_name, predefined) VALUES ('Main Course', 'Y'); 
            INSERT INTO Categories (category_name, predefined) VALUES ('Breakfast', 'Y'); 
            INSERT INTO Categories (category_name, predefined) VALUES ('Snack', 'Y');""")

        except Exception as e:
            print("An error occurred while resetting the database: ", e)

    def read_recipe_data(self, file_name):
        self._recipes = []
        try:
            with open(file_name, "r") as record:
                csv_reader = csv.reader(record)
                # next(record)
                for row in csv_reader:
                    # print(row)
                    id = row['id']
                    name = row['name']
                    ingredients = [ingredient.strip() for ingredient in row['ingredients'].split(', ')]
                    category = row['category']
                    recipe = Recipe(id, name, ingredients, category)
                    self.add_recipe(recipe)
        except FileNotFoundError as e:
            print(f"Error: The specified CSV file '{file_name}' was not found: {e}")
        except Exception as e:
            print("An error occurred: ", e)

    def load_recipes_from_db(self):
        recipes = []
        try:
            recipes = super().get_cursor.execute("""SELECT * FROM Recipes;""").fetchall()
            for recipe in recipes:
                id = recipe[0]
                name = recipe[1]
                ingredients = [ingredient.strip() for ingredient in recipe[2].split(', ')]
                category = recipe[3]
                recipes.append(Recipe(id, name, ingredients, category))
        except Exception as e:
            print("An error occurred.", e)
        self.recipes = recipes

    def create_recipe(self):
        name = input("Enter recipe name: ").strip()
        ingredients = input("Enter ingredients (comma-separated): ").split(',')
        try:
            rows = super().get_cursor.execute("""SELECT * FROM Categories;""").fetchall()
            if rows:
                print("Available Category Options: ")
                last_id = 1
                for row in rows:
                    id = row[0]
                    category_name = row[1]
                    last_id = id
                    print(f"{id} - {category_name}")
                # Get last category id and add one
                custom_id = last_id + 1
                print(f"{custom_id}. Create a Custom Category")
                category_option = int(input("Enter choice number of category: "))
                if category_option == custom_id:
                    category = input("Enter custom category: ").strip()
                    super().get_cursor.execute("INSERT INTO Categories (category_name, predefined) VALUES (?, ?)",(category, 'N'))
                    super().get_connection.commit()
                    # save to categories.csv
                else:
                    category = rows[category_option - 1][1].strip()
            else:
                category = input("Enter choice number of category: ").strip()
            return Recipe(None, name, ingredients, category)
        except Exception as e:
            print("An error has occurred.", e)
    def add_recipe(self, recipe):
        try:
            super().get_cursor.execute("INSERT INTO Recipes (name, ingredients, category) VALUES (?, ?, ?)", (recipe.name, ', '.join(recipe.ingredients), recipe.category))
            super().get_connection.commit()
            id = super().get_cursor.execute("""SELECT id FROM Recipes WHERE name  = ?;""", (recipe.name,)).fetchone()
            recipe.id = id[0]
            print(f"Add {recipe.name} successfully.")
            self.recipes.append(recipe)
        except Exception as e:
            print("An error has occurred while adding a recipe: ", e)

    def get_recipes_by_category(self, category):
        recipes = []
        try:
            if category is not None:
                rows = super().get_cursor.execute("""SELECT * FROM Recipes WHERE category like ? ;""", (category,)).fetchall()
                for row in rows:
                    id = row[0]
                    name = row[1]
                    ingredients = [ingredient.strip() for ingredient in row[2].split(',')]
                    category = row[3]
                    recipes.append(Recipe(id, name, ingredients, category))
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
                    id = row[0]
                    name = row[1]
                    ingredients = [ingredient.strip() for ingredient in row[2].split(',')]
                    category = row[3]
                    recipes.append(Recipe(id, name, ingredients, category))
        except Exception as e:
            print("An error has occurred.", e)
        return recipes

    def get_all_recipes(self):
        recipes = []
        try:
            rows = super().get_cursor.execute("""SELECT * FROM Recipes;""").fetchall()
            for row in rows:
                id = row[0]
                name = row[1]
                ingredients = [ingredient.strip() for ingredient in row[2].split(',')]
                category = row[3]
                recipes.append(Recipe(id, name, ingredients, category))
            if recipes:
                print(f"---------- All recipes ---------- ")
                for recipe in recipes:
                    print("\n")
                    print(f"---------- {recipe.name} recipe: ---------- ")
                    print(f"ID of {recipe.name} recipe:")
                    print(recipe.id)
                    print(f"Ingredients of {recipe.name} recipe : ")
                    print(recipe.ingredients)
                    print(f"Category of {recipe.name} recipe : ")
                    print(recipe.category)
                return recipes
            else:
                print("No recipes found!")
        except Exception as e:
            print("An error has occurred.", e)

    def view_recipe(self):
        recipe_name = input("Enter the recipe name you want to view: ").strip()
        recipes = []
        try:
            if recipe_name is not None:
                rows = super().get_cursor.execute("""SELECT * FROM Recipes WHERE name like ? ;""",
                                                  (recipe_name.strip(),)).fetchall()
                for row in rows:
                    id = row[0]
                    name = row[1]
                    ingredients = [ingredient.strip() for ingredient in row[2].split(',')]
                    category = row[3]
                    recipes.append(Recipe(id, name, ingredients, category))
                if recipes:
                    print(f"---------- {recipe_name} recipe ---------- ")
                    for recipe in recipes:
                        print(f"ID of {recipe_name} recipe : ")
                        print(recipe.id)
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
        val = input("Do you want to view the detailed recipe: (y/ n) ").strip()
        if val == 'y':
            self.view_recipe()
        else:
            print("Continuing to the main menu!")

    def update_recipe(self, recipe_id):
        try:
            recipe = self.get_cursor.execute("SELECT * FROM Recipes WHERE id=?", (recipe_id,)).fetchone()
            name_change = input(f"Do you want to update Recipe Name of ID {recipe_id}: (y/n) ").strip()
            if name_change.tolower() == "y":
                new_recipe_name = input("Enter the new recipe name: ").strip()
                recipe.name = new_recipe_name
            category_change = input(f"Do you want to update the Category of ID {recipe_id}: (y/n ").strip()
            if category_change.tolower() == "y":
                new_category = input("Enter the new category name: ").strip()
                recipe.category = new_category
            ingredients_change = input(f"Do you want to update the Ingredients of ID {recipe_id}: (y/n ").strip()
            if ingredients_change.tolower() == "y":
                new_ingredients_list = input("Enter tje new ingredients (comma-separated): ").split(',')
                recipe.ingredients = new_ingredients_list
            if recipe:
                self.get_cursor.execute("""
                    UPDATE Recipes 
                    SET name=?, ingredients=?, category=?
                    WHERE id=?
                """, (recipe.name, ', '.join(recipe.ingredients), recipe.category, recipe_id))
                self.get_connection.commit()
                # update CSV record
                print(f"Recipe with ID {recipe_id} updated successfully.")
            else:
                print(f"Recipe with ID {recipe_id} not found.")
        except Exception as e:
            print("An error has occurred.", e)

    def delete_recipe(self, recipe_id):
        try:
            recipe = self.get_cursor.execute("SELECT * FROM Recipes WHERE id=?", (recipe_id,)).fetchone()
            if recipe:
                self.get_cursor.execute("DELETE FROM Recipes WHERE id=?", (recipe_id,))
                self.get_connection.commit()
                print(f"Recipe with ID {recipe_id} deleted successfully.")
            else:
                print(f"Recipe with ID {recipe_id} not found.")
        except Exception as e:
            print("An error has occurred.", e)

    # def update_recipe(self, id):
    #     try:
    #         type = input("Type which attribute of Recipe you want to : Recipe Name/Category/Ingredients: ").strip()
    #         if type.lower() == 'category':
    #             try:
    #                 category = input("Enter Category for the Recipe: ")
    #                 super().get_cursor.execute("UPDATE Recipes SET category = ? WHERE id = ?",
    #                                            (category, id))
    #                 super().get_connection.commit()
    #                 print(f"Updated recipe with {id} successfully.")
    #             except Exception as e:
    #                 print("An error occurred while resetting the database: ", e)
    #         elif type.lower() == 'Ingredients':
    #             try:
    #                 ingredients = input("Enter Ingredients for the Recipe (comma-separated) : ")
    #                 super().get_cursor.execute("UPDATE Recipes SET Ingredients = ? WHERE id = ?",
    #                                            (', '.join(ingredients), id))
    #                 super().get_connection.commit()
    #                 print(f"Updated recipe with {id} successfully.")
    #             except Exception as e:
    #                 print("An error occurred while resetting
    #                 the database: ", e)
    #         else:
    #             print("Invalid input!")
    #     except:
    #             print(f"Recipe with {id} name not found!")
    #

def save_recipes_to_csv(recipes):
    with open('recipes.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["id", "Recipe Name", "Category", "Ingredients"])
        for recipe in recipes:
            writer.writerow([recipe.id, recipe.name, recipe.category, ", ".join(recipe.ingredients)])

def main():
    recipe_manager = RecipeManager("recipesDB.sqlite")
    # recipe_manager.reset_or_create_db()

    while True:
        print("\nRecipe Manager Menu:")
        print("1. Create a Recipe")
        print("2. View Recipes by Category")
        print("3. View Recipes by Ingredient")
        print("4. View Recipes by Recipe name")
        print("5. View all Recipes")
        print("6. Update Recipes")
        print("7. Delete Recipes")
        print("8. Quit")

        choice = input("Enter the number of your choice: ").strip()

        if choice == '1':
            try:
                recipe = recipe_manager.create_recipe()
                recipe_manager.add_recipe(recipe)
                save_recipes_to_csv(recipe_manager.recipes)
                print(f"Recipe '{recipe.name}' added successfully!")
            except Exception as e:
                print("An error has occurred.", e)

        elif choice == '2':
            try:
                category = input("Enter category to view recipes: ").strip()
                recipes = recipe_manager.get_recipes_by_category(category.strip())
                if recipes:
                    print(f"Recipes in the '{category}' category:")
                    for recipe in recipes:
                        print(recipe.name)
                    recipe_manager.view_recipe_or_continue()
                else:
                    print(f"No recipes found in the '{category}' category.")
            except Exception as e:
                print("An error has occurred.", e)

        elif choice == '3':
            try:
                ingredient = input("Enter ingredient to view recipes: ").strip()
                recipes = recipe_manager.get_recipes_by_ingredient(ingredient.strip())
                if recipes:
                    print(f"Recipes containing '{ingredient}':")
                    for recipe in recipes:
                        print(recipe.name)
                    recipe_manager.view_recipe_or_continue()
                else:
                    print(f"No recipes found containing '{ingredient}'.")
            except Exception as e:
                print("An error has occurred.", e)

        elif choice == '4':
            try:
                recipe_manager.view_recipe()
            except Exception as e:
                print("An error has occurred.", e)

        elif choice == '5':
            try:
                recipes = recipe_manager.get_all_recipes()
            except Exception as e:
                print("An error has occurred.", e)
        elif choice == '6':
            try:
                recipes = recipe_manager.get_all_recipes()
                if recipes:
                    id = input("Enter the recipe name to update: ")
                    if id:
                        recipe_manager.update_recipe(id)
                    else:
                        print("Invalid input!")

            except Exception as e:
                print("An error has occurred.", e)

        elif choice == '7':
            try:
                recipes = recipe_manager.get_all_recipes()
                id = int(input("Enter the Recipe ID you want to delete: "))
                recipe_manager.delete_recipe(id)
            except Exception as e:
                print("An error has occurred.", e)

        elif choice == '8':
            try:
                recipe_manager.close_db()  # Close the database connection
                print("Thank you for using the Recipe Creator and Manager Application!")
                break
            except Exception as e:
                print("An error has occurred.", e)
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
