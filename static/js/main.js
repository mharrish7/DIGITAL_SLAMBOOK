

$('.log').on('click',function(){
    window.location.href = '/auth'
})

$('.nlog').on('submit',function(ev){
    var n = $('#name').val();
    var pass = $('#pass').val();
    $.ajax({
        url : '/nlog',
        data: {
            nt : n,
            passt : pass},
        type: 'POST'
    }).done(function(data){
        if(data['info'] == 'correct'){
            window.location.href = '/nlog2';
        }
        else{
            $(".rinfo").text(data['info']);
        }
        
    });

    ev.preventDefault();
})