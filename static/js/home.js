$('.search').on('submit', function (ev) {
    var s = $('#searcht').val();
    var h = $('#hostel').val();
    var b = $('#branch').val();
    $.ajax({
        url: '/search',
        data: {
            st: s,
            ht: h,
            bt: b
        },
        type: 'POST'
    }).done(function (data) {
            document.querySelector('.results').innerHTML = "<hr>";
            f = data['con'];
        for (i of data['data']) {
            let t1 = "View Profile";
            // let t2 = ""
            // if (data['sent'].includes(i[1])) {
            //     t1 = "Sent";
            //     t2 = "disabled"
            // }



            if (i[1] == data['user']) {
                console.log('');
            } else {
                t4 = "";
                if(f[0].includes(i[1])){
                    t4 = "+1";
                }
                else if(f[1].includes(i[1])){
                    t4 = "+2";
                }
                else if(f[2].includes(i[1])){
                    t4 = "+3";
                }
                $('.results').append('<p>' + i[0] + "- @" + i[1] + "<span class = 'con'> " +  t4 +"</span>" + "</p>");
                $('.results').append('<p> ' + i[3] + " " + i[4] + "</p>");
                $('.results').append('<button class = ' + i[1] + ' ' + '>' + t1 + '</button>');
                document.querySelector('.' + i[1]).classList.add('veiw');
                $('.results').append('<hr>');
            }


        }
    });

ev.preventDefault();
})

$(document).on('click', '.veiw', function (ev) {
    var s = this.classList[0];
    let u = this;
    $.ajax({
        url: '/viewp',
        data: {
            st: s
        },
        type: 'POST'
    }).done(function (data) {
        $('.post').html("<h1>PROFILE</h1>");
        console.log(data);
        if (data['data'].length > 0) {
            let t = data['data'][0];
            let t1 = "Sent friends request";
            let t2 = ""
            console.log(data['friends'])
            if (data['friends'].includes(t[1])) {
                t1 = "Friends";
                t2 = "disabled"
            } else if (data['sent'].includes(t[1])) {
                t1 = "Sent";
                t2 = "disabled"
            }
            $('.post').append('<hr>');
            $('.post').append('<h2>' + t[0] + "</h2>");
            $('.post').append('<h3>' + t[1] + "</h3>");
            $('.post').append('<p> Email :' + t[2] + "</p>");
            $('.post').append('<p> Hostel :' + t[3] + "</p>");
            $('.post').append('<p> Branch :' + t[4] + "</p>");
            $('.post').append('<button class = ' + t[1] + ' ' + t2 + '>' + t1 + '</button>');
            $('.post').append('<hr>');
            document.querySelector('.' + t[1]).classList.add('req');
        } else {
            $('.post').append('Something is wrong');
        }

    });

})

$(document).on('click', '.req', function (ev) {
    var s = this.classList[0];
    let u = this;
    $.ajax({
        url: '/sfr',
        data: {
            st: s
        },
        type: 'POST'
    }).done(function (data) {
        if (data['info'] == 1) {
            console.log('ssd');
            console.log(u);
            u.innerHTML = "Sent";
            u.disabled = true;
        }

    });

})

$(document).on('click', '.fill', function (ev) {
    var s = this.classList[0];
    s = s.slice(0,-2);
    console.log(s);
    let u = this;
    document.querySelector('.fstitle').classList = ['fstitle'];
    document.querySelector('.fills').style.display = 'block';
    document.querySelector('.sumi').style.display = 'none';
    $('.fstitle').text(s + "'s SlamBook");
    document.querySelector('.fstitle').classList.add(s);
})



$('.fr').on('click', function (ev) {
    for(i of document.querySelectorAll('.nav')){
        i.style.backgroundColor = "#4D77FF";
    }
    this.style.backgroundColor = "rgba(0, 0, 0, 0.5)";
    $.ajax({
        url: '/fr',
        type: 'POST'
    }).done(function (data) {
        $('.post').html("<h1>Friends</h1>");

        if (data['data'].length > 0) {
            for (i of data['data']) {
                $('.post').append('<h2>' + i + "</h2>");
                $('.post').append('<hr>');

            }

        } else {
            $('.post').append('Go search in the right column to get some friends');
        }
    });


})

$('.fs').on('click', function (ev) {
    for(i of document.querySelectorAll('.nav')){
        i.style.backgroundColor = "#4D77FF";
    }
    this.style.backgroundColor = "rgba(0, 0, 0, 0.5)";
    $.ajax({
        url: '/fs',
        type: 'POST'
    }).done(function (data) {
        $('.post').html("<h1>Fill Slams</h1>");

        if (data['data'].length > 0) {
            t1 = 'Fill Slam';
            t2 = data['sent'];
            for (i of data['data']) {
                $('.post').append('<h2>' + i + "</h2>");
                d1 = i + 'fs';
                $('.post').append('<button class = ' + d1 + '>' + t1 + '</button>');
                if(t2.includes(i)){
                    d2 = i + 'fsc';
                    $('.post').append('<button class = ' + d2 + '>' + "Delete previous" + '</button>');
                    document.querySelector('.' + d2).classList.add('delete');
                }
                document.querySelector('.' + d1).classList.add('fill');
                console.log(document.querySelector('.' + d1));
                $('.post').append('<hr>');

            }

        } else {
            $('.post').append('You can fill slams only if you are friends');
        }

    });


})

$(document).on('click', '.delete', function (ev) {
    var s = this.classList[0];
    s = s.slice(0,-3);
    let u = this;
    $.ajax({
        url: '/dsl',
        data: {
            st: s
        },
        type: 'POST'
    }).done(function (data) {
        if (data['data'] == 1) {
            console.log('ssd');
            u.style.display = 'none';
        }

    });

})


$('.ys').on('click', function (ev) {
    for(i of document.querySelectorAll('.nav')){
        i.style.backgroundColor = "#4D77FF";
    }
    this.style.backgroundColor = "rgba(0, 0, 0, 0.5)";
    $.ajax({
        url: '/ys',
        type: 'POST'
    }).done(function (data) {
        $('.post').html("<h1>Your Slams</h1>");

        if (data['data'].length > 0) {
            for (d of data['data']) {
                $('.post').append("<h3>"  + d + "</h3>");
                let d1 = d + "ys";
                $('.post').append('<button class = ' + d1 + '>' + "View" + '</button>');
                document.querySelector('.' + d1).classList.add('show');
                $('.post').append('<hr>');

            }

        } else {
            $('.post').append('No slams received till now');
        }


    });


})

$(document).on('click', '.show', function (ev) {
    var s = this.classList[0];
    s = s.slice(0,-2);
    let u = this;
    $.ajax({
        url: '/showys',
        data: {
            st: s
        },
        type: 'POST'
    }).done(function (data) {
        let d = data['data'];
        console.log(d);
        document.querySelector('.shows').style.display = 'block';
        $('.shows2').html("<h1>Slam sent by " + d[1] + "</h1>");
        let d2 = data['Q'];
        for (let i = 2; i <= 7; i++) {
            $('.shows2').append("<h3>" + d2[i] + " </h3>");
            $('.shows2').append("<p>" + d[i] + " </p>");
            $('.shows2').append('<hr>');

        }
        $('.shows2').append('<h3> Memories </h3>');
        $('.shows2').append('<img class = "slami" src = "/static/images/' +data['user']  + "-"+ s + '.jpg" >');
    });

})


$('.frr').on('click', function (ev) {
    for(i of document.querySelectorAll('.nav')){
        i.style.backgroundColor = "#4D77FF";
    }
    this.style.backgroundColor = "rgba(0, 0, 0, 0.5)";
    $.ajax({
        url: '/frr',
        type: 'POST'
    }).done(function (data) {
        $('.post').html("<h1>Friend requests</h1>");

        if (data['data'].length > 0) {
            t1 = 'Accept friend request';
            console.log(data);
            for (i of data['data']) {

                $('.post').append('<h2>' + i + "</h2>");
                $('.post').append('<button class = ' + i + '>' + t1 + '</button>');
                $('.post').append('<hr>');

            }
            document.querySelector('.' + i).classList.add('acp');
        } else {
            $('.post').append('No requests right');
        }

    });


})


$(document).on('click', '.acp', function (ev) {
    var s = this.classList[0];
    let u = this;
    $.ajax({
        url: '/afr',
        data: {
            st: s
        },
        type: 'POST'
    }).done(function (data) {
        if (data['info'] == 1) {
            console.log('ssd');
            u.innerHTML = "Accepted";
            u.disabled = true;
        }

    });

})


$('.fills2').on('submit', function (ev) {
    var q1 = $('#q1').val();
    var q2 = $('#q2').val();
    var q3 = $('#q3').val();
    var q4 = $('#q4').val();
    var q5 = $('#q5').val();
    var q6 = $('#q6').val();
    var q7 = $('#q7').val();
    var tof = document.querySelector('.fstitle').classList[1];
    $.ajax({
        url: '/sendslam',
        data: {
            q1t: q1,
            q2t: q2,
            q3t: q3,
            q4t: q4,
            q5t: q5,
            q6t: q6,
            q7t: q7,
            st: tof
        },
        type: 'POST'
    }).done(function (data) {
        $('#res').text("Successfully sent");
        document.querySelector('.sumi').style.display = 'block';

    })
    ev.preventDefault();
});

$('.closeslam').on('click', function () {
    document.querySelector('.fills').style.display = 'none';
})

$('.closeshow').on('click', function () {
    document.querySelector('.shows').style.display = 'none';
})


$("#form").on("submit",function(e){
      formdata = new FormData($("#form")[0]);
      console.log(formdata);
      $.ajax({
          data :formdata,
          type : 'POST',
          url : '/pred',
          contentType: false,
          cache: false,
          processData: false
      })
      .done(function(data) {
        if(data.error){
          $('#res1').text(data['error']);
        }
        else{
          $('#res1').text("successfully upload");
        }
      });
      e.preventDefault();
  });