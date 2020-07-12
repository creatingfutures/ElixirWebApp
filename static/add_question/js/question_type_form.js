show_question_type_form = () => {
    const question_type = $("#id_question_type option:selected").val()
    $.ajax({
        url: '/ajax/question_type_form/',
        data: {
            question_type
        },
        success: (data) => $('.question_type_form').html(data)
    })
    $('.form-group').css('display', 'block')
}
$("#id_question_type").change(show_question_type_form)