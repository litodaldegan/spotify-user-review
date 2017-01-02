var mount_top_artists_graph = function (user_id) {

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
	                    .draw()
	        }
	})
}
