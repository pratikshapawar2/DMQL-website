from db import db

class Department(db.Model):
    __tablename__ = 'department'  # Use the exact table name from your database

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)  # Adjust columns based on your table schema
    # Add other columns as per your database table

    def __repr__(self):
        return f"<Department {self.name}>"
