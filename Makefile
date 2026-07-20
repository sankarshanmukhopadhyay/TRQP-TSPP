.PHONY: validate flagship-check assurance-check evidence

validate:
	python scripts/validate_repository.py
	python scripts/schema_check.py
	python scripts/verify_al_contract.py
	python scripts/validate_project_status.py
	python -m compileall -q harness scripts examples schemas

assurance-check: validate
	python scripts/generate_assurance_artifacts.py

evidence: assurance-check

flagship-check:
	python scripts/validate_repository.py
