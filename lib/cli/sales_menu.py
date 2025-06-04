
import os
from datetime import datetime
from tabulate import tabulate
from lib.services.sales_service import SalesService
from lib.services.item_service import ItemService
from lib.services.customer_service import CustomerService

class SalesMenu:
    def __init__(self):
        self.sales_service = SalesService()
        self.item_service = ItemService()
        self.customer_service = CustomerService()

    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_header(self):
        """Display the menu header"""
        print("=" * 60)
        print("           SALES MANAGEMENT")
        print("=" * 60)
        print()

    def display_menu(self):
        """Display sales menu options"""
        menu_options = [
            ["1", "🛒 New Sale", "Create a new sale transaction"],
            ["2", "📋 View All Sales", "Display all sales"],
            ["3", "🔍 View Sale Details", "View detailed sale information"],
            ["4", "❌ Cancel Sale", "Cancel/refund a sale"],
            ["5", "📊 Sales Summary", "View sales statistics"],
            ["6", "🔙 Back to Main Menu", "Return to main menu"]
        ]

        print("💰 SALES MENU")
        print(tabulate(menu_options, headers=["Option", "Action", "Description"], tablefmt="grid"))
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
                return '6'

    def new_sale(self):
        """Create a new sale"""
        self.clear_screen()
        self.display_header()
        print("🛒 NEW SALE")
        print("=" * 40)

        try:
            # Optional customer selection
            customer_id = None
            use_customer = input("Add customer to sale? (y/N): ").strip().lower()

            if use_customer == 'y':
                customer_search = input("Enter customer name or ID: ").strip()
                if customer_search.isdigit():
                    customer = self.customer_service.get_customer_by_id(int(customer_search))
                else:
                    customers = self.customer_service.search_customers(customer_search)
                    if customers:
                        customer = customers[0]  # Take first match
                    else:
                        customer = None

                if customer:
                    print(f"✅ Customer: {customer.full_name}")
                    customer_id = customer.id
                else:
                    print("❌ Customer not found. Proceeding without customer.")

            # Create sale
            sale = self.sales_service.create_sale(customer_id=customer_id)
            print(f"\n📝 Sale created (ID: {sale.id})")

            # Add items to sale
            print("\nAdding items to sale...")
            print("Enter item IDs (one per line, blank line to finish):")

            while True:
                item_input = input("Item ID: ").strip()
                if not item_input:
                    break

                try:
                    item_id = int(item_input)
                    item = self.item_service.get_item_by_id(item_id)

                    if not item:
                        print(f"❌ Item {item_id} not found!")
                        continue

                    if item.is_sold or item.quantity <= 0:
                        print(f"❌ Item '{item.name}' is not available!")
                        continue

                    # Get quantity
                    max_qty = item.quantity
                    while True:
                        try:
                            qty_input = input(f"Quantity (max {max_qty}, default 1): ").strip()
                            quantity = int(qty_input) if qty_input else 1
                            if 1 <= quantity <= max_qty:
                                break
                            else:
                                print(f"❌ Please enter quantity between 1 and {max_qty}")
                        except ValueError:
                            print("❌ Please enter a valid quantity!")

                    # Add item to sale
                    sale_item = self.sales_service.add_item_to_sale(sale.id, item_id, quantity)
                    print(f"✅ Added {quantity}x {item.name} - ${item.price * quantity:.2f}")

                except ValueError:
                    print("❌ Please enter a valid item ID!")
                except Exception as e:
                    print(f"❌ Error adding item: {e}")

            # Apply discount if needed
            discount_input = input("\nDiscount amount ($, optional): ").strip()
            discount = float(discount_input) if discount_input else 0

            # Apply tax if needed
            tax_input = input("Tax amount ($, optional): ").strip()
            tax = float(tax_input) if tax_input else 0

            # Complete sale
            completed_sale = self.sales_service.complete_sale(sale.id, discount=discount, tax=tax)

            if completed_sale:
                print(f"\n✅ Sale completed successfully!")
                print(f"Total: KES{completed_sale.final_total:.2f}")

                # Print receipt option
                print_receipt = input("\nPrint receipt? (y/N): ").strip().lower()
                if print_receipt == 'y':
                    self.print_receipt(completed_sale.id)
            else:
                print("❌ Failed to complete sale!")

        except Exception as e:
            print(f"❌ Error creating sale: {e}")

        input("\nPress Enter to continue...")

    def view_all_sales(self):
        """Display all sales"""
        self.clear_screen()
        self.display_header()
        print("📋 ALL SALES")
        print("=" * 40)

        try:
            sales = self.sales_service.get_all_sales()

            if not sales:
                print("No sales found.")
            else:
                table_data = []
                for sale in sales:
                    customer_name = sale.customer.full_name if sale.customer else "Walk-in"
                    table_data.append([
                        sale.id,
                        sale.sale_date.strftime('%Y-%m-%d %H:%M') if sale.sale_date else "N/A",
                        customer_name,
                        f"KES{sale.final_total:.2f}",
                        sale.status,
                        len(sale.items) if sale.items else 0
                    ])

                headers = ["ID", "Date", "Customer", "Total", "Status", "Items"]
                print(tabulate(table_data, headers=headers, tablefmt="grid"))
                print(f"\nTotal sales: {len(sales)}")
        except Exception as e:
            print(f"❌ Error retrieving sales: {e}")

        input("\nPress Enter to continue...")

    def view_sale_details(self):
        """View detailed sale information"""
        self.clear_screen()
        self.display_header()
        print("🔍 SALE DETAILS")
        print("=" * 40)

        try:
            sale_id = int(input("Enter sale ID: "))
            sale = self.sales_service.get_sale_with_details(sale_id)

            if not sale:
                print(f"❌ Sale with ID {sale_id} not found!")
                input("Press Enter to continue...")
                return

            # Display sale details
            customer_name = sale.customer.full_name if sale.customer else "Walk-in Customer"

            details = [
                ["Sale ID", sale.id],
                ["Date", sale.sale_date.strftime('%Y-%m-%d %H:%M:%S') if sale.sale_date else "N/A"],
                ["Customer", customer_name],
                ["Status", sale.status],
                ["Subtotal", f"KES{sale.subtotal:.2f}"],
                ["Discount", f"KES{sale.discount:.2f}"],
                ["Tax", f"KES{sale.tax:.2f}"],
                ["Final Total", f"KES{sale.final_total:.2f}"]
            ]

            print(tabulate(details, headers=["Field", "Value"], tablefmt="grid"))

            # Display items
            if sale.items:
                print(f"\n📦 ITEMS ({len(sale.items)} items)")
                print("-" * 50)

                items_data = []
                for sale_item in sale.items:
                    item = sale_item.item
                    items_data.append([
                        item.name,
                        sale_item.quantity,
                        f"KES{sale_item.unit_price:.2f}",
                        f"KES{sale_item.total_price:.2f}"
                    ])

                headers = ["Item", "Qty", "Unit Price", "Total"]
                print(tabulate(items_data, headers=headers, tablefmt="grid"))
        except ValueError:
            print("❌ Invalid sale ID!")
        except Exception as e:
            print(f"❌ Error retrieving sale details: {e}")

        input("\nPress Enter to continue...")

    def cancel_sale(self):
        """Cancel a sale"""
        self.clear_screen()
        self.display_header()
        print("❌ CANCEL SALE")
        print("=" * 40)

        try:
            sale_id = int(input("Enter sale ID to cancel: "))
            sale = self.sales_service.get_sale_by_id(sale_id)

            if not sale:
                print(f"❌ Sale with ID {sale_id} not found!")
                input("Press Enter to continue...")
                return

            if sale.status == 'cancelled':
                print("❌ Sale is already cancelled!")
                input("Press Enter to continue...")
                return

            customer_name = sale.customer.full_name if sale.customer else "Walk-in"

            print(f"\nSale to cancel:")
            print(f"ID: {sale.id}")
            print(f"Date: {sale.sale_date.strftime('%Y-%m-%d %H:%M') if sale.sale_date else 'N/A'}")
            print(f"Customer: {customer_name}")
            print(f"Total: KES{sale.final_total:.2f}")

            confirm = input("\n⚠️  Are you sure you want to cancel this sale? (y/N): ").strip().lower()

            if confirm == 'y':
                if self.sales_service.cancel_sale(sale_id):
                    print("✅ Sale cancelled successfully!")
                else:
                    print("❌ Failed to cancel sale!")
            else:
                print("❌ Cancellation aborted.")
        except ValueError:
            print("❌ Invalid sale ID!")
        except Exception as e:
            print(f"❌ Error cancelling sale: {e}")

        input("\nPress Enter to continue...")

    def sales_summary(self):
        """View sales summary"""
        self.clear_screen()
        self.display_header()
        print("📊 SALES SUMMARY")
        print("=" * 40)

        try:
            summary = self.sales_service.get_sales_summary()

            summary_data = [
                ["Total Sales", summary['total_sales']],
                ["Total Revenue", f"KES{summary['total_revenue']:.2f}"],
                ["Average Sale", f"KES{summary['average_sale']:.2f}"],
                ["Today's Sales", summary['today_sales']],
                ["Today's Revenue", f"KES{summary['today_revenue']:.2f}"],
                ["This Week's Sales", summary['week_sales']],
                ["This Week's Revenue", f"KES{summary['week_revenue']:.2f}"],
                ["This Month's Sales", summary['month_sales']],
                ["This Month's Revenue", f"KES{summary['month_revenue']:.2f}"]
            ]

            print(tabulate(summary_data, headers=["Metric", "Value"], tablefmt="grid"))

            # Top selling items
            print(f"\n🏆 TOP SELLING ITEMS")
            print("-" * 30)
            top_items = self.sales_service.get_top_selling_items(limit=5)

            if top_items:
                items_data = []
                for item_data in top_items:
                    items_data.append([
                        item_data['name'],
                        item_data['total_sold'],
                        f"KES{item_data['total_revenue']:.2f}"
                    ])

                headers = ["Item", "Sold", "Revenue"]
                print(tabulate(items_data, headers=headers, tablefmt="grid"))
            else:
                print("No sales data available.")

        except Exception as e:
            print(f"❌ Error retrieving sales summary: {e}")

        input("\nPress Enter to continue...")

    def print_receipt(self, sale_id):
        """Print a receipt for a sale"""
        try:
            sale = self.sales_service.get_sale_with_details(sale_id)
            if not sale:
                print("❌ Sale not found!")
                return

            print("\n" + "=" * 50)
            print("             THRIFT STORE RECEIPT")
            print("=" * 50)
            print(f"Sale ID: {sale.id}")
            print(f"Date: {sale.sale_date.strftime('%Y-%m-%d %H:%M:%S') if sale.sale_date else 'N/A'}")
            if sale.customer:
                print(f"Customer: {sale.customer.full_name}")
            print("-" * 50)

            if sale.items:
                for sale_item in sale.items:
                    item = sale_item.item
                    print(f"{item.name[:30]:<30} {sale_item.quantity:>3} x ${sale_item.unit_price:>6.2f} = ${sale_item.total_price:>8.2f}")

            print("-" * 50)
            print(f"{'Subtotal:':<40} KES{sale.subtotal:>8.2f}")
            if sale.discount > 0:
                print(f"{'Discount:':<40} -KES{sale.discount:>7.2f}")
            if sale.tax > 0:
                print(f"{'Tax:':<40} KES{sale.tax:>8.2f}")
            print(f"{'TOTAL:':<40} KES{sale.final_total:>8.2f}")
            print("=" * 50)
            print("         Thank you for your purchase!")
            print("=" * 50)
        except Exception as e:
            print(f"❌ Error printing receipt: {e}")

    def run(self):
        """Run the sales menu"""
        while True:
            try:
                self.clear_screen()
                self.display_header()
                self.display_menu()

                choice = self.get_user_choice()

                if choice == '1':
                    self.new_sale()
                elif choice == '2':
                    self.view_all_sales()
                elif choice == '3':
                    self.view_sale_details()
                elif choice == '4':
                    self.cancel_sale()
                elif choice == '5':
                    self.sales_summary()
                elif choice == '6':
                    break
            except Exception as e:
                print(f"❌ An error occurred: {e}")
                input("Press Enter to continue...")