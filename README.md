# Dev Setup
1. Clone the repo: `git clone git@github.com:simplefractal/hs-oaq.git`;
2. Create a virtualenv for Python 3.5: `mkvirtualenv hs-oaq -p /usr/bin/python3.5`;
3. Copy default postactivate: `cp contrib/proj_postactivate /your-virtualenvs-dir/hs-oaq/bin/postactivate`;
4. Edit `/your-virtualenvs-dir/hs-oap/bin/postactivate` for you custom env config and re-run the `workon` command;
5. Install the packages: `pip install -r dev-requirements.txt`;
6. Create postgres db: `createdb hs_oaq`;
7. Install redis ([click here](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-redis) if you're using Ubuntu)
8. Migrations: `python manage.py migrate`
9. Create admin user: `python manage.py createsuperuser`
10. Runserver: `python manage.py runserver`
11. Run django-rq for email sending: `python manage.py rqworker high low default`
12. Running the tests (you must run it inside `project` directory): `pytest'


# Alternative env setup
1. You can also create a `.env` file inside of `config` similar to `.env-example`


# Git Workflow
0. Create feature branch off of `develop` with the `feature` prefix such as `feature/sso-login`
1. Develop and commit in this branch
2. Make sure tests are passing with `pytest` command from the `project` directory
3. When finished, open a pull request
4. When reviewed and updated, merge into develop with the following commands or just use the Github merge button and remember deleting the remote branch:

```bash
$ git checkout develop
$ git merge --no-ff feature/sso-login
$ git push origin develop
$ git push origin :feature/sso-login  # deletes remote branch
```
