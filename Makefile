say_hi:
	@echo "Hi!" $(name)

create_env:
	python -m venv venv/normenv

cleanup:
	@echo "starting to remove cache and build folders.."
	rm -rf __pycache__
	rm -rf .ipynb_checkpoints
	rm -rf **/__pycache__
	rm -rf **/.ipynb_checkpoints
	rm -rf dist
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info
	@echo "done!"

package_it:
	python setup.py sdist bdist_wheel

publist_to:
	twine upload -r pypitest dist/*
