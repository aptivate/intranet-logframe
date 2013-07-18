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
			id: textarea.id
		})
		.html(textarea.value);
		replacement.replaceAll(textarea);

		var hidden = $("<input>", {
			type: 'hidden',
			name: textarea.name
		});
		hidden.insertAfter(replacement);
		replacement[0].hiddenField = hidden[0];
	});
	$('input[type="submit"]').on('submit', function() {
		$("textarea").each(function (index, textarea) {
			textarea.hiddenField.value = textarea.innerHTML;
		});
		return true;
	});
})();

