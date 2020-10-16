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

	//This is the code that im using to 
	var avatar_img = (typeof image.user_avatar === "undefined") ? `<img class="avatar" src="../static/img/blankavatar.jpg" alt="${image.user_name }">` : `<img class="avatar" src="${image.user_avatar}" alt="${image.user_name }">`;
	
	var image = image_data.image;
	var edit_img = (editable) ? `<a href="/images/edit/${image.id}"><i class="fas fa-edit"></i></a>` : "";
	var img = `<img class="modal-img" src="${image.upload_location}" alt="${image.name}">`;
	var content = `<div class="imginfo">
					`// ${avatar_img} //
					`
					<h5 class="modal-title">${image.name}> 
						<a href="/images/like/${image.id}"><i class="like far fa-heart" data-image="${image.id}"></i></a>
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
				//code to change the like icon
				_this.removeClass('some-class') 
				_this.removeClass('another-class')
			}
		);
	});

});
//var yes = String;
//yes = document.getElementsByName(`${image.user_avatar}`).value;
//if (typeof image.user_avatar !== 'undefined'){ //checks whether the user avatar has a defined string eg does it have a link
//	image.src = "../static/img/blankavatar.jpg"; //this will set the avatar_img to the link of the avatar if it exists 
// } else {
//	image.src = `${image.user_avatar}`; //this will set the avatar_img to a default img
//}
//var avalible = $(this).('a')
//var avatar_img = (avalible) ? `<img class="avatar" src="../static/img/blankavatar.jpg" alt="${image.user_name }"></img>` : `<img class="avatar" src="${image.user_avatar}" alt="${image.user_name }"></img>`;
// this code will be like hey does this person have an avatar or a file uploaded to user.avatar 
// or whether it has or has not got a string associated with it
// var avatar_img_avalility = $(this).
// var user_avatar = `${image.user_avatar}`; sets user_avatar as the users avatar00