import os
from tabulate import tabulate
from lib.models.base import create_tables
from lib.cli.item_menu import ItemMenu
from lib.cli.customer_menu import CustomerMenu
from lib.cli.sales_menu import SalesMenu
from lib.cli.reports_menu import ReportsMenu
from lib.services.sales_service import SalesService

class MainMenu:
    def __init__(self):
        self.item_menu = ItemMenu()
        self.customer_menu = CustomerMenu()
        self.sales_menu = SalesMenu()
        self.reports_menu = ReportsMenu()

        # Create tables if they don't exist
        create_tables()

    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_header(self):
        """Display the application header"""
        print("=" * 60)
        print("        THRIFT STORE MANAGEMENT SYSTEM")
        print("=" * 60)
        print()

    def display_dashboard(self):
        """Display dashboard with key statistics"""
        try:
            summary = SalesService.get_sales_summary()

            dashboard_data = [
                ["Total Sales", summary['total_sales']],
                ["Total Revenue", f"${summary['total_revenue']:.2f}"],
                ["Today's Sales", summary['today_sales']],
                ["Today's Revenue", f"${summary['today_revenue']:.2f}"]
            ]

            print("📊 DASHBOARD")
            print(tabulate(dashboard_data, headers=["Metric", "Value"], tablefmt="grid"))
            print()
        except Exception as e:
            print(f"Error loading dashboard: {e}")
            print()

    def display_menu(self):
        """Display the main menu options"""
        menu_options = [
            ["1", "🛍️  Item Management", "Add, view, edit, and manage inventory"],
            ["2", "👥 Customer Management", "Manage customer information"],
            ["3", "💰 Sales Management", "Process sales and view history"],
            ["4", "📊 Reports", "View sales reports and analytics"],
            ["5", "⚙️  System Settings", "Configure application settings"],
            ["6", "❌ Exit", "Close the application"]
        ]

        print("🏪 MAIN MENU")
        print(tabulate(menu_options, headers=["Option", "Feature", "Description"], tablefmt="grid"))
        print()

    def get_user_choice(self):
        """Get user's menu choice"""
        while True:
            try:
                choice = input("Enter your choice (1-6): ").strip()
                if choice in ['1', '2', '3', '4', '5', '6']:
                    return choice
                else:
                    print("❌ Invalid choice. Please enter a number between 1-6.")
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                return '6'

    def handle_menu_choice(self, choice):
        """Handle the user's menu choice"""
        if choice == '1':
            self.item_menu.run()
        elif choice == '2':
            self.customer_menu.run()
        elif choice == '3':
            self.sales_menu.run()
        elif choice == '4':
            self.reports_menu.run()
        elif choice == '5':
            self.show_settings()
        elif choice == '6':
            return False
        return True

    def show_settings(self):
        """Show system settings"""
        self.clear_screen()
        self.display_header()

        print("⚙️  SYSTEM SETTINGS")
        print("=" * 40)
        print("1. Database: SQLite (thrift_store.db)")
        print("2. Version: 1.0.0")
        print("3. Environment: Development")
        print()
        print("Settings menu coming soon...")
        print()
        input("Press Enter to continue...")

    def run(self):
        """Main application loop"""
        while True:
            try:
                self.clear_screen()
                self.display_header()
                self.display_dashboard()
                self.display_menu()

                choice = self.get_user_choice()

                if not self.handle_menu_choice(choice):
                    break

            except Exception as e:
                print(f"❌ An error occurred: {e}")
                input("Press Enter to continue...")

        print("\n👋 Thank you for using Thrift Store Management System!")
