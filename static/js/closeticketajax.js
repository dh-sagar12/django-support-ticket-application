console.log('working');


$('.openTicketBtn').click(function() {
    let ticketId =  this.getAttribute('value')
    let url =  this.getAttribute('url')
    let csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
    console.log(url, csrftoken);
    if (ticketId != null){
        $.ajax({
            type: 'POST', 
            url: url,
            data: {
                id: ticketId,
                csrfmiddlewaretoken: csrftoken,
            },
            success:(data)=>{
                console.log(data)
                $('.msgRes').addClass('messages')
                $('.msgRes').text(data.res)
                
                if (data.status == false){
                    console.log('herer');
                    setTimeout(() => {
                        location.reload()
                    }, 1000);
                }
                else if (data.status == true){
                    setTimeout(() => {
                        $('.msgRes').removeClass('messages')
                        $('.msgRes').text('')
                    }, 1000);
                }

            }
        })
    }


})



$('.closeBtn').click(function() {
    let ticketId = this.getAttribute('value')
    let url = this.getAttribute('url')
    console.log(url);
    let csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

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
