from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response:
        if (
            "non_field_errors" in response.data
            and "unique" == response.data.get("non_field_errors")[0].code
        ):
            response.data["detail"] = (
                "Já existe um relatório para este paciente nesta data."
            )
    return response
