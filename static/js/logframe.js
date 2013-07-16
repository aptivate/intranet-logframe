(function () {
	// $(".milestone-column").bind("click", function (e) {
	// $("textarea").live("click", function (e) {
	// $(".editable").on("click", "textarea", function (e) {
	$("textarea").each(function (index, textarea) {
		// var textarea = e.target;
		// alert($(this).html());
		var replacement = $("<div class='textarea-replacement'></div>");
		replacement.attr('contentEditable', true);
		replacement.attr('id', textarea.id);
		replacement.html(textarea.value);

		/*
		// http://www.quirksmode.org/dom/range_intro.html
		function getRangeObject(selectionObject) {
			if (selectionObject.getRangeAt)
				return selectionObject.getRangeAt(0);
			else { // Safari!
				var range = document.createRange();
				range.setStart(selectionObject.anchorNode,selectionObject.anchorOffset);
				range.setEnd(selectionObject.focusNode,selectionObject.focusOffset);
				return range;
			}
		}

		var selectionOrRange;
		if (window.getSelection) { // Microsoft way
			selectionOrRange = window.getSelection();
		}
		else if (document.selection) { // should come last; Opera!
			selectionOrRange = document.selection.createRange();
		}

		var oldRange;
		oldRange = getRangeObject(selectionOrRange);
		var newRange = document.createRange();
		newRange.setStart(replacement[0], oldRange.startOffset);
		newRange.setEnd  (replacement[0], oldRange.endOffset);

		// TODO IE support!
		selectionOrRange.removeAllRanges();
		selectionOrRange.addRange(newRange);
		*/

		replacement.replaceAll(textarea);
		// replacement.focus();
	});
})();

