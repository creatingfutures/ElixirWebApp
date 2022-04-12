$("#id_program").change(() => {
    const program_id = $("#id_program").val();
    $.ajax({
        url: '/ajax/load_modules/',
        type: 'GET',
        data: {
            program_id
        },
        success: data => {
            $("#id_module").html(
                data);
        }
    });
});

$("#id_module").change(() => {
    const module_id = $("#id_module").val();
    $.ajax({
        url: '/ajax/load_levels/',
        type: 'GET',
        data: {
            module_id
        },
        success: data => {
            $("#id_level").html(
                data);
        }
    });
});