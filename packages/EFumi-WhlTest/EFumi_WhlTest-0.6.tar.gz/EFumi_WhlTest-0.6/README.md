## Example Project

Not much to see here, mostly all applied from
[Packaging Python Projects](https://packaging.python.org/tutorials/packaging-projects/).

### Create wheel

Prepare system

```bash
python3 -m pip install --upgrade build
```

Build `.whl` file

```bash
python3 -m build
```

Find your `.whl` in `dist/`.

### Try installing your wheel

```bash
# create a virtual env so it can be deleted easily by deleting `myvirtualenv`
python3 -m venv myvirtualenv
# enable virtual env
source myvirtualenv/bin/activate
# install wheel
python3 -m pip install dist/dist/wheelie-0.0.1-py3-none-any.whl
# run program
myvirtualenv/bin/main.py
```
