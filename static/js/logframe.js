(function () {
	// $(".milestone-column").bind("click", function (e) {
	// $("textarea").live("click", function (e) {
	// $(".editable").on("click", "textarea", function (e) {
	$("textarea").each(function (index, textarea)
	{
		// var textarea = e.target;
		// alert($(this).html());
		var replacement = $("<div></div>",
		{
			class: 'textarea-replacement',
			contentEditable: true,
			id: textarea.name
		})
		.html(textarea.value);
		replacement.replaceAll(textarea);

		var hidden = $("<input>",
		{
			type: 'hidden',
			name: textarea.name,
			id:   textarea.id
		});
		hidden.insertAfter(replacement);
		replacement[0].hiddenField = hidden[0];
	});
	$('form[name="output"]').on('submit', function()
	{
		$('.textarea-replacement').each(function (index, div)
		{
			div.hiddenField.value = div.innerHTML;
		});
		return true;
	});

	function renumberIndicatorRow(row, oldIndex, newIndex)
	{
		row.attr('id', row.attr('id').replace("set-" + oldIndex,
			"set-" + newIndex));
		row.data('rowIndex', newIndex);
		row.find('input, textarea, div.textarea-replacement').each(
			function(index, input)
			{
				input.id = input.id.replace("-" + oldIndex + "-",
					"-" + newIndex + "-");
				if (input.hasAttribute('name'))
				{
					input.name = input.name.replace(
						"-" + oldIndex + "-",
						"-" + newIndex + "-");
				}
			});
		row.find('div.textarea-replacement').each(
			function(index, div)
			{
				div.hiddenField = $('input[name="' + div.id + '"]')[0]
			});
	}

	var totalFormsInput = $('#id_indicator_set-TOTAL_FORMS');

	function recountIndicators()
	{
		var numForms = $('.indicator-row').length - 1; // ignore the hidden template row
		totalFormsInput.val(parseInt(numForms));
		return numForms;
	}

	// Bind dynamically to allow newly-added rows to be handled 
	// without rebinding.
	$('.output').on('click', '.indicator-add-button', null, function()
	{
		var newFormIndex = recountIndicators();
		var table = $('#id_indicators');
		var newRow = $('#id_indicator_set-__prefix__').clone();
		newRow.attr('style', '');
		renumberIndicatorRow(newRow, '__prefix__', newFormIndex);
		table.append(newRow);
		// There's now one more form than there was, so update the
		// hidden field that tells Django how many forms are in the
		// formset.
		totalFormsInput.val(newFormIndex + 1);
	});

	var numForms = totalFormsInput.val();
	// Hide the extra blank form if there's at least one form visible.
	// Users can add more forms by clicking on the add button.
	if (numForms > 1)
	{
		var spare_form_id = "id_indicator_set-" + (numForms - 1);
		$('#' + spare_form_id).hide();
	}

	// Bind dynamically to allow newly-added rows to be handled 
	// without rebinding.
	$('.indicators').on('click', '.indicator-del-button', null, function()
	{
		// Shift all higher forms down by one
		var delRow = $(this).parents('.indicator-row');
		var delRowIndex = delRow.data('rowIndex');
		$('.indicator-row').each(
			function(i, rowElem)
			{
				var rowIndex = $.data(rowElem, 'rowIndex');
				if (rowIndex > delRowIndex)
				{
					renumberIndicatorRow($(rowElem), 
						rowIndex, rowIndex - 1);
				}
			});
		delRow.remove();
		recountIndicators();
	});
})();

