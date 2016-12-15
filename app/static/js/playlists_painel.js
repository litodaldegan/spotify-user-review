var mountPlaylists = function () {
    var playlists_name = [];
    for (var i = 0; i < playlists.length; i++) {
        var playlist = $($.parseHTML('<div></div>'));
        var img = $($.parseHTML('<img>'));
        var p = $($.parseHTML('<p></p>'));

        img.attr('src', playlists[i].image)
            .addClass('playlist-img img-responsive');
        p.html(playlists[i].name.substring(0, 60))
            .attr('title', playlists[i].name);

        playlist.addClass('playlist')
            .addClass('col-xs-6 col-sm-4 col-md-3 col-lg-2')
            .append(img)
            .append(p);
        $('#playlists').append(playlist);
    }
}

$(document).ready(function() {

    mountPlaylists();
});
