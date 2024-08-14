from django.test import SimpleTestCase, TestCase

from testapp.models import Company


class SqliteDatabaseTest(TestCase):
    """
    This serves as the control group for testing the SQLite database.
    """
    databases = ["default",]
    def setUp(self) -> None:
        # Specify the database name here (e.g., 'default', 'sqlite', 'mysql')
        self.db = 'default'

        Company.objects.using(self.db).create(name="Acme Corp", address="123 Elm St",
                                              established_date="2000-01-01")
        Company.objects.using(self.db).create(name="Globex", address="456 Oak St", established_date="2010-05-15")
        Company.objects.using(self.db).create(name="Initech", address="789 Pine St", established_date="1999-11-10")
        Company.objects.using(self.db).create(name="Hooli", address="101 Maple St", established_date="2005-07-20")

    def tearDown(self) -> None:
        Company.objects.using(self.db).all().delete()

    def test_all(self):
        """Test the all() method to return all objects."""
        companies = Company.objects.using(self.db).all()
        self.assertEqual(companies.count(), 4)

    def test_filter(self):
        """Test the filter() method to retrieve specific objects."""
        companies = Company.objects.using(self.db).filter(name__icontains="Corp")
        self.assertEqual(companies.count(), 1)
        self.assertEqual(companies.first().name, "Acme Corp")

    def test_exclude(self):
        """Test the exclude() method to exclude specific objects."""
        companies = Company.objects.using(self.db).exclude(name="Globex")
        self.assertEqual(companies.count(), 3)
        self.assertNotIn("Globex", [company.name for company in companies])

    def test_get(self):
        """Test the get() method to retrieve a single object."""
        company = Company.objects.using(self.db).get(name="Initech")
        self.assertEqual(company.address, "789 Pine St")

    def test_order_by(self):
        """Test the order_by() method to order the objects."""
        companies = Company.objects.using(self.db).order_by("established_date")
        self.assertEqual(companies.first().name, "Initech")

    def test_reverse(self):
        """Test the reverse() method to reverse the ordering of objects."""
        companies = Company.objects.using(self.db).order_by("established_date").reverse()
        self.assertEqual(companies.first().name, "Globex")

    def test_count(self):
        """Test the count() method to count the number of objects."""
        company_count = Company.objects.using(self.db).count()
        self.assertEqual(company_count, 4)

    def test_exists(self):
        """Test the exists() method to check if objects exist."""
        exists = Company.objects.using(self.db).filter(name="Hooli").exists()
        self.assertTrue(exists)

    def test_first(self):
        """Test the first() method to get the first object."""
        first_company = Company.objects.using(self.db).order_by("established_date").first()
        self.assertEqual(first_company.name, "Initech")

    def test_last(self):
        """Test the last() method to get the last object."""
        last_company = Company.objects.using(self.db).order_by("established_date").last()
        self.assertEqual(last_company.name, "Globex")


class LibSQLDatabaseTest(SimpleTestCase):
    """
    Testing that the same tests work on a libSQL database.
    """
    databases = ["libsql", "default"]

    def setUp(self) -> None:
        # Specify the database name here (e.g., 'default', 'sqlite', 'mysql')
        self.db = 'libsql'

        Company.objects.using(self.db).create(name="Acme Corp", address="123 Elm St",
                                              established_date="2000-01-01")
        Company.objects.using(self.db).create(name="Globex", address="456 Oak St", established_date="2010-05-15")
        Company.objects.using(self.db).create(name="Initech", address="789 Pine St", established_date="1999-11-10")
        Company.objects.using(self.db).create(name="Hooli", address="101 Maple St", established_date="2005-07-20")

    def tearDown(self) -> None:
        Company.objects.using(self.db).all().delete()

    def test_all(self):
        """Test the all() method to return all objects."""
        companies = Company.objects.using(self.db).all()
        self.assertEqual(companies.count(), 4)

    def test_filter(self):
        """Test the filter() method to retrieve specific objects."""
        companies = Company.objects.using(self.db).filter(name__icontains="Corp")
        self.assertEqual(companies.count(), 1)
        self.assertEqual(companies.first().name, "Acme Corp")

    def test_exclude(self):
        """Test the exclude() method to exclude specific objects."""
        companies = Company.objects.using(self.db).exclude(name="Globex")
        self.assertEqual(companies.count(), 3)
        self.assertNotIn("Globex", [company.name for company in companies])

    def test_get(self):
        """Test the get() method to retrieve a single object."""
        company = Company.objects.using(self.db).get(name="Initech")
        self.assertEqual(company.address, "789 Pine St")

    def test_order_by(self):
        """Test the order_by() method to order the objects."""
        companies = Company.objects.using(self.db).order_by("established_date")
        self.assertEqual(companies.first().name, "Initech")

    def test_reverse(self):
        """Test the reverse() method to reverse the ordering of objects."""
        companies = Company.objects.using(self.db).order_by("established_date").reverse()
        self.assertEqual(companies.first().name, "Globex")

    def test_count(self):
        """Test the count() method to count the number of objects."""
        company_count = Company.objects.using(self.db).count()
        self.assertEqual(company_count, 4)

    def test_exists(self):
        """Test the exists() method to check if objects exist."""
        exists = Company.objects.using(self.db).filter(name="Hooli").exists()
        self.assertTrue(exists)

    def test_first(self):
        """Test the first() method to get the first object."""
        first_company = Company.objects.using(self.db).order_by("established_date").first()
        self.assertEqual(first_company.name, "Initech")

    def test_last(self):
        """Test the last() method to get the last object."""
        last_company = Company.objects.using(self.db).order_by("established_date").last()
        self.assertEqual(last_company.name, "Globex")
