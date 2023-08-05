"""
This lib allows for the creation of tables, in an easy form.
Author : TheAssassin71 (https://github.com/megat69)
"""

class Table:
	"""
	The main table class, which contains the whole table.
	"""
	def __init__(self, name:str=None, size:tuple=None):
		"""
		:param name: The name of the table. None by default.
		:param size: The size of the table. If not filled, the table will be
		flexible. Otherwise, the table will only fit this size. This should be
		a tuple of (rows, columns).
		"""
		self.name = name
		self.size = None

		self.rows = []
		self.columns = []

		if size is not None:
			for x in range(size[0]):
				self.add_row([None for y in range(size[1])])

		self.size = size

	def add_row(self, row:(list, tuple)):
		"""
		Adds a row to the end of the table.
		Throws an exception if there is not enough values or too many values
		in the row.
		:param row: A list or tuple of values to add.
		"""
		# Throwing the exception
		if self.rows != [] and len(self.rows[0]) != len(row):
			raise Exception(f"Row length should be {len(self.rows[0])}, got {len(row)}")
		elif self.size is not None:
			raise Exception("Can't modify the table size if the size is fixed.")

		# Adding a new row to the table
		self.rows.append([])

		# Storing the values in the table
		for value in row:
			self.rows[-1].append(TableElement(value))

		# Putting the values in the columns
		if self.columns == []:  # If there is still nothing in the columns, we initialize them
			for value in row:
				self.columns.append([TableElement(value)])
		else:  # Adding them to the existing columns
			for index, value in enumerate(row):
				self.columns[index].append(TableElement(value))

	def add_column(self, column:(list, tuple)):
		"""
		Adds a column to the end of the table.
		Throws an exception if there is not enough values or too many values
		in the column.
		:param column: A list or tuple of values to add.
		"""
		# Throwing the exception
		if self.columns != [] and len(self.columns[0]) != len(column):
			raise Exception(f"Column length should be {len(self.columns[0])}, got {len(column)}")
		elif self.size is not None:
			raise Exception("Can't modify the table size if the size is fixed.")

		# Adding a new column to the table
		self.columns.append([])
		for value in column:
			self.columns[-1].append(TableElement(value))

		# Modifying the rows in consequence
		for index, value in enumerate(column):
			try:
				self.rows[index].append(TableElement(value))
			except IndexError:
				self.rows.append([])
				self.rows[index].append(TableElement(value))

	def add_rows(self, rows:(list, tuple)):
		"""
		Adds multiple rows to the table.
		:param row: A tuple/list of tuples/lists.
		"""
		for row in rows:
			self.add_row(row)

	def add_columns(self, columns:(list, tuple)):
		"""
		Adds multiple columns to the table.
		:param columns: A tuple/list of tuples/lists.
		"""
		for column in columns:
			self.add_column(column)

	def delete_row(self, index:int):
		"""
		Deletes the specified row.
		:param index: The index of the row.
		"""
		if index <= - len(self.rows) or index >= len(self.rows):
			raise Exception(f"Row index cannot be {index}, the length of the row is {len(self.rows)}.")
		elif self.size is not None:
			raise Exception("Can't modify the table size if the size is fixed.")

		# Removing the row
		self.rows.pop(index)
		# Removing the row from the columns
		for i in range(len(self.columns)):
			self.columns[i].pop(index)

	def delete_column(self, index:int):
		"""
		Deletes the specified column.
		:param index: The index of the column.
		"""
		if index <= - len(self.columns) or index >= len(self.columns):
			raise Exception(f"Column index cannot be {index}, the length of the column is {len(self.columns)}.")
		elif self.size is not None:
			raise Exception("Can't modify the table size if the size is fixed.")

		# Removing the row
		self.columns.pop(index)
		# Removing the row from the columns
		for i in range(len(self.rows)):
			self.rows[i].pop(index)

	def return_rows(self):
		"""
		:return: The rows as a list of lists.
		"""
		returnable_list = []

		for row in self.rows:
			returnable_list.append([])
			for value in row:
				returnable_list[-1].append(value.value)

		return returnable_list

	def return_columns(self):
		"""
		:return: The columns as a list of lists.
		"""
		returnable_list = []

		for column in self.columns:
			returnable_list.append([])
			for value in column:
				returnable_list[-1].append(value.value)

		return returnable_list

	def render_table(self, row_numbers_enabled:bool=True):
		"""
		Prints a stylized view of the table.
		:param row_numbers_enabled: Display the number of rows.
		"""
		if self.name is not None:
			print("-"*3, self.name, "-"*3)
		for row_number, row in enumerate(self.rows):
			if row_numbers_enabled is True:
				print(row_number, "->", end=" ")
			print("|", end=" ")
			for cell in row:
				if cell.name is not None:
					print(cell.name, ":", end=" ")
				print(cell.value, end=" | ")
			print()

	def set_element(self, row:int, column:int, value, name:str=None):
		"""
		Sets the value of an element.
		:param row: The row number.
		:param column: The column number.
		:param value: The value to insert in this cell.
		:param name: The name of the cell (optional).
		"""
		# If the row doesn't exist
		if row > len(self.rows) or row < - len(self.rows):
			raise Exception(f"Row number should be between -{len(self.rows)} and {len(self.rows)}, not {row}.")
		elif column > len(self.columns) or column < - len(self.columns):
			raise Exception(f"Column number should be between -{len(self.columns)} and {len(self.columns)}, not {column}.")

		self.rows[row][column] = TableElement(value, name=name)
		self.columns[column][row] = TableElement(value, name=name)


class TableElement:
	"""
	The value in a cell.
	"""
	def __init__(self, value, name:str=None):
		"""
		:param value: The value of the element.
		:param name: The name of the element (optional).
		"""
		self.value = value
		self.name = name
