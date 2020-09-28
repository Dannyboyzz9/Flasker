$(document).ready(function(){
	
	var $grid = $('.grid').masonry({
		gutter: 30
	});
	
	// layout Masonry after each image loads
	$grid.imagesLoaded().progress( function() {
		$grid.masonry('layout');
	});
	
});

$('.brick').click(function(){
	var image_data = $(this).data(image);
	var image = image_data.image;
	var description = `<p class="modal-desc">${image.description}</p>`;
	var title = `<h5 class="modal-title">${image.name} <i class="fa fa-times" data-dismiss="modal" aria-label="Close" aria-hidden="true"></i></h5>`;
	var img = `<img class="modal-img" src="${image.upload_location}" alt="${image.name}">`;
	var openlink = `<a href="${image.upload_location}" target="_blank">Open Image in Another Tab</a>`;
	$('#image-modal .modal-body').html(img + title + description + openlink);
	$('.modal').modal('show');
});