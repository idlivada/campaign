$(document).ready(function () {

    var zip_re = /^\d{5}?$/;
    var email_re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;

    $('#form-contact input').keyup(function(e) {
	var valid = form_input_set_color($('#fname'), $('#fname').val())
	valid &= form_input_set_color($('#lname'), $('#lname').val());
	valid &= form_input_set_color($('#email'), email_re.test($('#email').val()));
	valid &= form_input_set_color($('#street'), $('#street').val());
	valid &= form_input_set_color($('#city'), $('#city').val());
	valid &= form_input_set_color($('#state'), $('#state').val().length == 2);
	valid &= form_input_set_color($('#zipcode'), zip_re.test($('#zipcode').val()));
	valid &= form_input_set_color($('#phone'), valid_phone($('#phone').val()));

	if(valid) {
 	    $('#btn-contact-find').css('visibility', 'visible');
	} else {
 	    $('#btn-contact-find').css('visibility', 'hidden');
	}
    });


    function valid_phone(phone) {
	var match = phone.match(/\d/g);
	return match && match.length == 10;
    }

    $('#phone').focus(function() {
	$('#alert').show();
    })
    $('#phone').focusout(function() {
	$('#alert').hide();
    })

    function form_input_set_color(field, valid) {
	if(valid) {
	    field.parent().addClass('has-success');
	    field.parent().removeClass('has-error');
	} else {
	    field.parent().addClass('has-error');
	    field.parent().removeClass('has-success');
	}
	return !!valid;
    }

    $('#form-contact').submit(function(e) {
	params = {}

	$('input.contactinfo').each(function(i, e) { 
	    params[e.id] = $(e).val(); 
	});
	$.get('/locator/?'+$.param(params), function(data) {  
	    $.each(data, function(i, cong_data) {
		var cong_section = $('section.cong_template').clone(true, true);
		$('section.cong_template').removeClass('cong_template');
		cong_section.addClass('cong-active');
		
		var title = cong_data['chamber'] == 'house' ? 'Representative' : 'Senator';
		cong_data['fullname'] = title + ' ' + cong_data['first_name'] + ' ' + cong_data['last_name'];
		cong_section.find('.cong_name').html(cong_data['fullname']);

		if(!cong_data['twitter_id']) {
		    cong_section.find('.btn-tweet').hide();
		} else {
		    cong_section.find('.btn-tweet-text').html('Send a Tweet');
		}

		cong_section.data('cong_data', cong_data);

		$('#contact-info').hide();
		cong_section.show();
		$('#progress-area').show();

		$('#action-area').append(cong_section);	
	    });
	});
	return false;
    });
    
    $('section.cong-section .btn-call').click(function(e) {
	e.preventDefault();
	var cong_data = $(e.target).parents('section.cong-section').data('cong_data');
	var params = {'cong_id' : cong_data['bioguide_id'],
		      'phone'   : $('#phone').val().replace(/\D/g, '')};

	$('#call-template .cong-name').html(cong_data['fullname']);
	$('#call-template .your-name').html($('#fname').val()+' '+$('#lname').val());
	
	$.get('/call/?'+$.param(params), function(data) {
	});

	success_button($(this));
	update_progress();
    });


    $('section.cong-section .btn-tweet').click(function(e) {
	e.preventDefault();
	var twitter_id = $(e.target).parents('section.cong-section').data('cong_data')['twitter_id'];
	params = {'text' : '@'+twitter_id + ' ' + $('#tweet_template').html()};
	window.open('https://twitter.com/intent/tweet?'+$.param(params));

	success_button($(this));
	update_progress();
    });

    $('#learn-more').click(function(e) {
	$('#learn-more').hide();
	$('#full-description').show();
    })

    $('#alert').hide();
    $('#full-description').hide();
    $('#progress-area').hide();
    $('#btn-contact-find').css('visibility', 'hidden');

    function update_progress() {
	var total = $('section.cong-active .btn-progress-action').length;
	var completed = $('section.cong-active .btn-progress-action.btn-success').length;
	$('.progress-bar').css('width', (100.0 * completed/ total) + '%'); 
    }
    
    function success_button(btn) {
	btn.removeClass('btn-primary');
	btn.addClass('btn-success');
	var glyph = btn.find('.glyphicon');
	glyph.removeClass('glyphicon-earphone');
	glyph.removeClass('glyphicon-hand-up');
	glyph.addClass('glyphicon-check');
    }

    $('#privacy-link').click(function(e) {
	e.preventDefault();
	$('#privacy').show();
	$('#privacy-blurb').hide();
    });
});