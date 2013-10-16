(function () {
	function renumberRow(row, prefix, oldIndex, newIndex)
	{
		oldIndex = prefix + oldIndex;
		newIndex = prefix + newIndex;
		row.attr('id', row.attr('id').replace(oldIndex, newIndex));
		row.data('rowIndex', newIndex);
		row.find('input, textarea, tr, div.textarea-replacement').each(
			function(index, input)
			{
				input.id = input.id.replace(oldIndex, newIndex);
				if (input.hasAttribute('name'))
				{
					input.name = input.name.replace(oldIndex, newIndex);
				}
			});
		row.find('div.textarea-replacement').each(
			function(index, div)
			{
				div.hiddenField = $('input[name="' + div.id + '"]')[0]
			});
	}

	function renumberIndicatorRow(row, oldIndex, newIndex)
	{
		renumberRow(row, '_ind-', oldIndex, newIndex);
	}

	function renumberSubIndicatorRow(row, oldIndex, newIndex)
	{
		renumberRow(row, '_subind-', oldIndex, newIndex);
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
		var indicatorId = '#id_indicator_set_ind-' + indicatorIndex
		var numForms = $(indicatorId).find('.subindicator-row').length - 1;
		// TODO: keep an array of numForms for the subindicators?
		//totalFormsInput.val(parseInt(numForms));
		return numForms;
	}

	function addIndicatorFormset()
	{
		var newFormIndex = recountIndicators();
		var table = $('#id_indicators');
		var newRow = $('#id_indicator_set_ind-__prefix__').clone();
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

	function addSubIndicatorFormset(indicatorRow)
	{
		var table;
		// the first argument is an event when called from the button press
		// or a jquery object if called during set up.  Distinguish by looking
		// for the find() method.
		if ('find' in indicatorRow)
		{
			table = indicatorRow.find('table');
		}
		else
		{
			table = $(this).closest('table');
		}
		var addButtonRow = table.find('.subindicator-add-row');
		// extract the tr id, eg "indicator_set_ind-0" and extract the number after the -
		var indicatorId = table.closest('tr')[0].id
		var indicatorIndex = indicatorId.substr(indicatorId.indexOf('-') + 1);
		var newFormIndex = recountSubIndicators(indicatorIndex);
		var subindicatorRowId = '#id_ind-' + indicatorIndex + '_subindicator_set_subind-__prefix__';
		var newRow = table.find(subindicatorRowId).clone();
		newRow.attr('style', '');
		renumberSubIndicatorRow(newRow, '__prefix__', newFormIndex);
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
		// Shift all higher forms down by one
		var delRow = $(this).parents('.subindicator-row');
		var delRowIndex = delRow.data('rowIndex');
		$('.subindicator-row').each(
			function(i, rowElem)
			{
				var rowIndex = $.data(rowElem, 'rowIndex');
				if (rowIndex > delRowIndex)
				{
					renumberSubIndicatorRow($(rowElem), rowIndex, rowIndex - 1);
				}
			});
		delRow.remove();
		recountSubIndicators();
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

	function addSubIndicatorFormsToIndicators()
	{
		$('.indicator-row').each(
			function (index, item) {
				// There is always a template formset
				if ($(item).find('.subindicator-row').length == 1)
				{
					addSubIndicatorFormset($(item));
				}
			}
		);
	}

	// also from http://stackoverflow.com/a/14531126/3189
	function togglePlaceholderContent() {
		if (this.textContent) {
			this.dataset.divPlaceholderContent = 'true';
		}
		else {
			delete(this.dataset.divPlaceholderContent);
		}
	}

	/***************************************
	 * Above here are just function definitions, below here is the code
	 * that runs on page load.
	 ***************************************/

	// Replace each text area with a contentEditable box and hidden input
	$("textarea").each(function (index, textarea)
	{
		// placeholder stuff from http://stackoverflow.com/a/14531126/3189
		var replacement = $("<div></div>",
		{
			class: 'textarea-replacement',
			contentEditable: true,
			id: textarea.name,
			"data-placeholder": textarea.placeholder,
		})
		.html(textarea.value);
		if (textarea.value)
		{
			replacement[0].dataset.divPlaceholderContent = 'true';
		}
		if (textarea.attributes.extraclass)
		{
			replacement[0].className = 'textarea-replacement ' + textarea.attributes.extraclass.value;
		}
		replacement.replaceAll(textarea);

		addHiddenInputAfterTextarea(replacement, textarea);
	});

	// If there are no visible forms, create at least one
	// Users can add more forms by clicking on the add button.
	var totalFormsInput = $('#id_indicator_set_ind-TOTAL_FORMS');
	var numForms = totalFormsInput.val();
	if (numForms == 0)
	{
		addIndicatorFormset();
	}

	addSubIndicatorFormsToIndicators();

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
	$('.output').on('click', '.indicator-del-button', null, removeIndicatorFormset);

	// Bind dynamically to allow newly-added rows to be handled
	// without rebinding.
	$('.output').on('click', '.subindicator-add-button', null, addSubIndicatorFormset);

	// Bind dynamically to allow newly-added rows to be handled
	// without rebinding.
	$('.output').on('click', '.subindicator-del-button', null, removeSubIndicatorFormset);

	$('.output').on('keydown keypress input', 'div[data-placeholder]', null,
				togglePlaceholderContent);
})();
