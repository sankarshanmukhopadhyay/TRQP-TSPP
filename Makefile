.PHONY: validate flagship-check

validate:
	python scripts/validate_repository.py
	python scripts/schema_check.py
	python scripts/verify_al_contract.py
	python -m compileall -q harness scripts examples schemas

flagship-check:
	python scripts/validate_repository.py
