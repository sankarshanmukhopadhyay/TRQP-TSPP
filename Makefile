.PHONY: validate flagship-check assurance-check evidence v3-candidate-check

validate:
	python scripts/validate_repository.py
	python scripts/schema_check.py
	python scripts/verify_al_contract.py
	python scripts/validate_project_status.py
	python -m compileall -q harness scripts examples schemas
	python scripts/v3_profile_validator.py
	python scripts/test_v3_profile_validator.py

v3-candidate-check:
	python scripts/test_wp8_evidence_validator.py
	python scripts/v3_profile_validator.py
	python scripts/test_v3_profile_validator.py

assurance-check: validate
	python scripts/generate_assurance_artifacts.py

evidence: assurance-check

flagship-check:
	python scripts/validate_repository.py
