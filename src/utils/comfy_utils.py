import random
from src.constants import USE_MODEL


def call_node(node, kwargs):
    node_inject_func_name = getattr(node, "FUNCTION")
    node_injuect_func = getattr(node, node_inject_func_name)
    return node_injuect_func(**kwargs)


def random_inputs(INPUT_TYPES, exclude_fields):
    """
    Go through the input fields for a node and for whichever fields are not in exclude_fields,
    generate a random value for that field (within the field's range/selection/etc.).

    For example, if testing a node for image size permutations, the IMAGE fields will be the
    exclude_fields, and the rest of the fields should be set as random values - like if there is
    an INT field called "threshold" with max=100 and min=0, the threshold should be set to a
    random number between 0 and 100.

    Returns a dictionary of the inferred kwargs to be used when calling the node being tested.

    Currently only being applied to the required fields.
    TODO: Apply to optional fields as well if specified by an optional argument/config option.
    """

    inferred_kwargs = {}
    for field_ui_name, field_config in INPUT_TYPES["required"].items():
        if field_ui_name in exclude_fields:
            continue

        field_type = field_config[0]

        if isinstance(field_type, list):
            inferred_kwargs[field_ui_name] = random.choice(field_type)
        elif field_type.upper() == "BOOLEAN":
            inferred_kwargs[field_ui_name] = random.choice([True, False])
        elif (
            field_type.upper() == "INTEGER"
            or field_type.upper() == "INT"
            or field_type.upper() == "FLOAT"
        ):
            try:
                if field_type.upper() == "FLOAT":
                    inferred_kwargs[field_ui_name] = random.uniform(
                        field_config[1]["min"], field_config[1]["max"]
                    )
                else:
                    inferred_kwargs[field_ui_name] = random.randint(
                        field_config[1]["min"], field_config[1]["max"]
                    )
            except KeyError:
                raise AttributeError(
                    f"Field {field_ui_name} is an INT or FLOAT type, but does not have a valid range specified with 'min' and 'max' attributes."
                )
        elif field_type.upper() == "STRING":
            inferred_kwargs[field_ui_name] = "test_string"
        elif field_type.upper() == "MODEL":
            # TODO: conditional logic for model type
            inferred_kwargs[field_ui_name] = USE_MODEL
        elif field_type.upper() == "CONDITIONING":
            # TODO
            pass
        elif field_type.upper() == "IMAGE" or field_type.upper() == "IMAGES":
            # TODO import the generate random noise image function for this
            pass
        elif field_type.upper() == "MASK":
            pass
        else:
            raise AttributeError(f"Field type {field_type} is not recognized.")

    return inferred_kwargs
