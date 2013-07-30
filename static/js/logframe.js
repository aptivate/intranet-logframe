(function () {
	// $(".milestone-column").bind("click", function (e) {
	// $("textarea").live("click", function (e) {
	// $(".editable").on("click", "textarea", function (e) {
	$("textarea").each(function (index, textarea) {
		// var textarea = e.target;
		// alert($(this).html());
		var replacement = $("<div></div>", {
			class: 'textarea-replacement',
			contentEditable: true,
			id: textarea.name
		})
		.html(textarea.value);
		replacement.replaceAll(textarea);

		var hidden = $("<input>", {
			type: 'hidden',
			name: textarea.name,
			id:   textarea.id
		});
		hidden.insertAfter(replacement);
		replacement[0].hiddenField = hidden[0];
	});
	$('form[name="output"]').on('submit', function() {
		$('.textarea-replacement').each(function (index, div) {
			div.hiddenField.value = div.innerHTML;
		});
		return true;
	});
	var totalFormsInput = $('#id_indicator_set-TOTAL_FORMS');
	$('.indicator-add-button').on('click', function() {
		var numForms = $('.indicator-row').length - 1; // ignore the hidden template row
		var newFormIndex = numForms;
		totalFormsInput.val(parseInt(newFormIndex) + 1);

		var table = $('#id_indicators');
		var newRow = $('#id_indicator_set-__prefix__').clone();
		newRow.attr('style', '');
		newRow.find('input, textarea, div.textarea-replacement').each(
			function(index, input)
			{
				input.id   = input.id  .replace(/__prefix__/g, newFormIndex);
				if (input.hasOwnProperty('name'))
				{
					input.name = input.name.replace(/__prefix__/g, newFormIndex);
				}
			});
		table.append(newRow);
		newRow.find('div.textarea-replacement').each(
			function(index, div)
			{
				div.hiddenField = $('input[name="' + div.id + '"]')[0]
			});
	});
	var numForms = totalFormsInput.val();
	// Hide the extra blank form if there's at least one form visible.
	// Users can add more forms by clicking on the add button.
	if (numForms > 1)
	{
		var spare_form_id = "id_indicator_set-" + (numForms - 1);
		$('#' + spare_form_id).hide();
	}
})();

