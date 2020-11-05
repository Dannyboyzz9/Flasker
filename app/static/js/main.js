

//{{ liked if image.id in likes else not_liked }}

/**
 * The Following code will make sure that the correct values are loaded on to what
 * filter and catagory is associated with the image on the dropdown menus on the edit
 * page.
 */




/**  The following code is used for the functionality of the liking system
 *   The Code waits for a user to click the like button then sets the class/visual represnetation 
 * based on whether the like button has or has not been prevously been pressed. Once the like button is
 * pressed a JSON request is made to firebase. If a user has liked an img then
 * the heart will have the class fas and when it is clicked again the like info will be removed from firebase
 * and the heart will revert to the class far.
 */

$(document).ready(function(){
	
	$('#filter-select').change(function(e) {
		var new_filter = 'filter-' + this.value;
		$('#image figure').removeClass();
		$('#image figure').addClass(new_filter);
	});

	var $grid = $('.grid').masonry({
		gutter: 30
	});
	// layout Masonry after each image loads
	$grid.imagesLoaded().progress( function() {
		$grid.masonry('layout');
	});

	if ($('#filter-select').length > 0 ) {
		var filter = $('#filter-select').data('filter');
		$('#filter-select').val(filter);
	}
	
	if ($('#category').length > 0 ) {
		var category = $('#category').data('category');
		$('#category').val(category);
	}

	$('i.like').click(function(e) {
	
		/** This stops the Modal opening */
		e.stopPropagation();
		e.preventDefault();
	
		var like 		= $(this).hasClass('far');
		var image_id 	= $(this).data('image');
		var _this 		= $(this);
	
		/** this gets a JSON request */
		$.getJSON(
			$SCRIPT_ROOT + '/like', 
			{
				like: like,
				image_id: image_id
			}, 
			/**This will control the apperance of the heart when its clicked  */
			function(result) {
				if (result){
					if (like) {
						_this.removeClass('far'); 
						_this.addClass('fas');
					} else {
						_this.removeClass('fas');
						_this.addClass('far');
					}
				}

			}
		);
	});

	/** The Following code listens for the figure and associated Image under the class brick to be clicked.
	 * When clicked image data and scr are gathered from firebase and set as local variables.
	 * Modal content is then assinged with preassinged infomation with classes already assined 
	 * and variables are set to infomation that needs to be changed from each image as there are multiple 
	 * images and each one is unique. Python tags like ${image.upload_location} set the image to the correct image
	 * and recive the scr infomation from firebase. All the elements are then added together then displayed
	 * as a overlay under the class 'modal'
	 */
	$('.brick figure').click(function(){
		var image_data = $(this).closest('.brick').data(image);
		var editable = $(this).hasClass('editable');
		var image = image_data.image;
		var edit_img = (editable) ? `<a href="/images/edit/${image.id}"><i class="fas fa-edit"></i></a>` : "";

		var img = `	<figure class="filter-${image.filter}">
						<img class="modal-img" src="${image.upload_location}" alt="${image.name},${image.description}">
					</figure>`;

		var content = ` <div class="imginfo">
							<h5 class="modal-title">${image.name}> 
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

});
