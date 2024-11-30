from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///students.db"
db = SQLAlchemy(app)

class Student(db.Model):
    __tablename__: str = 'student'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Student('{self.name}', '{self.surname}', {self.age})"


@app.route('/add_students', methods=['GET', 'POST'])
def add_students():
    students = [
        Student(name='Stepan', surname='Ivanov', age=21),
        Student(name='Alesha', surname='Popov', age=19),
        Student(name='Whitney', surname='Houston', age=20),
        Student(name='Spider', surname='Man', age=21)
    ]
    db.session.add_all(students)
    db.session.commit()
    return jsonify({'message': 'Студенты добавлены'})

@app.route('/get_students_over_20', methods=['GET'])
def get_students_over_20():
    students = Student.query.filter(Student.age > 20).all()
    return jsonify([student.name for student in students])

@app.route('/get_students_sorted_by_age', methods=['GET'])
def get_students_sorted_by_age():
    students = Student.query.order_by(Student.age).all()
    return jsonify([student.name for student in students])

@app.route('/get_all_students', methods=['GET'])
def get_all_students():
    students = Student.query.all()
    return jsonify([student.name for student in students])

@app.route('/get_student_with_id_1', methods=['GET'])
def get_student_with_id_1():
    student = Student.query.filter(Student.id == 1).one_or_none()
    if student:
        return jsonify({'name': student.name, 'surname': student.surname, 'age': student.age})
    else:
        return jsonify({'message': 'Студент не найден'})

@app.route('/get_first_student', methods=['GET'])
def get_first_student():
    student = Student.query.first()
    if student:
        return jsonify({'name': student.name, 'surname': student.surname, 'age': student.age})
    else:
        return jsonify({'message': 'Студенты не найдены'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=5000, debug=True)

