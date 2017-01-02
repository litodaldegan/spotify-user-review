var mount_top_artists_graph = function (user_id) {

	var htmlButton = "<a id='google' href='http://www.google.com' target='_blank'>Click here to go to Google</a>"

	$.ajax({
	        dataType: 'json',
	        type: 'GET',
	        url: '/profile/artists/top10/' + user_id,
	        success: function (response) {

	                var visualization = d3plus.viz()
	                    .container("#top-artists")  
	                    .data(response.json_data)  
	                    .type("bar") 
	                    .id("name")
	                    .x({"value": "name", "label": false, "grid": false})
	                    .order({
	                       "sort": "desc",
	                       "value": "popularity"
	                    })
	                    .color({"scale": ["#337ab7"]})
	                    .y({"value": "popularity", "label": "Popularity", "range": [0, 100], "grid": {"color": "#333"}})
	                    .background("#232323")
	                    .axes({"background": {"color": "#232323"}})
	                    .tooltip({
	                    	"stacked": true,
	                    	"large": 250,
	                    	"html": function(d){

	                    	for (i = 0; i < response.json_data.length; i++){
	                    		if (response.json_data[i].name == d){
	                    			artist = response.json_data[i];
			                    	var show_info = '<div><a href=' + artist.url +
			                    		' target="_blank"><img style="width: 250px;height:250px;float:left;display:block" src=' +
			                    		artist.image + ' alt="See on spotify"></a></div>';
	                    		}
	                    	}
	                    	
	                    	return show_info;
	                    	}
	                    })
	                    .draw()
	        }
	})
}
