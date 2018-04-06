

$("#login-button").click(function(event)
	foo()
	{
		event.preventDefault();

		document.getElementById('form').submit();

		$('form').fadeOut(500);
		$('.wrapper').addClass('form-success');

	}
);
