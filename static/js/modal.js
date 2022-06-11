const ticketImg= document.getElementById('ticketImg');
console.log('working modal');

$('.attachmentImg').click(function(){
    let attImg  = this.getAttribute('src')
    ticketImg.setAttribute('src', attImg);
    console.log(attImg);
})

// console.log(attachments);


