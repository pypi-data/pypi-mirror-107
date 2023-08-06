import logging
from jsonschema import validate, ValidationError, SchemaError


INPUTTED_REPORT_SCHEMA = {
    "type": "object",
    "properties": {
        "incidents": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "source": {
                        "type": "object",
                        "properties": {
                            "ip": {"type": "string"},
                            "domain": {"type": "string"},
                            "country": {"type": "string"},
                            "opswat_scans": {
                                "type": "array",
                                "items": {"type": "string"}
                            },
                            "opswat_tags": {
                                "type": "array",
                                "items": {"type": "string"}
                            },
                            "gn_classification": {"type": "string"},
                            "gn_organization": {"type": "string"},
                            "gn_tags": {
                                "type": "array",
                                "items": {"type": "string"}
                            }
                        }
                    },
                    "destination": {
                        "type": "object",
                        "properties": {
                            "ip": {"type": "string"},
                            "domain": {"type": "string"},
                            "country": {"type": "string"},
                            "opswat_scans": {
                                "type": "array",
                                "items": {"type": "string"}
                            },
                            "opswat_tags": {
                                "type": "array",
                                "items": {"type": "string"}
                            },
                            "gn_classification": {"type": "string"},
                            "gn_organization": {"type": "string"},
                            "gn_tags": {
                                "type": "array",
                                "items": {"type": "string"}
                            }
                        }
                    }
                }
            }
        }
    }
}

GC_CSV_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "severity": {"enum": ["Low", "Medium", "High"]},
        "start_time (utc)": {"type": "string"},
        "incident_type": {"enum": ["Incident", "Deception", "Network Scan", "Reveal", "Experimental"]},
        "affected_assets": {"type": "string"},
        "tags": {"type": "string"},
        "incident_group": {"type": "string"},
        "exporting_error": {"type": "string"}
    },
    "required": ["id", "affected_assets"]
}

CENTRA_SCHEMA = {
    "type": "object",
    "properties": {
        "username": {"type": "string"},
        "dev_host": {"type": "string"},
        "password": {"type": "string"}
    },
    "required": ["username", "dev_host", "password"]
}


def is_valid_format(entity, schema) -> bool:
    valid = False
    try:
        validate(entity, schema)
        valid = True
    except (ValidationError, SchemaError):
        logging.error(f"Object validation failed.", exc_info=True)
    finally:
        return valid
