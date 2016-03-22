var margin = { top: 50, right: 0, bottom: 100, left: 30 },
      width = 960 - margin.left - margin.right,
      height = 430 - margin.top - margin.bottom,
      gridSize = Math.floor(width / 11),
      legendElementWidth = gridSize*2,
      buckets = 9,
      colors = ["#ffffd9","#edf8b1","#c7e9b4","#7fcdbb","#41b6c4","#1d91c0","#225ea8","#253494","#081d58"], // alternatively colorbrewer.YlGnBu[9]
      cities = ["Boston", "Chicago", "Denver", "New York", "Philadelphia"],
      offenses = ["Assault", "Battery", "Burglary", 
      "Criminal Sexual Offense", "Sexual Assault", 
      "Hatecrime", "Homicide", "Offense Involving Children", 
      "Robbery", "Theft","Weapon Violation"];
      dataset = 'heat_data.csv';



var handleData = function(dataset) {
  var svg = d3.select("body").append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
      .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  var cityLabels = svg.selectAll(".dayLabel")
      .data(cities)
      .enter().append("text")
        .text(function (d) { return d; })
        .attr("x", 0)
        .attr("y", function (d, i) { return i * gridSize; })
        .style("text-anchor", "left")
        .attr("transform", "translate(-6," + gridSize / 1.5 + ")")

  var offenseLabels = svg.selectAll(".offenseLabel")
      .data(offenses)
      .enter().append("text")
        .text(function(d) { return d; })
        .attr("x", function(d, i) { return i * gridSize; })
        .attr("y", height)
        .style("text-anchor", "middle")
        .attr("transform", "translate(" + gridSize / 2 + ", -6)")
        .attr("class","offenseLabel")
        .style("font-size","4px")


        var colorScale = d3.scale.quantile()
          .domain([0, buckets - 1, d3.max(dataset, function (d) { return d.count; })])
          .range(colors);

      var cards = svg.selectAll(".hour")
          .data(dataset, function(d) {return d.city+':'+d.offense;});

      cards.append("title");


      cards.enter().append("rect")
          .attr("x", function(d) { return (i-1) * gridSize; })
          .attr("y", function(d) { return (i-1) * gridSize; })
          .attr("rx", 4)
          .attr("ry", 4)
          .attr("class", "hour bordered")
          .attr("width", gridSize)
          .attr("height", gridSize)
          .style("fill", colors[0]);

      cards.transition().duration(1000)
          .style("fill", function(d) { return colorScale(d.count); });

      cards.select("title").text(function(d) { return d.count; });
      
      cards.exit().remove();

      var legend = svg.selectAll(".legend")
          .data([0].concat(colorScale.quantiles()), function(d) { return d; });

      legend.enter().append("g")
          .attr("class", "legend");

      legend.append("rect")
        .attr("x", function(d, i) { return legendElementWidth * i; })
        .attr("y", height)
        .attr("width", legendElementWidth)
        .attr("height", gridSize / 2)
        .style("fill", function(d, i) { return colors[i]; });

      legend.append("text")
        .attr("class", "mono")
        .text(function(d) { 
        	return "≥ " + Math.round(d); })
        .attr("x", function(d, i) { return legendElementWidth * i; })
        .attr("y", height + gridSize);

      legend.exit().remove();


}
   d3.csv(dataset, function(d) {
   		return {
   			city: d.City,
   			offense: d.Offense,
   			count: +d.count
   		};
   },
   function(data) {
   	//console.log(data)
   	handleData(data)
   })