import csv


class Recipe:
    def __init__(self, name, ingredients, category):
        self.name = name
        self.ingredients = ingredients
        self.category = category


class RecipeManager:
    def __init__(self):
        self.recipes = []


    def add_recipe(self, recipe):
        self.recipes.append(recipe)


    def get_recipes_by_category(self, category):
        return [recipe for recipe in self.recipes if recipe.category == category]


    def get_recipes_by_ingredient(self, ingredient):
        return [recipe for recipe in self.recipes if ingredient in recipe.ingredients]


def create_recipe():
    name = input("Enter recipe name: ")
    ingredients = input("Enter ingredients (comma-separated): ").split(',')
    category = input("Enter category: ")
    return Recipe(name, ingredients, category)


def save_recipes_to_csv(recipes):
    with open('recipes.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Recipe Name", "Category", "Ingredients"])


        for recipe in recipes:
            writer.writerow([recipe.name, recipe.category, ", ".join(recipe.ingredients)])


def load_recipes_from_csv():
    recipes = []
    try:
        with open('recipes.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                name = row['Recipe Name']
                category = row['Category']
                ingredients = [ingredient.strip() for ingredient in row['Ingredients'].split(',')]
                recipes.append(Recipe(name, ingredients, category))
    except FileNotFoundError:
        pass  # Handle the case where the file doesn't exist
    except Exception as e:
        print("An error occurred", e)
    return recipes


def main():
    recipe_manager = RecipeManager()
    recipes = load_recipes_from_csv()
    recipe_manager.recipes = recipes


    while True:
        print("\nRecipe Manager Menu:")
        print("1. Create a recipe")
        print("2. View recipes by category")
        print("3. View recipes by ingredient")
        print("4. Display all recipes")
        print("5. Quit")


        choice = input("Enter your choice: ")


        if choice == '1':
            recipe = create_recipe()
            recipe_manager.add_recipe(recipe)
            print(f"Recipe '{recipe.name}' added successfully!")
            save_recipes_to_csv(recipe_manager.recipes)
        elif choice == '2':
            category = input("Enter category to view recipes: ")
            recipes = recipe_manager.get_recipes_by_category(category)
            if recipes:
                print(f"Recipes in the '{category}' category:")
                for recipe in recipes:
                    print(recipe.name)
            else:
                print(f"No recipes found in the '{category}' category.")
        elif choice == '3':
            ingredient = input("Enter ingredient to view recipes: ")
            recipes = recipe_manager.get_recipes_by_ingredient(ingredient)
            if recipes:
                print(f"Recipes containing '{ingredient}':")
                for recipe in recipes:
                    print(recipe.name)
            else:
                print(f"No recipes found containing '{ingredient}'.")
        elif choice == '4':
            if not recipe_manager.recipes:
                print("No recipes found.")
            else:
                print("\nAll Recipies:")
                for recipe in recipe_manager.recipes:
                    print(f"Name: {recipe.name}, Category: {recipe.category}, Ingredients: {', '.join(recipe.ingredients)})

        elif choice == '5':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()