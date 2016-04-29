$(document).ready(function() {
    
    var input_url = document.getElementById('input_url').value;
    var submit_url = 'http://127.0.0.1:5000/url'+input_url;
    var myEl = document.getElementById('submit_button');
    myEl.addEventListener('click', function() {
        console.log('Hello world');
        $.ajax({
		   //url: submit_url, //TBD
		   url: 'http://127.0.0.1:5000/url/http://docs.imagga.com/static/images/docs/sample/japan-605234_1280.jpg',
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
		     	console.log('success');
		     	window.location = 'index2.html';
		      	document.getElementById('poet').innerHTML = data.title + ' by ' + data.author;
		      	document.getElementById('poem').innerHTML = data.lines;

		      	var slider = document.getElementById('rating');
		      	var slider_input = slider.value;
		      	slider.addEventListener('change',function(){
		      		document.getElementByName('level').innerHTML=slider_input;
		      		$.ajax({
		      			url: 'http://127.0.0.1:5000/url',//TBD
		      			type: 'POST',
		      			data:{
		      				rating: slider_input
		      			}
		      		});
		      	})
		   },
		   
		});

    });
});