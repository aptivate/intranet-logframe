(function () {
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

	function clearFormValues(node)
	{
		node.find('input, textarea, div.textarea-replacement').each(
			function(index, input)
			{
				/* We don't want to clear the management form stuff:
				 * ...-TOTAL_FORMS
				 * ...-INITIAL_FORMS
				 * etc */
				if ('name' in input && !input.name.match(/_FORMS$/))
				{
					input.value = "";
				}
			});
	}

	function recountIndicators()
	{
		var numForms = $('.indicator-row').length - 1; // ignore the hidden template row
		totalFormsInput.val(parseInt(numForms));
		return numForms;
	}

	function recountSubIndicators(indicatorIndex)
	{
		// ignore the hidden template row
		var indicatorId = '#id_indicator_set-' + indicatorIndex
		var numForms = $(indicatorId).find('.subindicator-row').length - 1;
		// TODO: keep an array of numForms for the subindicators?
		//totalFormsInput.val(parseInt(numForms));
		return numForms;
	}

	function addIndicatorFormset()
	{
		var newFormIndex = recountIndicators();
		var table = $('#id_indicators');
		var newRow = $('#id_indicator_set-__prefix__').clone();
		newRow.attr('style', '');
		renumberIndicatorRow(newRow, '__prefix__', newFormIndex);
		clearFormValues(newRow);
		textarea = newRow.find("textarea");
		addHiddenInputAfterTextarea(Array(textarea), textarea);
		table.append(newRow);
		// There's now one more form than there was, so update the
		// hidden field that tells Django how many forms are in the
		// formset.
		totalFormsInput.val(newFormIndex + 1);

		// update subindicator formset
		$(newRow).find('tr[class=subindicator-management] > input').each(
			function(index, input)
			{
				var oldId = input.id;
				var newId = oldId.replace('__prefix__', newFormIndex);
				$(input).attr('id', newId);

				var oldName = input.name;
				var newName = oldName.replace('__prefix__', newFormIndex);
				$(input).attr('name', newName);
			});
	}

	function removeIndicatorFormset()
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
					renumberIndicatorRow($(rowElem), rowIndex, rowIndex - 1);
				}
			});
		delRow.remove();
		recountIndicators();
	}

	// TODO: maybe need two versions - one which is attached to an element
	// that can use $(this) and one which is passed the element/id to use
	function addSubIndicatorFormset()
	{
		var addButtonRow = $(this).closest('tr');
		var table = $(this).closest('table');
		// extract the tr id, eg "indicator_set-0" and extract the number after the -
		var indicatorId = table.closest('tr')[0].id
		var indicatorIndex = indicatorId.substr(indicatorId.indexOf('-') + 1);
		var newFormIndex = recountSubIndicators(indicatorIndex);
		var subindicatorRowId = '#id_indicator_' + indicatorIndex + '_subindicator_set-__prefix__'
		var newRow = table.find(subindicatorRowId).clone();
		newRow.attr('style', '');
		renumberIndicatorRow(newRow, '__prefix__', newFormIndex);
		clearFormValues(newRow);
		textarea = newRow.find("textarea");
		addHiddenInputAfterTextarea(Array(textarea), textarea);
		addButtonRow.before(newRow);
		// TODO: update management form
		//var totalFormsInput = $('#id_indicator_set-TOTAL_FORMS');
	}

	function removeSubIndicatorFormset()
	{
		// TODO:
	}

	function addHiddenInputAfterTextarea(replacement, textarea)
	{
		var hidden = $("<input>",
		{
			type: 'hidden',
			name: textarea.name,
			id:   textarea.id
		});
		hidden.insertAfter(replacement);
		replacement[0].hiddenField = hidden[0];
	}

	function copyTextareaReplacementToHidden()
	{
		$('.textarea-replacement').each(function (index, div)
		{
			hiddenField = $('input[name="' + div.id + '"]');
			hiddenField[0].value = div.innerHTML;
		});
		return true;
	}

	/***************************************
	 * Above here are just function definitions, below here is the code
	 * that runs on page load.
	 ***************************************/

	// Replace each text area with a contentEditable box and hidden input
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

		addHiddenInputAfterTextarea(replacement, textarea);
	});

	// If there are no visible forms, create at least one
	// Users can add more forms by clicking on the add button.
	var totalFormsInput = $('#id_indicator_set-TOTAL_FORMS');
	var numForms = totalFormsInput.val();
	if (numForms == 0)
	{
		addIndicatorFormset();
	}

	// TODO: for each indicator, check for visible forms for the subindicator

	/***************************************
	 * Now we've set up, bind some functions
	 ***************************************/

	// on submit, we should the contents of the contentEditable div into the
	// hidden input element.
	$('form[name="output"]').on('submit', copyTextareaReplacementToHidden);

	// Bind dynamically to allow newly-added rows to be handled
	// without rebinding.
	$('.output').on('click', '.indicator-add-button', null, addIndicatorFormset);

	// Bind dynamically to allow newly-added rows to be handled
	// without rebinding.
	$('.indicators').on('click', '.indicator-del-button', null, removeIndicatorFormset);

	// Bind dynamically to allow newly-added rows to be handled
	// without rebinding.
	$('.output').on('click', '.subindicator-add-button', null, addSubIndicatorFormset);

	// Bind dynamically to allow newly-added rows to be handled
	// without rebinding.
	$('.subindicators').on('click', '.subindicator-del-button', null, removeSubIndicatorFormset);
})();
