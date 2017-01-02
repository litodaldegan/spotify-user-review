var mountPlaylists = function () {
    
    $.ajax({
        type: 'GET',
        url: '/profile/playlists/5',
        success: function (response) {

            for (var i = 0; i < response.playlists.length; i++){
                var show_playlist = $($.parseHTML('<div></div>'));
                var img = $($.parseHTML('<img>'));
                var p = $($.parseHTML('<p></p>'));
                var a = $($.parseHTML('<a></a>'));

                img.attr('src', response.playlists[i].image)
                    .addClass('playlist-img');

                p.html(response.playlists[i].name.substring(0, 60))
                    .attr('title', response.playlists[i].name);

                a.attr("href", response.playlists[i].url)
                    .attr("target", "_black")
                    .append(img);


                show_playlist.addClass('playlist')
                    .addClass('col-xs-12 col-sm-6 col-md-4 col-lg-4')
                    .append(a)
                    .append(p);
                $('#playlists').append(show_playlist);
            }
        }
    });
}

var clickInfo = function () {
    document.getElementById('avatar').addEventListener('click', function (e) {
        info = document.getElementById('display_info');

        if (info.style.height == "60px")
            info.style.height = "190px";
        else
            info.style.height = "60px";
    });
}

$(document).ready(function() {

    mountPlaylists();
    clickInfo();
});