def update_recipe(self, recipe_id, new_recipe):
    try:
        recipe = self.get_cursor.execute("SELECT * FROM Recipes WHERE id=?", (recipe_id,)).fetchone()
        if recipe:
            self.get_cursor.execute("""
                UPDATE Recipes 
                SET name=?, ingredients=?, category=?
                WHERE id=?
            """, (new_recipe.name, ', '.join(new_recipe.ingredients), new_recipe.category, recipe_id))
            self.get_connection.commit()
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