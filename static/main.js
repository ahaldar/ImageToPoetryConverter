$(document).ready(function() {
    
    
    var submit_url = 'http://127.0.0.1:5000/url'+input_url;
    var myEl = document.getElementById('submit_button');
    myEl.addEventListener('click', function(e) {
    	e.preventDefault();
    	var input_url_link = document.getElementById('input_url').value;
        console.log('Hello world');
        $.ajax({
		   //url: submit_url, //TBD
		   url: 'http://127.0.0.1:5000/url/' + input_url_link,
		   type: 'GET',
		   data: {
		      //obj: input_url
		   },
		   dataType: 'json',
		   /*error: function(request,error) {
		      	console.log('An error has occurred'+error);
		   }*/
		   error: function(request,error) {
			  console.log(error);
			},
		   success: function(data) {
		   	console.log(data);
		   	var poemtext = "";
		   		for(var i= 0;i<data.lines.length; i++ )
		   		{
		   			poemtext = poemtext + data.lines[i] + "<br>";
		   		}
		     	console.log('success');
		     	$('#screen1').fadeOut();
		     	$('#screen2').fadeIn();
		     	console.log(input_url);
		     	$('#image').attr('src', input_url_link);
		     	$('#poet').html(data.title + ' by ' + data.author);
		     	$('#poem').html(poemtext);
	      		// document.getElementById('poet').innerHTML = data.title + ' by ' + data.author;
	      		// document.getElementById('poem').innerHTML = data.lines;
	      		var slider = document.getElementById('rating');
	      		$('#sakshibutton').click(function(e){
	      			e.preventDefault();
	      			var slider_input = slider.value;
		     		$('#screen2').fadeOut();
	      			$('#screen1').fadeIn();
	      			// document.getElementByName('level').innerHTML=slider_input;
		      		// $.ajax({
		      		// 	url: 'http://127.0.0.1:5000/url',//TBD
		      		// 	type: 'POST',
		      		// 	data:{
		      		// 		rating: slider_input
		      		// 	}
		      		// });
	      		})

		      	
		   },
		   
		});

    });
});