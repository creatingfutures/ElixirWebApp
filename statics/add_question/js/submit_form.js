$('.form-group button').click(() => {
    fetch('/add_question/', {
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