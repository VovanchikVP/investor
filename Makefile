requirements:
	pipenv lock --clear
	pipenv install --dev
	pipenv run pre-commit install