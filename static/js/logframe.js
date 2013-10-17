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

	function setBackgroundByStatus(index, node) {
		var statusToColor = {'danger': "#e68080", 'warning': "#ffcc66", 'ok': "#85ce9d"};
		if (node.dataset.status in statusToColor) {
			node.style.background = statusToColor[node.dataset.status];
		}
	}

	$(".barchart-background").each(backgroundBarChart);
	$(".status-background").each(setBackgroundByStatus);
})();
