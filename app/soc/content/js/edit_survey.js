   
    var DEFAULT_LONG_ANSWER_TEXT = 'Write a Custom Prompt...';
    var DEFAULT_SHORT_ANSWER_TEXT = 'Write a Custom Prompt...';
    var DEFAULT_OPTION_TEXT = 'Add A New Option...';
    var min_rows = 10;
    max_rows = min_rows * 2;
    
    
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

   var survey = widget.find('tbody:first')
   var options = $('div#survey_options');
   
   var del_el = "<a class='delete'><img src='/soc/content/images/minus.gif'/></a>";
   var default_option = "<option>" + DEFAULT_OPTION_TEXT + "</option>";
   
   
   // Setup for existing surveys
   widget.find('label').prepend(del_el).end()
         .find('select').append(default_option)
                        .each(function(){
                        $(this).attr('name', 'survey_selection__' + $(this).attr('name') ) });

         widget.find('input').each(function(){
         $(this).attr('name', 'survey_short_answer__' + $(this).attr('name') ) });

         widget.find('textarea').each(function(){
         $(this).attr('name', 'survey_long_answer__' + $(this).attr('name') ) });
   
   
   options.find('button').click(function(e){

   var field_template =  $("<tr><th><label>" + del_el + "</label></th><td>  </td></tr>");

   var field_name = prompt('enter a field name');
   if (!field_name) return alert('invalid field name');
   
new_field = false;
var type = $(this).attr('id') + "__";

switch($(this).attr('id')){
case "short_answer":  
var new_field = "<input type='text'/>";
break;

case "long_answer": 


var new_field = "<textarea cols='40' rows='" + min_rows + "' />";


    
break;

case "selection": 
var new_field = "<select><option></option>" + default_option + "</select>";
break;
}

if (new_field) {
	
	field_count = survey.find('tr').length;
	new_field_count = field_count + 1;
    new_field = $(new_field);
    formatted_name = 'survey__' + new_field_count + '__' + type +  field_name;
    // maybe the name should be serialized in a more common format
    $(new_field).attr({ 'id': 'id_' + formatted_name, 'name': formatted_name });
	field_template.find('label').attr('for', 'id_' + formatted_name)
	                                         .append(field_name + ":").end()
				  .find('td').append(new_field);
	survey.append(field_template).trigger('init'); 

}
   });
   
   

 
survey.bind('init', function(){


widget.find('input').each(function(){ 
if ($(this).val().length < 1 | $(this).val() == DEFAULT_SHORT_ANSWER_TEXT) $(this).preserveDefaultText(DEFAULT_SHORT_ANSWER_TEXT); 
}); 

widget.find('textarea').each(function(){ 
if ($(this).val().length < 1 | $(this).val() == DEFAULT_LONG_ANSWER_TEXT) $(this).preserveDefaultText(DEFAULT_LONG_ANSWER_TEXT);
var sizer = sizeTextArea(min_rows, max_rows);
$(this).keyup(sizer).keyup(); // will this work?


}); 

widget.find('select').change(function(){

if ($(this).find('option:selected').text() == DEFAULT_OPTION_TEXT) {
var option_name = prompt("Name the new option");
if (option_name == null) return false; if (option_name.length < 1) return false;
$(this).prepend("<option>" + option_name + "</option>").find('option').each(function(){
   if ($(this).val().length < 1) $(this).remove();
}).end().find('option:first').attr('selected', 'selected');

}

});


widget.find('a.delete img').click(function(){
	this_field = $(this).parents('tr:first');
delete_this = confirm("Are you sure you want to delete this field?");
if (delete_this) this_field.remove();
});


}).trigger('init');




// Bind submit

$('form').bind('submit', function(){
 
 // Get all options for select menus
 widget.hide().find('select').each(function(){
 	options = Array();
 	$(this).find('option').each(function(){
 	if ($(this).text() != DEFAULT_OPTION_TEXT) options.push($(this).text());
	});
	$(this).html('').append("<option selected='selected'>" + options + "</option>")
});
 		


widget.find('input').each(function(){ 
if ( $(this).val() == DEFAULT_SHORT_ANSWER_TEXT) $(this).val('');
}); 

widget.find('textarea').each(function(){ 
if ($(this).val() == DEFAULT_LONG_ANSWER_TEXT) $(this).val('');
}); 

 $('input#id_s_html').val(widget.find('div#survey_options').remove().end().html()); // only needed for HTML
 
});

  
   
   });
   




function sizeTextArea(min, max) {
    return function(e) {
        if (!this.rows || this.rows < min) this.rows = min;
        while ((this.clientHeight >= this.scrollHeight 
                && this.rows > 1 && this.rows <= max) 
               || this.rows > max) this.rows -= 1;
        while ((this.clientHeight < this.scrollHeight 
                || this.rows < min) 
               && this.rows < max) this.rows += 1;
        if (this.rows == max
            && this.clientHeight < this.scrollHeight) this.style.overflow = 'auto';
        else this.style.overflow = 'hidden';
    }
}
