all:
	touch ./wayround_org/__init__.py
	./setup.py build_ext --inplace
	rm ./wayround_org/__init__.py
