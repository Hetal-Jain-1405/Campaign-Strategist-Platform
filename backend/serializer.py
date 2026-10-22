import json

def serialize(data):
    if hasattr(data, "model_dump_json"):
        return data.model_dump_json(indent=2)

    return json.dumps(data, indent=2, default=str)
