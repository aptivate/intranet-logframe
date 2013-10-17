(function () {
	function backgroundBarChart(index, node) {
		/* adapted from http://stackoverflow.com/a/12021283/3189 */
		var barFill = "#ccc";
		var barEmpty = "#fff";
		var percent = node.dataset.percent;
		node.style.background="-webkit-gradient(linear, left top,right top, color-stop("+percent+"%,"+barFill+"), color-stop("+percent+"%,"+barEmpty+"))";
		node.style.background="-moz-linear-gradient(left center,"+barFill+" "+percent+"%, "+barEmpty+" "+percent+"%)" ;
		node.style.background="-o-linear-gradient(left,"+barFill+" "+percent+"%, "+barEmpty+" "+percent+"%)";
		node.style.background= "linear-gradient(to right,"+barFill+" "+percent+"%, "+barEmpty+" "+percent+"%)" ;
	}

	$(".barchart-background").each(backgroundBarChart);
})();
