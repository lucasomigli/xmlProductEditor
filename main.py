import os
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import xml.etree.ElementTree as ET

class SimpleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("XML Editor App")

        # Create notebook (tabs)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Add tabs
        self.product_tab = ttk.Frame(self.notebook)
        self.export_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.product_tab, text="Product")
        self.notebook.add(self.export_tab, text="Export")

        # Initialize Product tab
        self.init_product_tab()

        # Initialize Export tab
        self.init_export_tab()

    def init_product_tab(self):
        # Product tab content
        self.product_file_dropdown_label = tk.Label(self.product_tab, text="Select Environment:")
        self.product_file_dropdown = ttk.Combobox(self.product_tab)
        self.product_file_dropdown['values'] = [d for d in os.listdir() if os.path.isdir(d)]
        self.product_file_dropdown.bind('<<ComboboxSelected>>', self.loadEnvironment)

        self.product_name_label = tk.Label(self.product_tab, text="Select Product XML:")
        self.product_name_dropdown = ttk.Combobox(self.product_tab)
        self.product_name_dropdown.bind('<<ComboboxSelected>>', self.loadEnvironment)


        # Products section
        self.productsLabel = tk.Label(self.product_tab, text="Products:")
        self.productsTable = self.create_table(self.product_tab)

        # Default Pricing Methods section
        self.defaultPricingMethodsLabel = tk.Label(self.product_tab, text="defaultPricingMethods:")
        self.defaultPricingMethodsTable = self.create_table(self.product_tab)

        # ValidMethods section
        self.validMethodsLabel = tk.Label(self.product_tab, text="Valid Methods:")
        self.validMethodsTable = self.create_table(self.product_tab)

        # InstrumentSchema section
        self.instrumentSchemaLabel = tk.Label(self.product_tab, text="Instrument Schema:")
        self.instrumentSchemaTable = self.create_table(self.product_tab)
        
        self.allTables = (self.instrumentSchemaTable, self.validMethodsTable, self.defaultPricingMethodsTable, self.productsTable)

        # Save button
        self.save_button = tk.Button(self.product_tab, text="Save", command=self.save_product_data)

        # Pack widgets
        self.product_file_dropdown_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.product_file_dropdown.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        self.product_name_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.product_name_dropdown.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        self.productsLabel.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.productsTable.grid(row=3, column=0, padx=10, pady=5, sticky="w")

        self.instrumentSchemaLabel.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        self.instrumentSchemaTable.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        self.validMethodsLabel.grid(row=6, column=0, padx=10, pady=5, sticky="w")
        self.validMethodsTable.grid(row=7, column=0, padx=10, pady=5, sticky="w")

        self.defaultPricingMethodsLabel.grid(row=6, column=1, padx=10, pady=5, sticky="w")
        self.defaultPricingMethodsTable.grid(row=7, column=1, padx=10, pady=5, sticky="w")

        self.save_button.grid(row=8, column=0, columnspan=2, pady=10)

    def init_export_tab(self):
        # Export tab content
        self.source_label = tk.Label(self.export_tab, text="Source:")
        self.source_dropdown = ttk.Combobox(self.export_tab, values=['UAT', 'DEV', 'PROD', 'TEMP'])

        self.export_button = tk.Button(self.export_tab, text="Export to:")
        self.export_to_dropdown = ttk.Combobox(self.export_tab, values=['UAT', 'DEV', 'PROD'])

        self.diff_button = tk.Button(self.export_tab, text="Diff")

        # Pack widgets
        self.source_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.source_dropdown.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        self.export_button.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.export_to_dropdown.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        self.diff_button.grid(row=2, column=0, columnspan=2, pady=10)

    def create_table(self, parent):
        columns = ("Tag", "Description", "rawXml")

        # Create a Treeview widget
        tree = ttk.Treeview(parent, columns=columns, show="headings")

        # Set column headings
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)

        # Add a vertical scrollbar
        vsb = ttk.Scrollbar(parent, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)

        # Pack the Treeview and scrollbar
        tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")

        # Enable editing for the Treeview
        tree.bind("<Double-1>", self.on_double_click)

        return tree

    def add_row_to_table(self, table, values):
        # Insert a new row into the table
        table.insert("", "end", values=values)

    def delete_selected_rows_from_table(self, table):
        # Get the selected items in the table
        selected_items = table.selection()

        # Delete selected rows
        for item in selected_items:
            table.delete(item)

    def on_double_click(self, event):
        # Allow editing when double-clicking on a cell
        item = self.productsTable.selection()[0]
        col = self.productsTable.identify_column(event.x)
        col = col.split("#")[-1]  # Extract column identifier
        self.productsTable.item(item, values=(col, "Edit Me", "Edit Me"))

    def delete_all_rows_from_table(self, table):
        # Get all item IDs in the table
        all_items = table.get_children()

        # Delete all rows
        for item in all_items:
            table.delete(item)
    
    def clearAllTables(self):
        for table in self.allTables:
            self.delete_all_rows_from_table(table)
    
            
    def loadEnvironment(self, event):
        
        products32 = self.product_file_dropdown.get() + "/products.xml"
        defaultPricingMethods = self.product_file_dropdown.get() + "/DefaultPricingMethods.xml"
        InstrumentSchema = self.product_file_dropdown.get() + "/nstrumentSchema.xml"
        VALIDMETHODS = self.product_file_dropdown.get() + "/VALIDMETHODS.xml"
    
        # Populate data
        self.clearAllTables()
        self.populateData(products32, defaultPricingMethods, InstrumentSchema, VALIDMETHODS)
    
    def populateData(self, _products32, _defaultPricingMethods, _InstrumentSchema, _VALIDMETHODS):
            
        self.loadData(_products32, self.productsTable)
        self.loadData(_defaultPricingMethods, self.defaultPricingMethodsTable)
        self.loadData(_InstrumentSchema, self.instrumentSchemaTable)
        self.loadData(_defaultPricingMethods, self.validMethodsTable)
        
    def loadData(self, input_file, table): 
        
        try:    
            tree = ET.parse(input_file)
            root = tree.getroot()

            # Populate the "Select Product XML" dropdown with PRODUCT node names
            product_names = [product.get('NAME') for product in root.findall('.//PRODUCT')]
            self.product_name_dropdown['values'] = product_names


            # Load data for the selected product
            selected_product_name = self.product_name_dropdown.get()
            self.delete_all_rows_from_table(table)
            selected_product = root.find(f'.//PRODUCT[@NAME="{selected_product_name}"]')

            if selected_product is not None:
                # Populate table
                for child in selected_product:
                    self.add_row_to_table(table, (child.tag, child.text, ET.tostring(child).decode('utf-8')))

            else:
                messagebox.showwarning("Warning", f"Product '{self.product_name_dropdown.get()}' not found in {input_file}.")

        except ET.ParseError as e:
            print(f"Error parsing XML file: {e}")
            
        except Exception as e:
            if not os.path.exists(input_file): 
                messagebox.showwarning("Warning", f"Product '{self.product_name_dropdown.get()}' not found in {input_file}.")
                self.clearAllTables()
        
    def save_product_data(self):
        selected_file = self.product_file_dropdown.get()

        try:
            tree = ET.parse(selected_file)
            root = tree.getroot()

            # Clear existing entries in the XML file
            for product in root.findall('.//PRODUCT'):
                root.remove(product)

            # Save new entries to the XML file
            for i in range(len(self.tag_entries)):
                product = ET.SubElement(root, 'PRODUCT', NAME=self.product_name_dropdown.get())

                data_type = ET.SubElement(product, 'DataType')
                data_type_tag = ET.SubElement(data_type, 'Tag')
                data_type_tag.text = self.tag_entries[i].get()
                data_type_description = ET.SubElement(data_type, 'Description')
                data_type_description.text = self.description_entries[i].get()
                data_type_raw_xml = ET.SubElement(data_type, 'rawXml')
                data_type_raw_xml.text = self.raw_xml_entries[i].get()

            # Save the modified XML tree to the file
            tree.write(selected_file)

            # Notify the user that the data has been saved
            messagebox.showinfo("Success", "Data saved successfully!")

        except ET.ParseError as e:
            print(f"Error parsing XML file: {e}")
            messagebox.showerror("Error", f"Error parsing XML file: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleApp(root)
    root.mainloop()
