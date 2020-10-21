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
	var editable = $(this).hasClass('editable');
	var image = image_data.image;
	var edit_img = (editable) ? `<a href="/images/edit/${image.id}"><i class="fas fa-edit"></i></a>` : "";
	var img = `<img class="modal-img" src="${image.upload_location}" alt="${image.name}">`;
	var content = `<div class="imginfo">
					<h5 class="modal-title">${image.name}> 
					<a href="/images/like/{{ image.id }}"><i class="far fa-heart"></i></a>
						${edit_img}
						<i class="fa fa-times" data-dismiss="modal" aria-label="Close" aria-hidden="true"></i>
					</h5>
					<p class="modal-desc">${image.description}</p>
					<small>${image.user_name}</small>
				</div>`;
	var openlink = `<a href="${image.upload_location}" target="_blank">Open Image in Another Tab</a>`;
	$('#image-modal .modal-body').html(img + content + openlink);
	$('.modal').modal('show');
});

//{{ liked if image.id in likes else not_liked }}

$(document).ready(function(){
	
	//some other code

	$('i.like').click(function(e) {
	
		e.stopPropagation();
		e.preventDefault();
	
		var like 		= $(this).hasClass('far');
		var image_id 	= $(this).data('image');
		var _this 		= $(this);
	
		$.getJSON(
			$SCRIPT_ROOT + '/like', 
			{
				like: like,
				image_id: image_id
			}, 
			function(result) {
				if (result){
					if (like) {
						_this.removeClass('far'); 
						_this.addClass('fas');
					} else {
						_this.removeClass('fas') 
						_this.addClass('far');
					}
				}

			}
		);
	});

});



////This is the code that im using to 
//	var avatar_img = (typeof image.user_avatar === "undefined") ? `<img class="avatar" src="../static/img/blankavatar.jpg" alt="${image.user_name }">` : `<img class="avatar" src="${image.user_avatar}" alt="${image.user_name }">`;
//
//if (condition) {
//	_this.removeClass('far')
//} else {
//	_this.removeClass('fas') 
//}
//
//code to change the like icon
//_this.removeClass('fas') 
//_this.removeClass('far')