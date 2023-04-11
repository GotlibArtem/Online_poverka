$('#true_check').click(function () {
	if ($(this).is(':checked')) {
		$('input:checkbox').prop('checked', true);
	} else {
		$('input:checkbox').prop('checked', false);
	}
});


$("#btn_clickToShop").click(function() {
	var allPribors = [];
	$("input:checked").each(function(i, item) {
		allPribors.push($(item).attr("value") + '<p>' );
	});
    alert ("Приборы добавлены в корзину");
	$("#pribors-Show").html(allPribors);
  });


  $(document).ready(function () {
    var overlay = $('#overlay_modal');
    var open_modal = $('.open_modal');
    var open_modal_table = $('.open_modal_table');
    var close = $('.modal_close, #overlay_modal');
    var modal = $('.modal_div');
    var KEYCODE_ESC = 27;

    open_modal.click(function (event) {
        event.preventDefault();
        var div = $(this).attr('href');
        overlay.fadeIn(400,
            function () {
                $(div)
                    .css('display', 'block')
                    .animate({
                        opacity: 1
                    }, 200);
            });
    });

    open_modal_table.click(function (event) {
        event.preventDefault();
        var div = $(this).attr('href');
        overlay.fadeIn(400,
            function () {
                $(div)
                    .css('display', 'block')
                    .animate({
                        opacity: 1
                    }, 200);
            });
    });

    $(document).keyup(function (e) {
        if (e.keyCode == KEYCODE_ESC)
            $(KEYCODE_ESC).click();
        $(modal).css('display', 'none');
        overlay.fadeOut(400);
    });

    close.click(function () {
        modal
            .animate({
                    opacity: 0
                }, 200,
                function () {
                    $(this).css('display', 'none');
                    overlay.fadeOut(400);
                }
            );
    });
});