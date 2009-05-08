
    
jQuery.fn.extend({
	preserveDefaultText: function(defaultValue, replaceValue)
	{
		$(this).focus(function()
		{
			if(typeof(replaceValue) == 'undefined')
				replaceValue = '';  
			if($(this).val() == defaultValue)
				$(this).val(replaceValue);
		});

		$(this).blur(function(){  
			if(typeof(replaceValue) == 'undefined')
				replaceValue = '';  
			if($(this).val() == replaceValue)
				$(this).val(defaultValue);
		});
		return $(this).val(defaultValue);
	}
});
    
   $(function(){
   
   var widget = $('div#survey_widget');
   widget.parents('td.formfieldvalue:first').css({ 'float': 'left', 
                                                   'width': 200 });

   var survey = widget.find('tbody:first');
   

if (widget.hasClass('create')) { 
widget.find('input').each(function(){ 
 $(this).preserveDefaultText($(this).val()); 
}); 

widget.find('textarea').each(function(){ 
$(this).preserveDefaultText($(this).val());
}); 

widget.find('select').change(function(){
});

}

// Bind submit

$('form').bind('submit', function(){
 $('input#id_s_html').val(widget.find('div#survey_options').remove().end().html());
});

  
   
   });
   
