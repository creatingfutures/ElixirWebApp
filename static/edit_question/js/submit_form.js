$('.form-group button').click(() => {
    question_pk = window.location.pathname.split('/').slice(-1, )
    fetch(`/edit_question/${question_pk}`, {
        method: 'POST',
        body: new FormData(document.querySelector('#box form')),
    }).then(res => res.json()).then(res => {
        if (!res.ok) {
            $('.error').html(`${res.message}`)
        } else {
            window.location.replace(`${window.location.origin}/questions/`)
        }
    })
})