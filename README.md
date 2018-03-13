# NCAA-Calculations

# Virtualenv
It's good practice to run a virtual env so the different installations don't step on each other for other projects. Check out this documentation: https://virtualenv.pypa.io/en/stable/userguide/

Once it is installed, in your project directory run the following command one time
`virtualenv .`
This will create the `bin` file and everything else needed for the virtualenv.

Going forward you can activate and deactivate like so
`source bin/activate`
`deactivate`

With the environment activated run
`pip2 install -r requirements.txt`
to install all of the project pre-reqs.
Then run the following command to run the code
`python2 server.py`

# Tests
`nosetests -v` will run all of the tests in the project in a test file and display the name of the test being run.
See `src/test_school.py` for a simple example for creating a test file.

You may want to have `nose-watch` running while doing dev since it will auto run tests as you make changes so you can tell when you have broken something and also hopefully push you more toward test driven development.

Simply open a terminal next to your IDE (or in it) and run `nosetests [-v] --with-watch`. Tests relevant to your changes will rerun whenever you change the file.
