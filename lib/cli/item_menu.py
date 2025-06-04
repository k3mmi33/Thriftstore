import os
from tabulate import tabulate
from lib.services.item_service import ItemService

class ItemMenu:
    def __init__(self):
        self.service = ItemService()

    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_header(self):
        """Display the menu header"""
        print("=" * 60)
        print("           ITEM MANAGEMENT")
        print("=" * 60)
        print()

    def display_menu(self):
        """Display item menu options"""
        menu_options = [
            ["1", "➕ Add New Item", "Add a new item to inventory"],
            ["2", "📋 View All Items", "Display all items in inventory"],
            ["3", "🔍 Search Items", "Search for specific items"],
            ["4", "✏️  Edit Item", "Modify item information"],
            ["5", "🗑️  Delete Item", "Remove item from inventory"],
            ["6", "📦 View Categories", "Show all item categories"],
            ["7", "🔙 Back to Main Menu", "Return to main menu"]
        ]

        print("🛍️  ITEM MENU")
        print(tabulate(menu_options, headers=["Option", "Action", "Description"], tablefmt="grid"))
        print()

    def get_user_choice(self):
        """Get user's menu choice"""
        while True:
            try:
                choice = input("Enter your choice (1-7): ").strip()
                if choice in ['1', '2', '3', '4', '5', '6', '7']:
                    return choice
                else:
                    print("❌ Invalid choice. Please enter a number between 1-7.")
            except KeyboardInterrupt:
                return '7'

    def add_item(self):
        """Add a new item"""
        self.clear_screen()
        self.display_header()
        print("➕ ADD NEW ITEM")
        print("=" * 40)

        try:
            name = input("Item name: ").strip()
            if not name:
                print("❌ Item name is required!")
                return

            description = input("Description (optional): ").strip() or None
            category = input("Category: ").strip()

            while True:
                try:
                    price = float(input("Price (KES): "))
                    break
                except ValueError:
                    print("❌ Please enter a valid price!")

            while True:
                try:
                    cost = float(input("Cost (KES, optional, default 0): ") or "0")
                    break
                except ValueError:
                    print("❌ Please enter a valid cost!")

            while True:
                try:
                    quantity = int(input("Quantity (default 1): ") or "1")
                    break
                except ValueError:
                    print("❌ Please enter a valid quantity!")

            condition = input("Condition (New/Excellent/Good/Fair/Poor, default Good): ").strip() or "Good"
            size = input("Size (optional): ").strip() or None
            brand = input("Brand (optional): ").strip() or None
            color = input("Color (optional): ").strip() or None

            item = self.service.create_item(
                name=name,
                description=description,
                category=category,
                price=price,
                cost=cost,
                quantity=quantity,
                condition=condition,
                size=size,
                brand=brand,
                color=color
            )

            print(f"\n✅ Item '{item.name}' added successfully! (ID: {item.id})")
        except Exception as e:
            print(f"❌ Error adding item: {e}")

        input("\nPress Enter to continue...")

    def view_all_items(self):
        """Display all items"""
        self.clear_screen()
        self.display_header()
        print("📋 ALL ITEMS")
        print("=" * 40)

        try:
            items = self.service.get_all_items()

            if not items:
                print("No items found.")
            else:
                # Prepare data for table
                table_data = []
                for item in items:
                    status = "❌ Sold" if item.is_sold else "✅ Available"
                    table_data.append([
                        item.id,
                        item.name[:30] + "..." if len(item.name) > 30 else item.name,
                        item.category,
                        f"KES{item.price:.2f}",
                        item.quantity,
                        item.condition,
                        status
                    ])

                headers = ["ID", "Name", "Category", "Price", "Qty", "Condition", "Status"]
                print(tabulate(table_data, headers=headers, tablefmt="grid"))
                print(f"\nTotal items: {len(items)}")
        except Exception as e:
            print(f"❌ Error retrieving items: {e}")

        input("\nPress Enter to continue...")

    def search_items(self):
        """Search for items"""
        self.clear_screen()
        self.display_header()
        print("🔍 SEARCH ITEMS")
        print("=" * 40)

        search_term = input("Enter search term (name, category, or brand): ").strip()

        if not search_term:
            print("❌ Search term cannot be empty!")
            input("Press Enter to continue...")
            return

        try:
            items = self.service.search_items(search_term)

            if not items:
                print(f"No items found matching '{search_term}'.")
            else:
                table_data = []
                for item in items:
                    status = "❌ Sold" if item.is_sold else "✅ Available"
                    table_data.append([
                        item.id,
                        item.name[:30] + "..." if len(item.name) > 30 else item.name,
                        item.category,
                        f"KES{item.price:.2f}",
                        item.condition,
                        status
                    ])

                headers = ["ID", "Name", "Category", "Price", "Condition", "Status"]
                print(tabulate(table_data, headers=headers, tablefmt="grid"))
                print(f"\nFound {len(items)} item(s) matching '{search_term}'")
        except Exception as e:
            print(f"❌ Error searching items: {e}")

        input("\nPress Enter to continue...")

    def edit_item(self):
        """Edit an existing item"""
        self.clear_screen()
        self.display_header()
        print("✏️  EDIT ITEM")
        print("=" * 40)

        try:
            item_id = int(input("Enter item ID to edit: "))
            item = self.service.get_item_by_id(item_id)

            if not item:
                print(f"❌ Item with ID {item_id} not found!")
                input("Press Enter to continue...")
                return

            print(f"\nEditing: {item.name}")
            print("(Press Enter to keep current value)\n")

            # Get new values
            name = input(f"Name [{item.name}]: ").strip() or item.name
            description = input(f"Description [{item.description or 'None'}]: ").strip() or item.description
            category = input(f"Category [{item.category}]: ").strip() or item.category

            price_input = input(f"Price [{item.price}]: ").strip()
            price = float(price_input) if price_input else item.price

            cost_input = input(f"Cost [{item.cost}]: ").strip()
            cost = float(cost_input) if cost_input else item.cost

            qty_input = input(f"Quantity [{item.quantity}]: ").strip()
            quantity = int(qty_input) if qty_input else item.quantity

            condition = input(f"Condition [{item.condition}]: ").strip() or item.condition
            size = input(f"Size [{item.size or 'None'}]: ").strip() or item.size
            brand = input(f"Brand [{item.brand or 'None'}]: ").strip() or item.brand
            color = input(f"Color [{item.color or 'None'}]: ").strip() or item.color

            # Update item
            updated_item = self.service.update_item(
                item_id,
                name=name,
                description=description,
                category=category,
                price=price,
                cost=cost,
                quantity=quantity,
                condition=condition,
                size=size,
                brand=brand,
                color=color
            )

            if updated_item:
                print(f"\n✅ Item '{updated_item.name}' updated successfully!")
            else:
                print("❌ Failed to update item!")
        except ValueError:
            print("❌ Invalid item ID!")
        except Exception as e:
            print(f"❌ Error updating item: {e}")

        input("\nPress Enter to continue...")

    def delete_item(self):
        """Delete an item"""
        self.clear_screen()
        self.display_header()
        print("🗑️  DELETE ITEM")
        print("=" * 40)

        try:
            item_id = int(input("Enter item ID to delete: "))
            item = self.service.get_item_by_id(item_id)

            if not item:
                print(f"❌ Item with ID {item_id} not found!")
                input("Press Enter to continue...")
                return

            print(f"\nItem to delete:")
            print(f"Name: {item.name}")
            print(f"Category: {item.category}")
            print(f"Price: KES{item.price:.2f}")

            confirm = input("\n⚠️  Are you sure you want to delete this item? (y/N): ").strip().lower()

            if confirm == 'y':
                if self.service.delete_item(item_id):
                    print("✅ Item deleted successfully!")
                else:
                    print("❌ Failed to delete item!")
            else:
                print("❌ Delete cancelled.")
        except ValueError:
            print("❌ Invalid item ID!")
        except Exception as e:
            print(f"❌ Error deleting item: {e}")

        input("\nPress Enter to continue...")

    def view_categories(self):
        """View all categories"""
        self.clear_screen()
        self.display_header()
        print("📦 ITEM CATEGORIES")
        print("=" * 40)

        try:
            categories = self.service.get_categories()

            if not categories:
                print("No categories found.")
            else:
                for i, category in enumerate(categories, 1):
                    print(f"{i}. {category}")
                print(f"\nTotal categories: {len(categories)}")
        except Exception as e:
            print(f"❌ Error retrieving categories: {e}")

        input("\nPress Enter to continue...")

    def run(self):
        """Run the item menu"""
        while True:
            try:
                self.clear_screen()
                self.display_header()
                self.display_menu()

                choice = self.get_user_choice()

                if choice == '1':
                    self.add_item()
                elif choice == '2':
                    self.view_all_items()
                elif choice == '3':
                    self.search_items()
                elif choice == '4':
                    self.edit_item()
                elif choice == '5':
                    self.delete_item()
                elif choice == '6':
                    self.view_categories()
                elif choice == '7':
                    break
            except Exception as e:
                print(f"❌ An error occurred: {e}")
                input("Press Enter to continue...")