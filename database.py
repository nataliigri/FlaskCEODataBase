import json
from datetime import time

class Field:
    def __init__(self, name, field_type):
        self.name = name
        self.type = field_type

    def validate(self, value):
        if self.type == "integer":
            return isinstance(value, int)
        elif self.type == "real":
            return isinstance(value, float)
        elif self.type == "char":
            return isinstance(value, str) and len(value) == 1
        elif self.type == "string":
            return isinstance(value, str)
        elif self.type == "time":
            return isinstance(value, time)
        return False


class Record:
    def __init__(self, data):
        self.data = data

    def validate(self, fields):
        for field in fields:
            if field.name in self.data:
                if not field.validate(self.data[field.name]):
                    raise Exception(f"Invalid value for field '{field.name}'")
        return True


class Table:
    def __init__(self, name):
        self.name = name
        self.fields = []
        self.records = []

    def add_field(self, field):
        self.fields.append(field)

    def edit_field(self, old_field_name, new_field):
        for i, field in enumerate(self.fields):
            if field.name == old_field_name:
                self.fields[i] = new_field
                return
        raise Exception("Field not found")

    def remove_field(self, field_name):
        for i, field in enumerate(self.fields):
            if field.name == field_name:
                del self.fields[i]
                return
        raise Exception("Field not found")

    def add_record(self, record):
        if not set(record.data.keys()).issubset({field.name for field in self.fields}):
            raise Exception("Invalid field names in record.")
        if record.validate(self.fields):
            self.records.append(record)
        else:
            raise Exception("Record validation failed")

    def to_dict(self):
        return {
            "fields": [(field.name, field.type) for field in self.fields],
            "records": [record.data for record in self.records]
        }

    @classmethod
    def from_dict(cls, name, data):
        table = cls(name)
        for field in data["fields"]:
            table.add_field(Field(field[0], field[1]))
        for record_data in data.get("records", []):
            table.add_record(Record(record_data))
        return table

    def view_records(self):
        return [record.data for record in self.records]


class Database:
    def __init__(self, name):
        self.name = name
        self.tables = {}

    def create_table(self, table_name):
        if table_name not in self.tables:
            self.tables[table_name] = Table(table_name)
        else:
            raise Exception("Table already exists")

    def remove_table(self, table_name):
        if table_name in self.tables:
            del self.tables[table_name]
        else:
            raise Exception("Table does not exist")

    def add_field_to_table(self, table_name, field):
        if table_name in self.tables:
            self.tables[table_name].add_field(field)
        else:
            raise Exception("Table does not exist")

    def edit_field_in_table(self, table_name, old_field_name, new_field):
        if table_name in self.tables:
            self.tables[table_name].edit_field(old_field_name, new_field)
        else:
            raise Exception("Table does not exist")

    def remove_field_from_table(self, table_name, field_name):
        if table_name in self.tables:
            self.tables[table_name].remove_field(field_name)
        else:
            raise Exception("Table does not exist")

    def add_record_to_table(self, table_name, record_data):
        if table_name in self.tables:
            record = Record(record_data)
            self.tables[table_name].add_record(record)
        else:
            raise Exception("Table does not exist")

    def save_to_disk(self):
        with open(f"{self.name}.json", "w") as f:
            data = {table_name: table.to_dict() for table_name, table in self.tables.items()}
            json.dump(data, f)

    def load_from_disk(self):
        try:
            with open(f"{self.name}.json", "r") as f:
                data = json.load(f)
                for table_name, table_data in data.items():
                    self.tables[table_name] = Table.from_dict(table_name, table_data)
        except FileNotFoundError:
            raise Exception("Database file not found")

    def view_table(self, table_name):
        if table_name in self.tables:
            return self.tables[table_name].to_dict()
        else:
            raise Exception("Table does not exist")

    def view_all_tables(self):
        return {table_name: table.to_dict() for table_name, table in self.tables.items()}

    def join_tables(self, table1_name, table2_name, common_field_name):
        if table1_name not in self.tables or table2_name not in self.tables:
            raise Exception("Одна з таблиць не існує.")

        table1 = self.tables[table1_name]
        table2 = self.tables[table2_name]

        common_field1 = next((f for f in table1.fields if f.name == common_field_name), None)
        common_field2 = next((f for f in table2.fields if f.name == common_field_name), None)

        if common_field1 is None or common_field2 is None:
            raise Exception("Спільне поле не знайдено у одній з таблиць.")

        joined_records = []

        records1 = table1.view_records()
        records2 = table2.view_records()

        for record1 in records1:
            for record2 in records2:
                if record1[common_field1.name] == record2[common_field2.name]:
                    joined_record = {**record1, **record2}
                    joined_records.append(joined_record)

        if not joined_records:
            raise Exception("Сполучених записів не знайдено.")

        return joined_records

if __name__ == "__main__":
    # Для тестування
    db = Database("test_db")
    print(db.name)

