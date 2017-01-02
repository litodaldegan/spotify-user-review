var mount_style_graph = function () {
        
        $.ajax({
                dataType: 'json',
                type: 'GET',
                url: '/profile/styles/5',
                success: function (response) {

                        var visualization = d3plus.viz()
                            .container("#treemap-styles")  
                            .data(response.json_data)  
                            .type("tree_map")   
                            .id("name")         
                            .size("value")
                            .labels({"align": "left", "valign": "top"})
                            .background("#232323")    
                            .draw()
                }
        })
}

$(document).ready(function() {

    mount_style_graph();
});