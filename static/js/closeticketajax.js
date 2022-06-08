console.log('working');
$('.closeBtn').click(function () {
    let ticketId = this.getAttribute('value')
    let url = this.getAttribute('url')
    console.log(url);
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    if (ticketId != null) {
        $.ajax({
            type: 'POST',
            url: url,
            data: {
                id: ticketId,
                csrfmiddlewaretoken: csrftoken,
            },
            success: (data) => {
                console.log(data);
                $('.msgRes').addClass('messages')

                // // document.querySelector('.msgRes').classList.add('messages')
                // // document.querySelector('.msgRes').InnerText = data
                $('.msgRes').text(data.res)

                if (data.status != 'closed'){

                    setTimeout(() => {
                        location.reload()
                    }, 1000);
                }
                else{
                    setTimeout(() => {
                        $('.msgRes').removeClass('messages')
                        $('.msgRes').text('')
                    }, 1000);
                }

            }
        })
    }
})
