# NCAA-Calculations

# Tests
`nosetests -v` will run all of the tests in the project in a test file and display the name of the test being run.
See `src/test_school.py` for a simple example for creating a test file.

You may want to have `nose-watch` running while doing dev since it will auto run tests as you make changes so you can tell when you have broken something and also hopefully push you more toward test driven development.

Simply open a terminal next to your IDE (or in it) and run `nosetests [-v] --with-watch`. Tests relevant to your changes will rerun whenever you change the file.
