add_option = () => {
    const form_idx = $('#id_form-TOTAL_FORMS').val();
    if (form_idx >= 4) {
        return null
    }
    option_html = ''
    $('.empty_form').children().each((index, item) => {
        item_html = $(item).prop('outerHTML').replace(/__prefix__/g, form_idx).replace(/Option /g,
            `Option ${parseInt(form_idx) + 1}`)

        option_html += index % 2 == 0 ? `<p>${item_html}` : `${item_html}</p>`
    })
    $('.options').append(`<div class="option">${option_html}</div>`);
    $('#id_form-TOTAL_FORMS').val(parseInt(form_idx) + 1);
}

$('.add_option').click(add_option);

$('.delete_option').click(() => {
    const form_idx = $('#id_form-TOTAL_FORMS').val();
    if (form_idx <= 0) {
        return null
    }
    $('#id_form-TOTAL_FORMS').val(parseInt(form_idx) - 1);
    $('.options .option').last().remove();
});