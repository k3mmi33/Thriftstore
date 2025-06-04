import os
from tabulate import tabulate
from lib.services.customer_service import CustomerService

class CustomerMenu:
    def __init__(self):
        self.service = CustomerService()

    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_header(self):
        """Display the menu header"""
        print("=" * 60)
        print("         CUSTOMER MANAGEMENT")
        print("=" * 60)
        print()

    def display_menu(self):
        """Display customer menu options"""
        menu_options = [
            ["1", "➕ Add New Customer", "Register a new customer"],
            ["2", "📋 View All Customers", "Display all customers"],
            ["3", "🔍 Search Customers", "Search for specific customers"],
            ["4", "👤 View Customer Details", "View detailed customer information"],
            ["5", "✏️  Edit Customer", "Modify customer information"],
            ["6", "🗑️  Delete Customer", "Remove customer from system"],
            ["7", "🔙 Back to Main Menu", "Return to main menu"]
        ]

        print("👥 CUSTOMER MENU")
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

    def add_customer(self):
        """Add a new customer"""
        self.clear_screen()
        self.display_header()
        print("➕ ADD NEW CUSTOMER")
        print("=" * 40)

        try:
            first_name = input("First name: ").strip()
            if not first_name:
                print("❌ First name is required!")
                input("Press Enter to continue...")
                return

            last_name = input("Last name: ").strip()
            if not last_name:
                print("❌ Last name is required!")
                input("Press Enter to continue...")
                return

            email = input("Email (optional): ").strip() or None
            phone = input("Phone (optional): ").strip() or None
            address = input("Address (optional): ").strip() or None
            city = input("City (optional): ").strip() or None
            postal_code = input("Postal code (optional): ").strip() or None
            notes = input("Notes (optional): ").strip() or None

            customer = self.service.create_customer(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                address=address,
                city=city,
                postal_code=postal_code,
                notes=notes
            )

            print(f"\n✅ Customer '{customer.full_name}' added successfully! (ID: {customer.id})")
        except Exception as e:
            print(f"❌ Error adding customer: {e}")

        input("\nPress Enter to continue...")

    def view_all_customers(self):
        """Display all customers"""
        self.clear_screen()
        self.display_header()
        print("📋 ALL CUSTOMERS")
        print("=" * 40)

        try:
            customers = self.service.get_all_customers()

            if not customers:
                print("No customers found.")
            else:
                table_data = []
                for customer in customers:
                    table_data.append([
                        customer.id,
                        customer.full_name,
                        customer.email or "N/A",
                        customer.phone or "N/A",
                        customer.city or "N/A",
                        customer.date_joined.strftime('%Y-%m-%d') if customer.date_joined else "N/A"
                    ])

                headers = ["ID", "Name", "Email", "Phone", "City", "Joined"]
                print(tabulate(table_data, headers=headers, tablefmt="grid"))
                print(f"\nTotal customers: {len(customers)}")
        except Exception as e:
            print(f"❌ Error retrieving customers: {e}")

        input("\nPress Enter to continue...")

    def search_customers(self):
        """Search for customers"""
        self.clear_screen()
        self.display_header()
        print("🔍 SEARCH CUSTOMERS")
        print("=" * 40)

        search_term = input("Enter search term (name, email, or phone): ").strip()

        if not search_term:
            print("❌ Search term cannot be empty!")
            input("Press Enter to continue...")
            return

        try:
            customers = self.service.search_customers(search_term)

            if not customers:
                print(f"No customers found matching '{search_term}'.")
            else:
                table_data = []
                for customer in customers:
                    table_data.append([
                        customer.id,
                        customer.full_name,
                        customer.email or "N/A",
                        customer.phone or "N/A",
                        customer.city or "N/A"
                    ])

                headers = ["ID", "Name", "Email", "Phone", "City"]
                print(tabulate(table_data, headers=headers, tablefmt="grid"))
                print(f"\nFound {len(customers)} customer(s) matching '{search_term}'")
        except Exception as e:
            print(f"❌ Error searching customers: {e}")

        input("\nPress Enter to continue...")

    def view_customer_details(self):
        """View detailed customer information"""
        self.clear_screen()
        self.display_header()
        print("👤 CUSTOMER DETAILS")
        print("=" * 40)

        try:
            customer_id = int(input("Enter customer ID: "))
            customer, sales = self.service.get_customer_with_sales(customer_id)

            if not customer:
                print(f"❌ Customer with ID {customer_id} not found!")
                input("Press Enter to continue...")
                return

            # Display customer details
            details = [
                ["ID", customer.id],
                ["Name", customer.full_name],
                ["Email", customer.email or "N/A"],
                ["Phone", customer.phone or "N/A"],
                ["Address", customer.address or "N/A"],
                ["City", customer.city or "N/A"],
                ["Postal Code", customer.postal_code or "N/A"],
                ["Date Joined", customer.date_joined.strftime('%Y-%m-%d') if customer.date_joined else "N/A"],
                ["Notes", customer.notes or "N/A"]
            ]

            print(tabulate(details, headers=["Field", "Value"], tablefmt="grid"))

            # Display sales history
            if sales:
                print(f"\n📊 SALES HISTORY ({len(sales)} sales)")
                print("-" * 40)

                sales_data = []
                total_spent = 0
                for sale in sales[-10:]:  # Show last 10 sales
                    sales_data.append([
                        sale.id,
                        sale.sale_date.strftime('%Y-%m-%d') if sale.sale_date else "N/A",
                        f"${sale.final_total:.2f}",
                        sale.status
                    ])
                    total_spent += sale.final_total

                headers = ["Sale ID", "Date", "Total", "Status"]
                print(tabulate(sales_data, headers=headers, tablefmt="grid"))
                print(f"\nTotal amount spent: ${total_spent:.2f}")
            else:
                print("\n📊 No sales history found.")
        except ValueError:
            print("❌ Invalid customer ID!")
        except Exception as e:
            print(f"❌ Error retrieving customer details: {e}")

        input("\nPress Enter to continue...")

    def edit_customer(self):
        """Edit an existing customer"""
        self.clear_screen()
        self.display_header()
        print("✏️  EDIT CUSTOMER")
        print("=" * 40)

        try:
            customer_id = int(input("Enter customer ID to edit: "))
            customer = self.service.get_customer_by_id(customer_id)

            if not customer:
                print(f"❌ Customer with ID {customer_id} not found!")
                input("Press Enter to continue...")
                return

            print(f"\nEditing: {customer.full_name}")
            print("(Press Enter to keep current value)\n")

            # Get new values
            first_name = input(f"First name [{customer.first_name}]: ").strip() or customer.first_name
            last_name = input(f"Last name [{customer.last_name}]: ").strip() or customer.last_name
            email = input(f"Email [{customer.email or 'None'}]: ").strip() or customer.email
            phone = input(f"Phone [{customer.phone or 'None'}]: ").strip() or customer.phone
            address = input(f"Address [{customer.address or 'None'}]: ").strip() or customer.address
            city = input(f"City [{customer.city or 'None'}]: ").strip() or customer.city
            postal_code = input(f"Postal code [{customer.postal_code or 'None'}]: ").strip() or customer.postal_code
            notes = input(f"Notes [{customer.notes or 'None'}]: ").strip() or customer.notes

            # Update customer
            updated_customer = self.service.update_customer(
                customer_id,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                address=address,
                city=city,
                postal_code=postal_code,
                notes=notes
            )

            if updated_customer:
                print(f"\n✅ Customer '{updated_customer.full_name}' updated successfully!")
            else:
                print("❌ Failed to update customer!")
        except ValueError:
            print("❌ Invalid customer ID!")
        except Exception as e:
            print(f"❌ Error updating customer: {e}")

        input("\nPress Enter to continue...")

    def delete_customer(self):
        """Delete a customer"""
        self.clear_screen()
        self.display_header()
        print("🗑️  DELETE CUSTOMER")
        print("=" * 40)

        try:
            customer_id = int(input("Enter customer ID to delete: "))
            customer = self.service.get_customer_by_id(customer_id)

            if not customer:
                print(f"❌ Customer with ID {customer_id} not found!")
                input("Press Enter to continue...")
                return

            print(f"\nCustomer to delete:")
            print(f"Name: {customer.full_name}")
            print(f"Email: {customer.email or 'N/A'}")
            print(f"Phone: {customer.phone or 'N/A'}")

            confirm = input("\n⚠️  Are you sure you want to delete this customer? (y/N): ").strip().lower()

            if confirm == 'y':
                if self.service.delete_customer(customer_id):
                    print("✅ Customer deleted successfully!")
                else:
                    print("❌ Failed to delete customer!")
            else:
                print("❌ Delete cancelled.")
        except ValueError:
            print("❌ Invalid customer ID!")
        except Exception as e:
            print(f"❌ Error deleting customer: {e}")

        input("\nPress Enter to continue...")

    def run(self):
        """Run the customer menu"""
        while True:
            try:
                self.clear_screen()
                self.display_header()
                self.display_menu()

                choice = self.get_user_choice()

                if choice == '1':
                    self.add_customer()
                elif choice == '2':
                    self.view_all_customers()
                elif choice == '3':
                    self.search_customers()
                elif choice == '4':
                    self.view_customer_details()
                elif choice == '5':
                    self.edit_customer()
                elif choice == '6':
                    self.delete_customer()
                elif choice == '7':
                    break
            except Exception as e:
                print(f"❌ An error occurred: {e}")
                input("Press Enter to continue...")