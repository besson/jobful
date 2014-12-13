  var diameter = 960,
      format = d3.format(",d"),
      color = d3.scale.category20c();

  var bubble = d3.layout.pack()
      .sort(null)
      .size([diameter, diameter])
      .padding(1.5);

  var svg = d3.select("body").append("svg")
      .attr("width", diameter)
      .attr("height", diameter)
      .attr("class", "bubble");

  d3.json("map/bubbles", function(error, bubbles) {
    var node = svg.selectAll(".node")
        .data(bubble.nodes(parseBubbles(bubbles)).filter(function(d) { return !d.children; }))
        .enter().append("g")
        .attr("class", "node")
        .attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });

        node.append("title")
            .text(function(d) { return d.className + ": " + format(d.value); });

        node.append("circle")
            .attr("r", function(d) { return d.r; })
            .style("fill", function(d) { return color(d.packageName); });

        node.append("text")
            .attr("dy", ".1em")
            .style("text-anchor", "middle")
            .attr("font-size", "10px")
            .html(function(d) { return d.className.substring(0, d.r / 2); });
   });

  d3.select(self.frameElement).style("height", diameter + "px");

function parseBubbles(bubbles) {
  var classes = [];

  bubbles.forEach(function(e) {
      if (e.radius > 5) {
        classes.push({parent: e, packageName: e.name, className: e.name, value: e.radius});
      }
  });

  return {children: classes}
}

