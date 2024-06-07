from lib.department import Department
from lib.__init__ import CONN, CURSOR

class TestDepartment:
    @classmethod
    def setup_class(cls):
        Department.create_table()

    @classmethod
    def teardown_class(cls):
        Department.drop_table()

    def setup_method(self, method):
        Department.drop_table()
        Department.create_table()

    def teardown_method(self, method):
        CONN.commit()

    def test_creates_table(self):
        Department.create_table()
        sql = "SELECT name FROM sqlite_master WHERE type='table' AND name='departments';"
        result = CURSOR.execute(sql).fetchone()
        assert result is not None

    def test_drops_table(self):
        Department.drop_table()
        sql = "SELECT name FROM sqlite_master WHERE type='table' AND name='departments';"
        result = CURSOR.execute(sql).fetchone()
        assert result is None

    def test_saves_department(self):
        department = Department(name="Finance", location="Building D")
        department.save()
        assert department.id is not None

    def test_creates_department(self):
        department = Department.create(name="Marketing", location="Building E")
        assert department.id is not None

    def test_updates_row(self):
        department = Department.create(name="Legal", location="Building F")
        department.name = "Legal Affairs"
        department.location = "Building F, 3rd Floor"
        department.update()
        updated_department = CURSOR.execute("SELECT * FROM departments WHERE id = ?", (department.id,)).fetchone()
        assert updated_department[1] == "Legal Affairs"
        assert updated_department[2] == "Building F, 3rd Floor"

    def test_deletes_record(self):
        department = Department.create(name="Research", location="Building G")
        department.delete()
        deleted_department = CURSOR.execute("SELECT * FROM departments WHERE id = ?", (department.id,)).fetchone()
        assert deleted_department is None
